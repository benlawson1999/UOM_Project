class Recipe:
    __slots__ = ["recipe_id", "ingredients", "quantity", "complete"]
    """Objects that contain the quanity of ingredients in a recipe.

    create_dict: Combines the two vectors to make one dictionary."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.complete = self.create_dict()

    def create_dict(self):
        """Combines the two vectors to make one dictonairy."""
        recipe_dict = {}
        for i in range(len(self.ingredients)):
            recipe_dict[self.ingredients[i]] = self.quantity[i]
        return recipe_dict
