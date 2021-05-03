from collections import namedtuple
from random import choices, choice, randint

import math
import numpy as np

"""
This code provide implementation of different functions used in the genetic algorithm for solving the multidimensional 
knapsack problem.
"""

__GOLDEN_RATIO = (1 + 5 ** 0.5) / 2


def get_str_weight(s: str, weights: list) -> int:
    """
    Given a solution string of length i, this function returns the weight of the solution.
    i represents the number of items.

    :param s: Binary string solution. If index i is 1, then item i is selected otherwise it is not selected
    :param weights: Weights of all items
    :return: Total weight of this binary string
    """
    return __get_str_attribute(s, weights)


def get_objective_value(s: str, benefits: list) -> int:
    """
    Given a solution string of length i, this function returns the objective function value of this solution.
    i represents the number of items.

    :param s: Binary string solution. If index i is 1, then item i is selected otherwise it is not selected
    :param benefits: Benefits of all items.
    :return: Total benefit of this binary string
    """
    return __get_str_attribute(s, benefits)


def cross_parenting(p1: str, p2: str, k: int) -> tuple:
    """
    Given two parents, get a pair of children resulting from cross-over. The cross-over point is specified by the
    parameter K. Each parent is a binary string. Parents have the same length.

    :param p1: Parent solution 1.
    :param p2: Parent solution 2.
    :param k: Cross over point. 0 < k < length(parents) - 1
    :return: Pair of children
    """
    if k < 0 or k > len(p1):
        return p1, p2

    return p1[:k] + p2[k:], p2[:k] + p1[k:]


def mutate(s: str, start: int, end: int) -> str:
    """
    Give a solution, this function mutate it. Mutation consists of flipping bits. Mutation can affect all or part of
    the solution. This is governed by the values of START and END.

    :param s:
    :param start:
    :param end:
    :return:
    """
    condition1 = len(s) == 0 or end < start
    condition2 = start < 0 or end > len(s)

    if condition1 or condition2:
        return s

    result = s[:start]
    segment = ''
    for i in range(start, end):
        segment += '1' if s[i] == '0' else '0'
    result += segment + s[end:]

    return result


def get_violation_count(s: str, weights: list, capacities: list) -> int:
    """

    :param s: A binary string solution
    :param weights: Weights of all items in each knapsack, represented as a matrix
    :param capacities: Capacities of all knapsacks
    :return:
    """
    if len(s) < 1:
        return False

    count_violations = 0

    for j in range(0, len(weights)):
        weight = get_str_weight(s, weights[j])
        if weight > capacities[j]:
            count_violations += 1

    return count_violations


# def is_feasible(s: str, weights: list, capacities: list) -> bool:
#     """
#     Check if a solution is feasible.
#
#     :param s: A solution tuple
#     :param weights:
#     :param capacities:
#     :return:
#     """
#     if len(s) < 1:
#         return False
#
#     return get_violation_count(s, weights, capacities)


def get_binary_solution(bits: int):
    """

    :param bits: Number of items to select from.
    :return:
    """
    s = []
    for i in range(0, bits):
        s.append(str(randint(0, 1)))
    return "".join(s)


def get_solution_stream(bits: int):
    """

    :param bits: Number of items to select from.
    :return:
    """
    while True:
        yield get_binary_solution(bits)


def get_generation(number_items: int, generation_size: int, benefits: list, weights: list, capacities: list, flag: bool = False,
                   prop: float = 0.05) -> list:
    """
    Given the number of items and the size of the generation, this function creates a pool of GENERATION_SIZE solutions.
    There is an optional parameter F for including infeasible solutions. Whenever f is specified, the proportion of
    infeasible solutions must also be specified. Otherwise, the default value of 0.05, i.e., 5 percent of
    GENERATION_SIZE is used.

    :param number_items:
    :param generation_size:
    :param benefits:
    :param capacities:
    :param weights:
    :param flag:
    :param prop:
    :return:
    """

    required_number_infeasible = math.floor(prop * generation_size) if flag else 0
    number_feasible = 0
    number_infeasible = 0
    generation = []

    # Get a stream of solutions
    for solution in get_solution_stream(number_items):
        condition1 = (number_feasible + number_infeasible == generation_size)
        condition2 = (number_infeasible == required_number_infeasible)
        if condition1 and condition2:
            break

        violation_count = get_violation_count(solution, weights, capacities)
        cost = cost_function(solution, benefits, violation_count, len(capacities))

        if violation_count != 0:
            if flag and number_infeasible < required_number_infeasible:
                generation.append(tuple([solution, violation_count, cost]))
                number_infeasible += 1
        else:
            generation.append(tuple([solution, violation_count, cost]))
            number_feasible += 1
    return generation


def cost_function(s: str, benefits: list, violation_count: int, number_constraints: int):
    numerator = get_objective_value(s, benefits) * math.exp(1 / abs(number_constraints - violation_count))
    denominator = math.exp(violation_count - 1 / abs(number_constraints - violation_count))
    return numerator / denominator


def get_fitted_solutions(population: list, sample_size: int):
    """
    Given a generation sorted by their cost, return a subset of best fitted solution.
    :return:
    """

    bias_weights = [solution[2] for solution in population]
    prob = np.array(bias_weights) / np.sum(bias_weights)

    # Get random integers between 0 and len(prob)-1, drawn according to prob
    choice_indices = np.random.choice(len(prob), size=sample_size, replace=False, p=prob)

    # Get corresponding solutions
    paths = [population[i] for i in choice_indices]
    return paths


def __get_str_attribute(s: str, attribute: list):
    """
    Given a binary solution string of length i, this function return an attribute as specified by the content of the
    ATTRIBUTE parameter

    :param s:
    :param attribute:
    :return:
    """
    result = 0
    for index, value in enumerate(s):
        result += int(value) * attribute[index]
    return result
