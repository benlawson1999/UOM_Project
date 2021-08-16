from scripts.generate_objects import Factories, Clients, Orders, SKUs, Recipes
from functions.WMAPE import wmape
import matplotlib.pyplot as plt
import numpy as np
import time

demand = {}
fulfilled_count = 0

orders_rank = list(Orders.items())


def solution_gen(Orders: dict):
    demand = {}
    fulfilled_count = 0
    for order in Orders.values():
        order.order_list(Recipes)  # combined the recipes into a list of ingredients
        order.optimal_factory_naive(Factories, demand)
        # choose the factory with the highest quanitity of ingredients in the order
        fulfilled_count += order.fulfilled  # 1 added if fulfilled, 0 if not
        for item, value in order.combined.items():
            if order.factory_id is None:
                continue
            if demand.get(order.factory_id) is None:
                demand[order.factory_id] = {}  # make a new entry
            if demand[order.factory_id].get(item) is None:
                demand[order.factory_id][item] = 0
            demand[order.factory_id][item] += value

    fulfilled_percent = fulfilled_count / len(Orders) * 100
    results = {}
    for factory in Factories.values():
        if demand.get(factory.factory_id) is None:
            demand[factory.factory_id] = {}
        for item, value in Factories[
            factory.factory_id
        ].factory_inventory.items():  # make a new entry
            if demand[factory.factory_id].get(item) is None:
                demand[factory.factory_id][item] = 0
            results[factory.factory_id] = wmape(
                demand[factory.factory_id], factory.factory_inventory
            )
    sorted_dict = dict(sorted(results.items(), key=lambda item: item[1]))
    mean_wmape = sum(results.values()) / len(results)
    return mean_wmape, results, fulfilled_percent


def neighbour_search(Orders: dict, time_limit=120):
    timeout_start = time.time()
    i = 0  # iteration count
    best = (10000,)
    best_order = list(Orders.keys())
    while time.time() < timeout_start + time_limit:
        time.sleep(0.25)
        if i > 4:
            return best, best_order
        n = np.random.randint(0, len(Orders) / 2)
        orders_head = orders_rank[:n]
        orders_tail = orders_rank[n:]
        np.random.shuffle(orders_tail)
        orders_head.extend(orders_tail)
        new_orders = dict(orders_head)

        results = solution_gen(new_orders)
        if results[0] < best[0]:
            best = results
            best_order = list(new_orders.keys())
            i = 0  # iteration count resets when improvement found
        else:
            i += 1
    return best, best_order


results = neighbour_search(Orders)
print(results)
