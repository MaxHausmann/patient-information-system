from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.animation import Animation

from threading import Thread
from serial import Serial
import numpy as np
from scipy.signal import find_peaks

# just for testing purposes
from time import sleep
from math import sin, pi
from random import randint


class PulsePlot(BoxLayout):

    graph = ObjectProperty(None)
    label_bpm = ObjectProperty(None)
    sample_interval = 0.01  # 10 ms
    calc_interval = 10
    count_threshold = 72
    calc_count = 0
    peak_count = 0
    
    def __init__(self, **kwargs):
        super(PulsePlot, self).__init__(**kwargs)
        self.plot = MeshLinePlot(color=[0, 0.5, 1, 1])
        self.pulse_measurement = PulseMeasurement()

    def start(self):
        #self.pulse_measurement.start()
        self.graph.add_plot(self.plot)
        Clock.schedule_interval(self.acquire, self.sample_interval)

    def stop(self):
        Clock.unschedule(self.acquire)
        self.pulse_measurement.reset_measurement()

    def acquire(self, dt):
        self.plot.points = []

        for i, j in enumerate(self.pulse_measurement.values):
            self.plot.points.append((i, j))
        
        self.calc_count += 1

        if self.calc_count > (1 / self.sample_interval * self.calc_interval):
            self.peak_count = find_peaks(self.pulse_measurement.values)[0].shape[0]
            self.calc_count = 0
            self.calc_bpm()

    def calc_bpm(self):
        print("peaks: ", self.peak_count)
        bpm = self.peak_count * (60 / self.calc_interval)
        print("bpm: ", bpm)
        self.label_bpm.text = str(round(bpm, -1))
        self.peak_count = 0
        self.bpm_animation()

    def bpm_animation(self):
        anim = Animation(opacity = 0, duration = .2) \
                + Animation(opacity = 1, duration = .02) \
                + Animation(opacity = 0, duration = .02) \
                + Animation(opacity = 1, duration = 1)
        anim.start(self.label_bpm)
        

class PulseMeasurement:

    MAX_SAMPLES = 100
    pulse_thread = None
    stop_thread = False
    values = np.zeros(MAX_SAMPLES) 
    sample_cnt = 0

    def __init__(self):
        self.reset_measurement()
        self.pulse_thread = Thread(target = self._thread, args = (lambda : self.stop_thread, ))
        self.pulse_thread.daemon = True
        self.pulse_thread.start()

    def _thread(self, stop):
        print("Acquisition thread started.")
        while True:
            self.values[self.sample_cnt] = ((50 * sin(self.sample_cnt * 0.1 * pi)) + 25)
            self.sample_cnt += 1
            if self.sample_cnt > self.MAX_SAMPLES-1:
                self.sample_cnt = 0
            sleep(0.1)

    def stop(self):
        self.reset_measurement()
        
    def reset_measurement(self):
        self.sample_cnt = 0