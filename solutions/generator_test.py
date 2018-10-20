#!/usr/bin/env python3
__author__= "Sofia Vanhanen"

import os
import sys
import input_generator

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)

def main():
    debug_print("Testing the input generation!!!")
    debug_print("Starting with one array.")
    debug_print(input_generator.generate_input())
    #debug_print("Now many arrays.")
    #debug_print(input_generator.generate_fake_inputs())

if __name__ == '__main__':
    main()