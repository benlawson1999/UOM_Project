"""Define the solution and returns results, also can be repeated with random shuffling.

generate_results: Generates a plot and summary statistics for a run of an algorithm.
generate_solutions: Generate a solution for the given algorithm.
experiment_wrapper: Allows repetition of a given algorithm N times and returns a plot."""
import sys
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from scripts.generate_objects import Factories, Orders, SKUs, Recipes
from functions.WMAPE import wmape
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import pickle


def generate_results(results_tuple: dict, algorithm: str, sort=True):
    """Generates a plot and summary statistics for a run of an algorithm."""

    if sort is True:
        results_dict = dict(sorted(results_tuple[2].items(), key=lambda item: item[1]))
    else:
        results_dict = results_tuple[2]
    mean_wmape = results_tuple[0]
    std_dev = np.std(list(results_tuple[2].values()))
    results_per_method = {"Mean": mean_wmape, "Standard deviation": std_dev}
    plt.bar(results_dict.keys(), results_dict.values(), 1, color="red")
    plt.title("Weighted MAPE for Warehouses Over One Run for Algorithm " + algorithm)
    print(f"Factory Demand: {results_tuple[1]}")
    print(f"Mean WMAPE: {mean_wmape}")
    print(f"Factory-wise WMAPE: {results_dict}")
    print(f"Percentage of Orders Fulfilled {results_tuple[3]}")
    plt.savefig("./images/" + algorithm + "_one_run.png", bbox_inches="tight")


def generate_solutions(
    orders_dict: dict, algorithm: str, factories_dict: dict, sku_dict: dict
):
    """Generate a solution for the given algorithm."""
    algorithm = algorithm.lower()
    if algorithm not in ["naive", "max", "min"]:
        raise ValueError("Please only select one of naive, max or min as the algorithm")
    factory_demand = {}

    fulfilled_count = 0
    start = time.time()
    for order in orders_dict.values():
        order.order_list(Recipes)
        if algorithm == "naive":
            order.optimal_factory_naive(factories_dict, factory_demand)
        elif algorithm == "max":
            order.optimal_factory_ranking_max(factories_dict, factory_demand)
        elif algorithm == "min":
            order.optimal_factory_ranking_min(factories_dict, factory_demand)

        fulfilled_count += order.fulfilled
        for item, value in order.combined.items():
            if order.factory_id is None:
                continue
            if factory_demand.get(order.factory_id) is None:
                factory_demand[order.factory_id] = {}  # make a new entry
            if factory_demand[order.factory_id].get(item) is None:
                factory_demand[order.factory_id][item] = 0
            factory_demand[order.factory_id][item] += value

    fulfilled_percent = fulfilled_count / len(orders_dict) * 100
    results = {}
    for factory in factories_dict.values():
        if factory_demand.get(factory.factory_id) is None:
            factory_demand[factory.factory_id] = {}
        for item, value in factory.factory_inventory.items():  # make a new entry
            if factory_demand[factory.factory_id].get(item) is None:
                factory_demand[factory.factory_id][item] = 0
            results[factory.factory_id] = wmape(
                factory.factory_inventory, factory_demand[factory.factory_id], sku_dict
            )
        mean_wmape = sum(results.values()) / len(results)
    end = time.time()
    elapsed = end - start
    results_tuple = tuple(
        [mean_wmape, factory_demand, results, fulfilled_percent, elapsed]
    )

    return results_tuple


def experiment_wrapper(
    orders_dict: dict,
    algorithm: str,
    factory_dict: dict,
    sku_dict: dict,
    solution_time_limit=None,
    iterations=100,
    plot=True,
):
    """Allows repetition of a given algorithm N times and returns a plot"""
    experiment_dict = {}
    if type(solution_time_limit) == type(iterations):
        raise TypeError(
            "Only one of solution_time_limit or iterations can be int, and the other must be NoneType"
        )

    if solution_time_limit is None:
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
        standard_deviation = {}
        fulfilled_percent = []
        for i in range(iterations):
            min_list.append(experiment_dict[i][0])
            standard_deviation[i] = np.std(list(experiment_dict[i][2].values()))
            fulfilled_percent.append(experiment_dict[i][3])
        min_list.sort()
        if plot is True:
            plt.bar(range(iterations), min_list, 1, color="red")
            plt.title(
                "Weighted MAPE for the "
                + algorithm
                + " Algorithm Across "
                + str(iterations)
                + " Iterations"
            )
            plt.savefig(
                "./images/" + algorithm + "_" + str(iterations) + ".png",
                bbox_inches="tight",
            )
    elif iterations is None:
        timeout_start = time.time()
        timed_iterations = 0
        while time.time() < timeout_start + solution_time_limit:
            order_list = list(orders_dict.items())
            random.shuffle(order_list)
            shuffled_order = dict(order_list)
            experiment_dict[timed_iterations] = generate_solutions(
                shuffled_order, algorithm, factory_dict, sku_dict
            )
            timed_iterations += 1
        timeout_end = time.time()
        time_end = timeout_end - timeout_start
        min_list = []
        standard_deviation = {}
        fulfilled_percent = []
        for i in range(timed_iterations):
            min_list.append(experiment_dict[i][0])
            standard_deviation[i] = np.std(list(experiment_dict[i][2].values()))
            fulfilled_percent.append(experiment_dict[i][3])
        min_list.sort()
        if plot is True:
            plt.bar(range(timed_iterations), min_list, 1, color="red")
            plt.title(
                "Weighted MAPE for the "
                + algorithm
                + " Algorithm Across "
                + str(timed_iterations)
                + " Iterations"
            )
            plt.savefig("./images/" + algorithm + "_time.png", bbox_inches="tight")

    with open("./images/" + algorithm + "_results.pickle", "wb") as outfile:
        pickle.dump(experiment_dict, outfile)

    return min_list, standard_deviation, fulfilled_percent, time_end, iterations
