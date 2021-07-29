from objects.factory_class import Factory
from objects.client_class import Client
from objects.order_class import Order
from objects.sku_class import SKU
import json
import sys
from pathlib import Path

sys.path.append(str(Path(".").absolute().parent))
objects = {}


def generate_factories(data: dict):
    """Code to generate factories"""

    return [Factory(factory_id=key, **value)for key, value in data.items()]


def generate_clients(data: dict):
    """Code to generate clients"""

    return [Client(client_id=key, **value) for key, value in data.items()]


def generate_orders(data: dict):
    """Code to generate orders"""

    return [Order(order_id=key, **value) for key, value in data.items()]


def generate_skus(data: dict):
    """"Code to generate skus"""

    return [SKU(type_id=key, **value) for key, value in data.items()]


objects["Factories"] = generate_factories(
    json.load(open("../data/config_factories.json")))

objects["Clients"] = generate_clients(
    json.load(open("../data/config_clients.json")))

objects["Orders"] = generate_orders(
    json.load(open("../data/config_orders.json")))

objects["SKUS"] = generate_skus(json.load(open("../data/config_skus.json")))
