#!/usr/bin/env python3

import numpy
import os
import sys
import builtins
import generator_test

def transform_source(arrays):
    # First align values to start at the same time
    arrays = align_values(arrays)

    # Then choose the values to use
    arrays = choose_values(arrays)

    # Then calculate mean of each index
    means = calculate_means(arrays)

    # Finally return the array of means
    return means

def align_values(arrays):
    final_arrays = [] # Three-dimensional
    for array in arrays:
        new_array = [] # Two-dimensional
        starting_time = 0
        for value in array:
            if (starting_time == 0):
                if value[1] > 0 or value[2] > 0:
                    starting_time = value[0]
            if (starting_time != 0): # no elif in order to handle first case
                new_array.append([value[0] - starting_time, value[1], value[2]])
        final_arrays.append(new_array)
    return final_arrays

def choose_values(arrays):
    # Here we choose which of the measurements to disregard and which to use.
    # We get approximately a few measurements every 0.1 seconds. We create the final array with measurements every 0.05 seconds.
    final_arrays = [] # Three-dimensional
    for array in arrays:
        new_array = [] # Two-dimensional
        currentTime = 0
        for value in array:
            if value[0] > currentTime:
                while (value[0] > currentTime + 50): # Ensure we didn't skip one (possible due to infrequent recordings)
                    if (currentTime == 0): # Corner case
                        new_array.append([currentTime, 0, 0])
                    else:
                        last_one = new_array[len(new_array) - 1].copy()
                        last_one[0] = currentTime
                        new_array.append(last_one)
                    currentTime += 50
                new_measurement = [currentTime, value[1], value[2]]
                new_array.append(new_measurement)
                currentTime += 50
        final_arrays.append(new_array)
    return final_arrays

def calculate_means(arrays):
    final_array = [] # Two-dimensional
    i = 0
    while True:
        time = i * 50
        mean_1 = 0
        mean_2 = 0
        number_of_arrays_handled = 0

        for array in arrays:
            if (len(array) > i):
                if array[i][0] != time and time != 0:
                    raise Exception('Time was not expected: ' + str(array[i][0]))
                mean_1 += array[i][1]
                mean_2 += array[i][2]
                number_of_arrays_handled += 1

        if (number_of_arrays_handled == 0):
            return final_array

        mean_1 = mean_1 / number_of_arrays_handled
        mean_2 = mean_2 / number_of_arrays_handled
        final_array.append([time, mean_1, mean_2])

        i += 1

    return final_array
