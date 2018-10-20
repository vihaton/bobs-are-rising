#!/usr/bin/env python3
__author__= "Sofia Vanhanen"

import numpy
import os
import sys
import random

NUMBER_OF_ARRAYS = 2
SIZE_OF_ARRAY = 10

def generate_fake_inputs():
    inputs = []
    for i in range(NUMBER_OF_ARRAYS):
        inputs.append(generate_input())
    return inputs

def generate_input():
    array = numpy.zeros((SIZE_OF_ARRAY, 3))
    for i in range(SIZE_OF_ARRAY):
        # TODO fix bad values
        array[i][0] = i + random.uniform(-0.1, 0.1)
        array[i][1] = 0
        array[i][2] =  0
        if (i > SIZE_OF_ARRAY / 5):
            array[i][1] = 50 + random.uniform(-5, 5)
            array[i][2] = 0
        if (i > SIZE_OF_ARRAY / 2):
            array[i][1] = (i / SIZE_OF_ARRAY) * 100 + random.uniform(-5, 5)
            array[i][2] = (i / SIZE_OF_ARRAY) * 100 + random.uniform(-5, 5)
        if (i > SIZE_OF_ARRAY - (SIZE_OF_ARRAY / 5)):
            array[i][1] = 20 + random.uniform(-5, 5)
            array[i][2] = 40 + random.uniform(-5, 5)
    return array