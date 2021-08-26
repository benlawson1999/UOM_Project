import json
import sys
from pathlib import Path
from objects.factory_class import Factory
from objects.client_class import Client
from objects.order_class import Order
from objects.sku_class import SKU
from objects.recipe_class import Recipe
import numpy as np
import pickle


sys.path.append(str(Path(".").absolute().parent))
Objects = {}


def generate_0factories(data: dict):
    """Code to generate factories"""
    factories = {}
    for key, value in data.items():
        for factory_key, factory_value in value.items():
            factories[key] = Factory(batch=key, **factory_value)
    return factories

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



def generate_0orders(data: dict, client_dict):
    """Code to generate orders"""
    orders = {}
    new_orders ={}
    new_orders_B = {}
    new_orders_C = {}
    new_orders_D = {}
    new_orders_E = {}
    new_orders_F = {}
    new_orders_G = {}
    batch_dict = {"Batch_A":new_orders,"Batch_B":new_orders_B,"Batch_C":new_orders_C,"Batch_D":new_orders_D,"Batch_E":new_orders_E,"Batch_F":new_orders_F,"Batch_G":new_orders_G}
    distance ={}
    for key, value in data.items():
        orders[key] = batch_dict[key]
        for id, info in value.items():
            batch_dict[key][id] = Order( **info)
            if batch_dict[key][id].postcode in distance:
                batch_dict[key][id].optimal_distance = distance[batch_dict[key][id].postcode]
            else:
                batch_dict[key][id].optimal_distance_calc(client_dict)
                distance[batch_dict[key][id].postcode] = batch_dict[key][id].optimal_distance

    return orders

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
        recipes[key] = Recipe( **value)
    return recipes


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
