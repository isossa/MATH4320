"""
This code implements a genetic algorithm for solving the multidimensional knapsack problem
"""
import random
from collections import namedtuple
from random import choices
from random import random
from utils import *
from data import *


def solution():
    number_items = 6
    number_knapsacks = 10
    benefits = [100, 600, 1200, 2400, 500, 2000]
    weights = [[8, 12, 13, 64, 22, 41],
               [8, 12, 13, 64, 22, 41],
               [3, 6, 4, 18, 6, 4],
               [5, 10, 8, 32, 6, 12],
               [5, 13, 8, 42, 6, 20],
               [5, 13, 8, 48, 6, 20],
               [0, 0, 0, 0, 8, 0],
               [3, 0, 4, 0, 8, 0],
               [3, 2, 4, 0, 8, 4],
               [3, 2, 4, 8, 8, 4]
               ]
    capacities = [80, 96, 20, 36, 44, 48, 10, 18, 22, 24]
    generation_size = 10

    population = [p for p in get_generation(number_items, generation_size, benefits, weights, capacities)]
    population_str = [p[0] for p in population]

    best_fit = get_fitted_solutions(population, int(len(population) / 2))
    best_fit = sorted(best_fit, key=lambda x: x[2])
    best_solution, _, best_cost = best_fit[0]
    best_obj_value = get_objective_value(best_solution, benefits)

    for i in range(10000):
        p1, _, _ = best_fit[randint(0, len(best_fit) - 1)]
        p2, _, _ = best_fit[randint(0, len(best_fit) - 1)]
        cross_over_point = randint(0, len(p1))
        children = list(cross_parenting(p1, p2, cross_over_point))
        mutation_rate = 0.1

        # Mutate children
        for index, child in enumerate(children):
            if random() < mutation_rate:
                start = randint(0, len(child))
                end = randint(start, len(child))
                children[index] = mutate(child, start, end)

        # Check solution validity and cost function
        for index, child in enumerate(children):
            if child not in population_str:
                violation_count = get_violation_count(child, weights, capacities)
                cost = cost_function(child, benefits, violation_count, len(capacities))
                if cost > best_cost:
                    best_solution = child
                    best_cost = cost
                    best_obj_value = get_objective_value(best_solution, benefits)

    return best_solution, best_obj_value, best_cost


def restart_solver():
    """
    This function restart the solver at random.

    Mimic boosting strategy. If the algorithm is executed for a large number of time, there is a high chance that the
    solution that appear the most is close to optimality.

    :return:
    """
    pass


if __name__ == '__main__':
    print(solution())
