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


ingredients = [
    "Apple",
    "Banana",
    "Chicken",
    "Beef",
    "Pork",
    "Garlic",
    "Mushrooms",
    "Pear",
    "Potatoes",
    "Cabbage",
    "Carrot",
]


def create_factories(n: int, ingredient_list: list):
    factories_json = {}
    inventory = {}
    inventory_size = np.random.choice([0, "1"], 100000, p=[0.05, 0.95])
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
            "postcode": gb_pc._data["postal_code"][np.random.randint(0, 27429)],
            "cost_weight": (np.random.randint(5, 20) / 10),
            "factory_inventory": inventory[k],
        }
    return factories_json


def create_skus(ingredient_list: list):
    skus_json = {}
    for i in range(len(ingredient_list)):
        skus_json[ingredient_list[i]] = {
            "type_id": "sku_id" + str(i),
            "unit_cost": np.random.randint(0, 15),
            "holding_cost": np.random.randint(0, 15),
            "temp_requirements": int(np.random.choice([0, 5, 25], 1)[0]),
            "target_level": int(
                np.random.choice([10, 50, 100], size=1, p=[0.85, 0.1, 0.05])[0]
            ),
        }
    return skus_json


def create_recipes(n: int):
    recipes_json = {}
    for i in range(n):
        p = np.random.randint(1, len(skus_json))
        recipes_json["recipe_" + str(i)] = {
            "ingredients": list(
                np.random.choice(list(skus_json.keys()), p, replace=False)[0:p]
            ),
            "quantities": (np.random.choice(range(1, 5), p)[0:p].tolist()),
        }
    return recipes_json


def create_orders(n: int):
    orders_json = {}
    for i in range(n):
        orders_json["order_" + str(i)] = {
            "client_id": np.random.choice(list(client_json.keys())),
            "recipes": list(
                np.random.choice(
                    list(recipes_json.keys()),
                    np.random.randint(1, len(recipes_json) + 1),
                )
            ),
            "product": [
                (np.random.choice(list(skus_json.keys()), np.random.randint(1, 2))[0])
            ],
            "factory_id": None,
        }
    return orders_json


client_json = create_clients(100)

with open("./automatic_data/config_clients.json", "w") as outfile:
    json.dump(client_json, outfile, indent=4)

factories_json = create_factories(n=10, ingredient_list=ingredients)

with open("./automatic_data/config_factories.json", "w") as outfile:
    json.dump(factories_json, outfile, indent=4)

skus_json = create_skus(ingredients)

with open("./automatic_data/config_skus.json", "w") as outfile:
    json.dump(skus_json, outfile, indent=4)

recipes_json = create_recipes(20)

with open("./automatic_data/config_recipes.json", "w") as outfile:
    json.dump(recipes_json, outfile, indent=4)

orders_json = create_orders(100)

with open("./automatic_data/config_orders.json", "w") as outfile:
    json.dump(orders_json, outfile, indent=4)
