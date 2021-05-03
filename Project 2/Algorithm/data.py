# Generate data for development
from collections import namedtuple
from random import choices

Items = namedtuple('Item', 'benefit, weights')
Knapsack = namedtuple('Knapsack', 'capacity')


def get_data(benefits: list, weights: list, capacities: list):
    items = []

    for i in range(0, len(benefits)):
        items.append(Items(benefits[i], list()))

    for j in range(0, len(weights)):
        for i in range(0, len(weights[0])):
            items[i].weights.append(weights[j][i])

    knapsacks = []
    for j in range(0, len(capacities)):
        knapsacks.append(Knapsack(capacities[j]))
    return items, knapsacks


def read_data(path):
    pass
