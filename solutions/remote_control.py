#!/usr/bin/env python3
__author__ = 'Jaakko Oinas'

import evdev
import ev3dev.auto as ev3
import threading
import time
import sys

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

def main():
    ## Initializing ##
    debug_print("Finding ps3 controller...")
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        debug_print(device.name)
        if device.name == 'PLAYSTATION(R)3 Controller':
            debug_print("PS3 FOUND!")
            ps3dev = device.fn

    # counter = 0
    # while True:
    #     devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    #     for device in devices:
    #         debug_print(device.name)
    #     counter += 1
    #     debug_print("-----------------", counter, "-------------------")
    #     time.sleep(5)
    #         # if device.name == 'PLAYSTATION(R)3 Controller':
    #         #     ps3dev = device.fn

    gamepad = evdev.InputDevice(ps3dev)

    speed = 0
    running = True

    class MotorThread(threading.Thread):
        def __init__(self):
            self.motor = ev3.LargeMotor(ev3.OUTPUT_A)
            threading.Thread.__init__(self)

        def run(self):
            debug_print("Engine running!")
            lastSpeed = speed
            round = 0
            while running:
                round += 1
                if round % 100000 is 0:
                    debug_print(round)
                #self.motor.run_direct(duty_cycle_sp=speed)
                if speed != lastSpeed:
                    debug_print("add speed ", speed)
                    lastSpeed = speed

            #self.motor.stop()
            debug_print("motor stop")

    motor_thread = MotorThread()
    motor_thread.setDaemon(True)
    motor_thread.start()


    for event in gamepad.read_loop():   #this loops infinitely
        if event.type == 1 and event.code == 304 and event.value == 1:
            debug_print("Cross button is pressed")
        if event.type == 1 and event.code == 305 and event.value == 1:
            debug_print("Round button is pressed")
        if event.type == 1 and event.code == 308 and event.value == 1:
            debug_print("Square button is pressed")
        if event.type == 1 and event.code == 307 and event.value == 1:
            debug_print("Triangle button is pressed")

        if event.type == 1 and event.code == 544 and event.value == 1:
            debug_print("Up button is pressed")
        if event.type == 1 and event.code == 547 and event.value == 1:
            debug_print("Right button is pressed")
        if event.type == 1 and event.code == 545 and event.value == 1:
            debug_print("Down button is pressed")
        if event.type == 1 and event.code == 546 and event.value == 1:
            debug_print("Left button is pressed")

        if event.type == 1 and event.code == 311 and event.value == 1:
            debug_print("R1 button is pressed")
        if event.type == 1 and event.code == 313 and event.value == 1:
            debug_print("R2 button is pressed")

        if event.type == 1 and event.code == 310 and event.value == 1:
            debug_print("L1 button is pressed")
        if event.type == 1 and event.code == 312 and event.value == 1:
            debug_print("L2 button is pressed")

        if event.type == 1 and event.code == 315 and event.value == 1:
            debug_print("Start button is pressed")
        if event.type == 1 and event.code == 314 and event.value == 1:
            debug_print("Select button is pressed")

        if event.type == 1 and event.code == 318 and event.value == 1:
            debug_print("Right joystick button is pressed")
        if event.type == 1 and event.code == 317 and event.value == 1:
            debug_print("Left joystick button is pressed")

        if event.type == 3 and event.code == 0:
            debug_print("Left X: ", event.value)
        if event.type == 3 and event.code == 1:
            debug_print("Left Y: ", event.value)

if __name__ == '__main__':
    main()


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