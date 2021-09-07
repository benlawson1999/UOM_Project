from scripts.generate_objects import Factories, Orders, SKUs, Recipes
from functions.WMAPE import wmape
import matplotlib.pyplot as plt
import numpy as np
from itertools import islice
import random
import time
import pickle


def generate_results(results_tuple: dict, algorithm: str):
    results_per_method = {}
    sorted_dict = dict(sorted(results_tuple[2].items(), key=lambda item: item[1]))
    mean_wmape = results_tuple[0]
    std_dev = np.std(list(results_tuple[2].values()))
    results_per_method = {"Mean": mean_wmape, "Standard deviation": std_dev}
    sorted_dict = dict(sorted(results_tuple[2].items(), key=lambda item: item[1]))
    plt.bar(sorted_dict.keys(), sorted_dict.values(), 1, color="red")
    plt.title("Weighted MAPE for Warehouses Over One Run for Algorithm "+algorithm)
    print(f"Factory Demand: {results_tuple[1]}")
    print(f"Mean WMAPE: {mean_wmape}")
    print(f"Factory-wise WMAPE: {sorted_dict}")
    print(f"Percentage of Orders Fulfilled {results_tuple[3]}")
    plt.savefig("./images/" + algorithm + "_one_run.png", bbox_inches="tight")


def generate_solutions(
    orders_dict: dict, algorithm: str, factories_dict: dict, sku_dict: dict
):
    algorithm = algorithm.lower()
    if algorithm not in ["naive", "max", "min"]:
        raise ValueError("Please only select one of naive, max or min as the algorithm")
    demand = {}

    fulfilled_count = 0
    start = time.time()
    for order in orders_dict.values():
        order.order_list(Recipes)  # combined the recipes into a list of ingredients
        if algorithm == "naive":
            order.optimal_factory_naive(factories_dict, demand)
        elif algorithm == "max":
            order.optimal_factory_ranking_max(factories_dict, demand)
        elif algorithm == "min":
            order.optimal_factory_ranking_min(factories_dict, demand)
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

    fulfilled_percent = fulfilled_count / len(orders_dict) * 100
    results = {}
    for factory in factories_dict.values():
        if demand.get(factory.factory_id) is None:
            demand[factory.factory_id] = {}
        for item, value in factory.factory_inventory.items():  # make a new entry
            if demand[factory.factory_id].get(item) is None:
                demand[factory.factory_id][item] = 0
            results[factory.factory_id] = wmape(
                factory.factory_inventory, demand[factory.factory_id], sku_dict
            )
        mean_wmape = sum(results.values()) / len(results)
    end = time.time()
    elapsed = end - start
    results_tuple = tuple([mean_wmape, demand, results, fulfilled_percent, elapsed])

    return results_tuple



def experiment_wrapper(
    orders_dict: dict,
    algorithm: str,
    factory_dict: dict,
    sku_dict: dict,
    time_sol=None,
    iterations=100,
    plot=True,
):
    experiment_dict = {}
    if type(time_sol) == type(iterations):
        raise TypeError(
            "Only one of time_sol or iterations can be int, and the other must be NoneType"
        )

    if time_sol == None:
        timeout_start = time.time()
        for i in range(iterations):
            order_list = list(orders_dict.items())
            random.shuffle(order_list)
            shuffled_order = dict(order_list)
            experiment_dict[i] = generate_solutions(
                shuffled_order, algorithm, factory_dict, sku_dict
            )
        timeout_end = time.time()
        time_end = timeout_end - timeout_start
        min_list = []
        standard = {}
        fulfilled_percent = []
        for i in range(iterations):
            min_list.append(experiment_dict[i][0])
            standard[i] = np.std(list(experiment_dict[i][2].values()))
            fulfilled_percent.append(experiment_dict[i][3])
        min_list.sort()
        if plot == True:
            plt.bar(range(iterations), min_list, 1, color="red")
            plt.title(
                "Weighted MAPE for the " +algorithm+" Algorithm Across "
                + str(iterations)
                + " Iterations"
            )
            plt.savefig(
                "./images/" + algorithm + "_" + str(iterations) + ".png",
                bbox_inches="tight",
            )
    elif iterations == None:
        timeout_start = time.time()
        its = 0
        while time.time() < timeout_start + time_sol:
            order_list = list(orders_dict.items())
            random.shuffle(order_list)
            shuffled_order = dict(order_list)
            experiment_dict[its] = generate_solutions(
                shuffled_order, algorithm, factory_dict, sku_dict
            )
            its += 1
        timeout_end = time.time()
        time_end = timeout_end - timeout_start
        min_list = []
        standard = {}
        fulfilled_percent = []
        for i in range(its):
            min_list.append(experiment_dict[i][0])
            standard[i] = np.std(list(experiment_dict[i][2].values()))
            fulfilled_percent.append(experiment_dict[i][3])
        min_list.sort()
        if plot == True:
            plt.bar(range(its), min_list, 1, color="red")
            plt.title(
                "Weighted MAPE for the "
                + algorithm
                + " Algorithm Across "
                + str(its)
                + " Iterations"
            )
            plt.savefig("./images/" + algorithm + "_time.png", bbox_inches="tight")

    with open("./images/" + algorithm + "_results.pickle", "wb") as outfile:
        pickle.dump(experiment_dict, outfile)

    return min_list, standard, fulfilled_percent, time_end, iterations
