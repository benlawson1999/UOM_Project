"""test"""
import random
import operator
import numpy as np


class Order:
    __slots__ = [
        "order_id",
        "client_id",
        "recipes",
        "product",
        "factory_id",
        "combined",
        "fulfilled",
        "optimal_distance",
        "factory_distance",
        "difference_distance",
    ]

    def __init__(self, order_id: int, **kwargs):
        self.order_id = order_id
        self.combined = None
        self.factory_distance = 1000

        for key, value in kwargs.items():
            setattr(self, key, value)

    def order_list(self, recipe_dict):  # gives all the ingredients needed in the order
        order_total = {}
        for i in self.recipes:  # list of ids

            for ingred in recipe_dict[i].complete:  # dict
                if ingred in order_total:
                    # add the value to the current total in the whole order
                    order_total[ingred] += recipe_dict[i].complete[ingred]
                else:
                    # create a new entry if theres not currently a entry
                    order_total[ingred] = recipe_dict[i].complete[ingred]

        for i in self.product:

            if i in order_total:

                order_total[i] += 1
            else:
                order_total[i] = 1
        self.combined = order_total

    def optimal_distance_setter(self, client_dict):
        self.optimal_distance = client_dict[self.client_id].optimal_distance

    def eligibility_check(self, factories_dict: dict, demand: dict):

        eligible_list = []
        for factories in factories_dict:
            if factories_dict[factories].Box_check(self.combined, demand) == True:
                eligible_list.append(factories)
        eligible_factories = {
            your_key: factories_dict[your_key] for your_key in eligible_list
        }
        return eligible_factories

    def optimal_factory_naive(
        self, factories_dict: dict, demand: dict, client_dict: dict
    ):

        eligible_factories = self.eligibility_check(factories_dict, demand)

        if not eligible_factories:
            self.fulfilled = 0
            return self.fulfilled
        else:
            optimal_id = random.choice(list(eligible_factories))
            self.factory_distance = factories_dict[optimal_id].consumer_distance(
                client_dict[self.client_id].postcode
            )
            self.difference_distance = self.factory_distance - self.optimal_distance
            self.factory_id = optimal_id
            self.fulfilled = 1
            return optimal_id

    def optimal_factory_ranking_max(
        self, factories_dict: dict, demand: dict, client_dict: dict
    ):
        eligible_factories = self.eligibility_check(factories_dict, demand)
        factories_quantity = {}
        if not eligible_factories:
            self.fulfilled = 0
            return self.fulfilled
        else:
            for factory in eligible_factories:
                factories_quantity[factory] = 0
                for item in self.combined:
                    factories_quantity[factory] += eligible_factories[
                        factory
                    ].factory_inventory[item]
            optimal_id = max(factories_quantity.items(), key=operator.itemgetter(1))[0]
            self.factory_distance = factories_dict[optimal_id].consumer_distance(
                client_dict[self.client_id].postcode
            )
            self.difference_distance = self.factory_distance - self.optimal_distance
            self.factory_id = optimal_id
            self.fulfilled = 1
            return optimal_id

    def optimal_factory_ranking_min(
        self, factories_dict: dict, demand: dict, client_dict: dict
    ):
        eligible_factories = self.eligibility_check(factories_dict, demand)
        factories_quantity = {}
        if not eligible_factories:
            self.fulfilled = 0
            return self.fulfilled
        else:
            for factory in eligible_factories:
                factories_quantity[factory] = 0
                for item in self.combined:
                    factories_quantity[factory] += eligible_factories[
                        factory
                    ].factory_inventory[item]

            optimal_id = min(factories_quantity.items(), key=operator.itemgetter(1))[0]
            self.factory_distance = factories_dict[optimal_id].consumer_distance(
                client_dict[self.client_id].postcode
            )
            self.difference_distance = self.factory_distance - self.optimal_distance
            self.factory_id = optimal_id
            self.fulfilled = 1

            return optimal_id
