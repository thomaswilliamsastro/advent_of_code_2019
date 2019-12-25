# -*- coding: utf-8 -*-
"""
Day 8: Space Image Format

@author: Tom Williams
"""

import time

import numpy as np
import matplotlib.pyplot as plt

start = time.time()

# Read in the image data

image = []

with open('../inputs/day_8_input.txt') as f:
    for digit in f.read().strip():
        image.append(int(digit))

image = np.array(image)

# The image is 25 pixels wide and 6 tall, so reshape (including the layers)

image_height = 25
image_width = 6

n_layers = int(len(image) / (image_height * image_width))

image = image.reshape((n_layers, image_width, image_height))

# Find the layer with the fewest 0 digits

min_zero_layer = np.argmin(np.bincount(np.where(image == 0)[0]))

# For that layer, count the number of 1s and the number of 2s, and multiply

n_counts = np.bincount(image[min_zero_layer, :, :].flatten())
n_1_n_2 = n_counts[1] * n_counts[2]
print('Solution to part 1: %d' % n_1_n_2)

# Part 2

# It's time to turn the image into something useful. For each position, the topmost non-transparent pixel determines the
# colour -- 0 is black, 1 is white, 2 is transparent.

final_image = np.array([image[:, i, j][image[:, i, j] != 2][0]
                        for i in range(image_width) for j in range(image_height)])
final_image = final_image.reshape(image_width, image_height)

plt.figure()
plt.imshow(final_image, cmap='gray')
plt.show()

print('Complete! Took %.2fs' % (time.time() - start))
