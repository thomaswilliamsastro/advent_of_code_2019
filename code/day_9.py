# -*- coding: utf-8 -*-
"""
Day 9: Sensor Boost

@author: Tom Williams
"""

import time

import numpy as np

from code.intcode_reader import IntcodeReader

start = time.time()

# # Test code
#
# # Should output a copy of itself
#
# intcode = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
#
# # Should output a 16 digit number
#
# intcode = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
#
# # Should output the large number in the middle
#
# intcode = [104, 1125899906842624, 99]

# Read in the input data

intcode = np.loadtxt('../inputs/day_9_input.txt',
                     delimiter=',',
                     dtype=int,)
intcode = list(intcode)

reader = IntcodeReader(intcode, verbose=False,
                       inputs=2,
                       )

reader.run()

print(reader.output)

print('Complete! Took %.2fs' % (time.time()-start))
