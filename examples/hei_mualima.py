#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

import os
import sys
import time

# state constants
ON = True
OFF = False
NORMAL_SPEED = 42

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)

def turn_right(tank_drive, speed, duration):
    accelerate_to(tank_drive, speed, speed, speed, speed / 2, duration / 2)
    accelerate_to(tank_drive, speed, speed / 2, speed, speed, duration / 2)

def turn_left(tank_drive, speed, duration):
    accelerate_to(tank_drive, speed, speed, speed / 2, speed, duration / 2)
    accelerate_to(tank_drive, speed / 2, speed, speed, speed, duration / 2)

def turn_around(tank_drive):
    tank_drive.on_for_seconds(-26.2, 26.2, 1.4) #calibrated to produce quite accurate 180 degrees

def interpolate_linear(start, targ, percent):
    return percent * (targ - start) + start

def accelerate_to(tank_drive, left_start=0, right_start=0, left_targ=50, right_targ=50, time_sec=1):
    start_millis = int(round(time.time() * 1000))
    delta = 0
    ceil = time_sec * 1000
    while (delta < ceil):
        lSpeed = interpolate_linear(left_start, left_targ, delta / ceil)
        rSpeed = interpolate_linear(right_start, right_targ, delta / ceil)
        delta = int(round(time.time() * 1000))
        delta = delta - start_millis
        if lSpeed != 0 or rSpeed != 0:
            tank_drive.on(lSpeed, rSpeed)


def chair_slalom(tank_drive):
    # the first two parameters can be unit classes or percentages.  

    rounds = 0
    while (rounds < 5):
        north = rounds % 2 == 0

        #accelerate to normal speed
        accelerate_to(tank_drive, 0, 0, NORMAL_SPEED, NORMAL_SPEED, 1)
        time.sleep(2)

        if north:
            turn_right(tank_drive, NORMAL_SPEED, 1)
            turn_left(tank_drive, NORMAL_SPEED, 1)
        else: 
            turn_left(tank_drive, NORMAL_SPEED, 1)
            turn_right(tank_drive, NORMAL_SPEED, 1)

        time.sleep(3)

        if north:
            turn_left(tank_drive, NORMAL_SPEED, 1)
            turn_right(tank_drive, NORMAL_SPEED, 1)
        else:
            turn_right(tank_drive, NORMAL_SPEED, 1)
            turn_left(tank_drive, NORMAL_SPEED, 1)

        time.sleep(3)

        accelerate_to(tank_drive, NORMAL_SPEED, NORMAL_SPEED, 0, 0, 1)

        turn_around(tank_drive)
        rounds += 1


def main():
    '''The main function of our program'''

    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')

    # print something to the screen of the device
    print('Hello World!')

    # print something to the output panel in VS Code
    debug_print('Hello VS Code!')

    tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

    chair_slalom(tank_drive)

    
    """
    while (True):
        turn_around(tank_drive)
        time.sleep(3)
    """

if __name__ == '__main__':
    main()
