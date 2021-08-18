from ortools.sat.python import cp_model
from scripts.generate_objects import Factories, Clients, Orders, SKUs, Recipes


def main(factory_dict, client_dict, order_dict, sku_dict, recipe_dict, exact=True):
    model = cp_model.CpModel()
    # initalise the model
    # [START VARIABLES]
    sum_all = 0
    sum_actual = 0
    all_orders = {}
    for count, item in enumerate(order_dict.values()):

        all_orders[count] = item

    # creates a dict of int:object for use by or_tools
    all_factories = {}

    for count, item in enumerate(factory_dict.values()):

        all_factories[count] = item
        # creates a dict of int:object for use by or_tools
    all_skus = {}

    for count, item in enumerate(sku_dict.values()):

        all_skus[count] = item
        # creates a dict of int:object for use by or_tools

    for count_factory, factory in enumerate(all_factories.items()):

        fulfilled = {}  # dict of [factory_id,order_id] : BoolVar

        factory_quantity = {}  # dict of [factory_id, type_id] : Int

        factory_demand = {}  # dict of [factory_id, type_id] : IntVar

        for count_order, order in enumerate(all_orders.items()):

            prefix = "%s_" % (factory.factory_id,)
            suffix = "_%s" % (order.order_id,)
            fulfilled[(count_factory, count_order)] = model.NewBoolVar(
                prefix + "fulfilled" + suffix
            )
            # binary variables for each order fulfilled by the factory

        for count_sku, sku in enumerate(all_skus.items()):
            prefix = "%s_%s_" % (factory.factory_id, sku.name)
            factory_demand[(count_factory, count_sku)] = model.NewIntVar(
                0,
                factory.factory_inventory[sku.name],
                prefix + "demand",
            )  # creates varibales for all the quantites of skus in each factory
            factory_quantity[(count_factory, count_sku)] = factory.factory_inventory[
                sku.name
            ]
            # creates a measure of the current quantity in the factories

            weight = abs(
                factory_demand[(count_factory, count_sku)]
                - factory_quantity[(count_factory, count_sku)]
            )

            sum_all += weight
            sum_actual += factory_demand[(count_factory, count_sku)]

    for count_order, order in enumerate(all_orders.items()):
        fulfilled_by = {}  # dict of [order_id,factory_id] : BoolVar
        items = {}  # dict of [order_id, type_id] : Int

        for count_factory, factory in enumerate(all_factories.items()):
            prefix = "%s_" % (order.order_id)
            suffix = "_%s" % (factory.factory_id)
            fulfilled_by[(count_order, count_factory)] = model.NewBoolVar(
                prefix + "fulfilled_by" + suffix
            )
            # binary varibale for which factory fullfiled the order
        for count_sku, sku in enumerate(all_skus.items()):
            if order.combined[sku.name] is None:
                items[(count_order, count_sku)] = 0
                # incase there is none of an ingredient in the order

            else:
                items[(count_order, count_sku)] = order.combined[sku.name]
        # [END VARIABLES]

        # [START CONSTRAINTS]
        for factory in list(all_factories.keys()):
            for order in list(all_orders.keys()):
                if exact == True:
                    model.Add(
                        sum(
                            fulfilled_by[(order, factory)]
                            for factory in list(all_factories.keys()) == 1
                        )
                    )  # ensure that all orders have been fulfilled
                else:
                    model.Add(
                        sum(
                            fulfilled_by[(order, factory)]
                            for factory in list(all_factories.keys()) <= 1
                        )
                    )  # to allow for some orders not being fulfilled
                model.Add(fulfilled_by[(order, factory)] == fulfilled[(factory, order)])
                # constraint so that a order is fulfilled, it will also be fulfilled in the factory
                for sku in list(all_skus.keys()):
                    model.Add(
                        factory_demand[(factory, sku)] <= factory_quantity[factory, sku]
                    )
                    model.Add(
                        sum(
                            [
                                fulfilled[(factory, order)] * items[(order, sku)]
                                for order in all_orders
                            ]
                        )
                        < factory_quantity[(factory, sku)]
                    )
                # ensure the demand does not outweigh the supply for a factory
        # [END CONSTRAINTS]

        # [START OBJECTIVE]
        obj_var = model.NewIntVar(0, 100, "WMAPE")
        model.AddMaxEquality(obj_var, [(sum_all / sum_actual) / len(all_orders)])
        model.Minimize(obj_var)
