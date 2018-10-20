#!/usr/bin/env python3

import numpy

def transform_source(arrays):
    # First align values to start at the same time
    arrays = align_values(arrays)

    # Then choose the values to use
    arrays = choose_values(arrays)

    # Then calculate mean of each index
    means = calculate_means(arrays)

    # Finally return the array of means
    return means

def calculate_means(arrays):
    # TODO
    return arrays

def choose_values(arrays):
    # Here we choose which of the measurements to disregard and which to use.
    # We get approximately a few measurements every 0.1 seconds. We create the final array with measurements every 0.05 seconds.
    final_arrays = []
    for array in arrays:
        new_array = []
        currentTime = 0
        for value in array:
            if value[0] > currentTime:
                while (value[0] > currentTime):
                    currentTime += 50
                new_measurement = [currentTime, value[1], value[2]]
                new_array.append(new_measurement)
        final_arrays.append(new_array)
    return final_arrays

def align_values(arrays):
    # TODO
    return []
        
