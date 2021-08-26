from scripts.generate_objects import Factories, Clients, Orders, SKUs, Recipes
from functions.WMAPE import wmape
import matplotlib.pyplot as plt
import numpy as np


def generate_results(results_tuple: dict):
    results_per_method = {}
    sorted_dict = dict(sorted(results_tuple[2].items(), key=lambda item: item[1]))
    mean_wmape = results_tuple[0]
    std_dev = np.std(list(results_tuple[2].values()))
    results_per_method = {"Mean": mean_wmape, "Standard deviation": std_dev}
    sorted_dict = dict(sorted(results_tuple[2].items(), key=lambda item: item[1]))
    plt.bar(sorted_dict.keys(), sorted_dict.values(), 1, color="red")
    print(f"Factory Demand: {results_tuple[1]}")
    print(f"Mean WMAPE: {mean_wmape}")
    print(f"Factory-wise WMAPE: {sorted_dict}")
    print(f"Percentage of Orders Fulfilled {results_tuple[3]}")


def generate_solutions(orders_dict: dict, algorithm: str, client_dict: dict, sku_dict: dict):
    algorithm = algorithm.lower()
    if algorithm not in ["naive", "max", "min"]:
        raise ValueError("Please only select one of naive, max or min as the algorithm")
    demand = {}
    fulfilled_count = 0
    for order in Orders.values():
        order.order_list(Recipes)  # combined the recipes into a list of ingredients
        if algorithm == "naive":
            order.optimal_factory_naive(Factories, demand, client_dict)
        elif algorithm == "max":
            order.optimal_factory_ranking_max(Factories, demand, client_dict)
        elif algorithm == "min":
            order.optimal_factory_ranking_min(Factories, demand, client_dict)
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
                demand[factory.factory_id], factory.factory_inventory, sku_dict
            )
        mean_wmape = sum(results.values()) / len(results)
        results_tuple = tuple([mean_wmape, demand, results, fulfilled_percent])

    return results_tuple


if __name__ == "__main__":
    results = generate_solutions(Orders, "naive", Clients, SKUs)
    generate_results(results)
