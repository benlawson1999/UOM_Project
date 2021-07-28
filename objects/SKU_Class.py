class SKU:
    # a given SKU, broad family
    def __init__(self, name, unit_cost, holding_cost, temp_requirements):
        self.type_ID = None  # ID for the type of ingredient ie Apple etc
        self.name = name  # name of the ingredient
        self.n_recipes = None  # number of recipes containing the SKU
        self.unit_cost = unit_cost  # unit cost of thr SKU
        self.holding_cost = holding_cost  # Holding cost of the SKU
        self.temp_requirements = temp_requirements  # Temperature to hold it at
        self.child_ID = None
        self.expiry = None

    def Recipes_containing(self, recipe_book):
        n_recipe = 0
        for i in recipe_book:
            if (
                self.name in recipe_book[i]
            ):  # see if the ingredient is in each recipe in the book
                n_recipe += 1
            else:
                continue
        self.n_recipes = n_recipe

    def SKU_ID(self, SID_dict):
        if self.name in SID_dict:  # if the information needs to be updated, but the
            self.type_ID = SID_dict[self.name]
        else:
            self.type_ID = len(SID_dict)  # create a new entry in the list for the SKU
            SID_dict[self.name] = self.type_ID


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
