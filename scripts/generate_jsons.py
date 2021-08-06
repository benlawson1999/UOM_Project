import pgeocode
import random
import json
import numpy as np

gb_pc = pgeocode.GeoDistance("GB")


def create_clients(n: int):
    client_json = {}
    for i in range(n):
        client_json["client_" + str(i)] = {
            "postcode": gb_pc._data["postal_code"][random.randint(0, 27429)],
            "tenure": random.randint(0, 8),
            "income": (random.randint(1, 200) * 1000),
            "age": random.randint(18, 100),
            "churn_chance": random.randint(0, 100),
        }
    return client_json


client_json = create_clients(20)
client = open("./automatic_data/config_clients.json", "w")
json.dump(client_json, client)
ingredients = ["foo", "bar"]


def create_factories(n: int, ingredient_list: list):
    factories_json = {}
    inventory = {}
    inventory_size = np.random.choice([0, "1"], 100000, p=[0.2, 0.8])
    mask = inventory_size == "1"
    inventory_size[mask] = np.random.choice(1000, len(inventory_size[mask]))
    for i in range(n):
        ingredients = {}
        ingredient_inv = {}
        for j in ingredient_list:
            ingredients[j] = int(np.random.choice(inventory_size, 1)[0])
        ingredient_inv[i] = ingredients
        inventory[i] = ingredient_inv[i]

    for k in range(n):
        factories_json["factory_" + str(k)] = {
            "postcode": gb_pc._data["postal_code"][random.randint(0, 27429)],
            "cost_weight": (random.randint(5, 20) / 10),
            "factory_inventory": inventory[k],
        }
    return factories_json


factories_json = create_factories(n=10, ingredient_list=ingredients)
factory = open("./automatic_data/config_factories.json", "w")
json.dump(factories_json, factory)
