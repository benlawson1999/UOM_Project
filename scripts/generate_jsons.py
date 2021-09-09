"""Functions to generate the JSONs used to generate objects.

create_SKUs: generates N jsons for ingredients and return a list of N length.
create_factories: generates N jsons with a random inventory of the ingredients.
create_recipes: generates N random combinations of the ingredients. Edibility is not guaranteed!
create_orders: generates N orders from a random UK postcode, with a random orders.
"""
import pgeocode
import random
import json
import numpy as np

gb_pc = pgeocode.GeoDistance("GB")


def create_skus(n: int):
    skus_json = {}

    for i in range(n):
        skus_json[i] = {
            "sku_id": i,
            "unit_cost": np.random.randint(0, 15),
        }
    ingredient_list = list(range(100))
    return skus_json, ingredient_list


def create_factories(n: int, ingredient_list: list):
    """generates N jsons with a random inventory of the ingredients."""
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


def create_recipes(n: int):
    """generates N random combinations of the ingredients."""
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
    """generates N orders from a random UK postcode, with a random orders."""
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
            "postcode": gb_pc._data["postal_code"][np.random.randint(0, 27429)],
            "batch": "Batch_A",
        }
    return orders_json


skus_json, ingredients = create_skus(5)

with open("./automatic_data/config_skus.json", "w") as outfile:
    json.dump(skus_json, outfile, indent=4)

factories_json = create_factories(n=2, ingredient_list=ingredients)

with open("./automatic_data/config_factories.json", "w") as outfile:
    json.dump(factories_json, outfile, indent=4)

skus_json = create_skus(ingredients)

with open("./automatic_data/config_skus.json", "w") as outfile:
    json.dump(skus_json, outfile, indent=4)

recipes_json = create_recipes(1)

with open("./automatic_data/config_recipes.json", "w") as outfile:
    json.dump(recipes_json, outfile, indent=4)

orders_json = create_orders(3)

with open("./automatic_data/config_orders.json", "w") as outfile:
    json.dump(orders_json, outfile, indent=4)
