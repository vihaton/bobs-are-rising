#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
import ev3dev2.auto as ev3
from ev3dev2.button import Button

import os
import sys
import time
import ast

import robot_io

models = []
maze_button_model = None
forest_model = None
sd = MoveSteering(OUTPUT_B, OUTPUT_C) #steer drive
motor_l = ev3.LargeMotor(ev3.OUTPUT_B)
motor_r = ev3.LargeMotor(ev3.OUTPUT_C)
btn = Button()

def get_models():
    global models
    return models

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def init_models():
    global models
    listOfFiles = os.listdir('.')  
    listOfFiles.sort()

    for i in range(len(listOfFiles)):
        name = listOfFiles[i]
        if ".thor" in name:
            debug_print("Start to read the model " + name)
            with open(name, "r") as file:
                model_str = file.read()
            model = ast.literal_eval(model_str)

            models.append(model)
            debug_print("Models are read")

def init_maze_model():
    global maze_button_model
    with open("model_maze.thor", "r") as file:
        model_str = file.read()
    maze_button_model = ast.literal_eval(model_str)
    debug_print("maze model read")

def init_forest_model():
    global forest_model
    with open("model_forest.thor", "r") as file:
        model_str = file.read()
    forest_model = ast.literal_eval(model_str)
    debug_print("forest model read")

def run_model(model):
    time_start = time.time() * 1000
    ind = 0
    postponed = 0
    while ind < len(model):
        t = time.time() * 1000
        value = model[ind]  #value = [time, speed left, speed right]
        delta = t - time_start
        if delta < value[0]: #we're not there yet, let's wait
            #debug_print("delta ", delta, " value ", value) #this takes a lot of time!!!
            postponed += 1
            continue
        
        if btn.left: #if we press left, it means start again
            return False
        if btn.right:
            return True #we'll skip this challange

        #let's update motor speeds
        motor_l.speed_sp = value[1]
        motor_r.speed_sp = value[2]
        motor_l.run_forever()
        motor_r.run_forever()

        #let's move forward with the values
        ind += 1
        
        # if ind % 100 is 0:
        #     debug_print("progress ", ind / len(model))

    motor_l.stop()
    motor_r.stop()
    debug_print("we postponed ", postponed, " iterations, ", postponed / len(model), "%")
    return True

def press_maze_button(): #used by main
    global sd, maze_button_model

    sd.on_for_seconds(0, -10, 1, brake=False) #to start the same way
    while not run_model(maze_button_model):
        debug_print("AGAIN! Sleep 1s")
        time.sleep(1)

def solve_forest():
    global forest_model
    while not run_model(forest_model):
        debug_print("AGAIN! Sleep 3s")
        time.sleep(3)

def run():
    init_models()
    global models, sd
    robot_io.init_console()

    print("BOB is teached by Thor and ready to run.")

    while not btn.any(): # While no (not any) button is pressed.
        time.sleep(0.01)  # Wait 0.01 second    

    for i in range(len(models)):
        t = time.time() * 1000
        debug_print("run model no " + str(i), "model length ", models[i][-1][0])
        while not run_model(models[i]): #until we get it right
            while not btn.any(): #let's wait for the press that we're ready
                time.sleep(0.01)
            debug_print("Let's try again in 1s!")
            time.sleep(1)
        debug_print("run took ", time.time() * 1000 - t)
    



if __name__ == '__main__':
    run()