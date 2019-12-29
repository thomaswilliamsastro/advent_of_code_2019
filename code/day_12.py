# -*- coding: utf-8 -*-
"""
Day 12: The N-Body Problem

@author: Tom Williams
"""

import time

import numpy as np

start = time.time()

# Number of steps to perform

n_steps = 1000
n_dim = 3

# initial_pos = np.array([(-1, 0, 2),
#                         (2, -10, -7),
#                         (4, -8, 8),
#                         (3, 5, -1)],
#                        dtype=np.float32)
# initial_pos = np.array([(-8, -10, 0),
#                         (5, 5, 10),
#                         (2, -7, 3),
#                         (9, -8, -3)],
#                        dtype=np.float32)

# Read in the input

initial_pos = []

f = open('../inputs/day_12_input.txt', 'r')

for line in f:
    line = line.strip('<>\n')
    cols = line.split(',')
    initial_pos.append(tuple([int(col.split('=')[1]) for col in cols]))

# Set up arrays for initial and current position, velocity, potential energy, and kinetic energy

initial_pos = np.array(initial_pos, dtype=np.float32)
initial_vel = np.zeros(initial_pos.shape, dtype=np.float32)

current_pos = initial_pos.copy()
current_vel = initial_vel.copy()
current_pot = np.sum(np.abs(current_pos), axis=1, dtype=np.float32)
current_kin = np.zeros(current_pot.shape, dtype=np.float32)

n_particles = initial_pos.shape[0]

# For part 2
repeat_found = np.array([0] * n_dim)
repeat_step = repeat_found.copy()

step = 0

# Comment or uncomment the appropriate while loop for each part

while not np.all(repeat_found):
# while step < n_steps:

    step += 1

    # Start by updating the velocities

    pos_diff = [current_pos - current_pos[i, :] for i in range(n_particles)]
    vel_diff = np.sign(pos_diff).sum(axis=1)
    current_vel += vel_diff

    # Update the positions, and calculate the potential and kinetic energies

    current_pos += current_vel

    # See if any moons have cycled back to their original positions

    planets_returned = np.all(current_pos == initial_pos, axis=0) & np.all(current_vel == initial_vel, axis=0)

    # If they have and this is the first instance, then save it

    idx = [planets_returned[i] and not repeat_found[i] for i in range(n_dim)]
    repeat_found[idx] = 1
    repeat_step[idx] = step

# Calculate the total energy at the end of the run

current_pot = np.sum(np.abs(current_pos), axis=1)
current_kin = np.sum(np.abs(current_vel), axis=1)
total_energy = np.sum(current_pot * current_kin)

print('Total energy after %d steps is %d' % (step, total_energy))

# Calculate the number of steps for history to repeat itself

print('Number of steps until history repeats itself is %d' % np.lcm.reduce(repeat_step))

print('Complete! Took %.2fs' % (time.time() - start))
