#!/usr/bin/env python3
__author__ = 'Jaakko Oinas, Vili Hätönen'

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering

import evdev
import ev3dev.auto as ev3
import threading
import time
import sys

from run_thor import *
from robot_io import *
from gather_data import *
from maze import *

FOLDER_NAME = "../data/"
FILE_NAME = "speed_data_tmp" 
WAIT_TIME = 5

DATA_SET_IND = 0 #write all data sets to different files

speed = 1
steer = 0

speedLimit = 15
steerLimit = 75

joystick_signal_threshold = 7

running = True

models = []

sd = MoveSteering(OUTPUT_B, OUTPUT_C) #steer drive
ladle = MediumMotor(OUTPUT_A)
cs = ColorSensor(INPUT_4)
btn = Button()


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
                    self.sd.on(steer, -speed) #for BOB (kauha takana)
                    #self.sd.on(steer, -speed) #for training robot
                else:
                    self.sd.off()
            else:
                if speed > joystick_signal_threshold:
                    self.sd.on(steer, -speed) #for BOB (kauha takana)
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
    global btn, cs, ladle, sd, speedLimit, steerLimit, joystick_signal_threshold, running, speed, steer, WAIT_TIME, FILE_NAME, DATA_SET_IND
    model_ind = 0
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

    motor_thread = MotorThread()
    motor_thread.setDaemon(True)
    motor_thread.start()

    init_console()

    init_models()

    models = get_models()

    debug_print("START LOOP")

    for event in gamepad.read_loop():   #this loops infinitely
        if event.type == 1 and event.code == 304:
            debug_print("X button is pressed. Stopping.")

            if event.value == 1:
                if not ladle.is_running:
                    debug_print("Ladle down start")
                    ladle.on(-50)
            else:
                debug_print("Ladle down stop")
                ladle.off()
            
        if event.type == 1 and event.code == 305 and event.value == 1:
            debug_print("Round button is pressed, turn on the line follower!")
            #start_data_gathering()

            cs.mode = 'COL-COLOR' #let's recognice colors

            cfe = lambda color_sensor : check_for_end_of_challange(color_sensor)
            #find the goal
            follow_line(cfe, sd, btn, cs, 45, 10, input_for_exit_condition=btn)
        if event.type == 1 and event.code == 308 and event.value == 1:
            debug_print("Square button is pressed run model " + str(model_ind))
            while not run_model(models[model_ind]):
                debug_print("AGAIN")
            model_ind += 1
            
        if event.type == 1 and event.code == 307:
            debug_print("Triangle button is pressed, lets stop")
            # sd.stop()
            # save_data_to_file(FILE_NAME + str(DATA_SET_IND) + ".txt")
            # DATA_SET_IND += 1
            if event.value == 1:
                if not ladle.is_running:
                    debug_print("Ladle up start")
                    ladle.on(50)
            else:
                debug_print("Ladle up stop")
                ladle.off()
        if event.type == 1 and event.code == 544 and event.value == 1:
            debug_print("Up button is pressed")
            
        if event.type == 1 and event.code == 547 and event.value == 1:
            debug_print("Right button is pressed")
        if event.type == 1 and event.code == 545 and event.value == 1:
            debug_print("Down button is pressed")
            # if event.value == 1:
            #     if not ladle.is_running:
            #         debug_print("Ladle down start")
            #         ladle.on(-50)
            # else:
            #     debug_print("Ladle down stop")
            #     ladle.off()
        if event.type == 1 and event.code == 546 and event.value == 1:
            debug_print("Left button is pressed")
        if event.type == 1 and event.code == 311 and event.value == 1:
            debug_print("R1 button is pressed")
            # if steerLimit < 100:
            #     steerLimit += 5
            #     debug_print("New steer limit is: ", steerLimit)
            #     print("Steer: ", steerLimit)

        if event.type == 1 and event.code == 313 and event.value == 1:
            #debug_print("R2 button is pressed")
            if speedLimit < 100:
                speedLimit += 5
                debug_print("New speed limit is: ", speedLimit)
                print("Speed: ", speed)

        if event.type == 1 and event.code == 310 and event.value == 1:
            debug_print("L1 button is pressed")
            if steerLimit > 0:
                steerLimit -= 5
                debug_print("New steer limit is: ", steerLimit)

        if event.type == 1 and event.code == 312 and event.value == 1:
            debug_print("L2 button is pressed")
            if speedLimit > 0:
                speedLimit -= 5
                debug_print("New speed limit is: ", speedLimit)
            
        if event.type == 1 and event.code == 315 and event.value == 1:
            debug_print("Start button is pressed")
            running = False
            break
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