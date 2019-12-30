# -*- coding: utf-8 -*-
"""
Day 16: Flawed Frequency Transmission

@author: Tom Williams
"""

import time

import numpy as np
import itertools


def calculate_fft(signal, base_pattern=[0, 1, 0, -1], n_phases=100):
    for phase in range(n_phases):

        output_signal = []

        for element in range(len(signal)):

            # Here, modify the pattern

            new_pattern = [[base_pattern[x]] * (element + 1) for x in range(len(base_pattern))]
            new_pattern = list(itertools.chain(*new_pattern))

            # If this pattern is shorter than the input (account for the fact we'll trim off the first digit later,
            # pad out as appropriate

            if len(new_pattern) - 1 < len(signal):
                n_repeats = int(np.ceil(len(signal) / (len(new_pattern) - 1)))
                new_pattern = new_pattern * n_repeats

            # Trim the first digit

            new_pattern = new_pattern[1:]

            # And finally make as long as the input signal

            new_pattern = new_pattern[:len(signal)]

            # Multiply everything together and add up

            pattern_value = np.sum(np.array(signal) * np.array(new_pattern))

            # Finally, take the last digit of the number
            pattern_value = int(str(pattern_value)[-1])

            output_signal.append(pattern_value)

        # After all of this, set the new input signal to the output signal

        signal = output_signal

    return signal


start = time.time()

n_phases = 100
part = 2

# Read in the input signal

f = open('../inputs/day_16_input.txt', 'r')
input_signal = f.read().strip()
f.close()

# Split up into separate integers

input_signal = [int(i) for i in str(input_signal)]

if part == 1:

    # Only take the first 8 digits for longer inputs

    final_signal = calculate_fft(input_signal)
    final_signal = final_signal[:8]
    final_signal = ''.join([str(i) for i in final_signal])

    print('First 8 digits from the input signal after 100 phases are %s' % final_signal)

else:

    # The final message offset is the first 7 digits of the input signal

    signal_offset = input_signal[:7]
    signal_offset = int(''.join([str(i) for i in signal_offset]))

    # Now the REAL input signal is the original repeated 10000 times

    input_signal = input_signal * 10000
    print(len(input_signal),signal_offset)
    input_signal = input_signal[signal_offset:]

    for phase in range(n_phases):
        total_sum = 0
        for i in range(len(input_signal) - 1, -1, -1):
            total_sum = (total_sum + input_signal[i]) % 10
            input_signal[i] = total_sum

    final_signal = input_signal.copy()
    final_signal = final_signal[:8]
    final_signal = ''.join([str(i) for i in final_signal])

    print('Final signal is %s' % final_signal)

print('Complete! Took %.2fs' % (time.time() - start))
