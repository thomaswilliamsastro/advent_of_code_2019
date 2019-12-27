# -*- coding: utf-8 -*-
"""
Day 12: The N-Body Problem

@author: Tom Williams
"""

import time
import itertools

import numpy as np

start = time.time()

# Number of steps to perform

n_steps = 1000
n_dim = 3

# initial_pos = np.array([(-1, 0, 2),
#                         (2, -10, -7),
#                         (4, -8, 8),
#                         (3, 5, -1)],
#                        dtype=float)
# initial_pos = np.array([(-8, -10, 0),
#                         (5, 5, 10),
#                         (2, -7, 3),
#                         (9, -8, -3)],
#                        dtype=float)

# Read in the input

initial_pos = []

f = open('../inputs/day_12_input.txt', 'r')

for line in f:
    line = line.strip('<>\n')
    cols = line.split(',')
    initial_pos.append(tuple([int(col.split('=')[1]) for col in cols]))

initial_pos = np.array(initial_pos,
                       dtype=float)

initial_vel = np.zeros(initial_pos.shape)
initial_pot = np.sum(np.abs(initial_pos), axis=1)
initial_kin = np.zeros(initial_pot.shape)

current_pos = initial_pos.copy()
current_vel = initial_vel.copy()
current_pot = initial_pot.copy()
current_kin = initial_kin.copy()

# Calculate all possible combinations of these particles

combinations = list(itertools.combinations(range(initial_pos.shape[0]), 2))

# For part 2
repeat_found = [False] * initial_pos.shape[1]
repeat_step = [0] * initial_pos.shape[1]

step = 0

# Comment or uncomment the appropriate while loop for each part

while not np.all(repeat_found):
    # while step < n_steps:

    # Start by updating the velocities

    for combination in combinations:
        pos_diff = current_pos[combination[0], :] - current_pos[combination[1], :]
        vel_diff = np.sign(pos_diff)

        # If the position in a particular axis is smaller in combination[0] than combination[1], pos_diff will be < 0
        # and so vel_diff = -1. In that case, the velocity will increase (and vice versa).

        current_vel[combination[1], :] += vel_diff
        current_vel[combination[0], :] -= vel_diff

    # Update the positions and velocities, and calculate the potential and kinetic energies

    current_pos += current_vel
    current_pot = np.sum(np.abs(current_pos), axis=1)
    current_kin = np.sum(np.abs(current_vel), axis=1)

    # See if any moons have cycled back to their original positions

    planets_returned = np.all(current_pos == initial_pos, axis=0) & np.all(current_vel == initial_vel, axis=0)

    for i, planet_returned in enumerate(planets_returned):

        if planet_returned and not repeat_found[i]:
            repeat_found[i] = True
            repeat_step[i] = step + 1

    step += 1

# Calculate the total energy at the end of the run

total_energy = np.sum(current_pot * current_kin)

print('Total energy after %d steps is %d' % (n_steps, total_energy))

# Calculate the number of steps for history to repeat itself

print(np.lcm.reduce(repeat_step))

print('Complete! Took %.2fs' % (time.time() - start))
