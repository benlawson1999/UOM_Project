"""Module to run constraint programming for a set of orders, using Weighted MAPE
as the objective function.

main: Calculate the Mean Weighted Mape for a set of Orders."""
import sys
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from ortools.sat.python import cp_model
from scripts.generate_objects import Factories, Orders, SKUs, Recipes
import time
from itertools import islice, chain


def main(
    factory_dict: dict,
    order_dict: dict,
    sku_dict: dict,
    recipe_dict: dict,
    time_limit=True,
    exact=True,
    scaling=1,
):
    """Calculate the Mean Weighted Mape for a set of Orders."""

    model = cp_model.CpModel()
    # initalise the model
    # [START VARIABLES]
    sum_actual = {}
    all_orders = {}
    error_abs = {}
    n = len(factory_dict)
    mape_limit = n * 100
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
        error_abs[count] = model.NewIntVar(
            0, 1000000000000000000, "x_loss_abs_%i" % count
        )
    all_skus = {}

    for count, item in enumerate(sku_dict.values()):

        all_skus[count] = item

        all_skus[count].unit_cost = int(all_skus[count].unit_cost * scaling)

        # creates a dict of int:object for use by or_tools

    for count_factory, factory in all_factories.items():

        for count_sku, sku in all_skus.items():
            prefix = "%s_%s_" % (factory.factory_id, sku.sku_id)
            factory_quantity[(count_factory, count_sku)] = 0
            if factory.factory_inventory.get(sku.name) is None:
                factory_quantity[(count_factory, count_sku)] = (
                    factory.factory_inventory[sku.name] * sku.unit_cost
                )
            else:
                factory_quantity[(count_factory, count_sku)] += (
                    factory.factory_inventory[sku.name] * sku.unit_cost
                )

            # creates a measure of the current quantity in the factories

    for count_order, order in all_orders.items():
        for count_factory, factory in all_factories.items():
            prefix = "%s_" % (order.order_id)
            suffix = "_%s" % (factory.factory_id)
            fulfilled_by[(count_order, count_factory)] = model.NewBoolVar(
                prefix + "fulfilled_by" + suffix
            )
            for count_sku, sku in all_skus.items():
                if order.combined.get(sku.sku_id) is None:
                    items[(count_order, count_sku)] = 0
                    # incase there is none of an ingredient in the order
                else:
                    items[(count_order, count_sku)] = (
                        order.combined[sku.sku_id] * sku.unit_cost
                    )

                if factory_demand.get((count_factory, count_sku)) is None:
                    factory_demand[(count_factory, count_sku)] = (
                        round(items[(count_order, count_sku)])
                        * fulfilled_by[(count_order, count_factory)]
                    )
                    # create factory demand
                else:
                    factory_demand[(count_factory, count_sku)] += (
                        round(items[(count_order, count_sku)])
                        * fulfilled_by[(count_order, count_factory)]
                    )
                    # adds to factory demand
    for count_factory, factory in all_factories.items():
        error_abs[count_factory] = sum(
            [
                factory_quantity[(count_factory, count_sku)]
                - factory_demand[(count_factory, count_sku)]
                for count_sku, sku in all_skus.items()
            ]
        )
        # calcuate the numerator for weighted mape
        sum_actual[count_factory] = sum(
            [
                factory_quantity[(count_factory, count_sku)]
                for count_sku, sku in all_skus.items()
            ]
        )
        print(sum_actual)
        # calculates the errors for the quantity and the demand

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

        for sku in list(all_skus.keys()):
            model.Add(factory_demand[(factory, sku)] <= factory_quantity[factory, sku])
            # ensure the demand does not outweigh the supply for a factory
        # [END CONSTRAINTS]
    # [START OBJECTIVE]
    obj_var = model.NewIntVar(0, mape_limit, "Sum WMAPE")
    numerator = {}
    denom = {}
    wmape = {}

    for count_factory, factory in all_factories.items():
        numerator[count_factory] = model.NewIntVar(0, 5000000000000000000, "sum_all")

        denom[count_factory] = model.NewIntVar(0, 5000000000000000000, "sum_quantity")

        wmape[count_factory] = model.NewIntVar(0, 100, "WMAPE")

        # adds new varibles to calcuate the weighted mape
        model.Add(numerator[count_factory] == error_abs[count_factory] * 100)

        model.Add(denom[count_factory] == sum_actual[count_factory])
        model.AddDivisionEquality(
            wmape[count_factory], numerator[count_factory], denom[count_factory]
        )

    sum_wmape = model.NewIntVar(0, 500, "sum_wmape")
    model.Add(sum_wmape == sum([wmape[f] for f in all_factories]))
    model.Add(obj_var == sum_wmape)
    model.Minimize(obj_var)
    # [END OBJECTIVE]

    solver = cp_model.CpSolver()
    if time_limit == True:
        solver.parameters.max_time_in_seconds = 20000
    # adds an optional time limit

    status = solver.Solve(model)
    # solves the model

    print("Solve status: %s" % solver.StatusName(status))
    print("Mean_Wmape: %i" % (solver.ObjectiveValue() / len(all_factories)))

    wmape_dict = {}
    for num, factory in enumerate(factory_dict):
        wmape_dict[factory] = solver.Value(wmape[num])

    return (solver.ObjectiveValue(), wmape_dict)


main(Factories, Orders, SKUs, Recipes)
