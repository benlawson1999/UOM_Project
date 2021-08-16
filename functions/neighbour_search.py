from scripts.generate_objects import Factories, Clients, Orders, SKUs, Recipes
from functions.WMAPE import wmape
from functions.naive_test import generate_solutions, generate_results
import matplotlib.pyplot as plt
import numpy as np
import time


def neighbour_search(orders_dict: dict, Type: str, time_limit=60):

    Type = Type.lower()
    if Type not in ["naive", "max", "min"]:
        raise ValueError(
            "Please only select one of naive, max or min as the objective function type"
        )
    orders_rank = list(Orders.items())
    timeout_start = time.time()
    i = 0  # iteration count
    best = (10000,)
    best_order = list(orders_dict.keys())
    while time.time() < timeout_start + time_limit:
        print(i)
        time.sleep(0.25)  # allows rest for the cpu to reduce usage
        if i > 4:
            return best, best_order # if 4 iterations go by without improvement, return current best
        n = np.random.randint(0, len(orders_dict) / 2)
        orders_head = orders_rank[:n]
        orders_tail = orders_rank[n:]
        np.random.shuffle(orders_tail)
        orders_head.extend(orders_tail)
        new_orders = dict(orders_head)

        results = generate_solutions(new_orders, Type)
        if results[0] < best[0]:
            best = results
            best_order = list(new_orders.keys())
            i = 0  # iteration count resets when improvement found
        else:
            i += 1
    return best, best_order


results, order = neighbour_search(Orders, "naive")
generate_results(results)
