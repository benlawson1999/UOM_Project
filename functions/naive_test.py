from scripts.generate_objects import Factories, Clients, Orders, SKUs, Target
from objects.factory_class import Factory
from objects.client_class import Client
from objects.order_class import Order
from objects.sku_class import SKU
from functions.WMAPE import wmape

fulfilled_count = 0
for i in Orders:

    Orders[i].order_list()
    Orders[i].optimal_factory_ranking_max(Factories)
    fulfilled_count += Orders[i].fulfilled
total_inventory = {}
fulfilled_percent = fulfilled_count / len(Orders) * 100
for i in Factories:

    for key in Factories[i].factory_inventory:
        if key in total_inventory:

            total_inventory[key] += Factories[i].factory_inventory[key]
        else:
            total_inventory[key] = Factories[i].factory_inventory[key]

result = wmape(total_inventory, Target)
print(result)
print(fulfilled_percent)
