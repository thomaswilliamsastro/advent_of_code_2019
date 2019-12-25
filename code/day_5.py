# -*- coding: utf-8 -*-
"""
Day 5: Sunny with a Chance of Asteroids

@author: Tom Williams
"""

import time

import numpy as np


def intcode_reader(intcode, system_id=1):
    # Given an input intcode, run the program

    program_complete = False
    idx = 0

    while not program_complete:

        # We check the intcode for an opcode. There are a number of options:
        # 1: add numbers
        # 2: multiply numbers
        # 3: take an input, and store it to a position
        # 4: output the value of its parameter
        # 5: jump-if-true: If first parameter non-zero, set idx to value of second parameter
        # 6: jump-if-false: If first parameter zero, set idx to value of second parameter
        # 7: less than
        # 8: equals

        # The intcode here can be up to 5 digits long. To save time here, pad with zeros to make it 5 long if some have
        # been omitted

        opcode = str(intcode[idx])

        if len(opcode) < 5:
            opcode = '{:05d}'.format(intcode[idx])

        # Pull out whether the parameters are in immediate or position mode.

        if opcode[0] == '1':
            third_mode = 'immediate'
        else:
            third_mode = 'position'
        if opcode[1] == '1':
            second_mode = 'immediate'
        else:
            second_mode = 'position'
        if opcode[2] == '1':
            first_mode = 'immediate'
        else:
            first_mode = 'position'

        # We'll need some positions. Positions are given by the three numbers following the opcode, so pull them out
        # here.

        step_forward = 2

        first_idx = intcode[idx + 1]

        if first_mode == 'immediate':
            first_term = first_idx
        else:
            first_term = intcode[first_idx]

        if opcode[-2:] in ['01', '02', '05', '06', '07', '08']:

            second_idx = intcode[idx + 2]

            if second_mode == 'immediate':
                second_term = second_idx
            else:
                second_term = intcode[second_idx]

            step_forward = 3

        if opcode[-2:] in ['01', '02', '07', '08']:
            third_idx = intcode[idx + 3]

            step_forward = 4

        if opcode[-2:] == '01':

            intcode[third_idx] = first_term + second_term

        elif opcode[-2:] == '02':

            intcode[third_idx] = first_term * second_term

        elif opcode[-2:] == '03':

            intcode[first_idx] = system_id

        elif opcode[-2:] == '04':

            print(first_term)

        elif opcode[-2:] == '05':

            if first_term != 0:
                idx = second_term
                step_forward = 0

        elif opcode[-2:] == '06':

            if first_term == 0:
                idx = second_term
                step_forward = 0

        elif opcode[-2:] == '07':

            if first_term < second_term:
                intcode[third_idx] = 1
            else:
                intcode[third_idx] = 0

        elif opcode[-2:] == '08':

            if first_term == second_term:
                intcode[third_idx] = 1
            else:
                intcode[third_idx] = 0

        elif opcode[-2:] == '99':

            program_complete = True

        else:

            raise Warning('Opcode %s not recognised!' % opcode)

        # Step forward

        idx += step_forward

        # If this puts us beyond the end of the input, the program is complete.

        if idx > len(intcode):
            program_complete = True

    return intcode


start = time.time()

# # Test cases -- 1 if system ID is 8, 0 otherwise
#
# original_intcode = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
#
# # 1 if less than 8, 0 otherwise
#
# original_intcode = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
#
# # 1 if equal to 8, 0 otherwise
#
# original_intcode = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
#
# # Jump tests: output 0 if input 0 or 1 otherwise
#
# original_intcode = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]

# Read in the intcode program

original_intcode = np.loadtxt('../inputs/day_5_input.txt',
                              delimiter=',',
                              dtype=int)

intcode = original_intcode.copy()

intcode_reader(intcode, system_id=5)

print('Complete! Took %.2fs' % (time.time() - start))
