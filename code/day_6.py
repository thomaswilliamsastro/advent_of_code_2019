# -*- coding: utf-8 -*-
"""
Day 6: Universal Orbit Map

@author: Tom Williams
"""

import time

import numpy as np

start = time.time()

# Test data: 42 orbits

# orbit_list = ['COM)B',
#               'B)C',
#               'C)D',
#               'D)E',
#               'E)F',
#               'B)G',
#               'G)H',
#               'D)I',
#               'E)J',
#               'J)K',
#               'K)L',
#               ]

# Read in the orbit data

orbit_list = np.loadtxt('../inputs/day_6_input.txt',
                        dtype=str)

orbits = {}

for orbit in orbit_list:

    orbit_split = orbit.split(')')

    orbit_1 = orbit_split[1]
    orbit_0 = orbit_split[0]

    orbits[orbit_1] = orbit_0

# Now, loop through this dictionary and count the number of orbits

n_orbits = 0

for orbit_object in orbits.keys():

    while orbit_object in orbits:
        n_orbits += 1
        orbit_object = orbits[orbit_object]

print('Number of orbits: %d' % n_orbits)

# Part Two: Find the minimum number of transfers from yourself to santa

you_code = 'YOU'
san_code = 'SAN'

you_orbits = []
san_orbits = []

while you_code in orbits:

    you_orbits.append(orbits[you_code])
    you_code = orbits[you_code]

while san_code in orbits:

    san_orbits.append(orbits[san_code])
    san_code = orbits[san_code]

you_set = set(you_orbits)
san_set = set(san_orbits)

orbits_test = you_set & san_set

min_transfers = min([you_orbits.index(orbit) + san_orbits.index(orbit) for orbit in you_set & san_set])

print('Minimum number of transfers: %d' % min_transfers)

print('Complete! Took %.2fs' % (time.time() - start))
