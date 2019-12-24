# -*- coding: utf-8 -*-
"""
Day 3: Crossed Wires

@author: Tom Williams
"""

import time

import numpy as np

start = time.time()

# Part One

# Read in the paths for the wires

path_keys = ['path_1', 'path_2']

path_inputs = np.loadtxt('../inputs/day_3_input.txt',
                         dtype=str,
                         delimiter=',')

paths = {}

for i in range(len(path_inputs)):
    paths[path_keys[i]] = list(path_inputs[i])

# Example paths for testing.

# paths = {path_keys[0]: ['R8', 'U5', 'L5', 'D3'],
#          path_keys[1]: ['U7', 'R6', 'D4', 'L4']}
#
# paths = {path_keys[0]: ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'],
#          path_keys[1]: ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83']}

# For each path, find the coordinates of each point on the path and record them

path_coords = {}

for key in path_keys:

    # Set up coordinates for each path for x- and y-positions

    path_coords[key] = [(0, 0)]

    for step in paths[key]:

        # Pull out the direction and how far you're going
        direction = step[0]
        n_steps = int(step[1:])

        for _ in range(n_steps):

            # If direction is 'U', we're incrementing y-position

            if direction == 'U':
                path_coords[key].append((path_coords[key][-1][0],
                                         path_coords[key][-1][1] + 1)
                                        )

            # If direction is 'D', decrement y-position

            elif direction == 'D':
                path_coords[key].append((path_coords[key][-1][0],
                                         path_coords[key][-1][1] - 1)
                                        )

            # If direction is 'L', decrement x-position

            elif direction == 'L':
                path_coords[key].append((path_coords[key][-1][0] - 1,
                                         path_coords[key][-1][1])
                                        )

            # If direction is 'R', increment x-position

            elif direction == 'R':
                path_coords[key].append((path_coords[key][-1][0] + 1,
                                         path_coords[key][-1][1])
                                        )

# Now having calculated all that, find the positions where they cross

path_1_set = set(path_coords[path_keys[0]])
path_2_set = set(path_coords[path_keys[1]])

crossing_positions = path_1_set & path_2_set

# Calculate the Manhattan distance to those points. All paths cross at the origin so ignore that one for the purposes
# of calculating the minimum distance. Also, if points are negative take the absolute.

distances = np.array([np.sum(np.abs(crossing_position)) for crossing_position in crossing_positions])
min_dist = np.min(distances[distances > 0])

print('Minimum distance is %d' % min_dist)

# Part Two

# We must now find the minimum number of steps for the wires to cross.

crossing_idx_1 = [[path_coords[path_keys[0]].index(crossing_position),crossing_position]
                  for crossing_position in crossing_positions]
crossing_idx_2 = [[path_coords[path_keys[1]].index(crossing_position),crossing_position]
                  for crossing_position in crossing_positions]

total_n_steps = []

for i in range(len(crossing_idx_1)):
    for j in range(len(crossing_idx_2)):
        if crossing_idx_1[i][-1] == crossing_idx_2[j][-1]:
            total_n_steps.append(crossing_idx_1[i][0] + crossing_idx_2[j][0])

total_n_steps = np.array(total_n_steps)

min_steps = np.min(total_n_steps[total_n_steps > 0])

print('Minimum steps is %d' % min_steps)

print('Complete! Took %.2fs' % (time.time() - start))
