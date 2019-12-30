# -*- coding: utf-8 -*-
"""
Day 15: Oxygen System

@author: Tom Williams
"""

import time

import numpy as np
import matplotlib.pyplot as plt

from code.intcode_reader import IntcodeReader


def get_adjacent(cell, maze):
    # Find all acceptable adjacent cells in the maze
    cells = []

    if current_cell[0] < maze.shape[1] - 1:

        # Get cell to right

        if maze[cell[1], cell[0] + 1] in [1, 2, 3]:
            cells.append((cell[0] + 1, cell[1]))

    if cell[0] > 0:

        # Get cell to left

        if maze[cell[1], cell[0] - 1] in [1, 2, 3]:
            cells.append((cell[0] - 1, cell[1]))

    if cell[1] < maze.shape[0] - 1:

        # Get cell above

        if maze[cell[1] + 1, cell[0]] in [1, 2, 3]:
            cells.append((cell[0], cell[1] + 1))

    if cell[1] > 0:

        # Get cell below

        if maze[cell[1] - 1, cell[0]] in [1, 2, 3]:
            cells.append((cell[0], cell[1] - 1))

    return cells


start = time.time()

intcode = np.loadtxt('../inputs/day_15_input.txt',
                     delimiter=',',
                     dtype=int, )
intcode = list(intcode)

# Set up initial positions and values. We'll use a value of 3 to indicate the starting tile, but the others will be 0
# for acceptable path, 1 for wall, 2 for oxygen.

current_pos = (0, 0)

positions = [current_pos]
position_value = [3]

# Set up arrays that describe movements
movements = [1, 3, 2, 4]
movements_dx = [0, -1, 0, 1]
movements_dy = [1, 0, -1, 0]
movement_i = 2

reader = IntcodeReader(intcode,
                       pause_on_output=1)

fully_explored = False

while not fully_explored:

    # print(movements[movement_i])
    reader.inputs = movements[movement_i]
    reader.output = []

    reader.run()
    output = reader.output

    new_position = (current_pos[0] + movements_dx[movement_i],
                    current_pos[1] + movements_dy[movement_i])

    try:
        idx = positions.index(new_position)
    except ValueError:
        positions.append(new_position)
        position_value.append(reader.output[-1])

    if output[-1] in [1, 2]:
        current_pos = new_position

        # We need to decide where to go next. Preferentially turn left.

        movement_i = (movement_i + 1) % 4

    else:

        # We've hit a wall, so take previous direction and turn right

        movement_i = (movement_i - 1) % 4

    # If we've returned to the origin, we should be done!

    if current_pos == (0, 0):
        fully_explored = True

# Once we've explored everywhere, turn this into a nice grid

x_min, x_max = np.min([x[0] for x in positions]), np.max([x[0] for x in positions])
y_min, y_max = np.min([y[1] for y in positions]), np.max([y[1] for y in positions])

maze = np.zeros([y_max - y_min + 1, x_max - x_min + 1])
maze[maze == 0] = 0

for i, position in enumerate(positions):
    x = position[0] - x_min
    y = position[1] - y_min

    maze[y, x] = position_value[i]

# Having filled in the whole maze (aaaah), now find the shortest path from entrance (3) to exit (2)

origin = np.where(maze == 3)
end = (np.where(maze == 2)[1][0], np.where(maze == 2)[0][0])

cells_waiting = [(origin[1][0], origin[0][0])]
cells_processed = []
cells_f_values = []

cell_parameters = {}
cell_parameters[cells_waiting[0]] = {'G': 0,
                                     'H': 10 * (np.abs(origin[1][0] - end[1]) + np.abs(origin[0][0] - end[0])),
                                     'parent': 'start'}
cell_parameters[cells_waiting[0]]['F'] = cell_parameters[cells_waiting[0]]['G'] + cell_parameters[cells_waiting[0]]['H']

cells_f_values.append(cell_parameters[cells_waiting[0]]['F'])

while end not in cells_processed:

    # Find where the minimum F value is and start with that one. If there are multiple, use the last one added

    idx = np.argmin(cells_f_values[::-1])

    current_cell = cells_waiting[idx]
    cells_processed.append(current_cell)
    cells_waiting.pop(idx)
    cells_f_values.pop(idx)

    # Find adjacent cells that are not walls

    cells = get_adjacent(current_cell, maze)

    # For each cell, calculate G (the number of steps from the starting cell), and H (the distance to the end, assuming
    # no walls)

    for cell in cells:

        # We only update ones that haven't been processed

        if cell not in cells_processed:
            g = cell_parameters[current_cell]['G'] + 10
            h = 10 * (np.abs(cell[0] - end[0]) + np.abs(cell[1] - end[1]))
            f = g + h

            cell_parameters[cell] = {'parent': current_cell,
                                     'G': g,
                                     'H': h,
                                     'F': f}

            cells_waiting.append(cell)
            cells_f_values.append(f)

# Working back from the final entry in cells_processed, get the parent

parent = end
n_steps = 0

while not parent == 'start':
    idx = cells_processed.index(parent)

    # Highlight the path
    # maze[parent[1], parent[0]] = 4
    parent = cell_parameters[cells_processed[idx]]['parent']
    n_steps += 1

print('Number of steps required is %d' % (n_steps - 1))

# Part Two: Fill the place with oxygen!

# We'll use 5 to indicate that oxygen is in the space

maze[end[1], end[0]] = 5

n_steps = 0

while np.any(maze == 1):

    idx = np.where(maze == 5)

    for i, j in zip(*idx):
        cells = get_adjacent((j, i), maze)

        for cell in cells:
            maze[cell[1], cell[0]] = 5

    n_steps += 1

print('Number of minutes to fill place with oxygen: %d' % n_steps)

plt.figure()
plt.imshow(maze, origin='lower', cmap='gray')
plt.axis('off')
# plt.show()

print('Complete! Took %.2fs' % (time.time() - start))
