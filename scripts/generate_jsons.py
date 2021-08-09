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
            "postcode": gb_pc._data["postal_code"][np.random.randint(0, 27429)],
            "cost_weight": (np.random.randint(5, 20) / 10),
            "factory_inventory": inventory[k],
        }
    return factories_json


factories_json = create_factories(n=10, ingredient_list=ingredients)
factory = open("./automatic_data/config_factories.json", "w")
json.dump(factories_json, factory)


def create_skus(ingredient_list: list):
    skus_json = {}
    for i in range(len(ingredient_list)):
        skus_json[ingredient_list[i]] = {
            "type_id": "sku_id" + str(i),
            "unit_cost": np.random.randint(0, 15),
            "holding_cost": np.random.randint(0, 15),
            "temp_requirements": int(np.random.choice([0, 5, 25], 1)[0]),
            "target_level": int(
                np.random.choice([0, 5, 10], size=1, p=[0.85, 0.1, 0.05])[0]
            ),
        }
    return skus_json


skus_json = create_skus(ingredients)

sku = open("./automatic_data/config_skus.json", "w")
json.dump(skus_json, sku)


def create_recipes(n: int):
    recipes_json = {}
    for i in range(n):
        p = np.random.randint(1, len(skus_json))
        recipes_json["recipe_" + str(i)] = {
            "ingredients": np.random.choice(list(skus_json.keys()), p)[0],
            "quantities": int(np.random.choice(range(1, 11), p)[0]),
        }
    return recipes_json


recipes_json = create_recipes(10)

recipe = open("./automatic_data/config_recipes.json", "w")
json.dump(recipes_json, recipe)


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
            "product": (
                np.random.choice(list(skus_json.keys()), np.random.randint(1, 2))[0]
            ),
            "factory_id": "foo",
        }
    return orders_json


orders_json = create_orders(10)

order = open("./automatic_data/config_orders.json", "w")
json.dump(orders_json, order)
