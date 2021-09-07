import pgeocode
import random
import json
import numpy as np

gb_pc = pgeocode.GeoDistance("GB")


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
    inventory_size = np.random.choice([0, "1"], 100000, p=[0, 1])
    mask = inventory_size == "1"
    inventory_size[mask] = np.random.choice(100, len(inventory_size[mask]))
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
            "factory_inventory": inventory[k],
        }
    return factories_json


def create_skus(ingredient_list: list):
    skus_json = {}
    for i in range(len(ingredient_list)):
        skus_json[ingredient_list[i]] = {
            "sku_id": i,
            "unit_cost": np.random.randint(0, 15),
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
            "quantity": (np.random.choice(range(1, 5), p)[0:p].tolist()),
        }
    return recipes_json


def create_orders(n: int):
    orders_json = {}
    for i in range(n):
        orders_json["order_" + str(i)] = {
            "recipes": list(
                np.random.choice(
                    list(recipes_json.keys()),
                    1,
                )
            ),
            "product": [
                (np.random.choice(list(skus_json.keys()), np.random.randint(1, 2))[0])
            ],
            "factory_id": None,
            "postcode" : gb_pc._data["postal_code"][np.random.randint(0, 27429)],
            "batch" = "Batch_A"
        }
    return orders_json


factories_json = create_factories(n=2, ingredient_list=ingredients)

with open("./automatic_data/config_factories.json", "w") as outfile:
    json.dump(factories_json, outfile, indent=4)

skus_json = create_skus(ingredients)

with open("./automatic_data/config_skus.json", "w") as outfile:
    json.dump(skus_json, outfile, indent=4)

recipes_json = create_recipes(1)

with open("./automatic_data/config_recipes.json", "w") as outfile:
    json.dump(recipes_json, outfile, indent=4)

orders_json = create_orders(1)

with open("./automatic_data/config_orders.json", "w") as outfile:
    json.dump(orders_json, outfile, indent=4)
