# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 10:18:02 2019

@author: s6lurich
"""

import SimpleITK as sitk
import numpy as np
from scipy import signal
from PIL import Image

class ImageProcessing:
    
    @staticmethod
    def __image_array_transformation(image_name):                        #name of the image with file extension "dcm" for dicom images
        image=sitk.ReadImage(image_name)                    
        ar = sitk.GetArrayFromImage(image)                  
        #ar1 = ar[0,:,:]                                     
        return ar

    @staticmethod
    def __array_image_transformation(arr, image_name):
        im = Image.fromarray(arr)
        im.save(image_name)

    @staticmethod
    def inversion(image_name):                                    
        ar1=ImageProcessing.__image_array_transformation(image_name)
        maxArr=np.max(ar1)                                               #find the highest grey value of the array
        new = maxArr-ar1                                                 #subtraction of the current grey values from the highest grey value, highest grey value becomes the lowest grey value of the new array
        ImageProcessing.__array_image_transformation(new, image_name)                                                     #return of the inverted image array
    
    @staticmethod
    def binarization(image_name,limit):                                  #input of the name of the image with file extension "dcm" for dicom images and the limit 
        ar1=ImageProcessing.__image_array_transformation(image_name)
        new=(ar1>=limit)*np.max(ar1)                                     #a comparison of the array values with the limit creats "True" and "False", which is equal to 1 and 0. These values are multiplied with the maximal grey values to create the new array.
        ImageProcessing.__array_image_transformation(new, image_name)
    
    @staticmethod
    def gamma_correction(image_name,gamma):
        ar1=ImageProcessing.__image_array_transformation(image_name)
        min_grey=np.min(ar1)                                             #find the lowest grey value of the array
        if min_grey<0:                                                   #checking minimum is negativ or positiv
            ar1=ar1-min_grey                                             #if the minimum is negativ, the array values are shifted in the positive area
            new = np.max(ar1)*(ar1/np.max(ar1))**(1/gamma)               #create a new array with the mathematical function of gamma correction     
            ImageProcessing.__array_image_transformation(new+min_grey, image_name)                          #move the array back in the starting area
        else:
            ar1=ar1-min_grey                                             #if positiv, shift to 0, lowest array value is 0.
            new = np.max(ar1)*(ar1/np.max(ar1))**(1/gamma)               #create a new array with the mathematical function of gamma correction
            ImageProcessing.__array_image_transformation(new+min_grey, image_name)                               #move the array back in the starting area 
    
    @staticmethod
    def smoothing(image_name):
        ar1=ImageProcessing.__image_array_transformation(image_name)
        kernel = 1/16*np.array([[1,2,1],[2,4,2],[1,2,1]])                 #definition of the smoothing filter
        new = signal.convolve(ar1,kernel)                                 #convolution of the smoothing filter with the array of the image
        ImageProcessing.__array_image_transformation(new, image_name)                                              #return and round 

    @staticmethod    
    def vert_edge_detection(image_name):
        ar1=ImageProcessing.__image_array_transformation(image_name)
        vert_soebel = 1/8*np.array([[-1,0,1],[-2,0,2],[-1,0,1]])          #vertical soebel filter
        new = signal.convolve(ar1,vert_soebel)                            #convolution of the image array with the vertical soebel filter
        ImageProcessing.__array_image_transformation(new, image_name)                                              #return and round 
    
    @staticmethod
    def hor_edge_detection(image_name):
        ar1=ImageProcessing.__image_array_transformation(image_name)
        hor_soebel = 1/8*np.array([[-1,-2,-1],[0,0,0],[1,2,1]])           #horizontal soebel filter
        new = signal.convolve(ar1,hor_soebel)                             #convolution of the image array with the horizontal soebel filter
        ImageProcessing.__array_image_transformation(new, image_name)                                              #return and round 