"""Module to run constraint programming for a set of orders, using Weighted MAPE
as the objective function.

main: Calculate the Mean Weighted Mape for a set of Orders."""
import sys
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from ortools.sat.python import cp_model


def call_cp_solver(
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
    # [START VARIABLES]
    factory_stock_holding = {}
    all_orders = {}
    difference_in_holding_and_demand = {}
    number_of_factories = len(factory_dict)
    mape_limit = number_of_factories * 100
    for count, order in enumerate(order_dict.values()):

        all_orders[count] = order
        order.order_list(recipe_dict)

    all_factories = {}

    factory_quantity = {}
    factory_demand = {}
    order_fulfilled_by = {}
    items_in_order = {}

    for count, factory in enumerate(factory_dict.values()):

        all_factories[count] = factory

        difference_in_holding_and_demand[count] = model.NewIntVar(
            0, 10000000000000000, "x_loss_abs_%i" % count
        )
    all_skus = {}

    for count, sku in enumerate(sku_dict.values()):

        all_skus[count] = sku

        all_skus[count].unit_cost = int(all_skus[count].unit_cost * scaling)

    for count_factory, factory in all_factories.items():

        for count_sku, sku in all_skus.items():

            factory_quantity[(count_factory, count_sku)] = 0
            if factory.factory_inventory.get(sku.name) is None:
                factory_quantity[(count_factory, count_sku)] = (
                    factory.factory_inventory[sku.name] * sku.unit_cost
                )
            else:
                factory_quantity[(count_factory, count_sku)] += (
                    factory.factory_inventory[sku.name] * sku.unit_cost
                )

    for count_order, order in all_orders.items():

        for count_factory, factory in all_factories.items():

            prefix = "%s_" % (order.order_id)
            suffix = "_%s" % (factory.factory_id)
            order_fulfilled_by[(count_order, count_factory)] = model.NewBoolVar(
                f"order {prefix} fulfilled_by {suffix}"
            )
            for count_sku, sku in all_skus.items():
                if order.combined.get(sku.sku_id) is None:
                    items_in_order[(count_order, count_sku)] = 0

                else:
                    items_in_order[(count_order, count_sku)] = (
                        order.combined[sku.sku_id] * sku.unit_cost
                    )

                if factory_demand.get((count_factory, count_sku)) is None:
                    factory_demand[(count_factory, count_sku)] = (
                        round(items_in_order[(count_order, count_sku)])
                        * order_fulfilled_by[(count_order, count_factory)]
                    )

                else:
                    factory_demand[(count_factory, count_sku)] += (
                        round(items_in_order[(count_order, count_sku)])
                        * order_fulfilled_by[(count_order, count_factory)]
                    )

    for count_factory, factory in all_factories.items():
        difference_in_holding_and_demand[count_factory] = sum(
            [
                factory_quantity[(count_factory, count_sku)]
                - factory_demand[(count_factory, count_sku)]
                for count_sku, sku in all_skus.items()
            ]
        )

        factory_stock_holding[count_factory] = sum(
            [
                factory_quantity[(count_factory, count_sku)]
                for count_sku, sku in all_skus.items()
            ]
        )

        # [END VARIABLES]

        # [START CONSTRAINTS]
    for factory in list(all_factories.keys()):
        for order in list(all_orders.keys()):
            if exact is True:

                model.Add(
                    sum(
                        [
                            order_fulfilled_by[(order, factory_c)]
                            for factory_c in list(all_factories.keys())
                        ]
                    )
                    == 1
                )
            else:
                model.Add(
                    sum(
                        [
                            order_fulfilled_by[(order, factory)]
                            for factory in list(all_factories.keys())
                        ]
                    )
                    <= 1
                )

        for sku in list(all_skus.keys()):
            model.Add(factory_demand[(factory, sku)] <= factory_quantity[factory, sku])

        # [END CONSTRAINTS]
    # [START OBJECTIVE]
    obj_var = model.NewIntVar(0, mape_limit, "Sum WMAPE")
    mape_numerator = {}
    mape_denominator = {}
    wmape = {}

    for count_factory, factory in all_factories.items():
        mape_numerator[count_factory] = model.NewIntVar(
            0, 5000000000000000000, "sum_all"
        )

        mape_denominator[count_factory] = model.NewIntVar(
            0, 5000000000000000000, "sum_quantity"
        )

        wmape[count_factory] = model.NewIntVar(0, 100, "WMAPE")

        model.Add(
            mape_numerator[count_factory]
            == difference_in_holding_and_demand[count_factory] * 100
        )

        model.Add(
            mape_denominator[count_factory] == factory_stock_holding[count_factory]
        )
        model.AddDivisionEquality(
            wmape[count_factory],
            mape_numerator[count_factory],
            mape_denominator[count_factory],
        )

    sum_wmape = model.NewIntVar(0, 500, "sum_wmape")
    model.Add(sum_wmape == sum([wmape[f] for f in all_factories]))
    model.Add(obj_var == sum_wmape)
    model.Minimize(obj_var)
    # [END OBJECTIVE]

    solver = cp_model.CpSolver()

    if time_limit is True:
        solver.parameters.max_time_in_seconds = 20000

    status = solver.Solve(model)

    print("Solve status: %s" % solver.StatusName(status))
    print("Mean_Wmape: %i" % (solver.ObjectiveValue() / len(all_factories)))

    wmape_dict = {}
    for num, factory in enumerate(factory_dict):
        wmape_dict[factory] = solver.Value(wmape[num])

    return (solver.ObjectiveValue(), wmape_dict)
