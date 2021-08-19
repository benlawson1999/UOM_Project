import json
import sys
from pathlib import Path
from objects.factory_class import Factory
from objects.client_class import Client
from objects.order_class import Order
from objects.sku_class import SKU
from objects.recipe_class import Recipe
import numpy as np


sys.path.append(str(Path(".").absolute().parent))
Objects = {}


def generate_factories(data: dict):
    """Code to generate factories"""
    factories = {}
    for key, value in data.items():
        factories[key] = Factory(factory_id=key, **value)
    return factories


def generate_clients(data: dict, factory_dict: dict):
    """Code to generate clients"""
    clients = {}
    for key, value in data.items():
        clients[key] = Client(client_id=key, **value)
        clients[key].optimal_distance_calc(factory_dict)
    return clients


def generate_orders(data: dict, client_dict):
    """Code to generate orders"""
    orders = {}
    for key, value in data.items():
        orders[key] = Order(order_id=key, **value)
        orders[key].optimal_distance_setter(client_dict)
    return orders


def generate_skus(data: dict):
    """ "Code to generate skus"""
    skus = {}
    for key, value in data.items():
        skus[key] = SKU(name=key, **value)
    return skus


def generate_recipes(data: dict):
    """Code to generate recipes"""
    recipes = {}
    for key, value in data.items():
        recipes[key] = Recipe(recipe_id=key, **value)
    return recipes


if __name__ == "__main__":
    Factories = generate_factories(
        json.load(open("./automatic_data/config_factories.json"))
    )
    Clients = generate_clients(
        json.load(open("./automatic_data/config_clients.json")), Factories
    )
    Orders = generate_orders(
        json.load(open("./automatic_data/config_orders.json")), Clients
    )
    SKUs = generate_skus(json.load(open("./automatic_data/config_skus.json")))
    Recipes = generate_recipes(json.load(open("./automatic_data/config_recipes.json")))
