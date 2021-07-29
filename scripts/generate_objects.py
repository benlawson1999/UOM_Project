from objects.factory_class import Factory
from objects.client_class import Client
from objects.order_class import Order
from objects.sku_class import SKU
import json
import sys
from pathlib import Path

sys.path.append(str(Path(".").absolute().parent))

objects = ["factories", "clients", "orders", "skus"]
dic = {}


def generate_factories(data):
    """Code to generate factories"""

    return [Factory(Factory_ID=key, **value)for key, value in data.items()]


def generate_clients(data):
    """Code to generate clients"""

    return [Client(client_id=key, **value) for key, value in data.items()]


def generate_orders(data):
    """Code to generate orders"""

    return [Order(order_id=key, **value) for key, value in data.items()]


def generate_skus(data):
    """"Code to generate skus"""

    return [SKU(type_id=key, **value) for key, value in data.items()]


if __name__ == "__main__":
    for i in objects:

        with open("../data/config_"+i+".json") as fh:
            data = json.load(fh)
            dic[i.capitalize()] = eval("generate_"+i+"(data)")
