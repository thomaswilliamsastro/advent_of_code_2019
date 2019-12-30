# -*- coding: utf-8 -*-
"""
Day 14: Space Stoichiometry

@author: Tom Williams
"""

import time

import numpy as np


def calculate_quantity(chem_reactants, chem_products,
                       bottom_key='ORE', total=1):
    if bottom_key == 'FUEL':
        return total

    q = 0
    for i, reactants in enumerate(chem_reactants):

        if bottom_key in reactants:
            parents, *_ = chem_products[i]
            parent_yield = chem_products[i][parents]

            q += np.ceil(calculate_quantity(chem_reactants,
                                            chem_products,
                                            bottom_key=parents,
                                            total=total) / parent_yield) * \
                 reactants[bottom_key]
    return q


start = time.time()

f = open('../inputs/day_14_input.txt', 'r')

chem_reactants = []
chem_products = []

# For each product in the reactions, save the reactants and the number of each required

for line in f:

    reactants, products = line.strip().split('=>')

    product_yield, product_name = products.split()

    # Pull out the name and yield for the product

    chem_products.append({product_name: int(product_yield)})

    # And then for each reactant, save the name and required amount

    reactants = reactants.split(',')

    reactant_dict = {}

    for reactant in reactants:
        reactant_amount, reactant_name = reactant.split()

        reactant_dict[reactant_name] = int(reactant_amount)

    chem_reactants.append(reactant_dict)

total_ore = calculate_quantity(chem_reactants, chem_products)

print('Total ore required is %d' % total_ore)

# Part Two: How much fuel can you make with 1e12 ore?

max_ore = 1000000000000
fuel_min, fuel_max = 1, 10000000

while fuel_max - fuel_min > 1:

    fuel = (fuel_max + fuel_min) // 2

    total_ore = calculate_quantity(chem_reactants, chem_products,
                                   total=fuel)

    if total_ore > max_ore:
        fuel_max = fuel
    else:
        fuel_min = fuel

print('With a trillion ore, can create %d fuel' % fuel_min)

print('Complete! Took %.2fs' % (time.time() - start))
