#!/usr/bin/env python3
__author__ = "Vili Hätönen"

#import numpy as np
import ev3dev2
from robot_io import *
import threading
import time
from math import floor
import ev3dev2.auto as ev3


measure = True

class DataThread(threading.Thread):
    def __init__(self):
        self.speed_data = []
        self.motor_l = ev3.LargeMotor(ev3.OUTPUT_B)
        self.motor_r = ev3.LargeMotor(ev3.OUTPUT_C)
        threading.Thread.__init__(self)

    def run(self):
        debug_print("Start measuring data!")
        time_start = time.time() * 1000
        while measure:
            t = time.time() * 1000 - time_start
            speed_l = self.motor_l.speed    #Returns the current motor speed in tacho counts per second
            speed_r = self.motor_r.speed
            if floor(t/10) % 100:
                debug_print("time ", t, " speed ", [speed_l, speed_r])


def start_data_gathering():
    data_thread = DataThread()
    data_thread.setDaemon(True)
    data_thread.start()