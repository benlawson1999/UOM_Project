from scripts.generate_objects import Factories, Clients, Orders, SKUs, Target, Recipes
from objects.factory_class import Factory
from objects.client_class import Client
from objects.order_class import Order
from objects.sku_class import SKU
from objects.recipe_class import Recipe
from functions.WMAPE import wmape

fulfilled_count = 0
for k in Orders:

    Orders[k].order_list(Recipes)
    Orders[k].optimal_factory_ranking_min(Factories)

    fulfilled_count += Orders[k].fulfilled
total_inventory = {}
fulfilled_percent = fulfilled_count / len(Orders) * 100
for k in Factories:

    for key in Factories[k].factory_inventory:
        if key in total_inventory:

            total_inventory[key] += Factories[k].factory_inventory[key]
        else:
            total_inventory[key] = Factories[k].factory_inventory[key]
print(total_inventory)
print(Target)
result = wmape(total_inventory, Target)
print(result)
print(fulfilled_percent)
