#!/usr/bin/env python3

from robot_utils import *
from robot_io import *

YELLOW = 4
WHITE = 6
COLORS=('unknown','black','blue','green','yellow','red','white','brown')


def check_for_button(color_sensor):
    c = color_sensor.value()
    print("color = ", c , " = ", COLORS[c])
    if color_sensor.color() is YELLOW: #we're on the yellow button
        return True
    return False

def follow_line(sd, button, color_sensor, steering=10, speed=40): #let's follow the right edge!
    while True:
        steering, speed = calibrate_steer_and_speed(button, steering, speed)
        c = color_sensor.value()
        print(steering, speed)
        print(c , " = ", COLORS[c])

        if c is WHITE:   #when we're on top of the line, steer right
            sd.on(steering, speed)
        else:                               #were not on the line, steer left
            sd.on(-steering, speed)


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
    button_pressed = False
    print("let's follow the line to find a button!")

    color_sensor.mode = 'COL-COLOR' #let's recognice colors

    #etsitään nappi
    while not button_pressed:
        follow_line(sd, button, color_sensor,40, 15) #40 for steering and 15 for speed follows also 90*degree angles
        button_pressed = check_for_button(color_sensor)


    while True: #stop program to read screen
        if button.any():
            break
            
    print("button found!")
    #odotetaan siirtymä ja valmistaudutaan jatkamaan


    