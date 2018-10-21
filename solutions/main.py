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
from maze import *
from gather_data import start_data_gathering
from run_thor import *

# state constants
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

    init_console()

    init_maze_model()
    init_forest_model()

    print("BOB is teached by Thor and ready to run.")
    debug_print("BOB is teached by Thor and ready to run.")
    while not btn.any(): # While no (not any) button is pressed.
        time.sleep(0.01)  # Wait 0.01 second    

    press_maze_button()

    #we're at the button
    solve_maze(sd, cs, btn)

    solve_forest()

def calibrate():
    while True:
        cfe = lambda color_sensor : check_for_end_of_challange(color_sensor)
        #find the goal
        follow_line(cfe, sd, btn, cs, 45, -10, input_for_exit_condition=cs)
        debug_print("Goal is found")



if __name__ == '__main__':
    main()
    #calibrate()
