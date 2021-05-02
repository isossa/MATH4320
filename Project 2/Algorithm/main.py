"""
This code implements a genetic algorithm for solving the multidimensional knapsack problem
"""
from collections import namedtuple
from random import choices
from utils import *
from data import *

"""
Step 0: Initialization
    1. Randomly generate a pool of K solutions.
    2. Use a binary flag to determine whether this pool of solutions contains only feasible solutions or not.
"""


def solve(items: Items, knapsacks: Knapsack):
    """

    :param items:
    :param knapsacks:
    :return:
    """
    benefits = list(items.values())
    print(get_str_value("00000000", benefits))
    print(get_str_value("00100000", benefits))
    print(get_str_value("11111111", benefits))


"""
 TEST
"""


def test():
    number_items = 20
    number_knapsacks = 30
    items, knapsacks = get_data(number_items, number_knapsacks)
    generation_size = 1

    print(items)
    print(f'{knapsacks}\n')

    benefits = [x.benefit for x in items]
    weights = [x.weight for x in items]
    capacities = [x.capacity for x in knapsacks]

    for i in get_generation(number_items, generation_size, weights, capacities, flag=True, prop=1):
        print(i)


test()

