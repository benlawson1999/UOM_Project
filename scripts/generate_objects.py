import json
import sys
from pathlib import Path
from objects.factory_class import Factory
from objects.client_class import Client
from objects.order_class import Order
from objects.sku_class import SKU


sys.path.append(str(Path(".").absolute().parent))
Objects = {}


def generate_factories(data: dict):
    """Code to generate factories"""
    factories = {}
    for key, value in data.items():
        factories[key] = Factory(factory_id=key, **value)
    return factories


def generate_clients(data: dict):
    """Code to generate clients"""
    clients = {}
    for key, value in data.items():
        clients[key] = Client(client_id=key, **value)
    return clients


def generate_orders(data: dict):
    """Code to generate orders"""
    orders = {}
    for key, value in data.items():
        orders[key] = Order(order_id=key, **value)
    return orders


def generate_skus(data: dict):
    """ "Code to generate skus"""
    skus = {}
    for key, value in data.items():
        skus[key] = SKU(type_id=key, **value)
    return skus


Factories = generate_factories(json.load(open("./data/config_factories.json")))

Clients = generate_clients(json.load(open("./data/config_clients.json")))

Orders = generate_orders(json.load(open("./data/config_orders.json")))

SKUs = generate_skus(json.load(open("./data/config_skus.json")))
