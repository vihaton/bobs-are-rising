#!/usr/bin/env python3
__author__= "Vili Hätönen"
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button

from robot_utils import *
from robot_io import *

# state constants
ON = True
OFF = False
NORMAL_SPEED = 42
td = MoveTank(OUTPUT_B, OUTPUT_C) #tank drive
sd = MoveSteering(OUTPUT_B, OUTPUT_C) #steer drive
cs = ColorSensor(INPUT_4)
btn = Button()

YELLOW = 4
RED = 5
WHITE = 6
COLORS=('unknown','black','blue','green','yellow','red','white','brown')
CONSECUTIVE_REDS = 0
CONSECUTIVE_YELLOWS = 0

def check_for_button(color_sensor):
    global CONSECUTIVE_YELLOWS
    c = color_sensor.value()
    print("color = ", c , " = ", COLORS[c])
    if c is YELLOW:
        CONSECUTIVE_YELLOWS += 1
    else:
        CONSECUTIVE_YELLOWS = 0

    if CONSECUTIVE_YELLOWS > 3: #we have found the button
        return True
    return False


def check_for_end_of_challange(color_sensor):
    global CONSECUTIVE_REDS
    c = color_sensor.value()
    print("cfe: ", c, " = ", COLORS[c])
    if c is RED:
        CONSECUTIVE_REDS += 1
    else:
        CONSECUTIVE_REDS = 0

    if CONSECUTIVE_REDS > 3:
        return True
    return False

def follow_line(func_condition_to_exit, sd, button, color_sensor, steering=10, speed=40, right_edge=True, input_for_exit_condition=None): #let's follow the right edge!
    if right_edge: right_edge = 1
    else: right_edge = -1

    while not func_condition_to_exit(input_for_exit_condition):
        steering, speed = calibrate_steer_and_speed(button, steering, speed)
        c = color_sensor.value()
        print(steering, speed)
        print(c , " = ", COLORS[c])

        if c is WHITE:   #when we're on top of the line (and follow right edge), steer right
            sd.on(right_edge * steering, speed)
        else:                               #were not on the line (-:-), steer left
            sd.on(right_edge * -steering, speed)

def press_the_button():
    #accelerate a little sprint
    accelerate_to(td, left_start=15, right_start=15, left_targ=25, right_targ=25, duration_sec=0.25) 
    time.sleep(0.6)
    #stop
    accelerate_to(td, 25, 25, 0, 0, 0.5) 

    #move backwards
    accelerate_to(td, 0, 0, -30, -30, 0.5)
    time.sleep(1.007)
    #stop
    accelerate_to(td, -30, -30, 0, 0, 0.5)


# #DEPRACATED
# def follow_line_with_interpolation(sd, color_sensor, steering=10, speed=40): #let's follow the right edge!
#     max_steers = [10, -50]     #the starting and ending points of interpolation
#     length_of_interpol = 100    #how many loops w/o seeing white before we reach the max steer to right
#     loops_wo_white = 0

#     while True:
#         c = color_sensor.value()
#         print("color = ", c , " = ", COLORS[c])

#         if loops_wo_white >= length_of_interpol: #let's limit the overflow
#             loops_wo_white = length_of_interpol - 1

#         steer = interpolate_linear(max_steers[0], max_steers[1], loops_wo_white / length_of_interpol)
#         debug_print("interpolated steer ", steer)

#         if c is WHITE:   #when we're on top of the line, steer right
#             sd.on(steer, speed)
#             loops_wo_white = 0
#         else:                               #were not on the line, steer left
#             sd.on(steer, speed)
#             loops_wo_white += 1

def solve_maze(sd, color_sensor, button):
    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')

    print("let's follow the line to find a button!")

    color_sensor.mode = 'COL-COLOR' #let's recognice colors

    cfb = lambda color_sensor : check_for_button(color_sensor) #my first lambda funcion ever

    #etsitään nappi seuraamalla valkoista viivaa kunnes nappi löytyy
    follow_line(cfb, sd, button, color_sensor,47, 12, input_for_exit_condition=color_sensor) #42 for steering and 15 for speed follows also 90*degree angles
    
    print("button found!")
    #odotetaan siirtymä ja valmistaudutaan jatkamaan

    press_the_button()

    #let's find the white line again
    #turn_to_find_color(sd, color_sensor)
    turn_90(sd)

    cfe = lambda color_sensor : check_for_end_of_challange(color_sensor)
    #find the goal
    follow_line(cfe, sd, button, color_sensor, 47, 12, input_for_exit_condition=color_sensor)

    print("end found!")
    while True: #stop program to read screen
        if button.any():
            break


if __name__ == '__main__':
    solve_maze(sd, cs, btn)
    