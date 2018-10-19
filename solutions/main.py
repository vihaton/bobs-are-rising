#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

import time

#our own code
from robot_utils import *
from robot_io import *

# state constants
ON = True
OFF = False
NORMAL_SPEED = 42


def l_shape(tank_drive):
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

    tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

    #chair_slalom(tank_drive)

    #l_shape(tank_drive)

    while (True):
        turn_90(tank_drive, True)
        time.sleep(3)

if __name__ == '__main__':
    main()
