# -*- coding: utf-8 -*-
"""
Day 1: The Tyranny of the Rocket Equation

@author: Tom Williams
"""

import numpy as np
import time

start = time.time()

# Part One

# Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module,
# take its mass, divide by three, round down, and subtract 2.

# Import the module masses

masses = np.loadtxt('../inputs/day_1_input.txt')

total_fuel = np.sum(np.floor(masses/3)-2)

print(total_fuel)

# Part 2

# We must now include the fact that the fuel has mass, and that the fuel therefore requires more fuel!

total_fuel = np.zeros(len(masses))

for i, mass in enumerate(masses):

    fuel_accounted_for = False
    fuel = mass.copy()

    while not fuel_accounted_for:

        additional_fuel = np.floor(fuel/3)-2

        if additional_fuel <= 0:
            fuel_accounted_for = True

        else:
            total_fuel[i] += additional_fuel
            fuel = additional_fuel

print(total_fuel.sum())

print('Complete! Took %.2fs' % (time.time()-start))

