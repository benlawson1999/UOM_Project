class Recipe:
    __slots__ = ["recipe_id", "ingredients", "quantities", "complete"]

    def __init__(self, recipe_id: str, ingredients: list, quantities: list):
        self.recipe_id = recipe_id
        self.ingredients = ingredients
        self.quantities = quantities
        self.complete = self.create_dict()

    def create_dict(self):
        recipe_dict = {}
        for i in range(len(self.ingredients)):
            print(i)
            print(self.ingredients[i])
            print(self.quantities[i])
            recipe_dict[self.ingredients[i]] = self.quantities[i]
        return recipe_dict
