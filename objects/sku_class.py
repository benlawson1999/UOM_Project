class SKU:
    __slots__ = [
        "type_id",
        "name",
        "unit_cost",
        "holding_cost",
        "temp_requirements",
        "recipe_percent",
        "child_id",
        "expiry",
        "target_level",
    ]
    # a given SKU, broad family

    def __init__(self, type_id: int, **kwargs):
        self.type_id = type_id  # ID for the type of ingredient ie Apple etc
        self.recipe_percent = None  # number of recipes containing the SKU
        self.child_id = None
        self.expiry = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def Recipes_containing(self, recipe_book):
        n_recipe = 0
        for item in recipe_book.values():
            if (
                self.name in item["ingredients"]
            ):  # see if the ingredient is in each recipe in the book
                n_recipe += 1
            else:
                continue
        recipe_percent = n_recipe / len(recipe_book) * 100
        self.recipe_percent = recipe_percent


class Child(SKU):
    # gives instances with the same values as the overall SKU ie Apple
    _sentinel = object()

    def __init__(
        self,
        x,
        name=_sentinel,
        unit_cost=_sentinel,
        holding_cost=_sentinel,
        temp_requirements=_sentinel,
    ):

        if name is self._sentinel:

            name = x.name
            unit_cost = x.unit_cost
            holding_cost = x.holding_cost
            temp_requirements = x.temp_requirements

            SKU.__init__(self, name, unit_cost, holding_cost, temp_requirements)

            self_ID = 0
            self.child_ID = name + str(self_ID)
            self_ID += 1

    def Set_Expiry(self, Date):
        self.expiry = Date
