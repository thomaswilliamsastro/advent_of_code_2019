# -*- coding: utf-8 -*-
"""
Day 4: Secure Container

@author: Tom Williams
"""

import time

import numpy as np

start = time.time()

# Part One

# Given password range

password_range = 152085, 670283

n_passwords = 0

for password in np.arange(password_range[0], password_range[1] + 1):

    # Convert into a string for later manipulation

    str_password = str(password)

    # The password only has ascending digits

    if "".join(sorted(str_password)) == str_password:

        # The password must have 2 adjacent identical digits

        for i in range(len(str_password)-1):

            if str_password[i] == str_password[i+1]:

                # Part one solution

                # n_passwords += 1
                # break

                # Part two: there must be at least one set of only 2 identical adjacent digits

                if i == 0:
                    if str_password[i+2] != str_password[i]:
                        n_passwords += 1
                        break
                elif i >= len(str_password)-2:
                    if str_password[i-1] != str_password[i]:
                        n_passwords += 1
                        break
                else:
                    if str_password[i-1] != str_password[i] and str_password[i+2] != str_password[i]:
                        n_passwords += 1
                        break

print('Number of passwords: %d' % n_passwords)

print('Complete! Took %.2fs' % (time.time()-start))
