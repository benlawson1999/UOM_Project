def wmape(actual: dict, target: dict):
    sum_all = 0
    sum_actual = 0

    for item in actual:
        # make a new entry
        weight = abs(actual[item] - target[item])

        sum_all += weight
        sum_actual += actual[item]
    if sum_actual == 0:

        final = 100

    else:
        final = sum_all / sum_actual
    return final
