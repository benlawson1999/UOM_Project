import json
import sys
import os
from pathlib import Path
from scripts.generate_objects import Factories, Clients, Orders, SKUs
from objects.factory_class import Factory
from objects.client_class import Client
from objects.order_class import Order
from objects.sku_class import SKU


for i in Orders:
    Orders[i].order_list()

    print(Orders[i].combined)
    Orders[i].optimal_factory_naive(Factories)
