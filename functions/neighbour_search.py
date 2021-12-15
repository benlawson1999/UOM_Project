"""Module to run directed neighbourhood search for the 3 random search algorithms.

neighbour_search: Runs the chosen algorithm until either the system times out,
or x runs are reached without improvement.
"""
import sys
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from functions.naive_test import generate_solutions
import numpy as np
import time


def neighbour_search(
    orders_dict: dict,
    algorithm: str,
    factories_dict: dict,
    sku_dict: dict,
    time_limit=600000,
    iteration_limit=4,
):
    """Runs the chosen algoirthm until one of the two break criteria are met."""

    algorithm = algorithm.lower()
    if algorithm not in ["naive", "max", "min"]:
        raise ValueError("Please only select one of naive, max or min as the algorithm")
    orders_rank = list(orders_dict.items())
    timeout_start = time.time()
    iteration_count = int(0)
    best_order = list(orders_dict.keys())
    best = generate_solutions(orders_dict, algorithm, factories_dict, sku_dict)
    distance_dict = {}
    while time.time() < timeout_start + time_limit:
        if iteration_count > iteration_limit:
            return (
                best,
                best_order,
            )
        if len(orders_dict) < 2:
            return (
                generate_solutions(orders_dict, algorithm, factories_dict, sku_dict),
                best_order,
            )

        distance_dict = {}

        for order in orders_dict:
            distance_dict[order] = orders_dict[order].calculate_difference(
                factories_dict
            )
        orders_rank = dict(sorted(distance_dict.items(), key=lambda item: item[1]))

        n = int(len(orders_dict) / 4)

        orders_head = list(orders_rank.items())[:n]
        orders_tail = list(orders_rank.items())[n:]
        np.random.shuffle(orders_tail)
        orders_head.extend(orders_tail)
        new_orders = dict(orders_head)
        generate_new_orders = {}
        for i in list(new_orders.keys()):
            generate_new_orders[i] = orders_dict[i]

        results = generate_solutions(
            generate_new_orders, algorithm, factories_dict, sku_dict
        )
        if results[0] < best[0]:
            best = results
            best_order = list(new_orders.keys())
            iteration_count = 0
        else:
            iteration_count += int(1)

    return best, best_order
