from scripts.generate_objects import Factories, Clients, Orders, SKUs, Recipes
from functions.WMAPE import wmape
import matplotlib.pyplot as plt
import numpy as np

demand = {}
fulfilled_count = 0
print(len(Orders))

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
results_per_method = {}
mean_wmape = sum(results.values()) / len(results)
std_dev = np.std(list(results.values()))
results_per_method["naive"] = {"Mean": mean_wmape, "Standard deviation": std_dev}
plt.bar(sorted_dict.keys(), sorted_dict.values(), 1, color="red")


print(f"Factory Demand: {demand}")
print(f"Mean WMAPE: {mean_wmape}")
print(f"Factory-wise WMAPE: {results}")
print(f"Percentage of Orders Fulfilled {fulfilled_percent}")
