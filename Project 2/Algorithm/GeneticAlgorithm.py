from collections import namedtuple
from random import choices, choice

"""
This code implements a genetic algorithm for solving the multidimensional knapsack problem
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


"""
Step 0: Initialization
    1. Randomly generate a pool of K solutions.
    2. Use a binary flag to determine whether this pool of solutions contains only feasible solutions or not.
"""

# Generate data for development
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


# print(is_feasible(("00000000", "00000000", "10000000"), list(knapsacks_test.values())))

def get_binary_solution(bits: int):
    s = []
    for i in range(0, bits):
        s.append(str(choice(range(0, 2))))
    return "".join(s)


def test():
    number_items = 20
    number_knapsacks = 30
    items, knapsacks = get_data(number_items, number_knapsacks)
    generation_size = 10000

    print(items)
    print(f'{knapsacks}\n')

    benefits = [x.benefit for x in items]
    weights = [x.weight for x in items]
    capacities = [x.capacity for x in knapsacks]

    generation = [get_binary_solution(number_items) for x in range(0, generation_size)]

    for i in range(0, 5):
        while True:
            solution = []
            for p in choices(range(0, generation_size), k=2):
                solution.append(generation[p])

            if is_feasible(tuple(solution), weights, capacities):
                break
        print(f'Solution {i + 1}:')
        for s in solution:
            print(s, get_str_value(s, benefits), get_str_weight(s, weights))
        print(f'{get_objective_value(solution, benefits)}\n')


test()
