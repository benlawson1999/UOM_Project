
import random
import operator
import numpy as np


class Order:
    """Object containing all the information about an order.

    order_list: gives all the ingredients needed in the order.
    optimal_distance_calc: Calculate the lowest distance between an order the factories.
    calculate_difference: Calcuate the difference between the optimal and current distance.
    eligibility_check: Returns all eligible factories for this order.
    optimal_factory_naive: Uses random choice as the criteria for allocation to a factory.
    optimal_factory_ranking_max: Uses the maximum of included SKUs as the criteria for allocation to a factory.
    optimal_factory_ranking_min: Uses the minimum of included SKUs as the criteria for allocation to a factory.
    """

    __slots__ = [
        "order_id",
        "postcode",
        "recipes",
        "product",
        "factory_id",
        "combined",
        "fulfilled",
        "optimal_distance",
        "factory_distance",
        "difference_distance",
        "batch",
    ]

    def __init__(self, order_id: int, **kwargs):
        self.order_id = order_id
        self.combined = None
        self.factory_distance = 1000

        for key, value in kwargs.items():
            setattr(self, key, value)

    def order_list(self, recipe_dict):
        """Gives all the ingredients needed in the order."""
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

    def optimal_distance_calc(self, factories_dict: dict):
        """Calculate the lowest distance between an order the factories."""
        all_distances = np.array([])
        for factory in factories_dict.values():
            all_distances = np.append(
                all_distances,
                (factory.consumer_distance(self.postcode)),
            )
        self.optimal_distance = np.min(all_distances)

    def calculate_difference(self, factories_dict: dict):
        """Calcuate the difference between the optimal and current distance."""
        if self.factory_id == None:
            return 100000
        else:
            self.difference_distance = (
                factories_dict[self.factory_id].consumer_distance(self.postcode)
                - self.optimal_distance
            )
        return self.difference_distance

    def eligibility_check(self, factories_dict: dict, demand: dict):
        """Returns all eligible factories for this order."""
        eligible_list = []
        for factories in factories_dict.values():
            if factories.Box_check(self.combined, demand) == True:
                eligible_list.append(factories.factory_id)
        eligible_factories = {
            your_key: factories_dict[your_key] for your_key in eligible_list
        }
        return eligible_factories

    def optimal_factory_naive(
        self,
        factories_dict: dict,
        demand: dict,
    ):
       """Uses random choice as the criteria for allocation to a factory."""

        eligible_factories = self.eligibility_check(factories_dict, demand)

        if not eligible_factories:
            self.fulfilled = 0
            self.factory_id = None
            return self.fulfilled
        else:
            optimal_id = random.choice(list(eligible_factories))
            self.factory_distance = factories_dict[optimal_id].consumer_distance(
                self.postcode
            )
            self.difference_distance = self.factory_distance - self.optimal_distance
            self.factory_id = optimal_id
            self.fulfilled = 1
            return optimal_id

    def optimal_factory_ranking_max(
        self,
        factories_dict: dict,
        demand: dict,
    ):
        """Uses the maximum of included SKUs as the criteria for allocation to a factory."""
        eligible_factories = self.eligibility_check(factories_dict, demand)
        factories_quantity = {}
        if not eligible_factories:
            self.fulfilled = 0
            self.factory_id = None
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
                self.postcode
            )
            self.difference_distance = self.factory_distance - self.optimal_distance
            self.factory_id = optimal_id
            self.fulfilled = 1
            return optimal_id

    def optimal_factory_ranking_min(
        self,
        factories_dict: dict,
        demand: dict,
    ):
        """Uses the minimum of included SKUs as the criteria for allocation to a factory."""
        eligible_factories = self.eligibility_check(factories_dict, demand)
        factories_quantity = {}
        if not eligible_factories:
            self.fulfilled = 0
            self.factory_id = None
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
                self.postcode
            )
            self.difference_distance = self.factory_distance - self.optimal_distance
            self.factory_id = optimal_id
            self.fulfilled = 1

            return optimal_id
