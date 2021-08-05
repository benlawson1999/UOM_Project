def wmape(actual: dict, target: dict):
    sum_all = 0
    sum_actual = 0
    for i in actual:
        weight = abs(actual[i] - target[i]) * 100
        sum_all += weight
        sum_actual += actual[i]
    if sum_actual == 0:
        final = 0
    else:
        final = sum_all / sum_actual
    return final
