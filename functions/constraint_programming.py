from ortools.sat.python import cp_model
from scripts.generate_objects import Factories, Clients, Orders, SKUs, Recipes


def main(factory_dict, client_dict, order_dict, sku_dict, recipe_dict, exact=True):
    model = cp_model.CpModel()
    # initalise the model
    # creates the variables and quantities
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

    for count, factory in enumerate(all_factories.items()):

        fulfilled = {}  # dict of [factory_id,order_id] : BoolVar

        factory_quantity = {}  # dict of [factory_id, type_id] : Int

        factory_demand = {}  # dict of [factory_id, type_id] : IntVar

        for count_o, order in enumerate(all_orders.items()):

            prefix = "%s_" % (factory.factory_id,)
            suffix = "_%s" % (order.order_id,)
            fulfilled[(count, count_o)] = model.NewBoolVar(
                prefix + "fulfilled" + suffix
            )
            # binary variables for each order fulfilled by the factory

        for count_s, sku in enumerate(all_skus.items()):
            prefix = "%s_%s_" % (factory.factory_id, sku.name)
            factory_demand[(count, count_s)] = model.NewIntVar(
                0,
                factory.factory_inventory[sku.name],
                prefix + "demand",
            )  # creates varibales for all the quantites of skus in each factory
            factory_quantity[(count, count_s)] = factory.factory_inventory[sku.name]
            # creates a measure of the current quantity in the factories

    for count, order in enumerate(all_orders.items()):
        fulfilled_by = {}  # dict of [order_id,factory_id] : BoolVar
        items = {}  # dict of [order_id, type_id] : Int

        for count_f, factory in enumerate(all_factories.items()):
            prefix = "%s_" % (order.order_id)
            suffix = "_%s" % (factory.factory_id)
            fulfilled_by[(count, count_f)] = model.NewBoolVar(
                prefix + "fulfilled_by" + suffix
            )
            # binary varibale for which factory fullfiled the order
        for count_s, sku in enumerate(all_skus.items()):
            if order.combined[sku.name] is None:
                items[(count, count_s)] = 0
                #incase there is none of an ingredient in the order

            else:
                items[(count, count_s)] = order.combined[sku.name]

        # create the constraints
        for f in list(all_factories.keys()):
            for o in list(all_orders.keys()):
                if exact == True:
                    model.Add(
                        sum(fulfilled_by[(o, f)] for o in list(all_orders.keys()) == 1)
                    )  # ensure that all orders have been fulfilled
                else:
                    model.Add(
                        sum(fulfilled_by[(o, f)] for o in list(all_orders.keys()) <= 1)
                    )  # to allow for some orders not being fulfilled
                    for s in list(all_skus.keys()):
                        model.Add(factory_demand[(f, s)] <= factory_quantity[f, s])
                # ensure the demand does not outweigh the supply for a factory]
                    if fulfilled[(f,o)] == 1:
                        pass
