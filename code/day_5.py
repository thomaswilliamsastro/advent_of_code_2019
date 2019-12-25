# -*- coding: utf-8 -*-
"""
Day 5: Sunny with a Chance of Asteroids

@author: Tom Williams
"""

import time

import numpy as np

from code.intcode_reader import IntcodeReader

start = time.time()

# # Test cases -- 1 if system ID is 8, 0 otherwise
#
# intcode = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
#
# # 1 if less than 8, 0 otherwise
#
# intcode = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
#
# # 1 if equal to 8, 0 otherwise
#
# intcode = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
#
# # Jump tests: output 0 if input 0 or 1 otherwise
#
# intcode = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]

# Read in the intcode program

intcode = np.loadtxt('../inputs/day_5_input.txt',
                     delimiter=',',
                     dtype=int)

reader = IntcodeReader(intcode, inputs=5)
reader.run()

print('Complete! Took %.2fs' % (time.time() - start))
