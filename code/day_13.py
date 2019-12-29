# -*- coding: utf-8 -*-
"""
Day 11: Space Police

@author: Tom Williams
"""

import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from code.intcode_reader import IntcodeReader

start = time.time()

# Graphics or not

graphics = True

intcode = np.loadtxt('../inputs/day_13_input.txt',
                     delimiter=',',
                     dtype=int, )
intcode = list(intcode)

reader = IntcodeReader(intcode)
reader.run()

# Count up the number of block tiles

output = reader.output

tiles = np.array(output[2::3])
n_blocks = len(np.where(tiles == 2)[0])

print('There are %d blocks' % n_blocks)

# Part 2: Play some breakout!

move = 0
paddle_input = 0
program_complete = False
board_setup = False

intcode[0] = 2

reader = IntcodeReader(intcode,
                       pause_on_input=True,
                       inputs=paddle_input)

if graphics:
    plt.figure(figsize=(12, 8))

while not program_complete:

    reader.output = []
    reader.inputs = paddle_input

    plt.clf()

    reader.run()

    # Check to see if this is the last step
    program_complete = reader.program_complete

    # Pull out tiles and their positions, and the score
    output = reader.output
    # print(output)

    # The program outputs position and score changes, so check for those
    score_start = np.where(np.array(output) == -1)[0]

    if len(score_start) == 0:
        positions = output.copy()
        score = score.copy()
    elif len(score_start) == 1:
        positions = output[:int(score_start)] + output[int(score_start) + 3:]
        score = output[int(score_start):int(score_start) + 3]
    else:

        # If the ball destroys 2 blocks we get 2 score updates! Take the final one and remove the others from the
        # list.

        for i, idx in enumerate(score_start[:-1]):
            idx += 3*i
            del output[idx:idx + 3]

        score_start = np.where(np.array(output) == -1)[0]

        positions = output[:int(score_start)] + output[int(score_start) + 3:]
        score = output[int(score_start):int(score_start) + 3]

    x_coords = positions[::3]
    y_coords = positions[1::3]
    tile = positions[2::3]

    # If we're on step one, set up the board
    if not board_setup:
        board = np.zeros([np.max(y_coords) + 1,
                          np.max(x_coords) + 1])
        board_setup = True

    board[y_coords, x_coords] = tile

    if graphics:

        plt.imshow(board,
                   cmap='rainbow')
        plt.axis('off')

        plt.text(board.shape[1], -3,
                 'Fakeout!',
                 ha='right',
                 fontsize=24, c=cm.rainbow(np.random.rand()),
                 )

        plt.text(0, -3,
                 'Score: %s ' % score[-1],
                 fontsize=24, fontweight='bold',
                 )

        # If the ball has hit the floor, print out a game over message and break

        if np.any(board[board.shape[0] - 1, :] == 4):
            plt.text(board.shape[1] / 2, -3,
                     'GAME OVER',
                     ha='center',
                     fontsize=24, fontweight='bold',
                     )

        plt.pause(0.01)

    # We want to update the position of the intersect with the ball

    paddle_pos = np.where(board == 3)
    ball_pos = np.where(board == 4)

    # Check if the ball is moving left or right

    # Move the paddle as underneath the ball as possible

    paddle_input = np.sign(ball_pos[1][0]-paddle_pos[1][0])

if graphics:
    plt.show()

print(score[-1])

print('Complete! Took %.2fs' % (time.time() - start))
