#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button

import time

#our own code
from robot_utils import *
from robot_io import *
from maze import solve_maze
from gather_data import start_data_gathering

# state constants
ON = True
OFF = False
NORMAL_SPEED = 42
td = MoveTank(OUTPUT_B, OUTPUT_C) #tank drive
sd = MoveSteering(OUTPUT_B, OUTPUT_C) #steer drive
cs = ColorSensor(INPUT_4)
btn = Button()

def l_shape():
    tank_drive = td
    accelerate_to(tank_drive,0,0,NORMAL_SPEED, NORMAL_SPEED,1)
    time.sleep(2)
    accelerate_to(tank_drive, NORMAL_SPEED, NORMAL_SPEED, 0,0,1)
    turn_90(tank_drive, True)
    accelerate_to(tank_drive, 0,0,NORMAL_SPEED, NORMAL_SPEED,1)
    time.sleep(1)
    accelerate_to(tank_drive, NORMAL_SPEED, NORMAL_SPEED, 0,0,1)

def main():

    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')

    # print something to the screen of the device
    print('Hello World!')

    # print something to the output panel in VS Code
    debug_print('Hello VS Code!')

    start_data_gathering()    

    solve_maze(sd, cs, btn)

    #solve_forest(sd, cs, btn)

    #calibrate_turn(turn_90, td)

if __name__ == '__main__':
    main()
