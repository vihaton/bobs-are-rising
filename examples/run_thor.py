#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
import ev3dev2.auto as ev3

import os
import sys
import time
import ast

folder_name = "../data/"
model_name = "model_1.thor"

model = None
sd = MoveSteering(OUTPUT_B, OUTPUT_C) #steer drive
motor_l = ev3.LargeMotor(ev3.OUTPUT_B)
motor_r = ev3.LargeMotor(ev3.OUTPUT_C)

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def init_model():
    global model
    with open(model_name, "r") as file:
        model = ast.literal_eval(file.read())

def run_circle():
    init_model()
    global model, sd
    
    time_start = time.time() * 1000
    ind = 0
    while ind < len(model):
        t = time.time() * 1000
        value = model[ind]              #value = [time, speed left, speed right]
        if t - time_start < value[0]: #we're not there yet, let's wait
            continue
        
        #let's update motor speeds
        motor_l.speed_sp = value[1]
        motor_r.speed_sp = value[2]
        motor_l.run_forever()
        motor_r.run_forever()

        #let's move forward with the values
        ind += 1
        
        if ind % 1000 is 0:
            debug_print("progress ", ind / len(model))

    motor_l.stop()
    motor_r.stop()



if __name__ == '__main__':
    run_circle()