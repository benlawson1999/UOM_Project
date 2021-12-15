import pgeocode


gb_pc = pgeocode.GeoDistance("GB")


class Factory:
    """Class to define a factory.

    box_check: see if the factory is elgigible for a given order.
    consumer_distance: calcuates the Haversine distance between an order and the factory"""

    __slots__ = [
        "factory_id",
        "recipes",
        "postcode",
        "factory_inventory",
        "eligible",
        "batch",
    ]

    # class of factory
    def __init__(self, factory_id: int, **kwargs):
        self.factory_id = factory_id
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.eligible = None

    def box_check(self, box_in, factory_demand):
        """function to check if a factory can complete an order"""
        check = all(sku in self.factory_inventory.keys() for sku in (box_in.keys()))
        # if this is true, see if they can do the order
        factory_box = {}
        if check is True:
            for ingredient in box_in:
                if factory_demand.get(self.factory_id) is None:

                    factory_demand[self.factory_id] = {}  # make a new entry
                if factory_demand[self.factory_id].get(ingredient) is None:

                    factory_demand[self.factory_id][ingredient] = 0

                factory_box[ingredient] = (
                    self.factory_inventory[ingredient]
                    - box_in[ingredient]
                    - factory_demand[self.factory_id][ingredient]
                )

            if all(value >= 0 for value in factory_box.values()) is True:

                self.eligible = True

            else:
                self.eligible = False

        else:
            self.eligible = False

        return self.eligible

    def consumer_distance(self, order_location):
        """Function to find the Haversine distance between the factory and the order"""
        fact_dist = gb_pc.query_postal_code(self.postcode, order_location)
        return fact_dist
