# -*- coding: utf-8 -*-
"""
Day 7: Amplification Circuit

@author: Tom Williams
"""

import time
from itertools import permutations

import numpy as np

from code.intcode_reader import IntcodeReader

start = time.time()

# Test programs

# # Should produce 43210
#
# intcode = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
#
# # Should produce 54321
#
# intcode = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]

# Read in the intcode

intcode = np.loadtxt('../inputs/day_7_input.txt',
                     delimiter=',',
                     dtype=int)

phase_settings = [0, 1, 2, 3, 4]
phase_combinations = list(permutations(phase_settings))

signal = []

for phase_combination in phase_combinations:

    input_signal = 0

    for phase_setting in phase_combination:
        inputs = [phase_setting, input_signal]

        reader = IntcodeReader(intcode, inputs=inputs)
        reader.run()

        # Pull the output from here and feed back in for the next iteration

        input_signal = reader.output[-1]

    signal.append(input_signal)

max_signal = np.max(signal)
max_signal_pos = np.argmax(signal)
best_combination = "".join([str(value) for value in phase_combinations[max_signal_pos]])
print('Maximum signal is %d with combination %s ' % (max_signal, best_combination))

# Part 2

# We now have a feedback loop. Into this we put the phase settings 5 through 9, and loop around and around until the
# program halts

# Testing programs

# Should produce 139629729 (from phase setting sequence 9,8,7,6,5)

# intcode = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0,
#            0, 5]

phase_settings = [5, 6, 7, 8, 9]
phase_combinations = list(permutations(phase_settings))

signal = []

for phase_combination in phase_combinations:

    input_signal = 0

    # Set up a number of machines in a dictionary

    readers = {}

    for i in range(len(phase_combination)):
        readers[i] = IntcodeReader(intcode, pause_on_output=1)

    amplification_finished = False

    while not amplification_finished:

        programs_complete = []

        for i, phase_setting in enumerate(phase_combination):
            inputs = [phase_setting, input_signal]

            readers[i].inputs = inputs
            readers[i].run()

            # Pull the output from here and feed back in for the next iteration

            input_signal = readers[i].output[-1]

            programs_complete.append(readers[i].program_complete)

        amplification_finished = np.all(programs_complete)

    signal.append(input_signal)

max_signal = np.max(signal)
max_signal_pos = np.argmax(signal)
best_combination = "".join([str(value) for value in phase_combinations[max_signal_pos]])
print('Maximum signal is %d with combination %s ' % (max_signal, best_combination))

print('Complete! Took %.2fs' % (time.time() - start))
