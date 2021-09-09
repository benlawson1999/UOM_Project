import json
import sys

from pathlib import Path
from objects.factory_class import Factory
from objects.order_class import Order
from objects.sku_class import SKU
from objects.recipe_class import Recipe
import numpy as np
import pickle


sys.path.append(str(Path(".").absolute().parent))
Objects = {}


def generate_factories(data: dict):
    """Code to generate factories"""
    factories = {}
    for key, value in data.items():
        factories[key] = Factory(factory_id=key, **value)
    return factories


def generate_orders(data: dict, factories_dict: dict):
    """Code to generate orders"""
    orders = {}
    for key, value in data.items():
        orders[key] = Order(order_id=key, **value)
        orders[key].optimal_distance_calc(factories_dict)
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
        recipes[key] = Recipe(**value)
    return recipes


Factories = generate_factories(
    json.load(open("./automatic_data/config_factories.json"))
)

Orders = generate_orders(
    json.load(open("./automatic_data/config_orders.json")), Factories
)
SKUs = generate_skus(json.load(open("./automatic_data/config_skus.json")))
Recipes = generate_recipes(json.load(open("./automatic_data/config_recipes.json")))
