class Recipe:
    __slots__ = ["recipe_id", "ingredients", "quantity", "complete","quantities"]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.complete = self.create_dict()

    def create_dict(self):
        recipe_dict = {}
        for i in range(len(self.ingredients)):
            recipe_dict[self.ingredients[i]] = self.quantities[i]
        return recipe_dict
