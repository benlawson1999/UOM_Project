def wmape(factory_sku_holding: dict, desired_sku_holding: dict, skus: dict):
    """Calcualtes the weighted MAPE for a given warehouse"""
    sum_all = 0
    sum_factory_sku_holding = 0

    for sku in factory_sku_holding:
        if skus.get(sku) is None:
            weight = 0
        else:
            if desired_sku_holding.get(sku) is None:
                weight = factory_sku_holding[sku] * skus[sku].unit_cost
            else:
                weight = (factory_sku_holding[sku] - desired_sku_holding[sku]) * skus[
                    sku
                ].unit_cost
            sum_all += weight
            sum_factory_sku_holding += factory_sku_holding[sku] * skus[sku].unit_cost
    if sum_factory_sku_holding == 0:

        final = 100

    else:
        final = sum_all / sum_factory_sku_holding
    return final
