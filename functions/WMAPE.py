import numpy as np


def wmape(actual: dict, target: dict, skus: dict):
    sum_all = 0
    sum_actual = 0

    for item in actual:
        if skus.get(item) is None:
            weight = 0
        # make a new entry
        else:
            if target.get(item) is None:
                weight = actual[item] * skus[item].unit_cost
            else:
                weight = (actual[item] - target[item]) * skus[item].unit_cost
            sum_all += weight
            sum_actual += actual[item] * skus[item].unit_cost
    if sum_actual == 0:

        final = 100

    else:
        final = sum_all / sum_actual
    return final
