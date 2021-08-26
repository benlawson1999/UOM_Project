from scripts.generate_objects import Factories, Clients, Orders, SKUs, Recipes
from functions.WMAPE import wmape
from functions.naive_test import generate_solutions, generate_results
import matplotlib.pyplot as plt
import numpy as np
import time


def neighbour_search(
    orders_dict: dict, algorithm: str, client_dict: dict, sku_dict: dict, time_limit=60, directed = True
):

    algorithm = algorithm.lower()
    if algorithm not in ["naive", "max", "min"]:
        raise ValueError("Please only select one of naive, max or min as the algorithm")
    orders_rank = list(orders_dict.items())
    timeout_start = time.time()
    i = 0  # iteration count
    best = (10000,)
    best_order = list(orders_dict.keys())
    while time.time() < timeout_start + time_limit:
        if i > 4:
            return (
                best,
                best_order,
            )  # if 5 iterations go by without improvement, return current best
        if len(orders_dict) < 2:
            return generate_solutions(orders_dict, algorithm, client_dict, sku_dict), best_order
        else:
            distance_dict = {}
            if directed == True:
                for order in Orders_dict:
                    distance_dict[order] = orders_dict[order].difference_distance
                orders_rank = dict(sorted(distance_dict.items(), key=lambda item: item[1]))
            else:
                orders_rank = orders_dict

            n = len(orders_dict) / 4

            orders_head = orders_rank[:n]
            orders_tail = orders_rank[n:]
            np.random.shuffle(orders_tail)
            orders_head.extend(orders_tail)
            new_orders = dict(orders_head)

        results = generate_solutions(new_orders, algorithm, client_dict, sku_dict)
        if results[0] < best[0]:
            best = results
            best_order = list(new_orders.keys())
            i = 0  # iteration count resets when improvement found
        else:
            i += 1
    return best, best_order


if __name__ == "__main__":
    results, order = neighbour_search(Orders, "naive", Clients)
    generate_results(results)
