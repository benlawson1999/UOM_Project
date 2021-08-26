from ortools.sat.python import cp_model
from scripts.generate_objects import Factories, Clients, Orders, SKUs, Recipes


def main(factory_dict, client_dict, order_dict, sku_dict, recipe_dict, exact=True):
    model = cp_model.CpModel()
    # initalise the model
    # [START VARIABLES]
    sum_all = {}
    sum_actual = {}
    all_orders = {}
    error_abs = {}
    n = len(factory_dict)
    for count, item in enumerate(order_dict.values()):

        all_orders[count] = item
        item.order_list(recipe_dict)

    # creates a dict of int:object for use by or_tools
    all_factories = {}
    fulfilled = {}  # dict of [factory_id,order_id] : BoolVar
    factory_quantity = {}  # dict of [factory_id, type_id] : Int

    factory_demand = {}  # dict of [factory_id, type_id] : IntVar
    fulfilled_by = {}  # dict of [order_id,factory_id] : BoolVar
    items = {}  # dict of [order_id, type_id] : Int
    temp = {}

    for count, item in enumerate(factory_dict.values()):

        all_factories[count] = item
        # creates a dict of int:object for use by or_tools
        error_abs[count] = model.NewIntVar(0, 100000, "x_loss_abs_%i" % count)
    all_skus = {}

    for count, item in enumerate(sku_dict.values()):

        all_skus[count] = item
        # creates a dict of int:object for use by or_tools

    for count_factory, factory in all_factories.items():

        for count_order, order in all_orders.items():

            prefix = "%s_" % factory.factory_id
            suffix = "_%s" % order.order_id
            fulfilled[(count_factory, count_order)] = model.NewBoolVar(
                prefix + "fulfilled" + suffix
            )

            # binary variables for each order fulfilled by the factory

        for count_sku, sku in all_skus.items():
            prefix = "%s_%s_" % (factory.factory_id, sku.name)
            factory_quantity[(count_factory, count_sku)] = factory.factory_inventory[
                sku.name
            ]

            # creates a measure of the current quantity in the factories

    for count_order, order in all_orders.items():
        for count_sku, sku in all_skus.items():
            if order.combined.get(sku.name) is None:
                items[(count_order, count_sku)] = 0
                # incase there is none of an ingredient in the order
            else:
                items[(count_order, count_sku)] = order.combined[sku.name]

            for count_factory, factory in all_factories.items():
                prefix = "%s_" % (order.order_id)
                suffix = "_%s" % (factory.factory_id)
                fulfilled_by[(count_order, count_factory)] = model.NewBoolVar(
                    prefix + "fulfilled_by" + suffix
                )
                if factory_demand.get((count_factory, count_sku)) is None:
                    factory_demand[(count_factory, count_sku)] = (
                        items[(count_order, count_sku)]
                        * fulfilled[(count_factory, count_order)]
                    )
                else:
                    factory_demand[(count_factory, count_sku)] += (
                        items[(count_order, count_sku)]
                        * fulfilled[(count_factory, count_order)]
                    )
    for count_factory, factory in all_factories.items():
        temp[count_factory] = model.NewIntVar(-10000, 10000, "temp_%i" % count_factory)

        for count_sku, sku in all_skus.items():
            temp[(count_factory, count_sku)] = model.NewIntVar(
                -10000, 10000, "temp_%s_%s" % (count_factory, count_sku)
            )
            model.Add(
                temp[(count_factory, count_sku)]
                == (
                    factory_quantity[(count_factory, count_sku)]
                    - factory_demand[(count_factory, count_sku)]
                )
            )
            if temp.get(count_factory) is None:
                temp[count_factory] = temp[(count_factory, count_sku)]
            else:
                temp[count_factory] += temp[(count_factory, count_sku)]
            if sum_actual.get(count_factory) is None:
                sum_actual[count_factory] = factory_demand[(count_factory, count_sku)]
            else:
                sum_actual[count_factory] += factory_demand[(count_factory, count_sku)]

        model.Add(error_abs[count_factory] == temp[count_factory])

        # [END VARIABLES]

        # [START CONSTRAINTS]
    for factory in list(all_factories.keys()):
        for order in list(all_orders.keys()):
            if exact == True:

                model.Add(
                    sum(
                        [
                            fulfilled_by[(order, factory_c)]
                            for factory_c in list(all_factories.keys())
                        ]
                    )
                    == 1
                )  # ensure that all orders have been fulfilled
            else:
                model.Add(
                    sum(
                        [
                            fulfilled_by[(order, factory)]
                            for factory in list(all_factories.keys())
                        ]
                    )
                    <= 1
                )  # to allow for some orders not being fulfilled
            model.Add(fulfilled_by[(order, factory)] == fulfilled[(factory, order)])
            # constraint so that a order is fulfilled, it will also be fulfilled in the factory
        for sku in list(all_skus.keys()):
            model.Add(factory_demand[(factory, sku)] <= factory_quantity[factory, sku])
            # ensure the demand does not outweigh the supply for a factory
        # [END CONSTRAINTS]

    # [START OBJECTIVE]
    obj_var = model.NewIntVar(0, 10000, "Mean WMAPE")
    numerator = {}
    denom = {}
    wmape = {}
    length = model.NewIntVar(0, len(factory_dict), "Length")
    model.Add(length == n)
    mean_wmape = model.NewIntVar(0, 100, "Mean_wmape")

    for count_factory, factory in all_factories.items():
        numerator[count_factory] = model.NewIntVar(0, 5000000, "sum_all")
        denom[count_factory] = model.NewIntVar(0, 5000000, "sum_actual")
        wmape[count_factory] = model.NewIntVar(0, 100, "WMAPE")
        model.Add(numerator[count_factory] == error_abs[count_factory])
        model.Add(denom[count_factory] == sum_actual[count_factory])
        model.AddDivisionEquality(
            wmape[count_factory], numerator[count_factory], denom[count_factory]
        )

    sum_wmape = model.NewIntVar(0, 1000, "sum_wmape")
    model.Add(sum_wmape == sum([wmape[f] for f in all_factories]))
    model.AddDivisionEquality(mean_wmape, sum_wmape, length)
    model.Add(obj_var == mean_wmape)
    model.Minimize(obj_var)
    # [END OBJECTIVE]

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0

    status = solver.Solve(model)

    print("Solve status: %s" % solver.StatusName(status))
    print("Minimum Wmape: %i" % solver.ObjectiveValue())
    print(factory_demand)
    print(factory_quantity)


main(Factories, Clients, Orders, SKUs, Recipes)
