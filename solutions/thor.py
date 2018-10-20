#!/usr/bin/env python3
__author__= "Sofia Vanhanen"

def transform_source(arrays):
    # First align values to start at the same time
    arrays = align_values(arrays)

    # Then calculate mean of each index
    means = calculate_means(arrays)

    # Finally return the array of means
    return means

def calculate_means(arrays):
    # TODO
    return arrays

def align_values(arrays):
    # TODO
    return []
        
