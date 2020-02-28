import serial 
import datetime

def pulserate():
    
    #Datum und Uhrzeit 
    
    currentT = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    #serielle Schnittstelle auslesen
    
    ser = serial.Serial('/dev/ttyUSB0')
    ser.baudrate=11520
    
    while True:
       
        data = ser.readline()
        data = data.decode('utf-8').strip()
    
    return [data, currentT]         
 
    ser.close()