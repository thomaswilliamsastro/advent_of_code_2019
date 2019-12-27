# -*- coding: utf-8 -*-
"""
Day 11: Space Police

@author: Tom Williams
"""

import time

import numpy as np
import matplotlib.pyplot as plt

from code.intcode_reader import IntcodeReader

start = time.time()

part = 2

intcode = np.loadtxt('../inputs/day_11_input.txt',
                     delimiter=',',
                     dtype=int, )
intcode = list(intcode)

# Start a dictionary to record useful stuff for the robot

directions = ['up', 'right', 'down', 'left']

# Starting position for the robot

coords = (0, 0)
colour = {1:0,
          2:1}[part]
direction = 'up'

# Put this into a dictionary

robot = {'colour': [colour], 'coords': [coords], 'direction': [direction]}

program_complete = False

reader = IntcodeReader(intcode, verbose=False,
                       pause_on_output=2
                       )

while not program_complete:

    # We now want to run the intcode until it produces two outputs
    reader.inputs = colour
    reader.run()
    output = reader.output

    # First, pull out the direction it's turning
    turn = output[-1]
    if turn == 0:
        turn = -1

    colour = output[-2]

    # Update the tile colour the robot is on
    robot['colour'][robot['coords'].index(coords)] = colour

    direction = directions[(directions.index(direction) + turn) % 4]
    robot['direction'].append(direction)

    # And from that, calculate the coordinates it'll be moving to
    if direction == 'up':
        coords = (coords[0], coords[1] + 1)
    elif direction == 'down':
        coords = (coords[0], coords[1] - 1)
    elif direction == 'left':
        coords = (coords[0] - 1, coords[1])
    elif direction == 'right':
        coords = (coords[0] + 1, coords[1])
    else:
        raise Warning('Direction %s not understood' % direction)

    try:
        colour = robot['colour'][robot['coords'].index(coords)]
    except ValueError:
        colour = 0
        robot['coords'].append(coords)
        robot['colour'].append(colour)

    program_complete = reader.program_complete

n_panels = len(robot['coords'])

print('Number of panels painted: %d' % n_panels)

# Part Two: Start on a black panel and paint away

# Pull out x- and y-coords, shift to a minimum

if part == 2:

    x_pos = np.array([i[0] for i in robot['coords']])
    y_pos = np.array([i[1] for i in robot['coords']])

    x_pos -= np.min(x_pos)
    y_pos -= np.min(y_pos)

    registration = np.zeros([np.max(y_pos) + 1,
                             np.max(x_pos) + 1])

    for pos in range(len(x_pos)):
        registration[y_pos[pos], x_pos[pos]] = robot['colour'][pos]

    plt.figure()
    plt.imshow(registration, origin='lower', cmap='gray')
    plt.show()

print('Complete! Took %.2fs' % (time.time() - start))
