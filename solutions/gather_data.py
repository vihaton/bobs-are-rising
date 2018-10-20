#!/usr/bin/env python3
__author__ = "Vili Hätönen"

#import numpy as np
import ev3dev2
from robot_io import *
import threading
import time
from math import floor
import ev3dev2.auto as ev3
from ev3dev2.button import Button


measure = True

class DataThread(threading.Thread):
    def __init__(self):
        self.speed_data = []
        self.motor_l = ev3.LargeMotor(ev3.OUTPUT_B)
        self.motor_r = ev3.LargeMotor(ev3.OUTPUT_C)
        self.btn = Button()
        threading.Thread.__init__(self)

    def run(self):
        debug_print("Start measuring data!")
        time_start = time.time() * 1000
        while measure:
            t = time.time() * 1000 - time_start
            speed_l = self.motor_l.speed    #Returns the current motor speed in tacho counts per second
            speed_r = self.motor_r.speed
            self.speed_data.append([t, speed_l, speed_r])
            # if floor(t/10) % 10 is 0:
            #     debug_print("time ", t, " floor(t/10) ", floor(t/10), " speed ", [speed_l, speed_r])
            
            if self.btn.enter: # let's send the data and restart measurements
                debug_print(self.speed_data)
                time.sleep(4.8) # wait for 5 sec to set to robot to beginning again
                time_start = time.time() * 1000


def start_data_gathering():
    data_thread = DataThread()
    data_thread.setDaemon(True)
    data_thread.start()