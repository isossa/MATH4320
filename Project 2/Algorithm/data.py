# Generate data for development
from collections import namedtuple
from random import choices

Items = namedtuple('Item', 'benefit, weight')
Knapsack = namedtuple('Knapsack', 'capacity')


def get_data(number_items, number_knapsacks):
    benefits = choices(range(1, 3), k=number_items)
    weights = choices(range(2, 10), k=number_items)
    capacities = choices(range(50, 100), k=number_knapsacks)

    items = []

    for i in range(0, len(benefits)):
        items.append(Items(benefits[i], weights[i]))

    knapsacks = []
    for j in range(0, len(capacities)):
        knapsacks.append(Knapsack(capacities[j]))
    return items, knapsacks
