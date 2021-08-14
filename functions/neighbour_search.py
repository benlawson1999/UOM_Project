from scripts.generate_objects import Factories, Clients, Orders, SKUs, Recipes
from functions.WMAPE import wmape

best_average = 1000
demand = {}
fulfilled_count = 0
best_order = []
for order in Orders.values():
    order.order_list(Recipes)  # combined the recipes into a list of ingredients
    order.optimal_factory_naive(
        Factories
    )  # choose the factory with the highest quanitity of ingredients in the order
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
    for item, value in demand[factory.factory_id].items():  # make a new entry
        if demand[factory.factory_id].get(item) is None:
            demand[factory.factory_id][item] = 0
    results[factory.factory_id] = wmape(
        demand[factory.factory_id], factory.factory_inventory
    )
mean_wmape = sum(results.values()) / len(results)

if mean_wmape < best_average:
    best_average = mean_wmape
    best_order = list(Orders.keys())

print(mean_wmape)
print(best_order)
new_order = list(Orders.keys())[: int(len(Orders) * 0.25)]
tail = list(Orders.keys())[int(len(Orders) * 0.25) :]
for order in new_order.values():
    order.factory_id = None
