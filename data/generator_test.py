#!/usr/bin/env python3
__author__= "Sofia Vanhanen"

import os
import sys
import input_generator
import thor

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)

def main():
    debug_print("Testing the input generation!!!")
    debug_print("Starting with one array.")
    debug_print(input_generator.generate_input())
    debug_print("Now many arrays.")
    inputs = input_generator.generate_fake_inputs()
    debug_print(inputs)
    debug_print("Testing align_values.")
    inputs = thor.align_values(inputs)
    debug_print(inputs)
    debug_print("Testing choose_values.")
    inputs = thor.choose_values(inputs)
    debug_print(inputs)
    debug_print("Testing calculate_means.")
    inputs = thor.calculate_means(inputs)
    debug_print(inputs)

if __name__ == '__main__':
    main()