from ortools.sat.python import cp_model
from scripts.generate_objects import Factories, Clients, Orders, SKUs, Recipes


def main(factory_dict, client_dict, order_dict, sku_dict, recipe_dict, exact=True):
    model = cp_model.CpModel()
    all_orders = {}
    for count, item in enumerate(order_dict.values()):
        all_orders[count] = item.order_id
    all_factories = {}
    for count, item in enumerate(factory_dict.values()):
        all_orders[count] = item.factory_id
    all_skus = {}
    for count, item in enumerate(sku_dict.values()):
        all_orders[count] = item.type_id

    for count, factory in enumerate(factory_dict.values()):
        fulfilled = {}
        for count_o, order in enumerate(order_dict.values()):
            prefix = "%s_" % (factory.factory_id,)
            suffix = "_%s" % (order.order_id,)
            fulfilled[count, count_o] = model.NewBoolVar(prefix + "fulfilled" + suffix)
            # binary variables for each order fulfilled by the factory

        for sku in sku_dict.values():
            prefix = "%s_%s_" % (factory.factory_id, sku.name)
            quantity = model.NewIntVar(
                sku.target_level,
                factory.factory_inventory[sku.name],
                prefix + "quantity",
            )  # creates varibales for all the quantites of skus in each factory

    for count, order in enumerate(order_dict.values()):
        fulfilled_by = {}
        for count_f, factory in enumerate(factory_dict.values()):
            prefix = "%s_" % (order.order_id)
            suffix = "_%s" % (factory.factory_id)
            fulfilled_by[(count, count_f)] = model.NewBoolVar(
                prefix + "fulfilled_by" + suffix
            )
            # binary varibale for which factory fullfiled the order
    if exact == True:  # so that all orders are fulfilled
        for f in list(all_factories.keys()):
            for o in list(all_orders.keys()):
                model.Add(sum(shifts[(o, f)] for o in list(all_orders.keys()) == 1))
    else:  # if not fulfilling all orders is permissable
        for f in list(all_factories.keys()):
            for o in list(all_orders.keys()):
                    model.Add(sum(shifts[(o, f)] for o in list(all_orders.keys()) <= 1))
