#!/usr/bin/env python3
__author__= "Sofia Vanhanen"

import numpy
import os
import sys
import random

NUMBER_OF_ARRAYS = 20
SIZE_OF_ARRAY = 10000

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
        array[i][1] = (i / SIZE_OF_ARRAY) * 100
        array[i][2] = (i / SIZE_OF_ARRAY) * 100
        if (i > SIZE_OF_ARRAY / 2):
            array[i][1] = 50
            array[i][2] = 0
        elif (i > SIZE_OF_ARRAY - (SIZE_OF_ARRAY / 5)):
            array[i][1] = 20
            array[i][2] = 40
    array = numpy.random.normal(array, 0.1)
    return array