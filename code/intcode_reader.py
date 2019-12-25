# -*- coding: utf-8 -*-
"""
Intcode reader

@author: Tom Williams
"""

import numpy as np


class IntcodeReader:

    def __init__(self, intcode, inputs=None, verbose=False, amplifier=False):
        self.program_complete = False
        self.amplifier = amplifier
        self.idx = 0
        self.inputs = inputs
        self.inputs_idx = 0

        # Store the intcode, the original (since bits will get replaced), and the instruction code
        self.intcode = intcode.copy()
        self.original_intcode = intcode.copy()
        self.instruction = None

        # Opcode, associated parameters, and steps to move after executing
        self.opcode = None
        self.n_parameters = None
        self.parameters = None
        self.positions = None
        self.n_steps = 0

        # Modes for the parameters
        self.modes = None

        # And any outputs saved
        self.output = []

        self.verbose = verbose

    def parse_opcode(self):

        self.instruction = '{:05d}'.format(self.intcode[self.idx])
        self.modes = [int(self.instruction[2]),
                      int(self.instruction[1]),
                      int(self.instruction[0])]

        self.opcode = int(self.instruction[-2:])

        self.n_parameters = {1: 3,
                             2: 3,
                             3: 1,
                             4: 1,
                             5: 2,
                             6: 2,
                             7: 3,
                             8: 3,
                             99: 0,
                             }[self.opcode]

        self.n_steps = self.n_parameters + 1

        # Pull out values depending on whether they're in immediate or position mode

        self.parameters = np.zeros(self.n_parameters,
                                   dtype=int)
        self.positions = np.zeros(self.n_parameters,
                                  dtype=int)

        for i in range(self.n_parameters):

            self.positions[i] = self.intcode[self.idx + i + 1]

            if self.modes[i] == 0:
                self.parameters[i] = self.intcode[self.positions[i]]
            elif self.modes[i] == 1:
                self.parameters[i] = self.positions[i]
            else:
                raise Warning('Unsupported mode %d' % self.modes[i])

    def run(self):

        while not self.program_complete:

            self.parse_opcode()

            # There are a number of opcode options:
            # 1: add numbers
            # 2: multiply numbers
            # 3: take an input, and store it to a position
            # 4: output the value of its parameter
            # 5: jump-if-true: If first parameter non-zero, set idx to value of second parameter
            # 6: jump-if-false: If first parameter zero, set idx to value of second parameter
            # 7: less than
            # 8: equals

            if self.opcode == 1:

                self.intcode[self.positions[2]] = self.parameters[0] + self.parameters[1]

            elif self.opcode == 2:

                self.intcode[self.positions[2]] = self.parameters[0] * self.parameters[1]

            elif self.opcode == 3:

                if type(self.inputs) == list:
                    input = self.inputs[self.inputs_idx]

                    self.inputs_idx = np.min([self.inputs_idx + 1, len(self.inputs) - 1])

                else:
                    input = self.inputs

                self.intcode[self.positions[0]] = input

            elif self.opcode == 4:

                if self.verbose:
                    print(self.parameters[0])
                self.output.append(self.parameters[0])
                if self.amplifier:
                    self.idx += self.n_steps
                    return

            elif self.opcode == 5:

                if self.parameters[0] != 0:
                    self.idx = self.parameters[1]
                    self.n_steps = 0

            elif self.opcode == 6:

                if self.parameters[0] == 0:
                    self.idx = self.parameters[1]
                    self.n_steps = 0

            elif self.opcode == 7:

                if self.parameters[0] < self.parameters[1]:
                    self.intcode[self.positions[2]] = 1
                else:
                    self.intcode[self.positions[2]] = 0

            elif self.opcode == 8:

                if self.parameters[0] == self.parameters[1]:
                    self.intcode[self.positions[2]] = 1
                else:
                    self.intcode[self.positions[2]] = 0

            elif self.opcode == 99:

                self.program_complete = True

            else:

                raise Warning('Opcode %d not recognised!' % self.opcode)

            # Step forward

            self.idx += self.n_steps

            # If this puts us beyond the end of the input, the program is complete.

            if self.idx > len(self.intcode):
                self.program_complete = True
