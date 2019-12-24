# -*- coding: utf-8 -*-
"""
Day 2: 1202 Program Alarm

@author: Tom Williams
"""

import numpy as np
import time


def intcode_reader(intcode):
    # Given an input intcode, run the program

    program_complete = False
    idx = 0

    while not program_complete:

        # We check the intcode for an opcode. There are 3 options -- 1, 2, and 99.

        # We'll need some positions. Positions are given by the three numbers following the opcode, so pull them out
        # here.

        first_idx = intcode[idx + 1]
        second_idx = intcode[idx + 2]
        third_idx = intcode[idx + 3]

        # If the opcode is a 1, we're adding numbers

        if intcode[idx] == 1:

            intcode[third_idx] = intcode[first_idx] + intcode[second_idx]

        # If the opcode is a 2, we're multiplying

        elif intcode[idx] == 2:

            intcode[third_idx] = intcode[first_idx] * intcode[second_idx]

        elif intcode[idx] == 99:

            program_complete = True

        else:

            raise Warning('Opcode not recognised!')

        # Finally, we move along 4 steps for the next bit of the intcode.

        idx += 4

        # If this puts us beyond the end of the input, the program is complete.

        if idx > len(intcode):
            program_complete = True

    return intcode


start = time.time()

# Part One

# Read in the intcode program

original_intcode = np.loadtxt('../inputs/day_2_input.txt',
                              delimiter=',',
                              dtype=int)

intcode = original_intcode.copy()

# Restore the program to the to the "1202 program alarm" state

intcode[1] = 12
intcode[2] = 2

intcode = intcode_reader(intcode)

print(intcode[0])

# Part Two

# We now want to replace the numbers in position 1 and 2 to get the output 19690720 (in position 0). These will be
# between 0 and 99, inclusive.

first_idxs = np.arange(0, 100)
second_idxs = first_idxs.copy()

for first_idx in first_idxs:
    for second_idx in second_idxs:

        # Make sure to use the original, clean intcode

        intcode = original_intcode.copy()

        intcode[1] = first_idx
        intcode[2] = second_idx

        intcode = intcode_reader(intcode)

        if intcode[0] == 19690720:

            print('Solution found! %d ' % (100*first_idx+second_idx))
            break

print('Complete! Took %.2fs' % (time.time() - start))
