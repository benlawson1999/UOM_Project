class SKU:
    __slots__ = ["sku_id", "name", "unit_cost", "recipe_percent"]
    """Object that contains all relevant information about a SKU"""
    # a given SKU, broad family

    def __init__(self, **kwargs):
        # number of recipes containing the SKU
        for key, value in kwargs.items():
            setattr(self, key, value)
