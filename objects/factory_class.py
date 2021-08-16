# import pgeocode  # may need to be installed at the copmmand line
from collections import Counter

import random

# gb_pc = pgeocode.GeoDistance("GB")


class Factory:
    __slots__ = [
        "factory_id",
        "cost_weight",
        "postcode",
        "factory_inventory",
        "eligible",
    ]

    # class of factory
    def __init__(self, factory_id: int, **kwargs):
        self.factory_id = factory_id
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.eligible = None

    def Box_check(self, box_in, demand):
        # function to check if a factory can complete an order
        check = all(item in self.factory_inventory.keys() for item in (box_in.keys()))
        # if this is true, see if they can do the order
        fact_box = {}
        if check == True:
            for ingredient in box_in:
                if demand.get(self.factory_id) is None:

                    demand[self.factory_id] = {}  # make a new entry
                if demand[self.factory_id].get(ingredient) is None:

                    demand[self.factory_id][ingredient] = 0

                fact_box[ingredient] = (
                    self.factory_inventory[ingredient]
                    - box_in[ingredient]
                    - demand[self.factory_id][ingredient]
                )

            if all(value >= 0 for value in fact_box.values()) == True:

                self.eligible = True

            else:
                self.eligible = False

        else:
            self.eligible = False

        return self.eligible

    def Cons_dist(self, order):
        # Function to find the Haversine distance between the factory and the order
        fact_dist = gb_pc.query_postal_code(self.postcode, order.location)
        return fact_dist
