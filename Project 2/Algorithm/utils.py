from collections import namedtuple
from random import choices, choice

import math

"""
This code provide implementation of different functions used in the genetic algorithm for solving the multidimensional 
knapsack problem.
"""


def get_str_value(s: str, benefits: list) -> int:
    """
    Given a solution string of length i, this function returns the z-value of this solution.
    i represents the number of items.

    :param s: Binary string solution. If index i is 1, then item i is selected otherwise it is not selected
    :param benefits: Benefits of all items.
    :return: Total benefit of this binary string
    """
    return __get_str_attribute(s, benefits)


def get_str_weight(s: str, weights: list) -> int:
    """
    Given a solution string of length i, this function returns the weight of the solution.
    i represents the number of items.

    :param s: Binary string solution. If index i is 1, then item i is selected otherwise it is not selected
    :param weights: Weights of all items
    :return: Total weight of this binary string
    """
    return __get_str_attribute(s, weights)


def get_objective_value(s: tuple, benefits: list) -> int:
    """
    Given a solution, this function return the objective function value
    :param benefits: Benefit of each item.
    :param s: Tuple of k elements, each representing the solution of one knapsack
    :return: Objective function of this solution
    """
    obj_value = 0
    for i in s:
        obj_value += get_str_value(i, benefits)

    return obj_value


def cross_parenting(p1, p2, k) -> tuple:
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


def verify_unique_positional_assignment(s: tuple):
    """
    Check if an item is selected only once

    :param s: A solution tuple
    :return:
    """
    if len(s) < 1:
        return False

    number_of_items = len(s[0])

    for i in range(0, number_of_items):
        total = 0
        for j in range(0, len(s)):
            total += int(s[j][i])
        if total > 1:
            return False
    return True


def solution_is_within_capacity(s: tuple, weights: list, capacities: list):
    """

    :param s: A binary string solution
    :param weights: Weights of all items
    :param capacities: Capacities of all knapsacks
    :return:
    """
    if len(s) < 1:
        return False

    for j in range(0, len(s)):
        weight = get_str_weight(s[j], weights)
        if weight > capacities[j]:
            return False
    return True


def is_feasible(s: tuple, weights: list, capacities: list) -> bool:
    """
    Check if a solution is feasible.

    :param s: A solution tuple
    :param weights:
    :param capacities:
    :return:
    """
    if len(s) < 1:
        return False

    return verify_unique_positional_assignment(s) and solution_is_within_capacity(s, weights, capacities)


def get_binary_solution(bits: int):
    s = []
    for i in range(0, bits):
        s.append(str(choice(range(0, 2))))
    return "".join(s)


def get_stream_solution(bits: int):
    while True:
        yield get_binary_solution(bits)


def get_generation(number_items: int, generation_size: int, weights: list, capacities: list, flag: bool = False,
                   prop: float = 0.05) -> list:
    """
    Given the number of items and the size of the generation, this function creates a pool of GENERATION_SIZE solutions.
    There is an optional parameter F for including infeasible solutions. Whenever f is specified, the proportion of
    infeasible solutions must also be specified. Otherwise, the default value of 0.05, i.e., 5 percent of
    GENERATION_SIZE is used.

    :param number_items:
    :param generation_size:
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
    solution = list()
    for child in get_stream_solution(number_items):
        condition1 = (number_feasible + number_infeasible == generation_size)
        condition2 = (number_infeasible == required_number_infeasible)
        if condition1 and condition2:
            break

        if len(solution) < len(capacities):
            solution.append(child)
        elif len(solution) == len(capacities):
            if not is_feasible(tuple(solution), weights, capacities):
                if flag and number_infeasible < required_number_infeasible:
                    generation.append(solution)
                    number_infeasible += 1
            else:
                generation.append(solution)
                number_feasible += 1
            solution = list()
    return generation


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
