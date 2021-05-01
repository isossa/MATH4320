"""
This code implements a genetic algorithm for solving the multidimensional knapsack problem
"""

# Generate data for development
items_test = {i: b for i, b in enumerate([3, 1, 2, 1, 2, 2, 1, 5])}
knapsacks_test = [4, 5, 6]


def get_objective_value(s: str, benefits: list) -> int:
    """
    Given a solution string of length j, this function return the objective function value of this solution.
    j represents the number of knapsacks.

    :param s: Binary string solution. If index i is 1, then item i is selected otherwise it is not selected
    :param benefits: Benefit of each item.
    :return: Total benefit of this solution
    """
    obj_value = 0
    for index, value in enumerate(s):
        obj_value += int(value) * benefits[index]
    return obj_value


"""
Step 0: Initialization
    1. Randomly generate a pool of K solutions.
    2. Use a binary flag to determine whether this pool of solutions contains only feasible solutions or not.
"""


def solve(items: dict, knapsacks: list):
    """

    :param items:
    :param knapsacks:
    :return:
    """
    benefits = list(items.values())
    print(get_objective_value("00000000", benefits))
    print(get_objective_value("00100000", benefits))


solve(items_test, knapsacks_test)
