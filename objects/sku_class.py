class SKU:
    __slots__ = ["sku_id", "name", "unit_cost"]
    # a given SKU, broad family

    def __init__(self, **kwargs):
          # number of recipes containing the SKU
        for key, value in kwargs.items():
            setattr(self, key, value)
