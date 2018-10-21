#!/usr/bin/env python3
__author__ = 'Jaakko Oinas, Vili Hätönen'

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering

import evdev
import ev3dev.auto as ev3
import threading
import time
import sys

from gather_data import *

FOLDER_NAME = "../data/"
FILE_NAME = "speed_data_tmp.txt"
WAIT_TIME = 5

speed = 1
steer = 0

speedLimit = 10
steerLimit = 75

joystick_signal_threshold = 7

running = True

sd = MoveSteering(OUTPUT_B, OUTPUT_C) #steer drive

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)

    ## Some helpers ##
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.

    val: float or int
    src: tuple
    dst: tuple

    example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
    """
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

def scale_stick(value):
    return scale(value,(0,255),(-100,100))


class MotorThread(threading.Thread):
    def __init__(self):
        #self.motor = ev3.LargeMotor(ev3.OUTPUT_A)
        global sd
        self.sd = sd
        threading.Thread.__init__(self)

    def run(self):
        debug_print("Engine running!")
        global speed, steer, joystick_signal_threshold, running
        lastSpeed = speed
        round = 0
        while running:
            round += 1 
            if speed < 0:
                if speed < -joystick_signal_threshold:
                    self.sd.on(-steer, speed) #for BOB
                    #self.sd.on(steer, -speed) #for training robot
                else:
                    self.sd.off()
            else:
                if speed > joystick_signal_threshold:
                    self.sd.on(-steer, speed) #for BOB
                    #self.sd.on(steer, -speed) #for training robot
                else:
                    self.sd.off()
            #self.motor.run_direct(duty_cycle_sp=speed)
            # if speed != lastSpeed:
            #     debug_print("add speed ", speed)
            #     lastSpeed = speed

        #self.motor.stop()
        debug_print("motor stop")

def run():
    global sd, speedLimit, steerLimit, joystick_signal_threshold, running, speed, steer, WAIT_TIME, FILE_NAME
    
    ## Initializing ##
    debug_print("Finding ps3 controller...")
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        debug_print(device.name)
        if device.name == 'Wireless Controller': #PS4
        #if device.name == 'PLAYSTATION(R)3 Controller': #PS3
            debug_print("PS3 FOUND!")
            ps3dev = device.fn

    gamepad = evdev.InputDevice(ps3dev)

    #lets refresh the file
    with open(FILE_NAME, "w") as file:
        file.write("")

    motor_thread = MotorThread()
    motor_thread.setDaemon(True)
    motor_thread.start()



    for event in gamepad.read_loop():   #this loops infinitely
        if event.type == 1 and event.code == 304 and event.value == 1:
            debug_print("X button is pressed. Stopping.")
            running = False
            break
        if event.type == 1 and event.code == 305 and event.value == 1:
            debug_print("Round button is pressed, let's start recording!")
            start_data_gathering()

        if event.type == 1 and event.code == 308 and event.value == 1:
            debug_print("Square button is pressed")
        if event.type == 1 and event.code == 307 and event.value == 1:
            debug_print("Triangle button is pressed, lets stop")
            sd.stop()
            save_data_to_file(FILE_NAME)

        if event.type == 1 and event.code == 544 and event.value == 1:
            debug_print("Up button is pressed")

        if event.type == 1 and event.code == 547 and event.value == 1:
            debug_print("Right button is pressed")
        if event.type == 1 and event.code == 545 and event.value == 1:
            debug_print("Down button is pressed")
        if event.type == 1 and event.code == 546 and event.value == 1:
            debug_print("Left button is pressed")
        if event.type == 1 and event.code == 311 and event.value == 1:
            #debug_print("R1 button is pressed")
            if steerLimit < 100:
                steerLimit += 5
                debug_print("New steer limit is: ", steerLimit)
                print("Steer: ", steerLimit)
        if event.type == 1 and event.code == 313 and event.value == 1:
            #debug_print("R2 button is pressed")
            if speedLimit < 100:
                speedLimit += 5
                debug_print("New speed limit is: ", speedLimit)
                print("Speed: ", speed)

        if event.type == 1 and event.code == 310 and event.value == 1:
            #debug_print("L1 button is pressed")
            if steerLimit > 0:
                steerLimit -= 5
                debug_print("New steer limit is: ", steerLimit)
        if event.type == 1 and event.code == 312 and event.value == 1:
            #debug_print("L2 button is pressed")
            if speedLimit > 0:
                speedLimit -= 5
                debug_print("New speed limit is: ", speedLimit)

        if event.type == 1 and event.code == 315 and event.value == 1:
            debug_print("Start button is pressed")
        if event.type == 1 and event.code == 314 and event.value == 1:
            debug_print("Select button is pressed")

        if event.type == 1 and event.code == 318 and event.value == 1:
            debug_print("Right joystick button is pressed")
        if event.type == 1 and event.code == 317 and event.value == 1:
            debug_print("Left joystick button is pressed")
        
        #if event.type == 3 and event.code == 0:
            #steer = scale_stick(event.value)
            #debug_print("Left X: ", event.value, "Steer: ", steer)
        if event.type == 3 and event.code == 1:
            #speed = scale_stick(event.value)
            speed = scale(event.value,(0,255),(-speedLimit,speedLimit))
            #debug_print("speed: ", speed)
            #debug_print("Left Y: ", event.value, "Speed: ", speed)

        if event.type == 3 and event.code == 3:
            #debug_print("Right X: ", event.value, "Steer: ", steer)
            steer = scale(event.value,(0,255),(-steerLimit,steerLimit))
            #debug_print("steer: ", steer)
        # if event.type == 3 and event.code == 4:
            #steer = scale_stick(event.value)
            #debug_print("Right Y: ", event.value, "Speed: ", speed)
        



        #debug_print("type: ", event.type, "code: ", event.code, "value: ", event.value)

            # if event.type == 1 and event.code == 292:
            #     debug_print("Up button is pressed")
            # if event.type == 1 and event.code == 293:
            #     debug_print("Right button is pressed")
            # if event.type == 1 and event.code == 294:
            #     debug_print("Down button is pressed")
            # if event.type == 1 and event.code == 295:
            #     debug_print("Left button is pressed")
            # running = False
            # break
        # if event.type == 3:             #A stick is moved
        #     if event.code == 5:         #Y axis on right stick
        #         speed = scale_stick(event.value)

        # if event.type == 1 and event.code == 302 and event.value == 1:
        #     debug_print("X button is pressed. Stopping.")
        #     running = False
        #     break

if __name__ == "__main__":
    run()