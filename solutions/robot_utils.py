#!/usr/bin/env python3

import time

def turn_right(tank_drive, speed, duration):
    accelerate_to(tank_drive, speed, speed, speed, speed / 2, duration / 2)
    accelerate_to(tank_drive, speed, speed / 2, speed, speed, duration / 2)

def turn_left(tank_drive, speed, duration):
    accelerate_to(tank_drive, speed, speed, speed / 2, speed, duration / 2)
    accelerate_to(tank_drive, speed / 2, speed, speed, speed, duration / 2)

def turn_around(tank_drive):
    tank_drive.on_for_seconds(-26.2, 26.2, 1.4) #calibrated to produce quite accurate 180 degrees

def turn_90(tank_drive, left=True):
    tank_drive.on_for_seconds(-13, 13, 1.4)


def interpolate_linear(start, targ, percent):
    if percent > 100: #to limit the percent to 100
        percent = 100
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

def calibrate_turn(turn_func, tank_drive):
    while True:
        turn_func(tank_drive, True)
        time.sleep(3)

def calibrate_steer_and_speed(button, steering, speed):
    if button.up:
        speed += 5
    elif button.down:
        speed -= 5
    elif button.left:
        steering -= 5
    elif button.right:
        steering += 5
    return steering, speed