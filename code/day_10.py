# -*- coding: utf-8 -*-
"""
Day 10: Monitoring Station

@author: Tom Williams
"""

import time

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

start = time.time()

# Test field

field = np.array([[0, 1, 0, 0, 1],
                  [0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1],
                  [0, 0, 0, 0, 1],
                  [0, 0, 0, 1, 1]]
                 )

# Read in the data

asteroid_file = open('../inputs/day_10_input.txt', 'r').read().split()

field = np.zeros([len(asteroid_file), len(asteroid_file[0])])

for i in range(field.shape[0]):
    for j in range(field.shape[1]):

        if asteroid_file[i][j] == '#':
            field[i,j] = 1

# Here, i is y and j is x

n_visible = np.zeros(field.shape)
n_visible[field == 0] = np.nan

asteroid_positions = list(zip(*np.where(n_visible == 0)))

# For each asteroid, loop over the positions of other asteroids, pulling out the distances to them and the angles
# between them

asteroid_data = {}

for asteroid_position_1 in asteroid_positions:

    asteroid_data[asteroid_position_1] = {}

    r2 = np.zeros(len(asteroid_positions) - 1)
    theta = np.zeros(len(asteroid_positions) - 1)
    coords = []

    idx = 0

    for asteroid_position_2 in asteroid_positions:

        # Obviously, the asteroid can see itself but it doesn't count

        if asteroid_position_2 != asteroid_position_1:
            dy = asteroid_position_2[0] - asteroid_position_1[0]
            dx = asteroid_position_2[1] - asteroid_position_1[1]

            r2[idx] = dx ** 2 + dy ** 2
            theta[idx] = np.arctan2(dy, dx)

            idx += 1

            coords.append(asteroid_position_2)

    asteroid_data[asteroid_position_1]['r2'] = r2
    asteroid_data[asteroid_position_1]['theta'] = theta
    asteroid_data[asteroid_position_1]['coords'] = coords

    n_visible[asteroid_position_1] = len(np.unique(theta))

# Finally, pull out the coordinates of the highest number

n_max = np.nanmax(n_visible)
best_position = np.where(n_visible == n_max)
best_pos_tuple = (best_position[0][0], best_position[1][0])

print('The maximum number of visible asteroids is %d' % n_max)

# Part Two:

# We now vaporise asteroids using a big ol' laser. Which is the 200th asteroid to be vaporised?

# Put the data in a pandas dataframe and sort by both theta and distance

raw_data = asteroid_data[best_pos_tuple]

df = pd.DataFrame(raw_data)
df['theta'] += np.pi/2

df_high = df[df['theta'] >= 0].sort_values(['theta', 'r2'])
df_low = df[df['theta'] < 0].sort_values(['theta', 'r2'])

df_sort = pd.concat([df_high, df_low])

asteroids_obliterated = [best_pos_tuple]
thetas = [-99]

for idx, row in df_sort.iterrows():

    if row['coords'] not in asteroids_obliterated and row['theta'] != thetas[-1]:
        thetas.append(row['theta'])
        asteroids_obliterated.append(row['coords'])

pos_obliterated = asteroids_obliterated[200][1] * 100 + asteroids_obliterated[200][0]

print('Position of 200th obliterated asteroid is %d' % pos_obliterated)

print('Complete! Took %.2fs' % (time.time() - start))
