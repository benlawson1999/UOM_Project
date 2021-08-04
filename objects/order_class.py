class Order:
    __slots__ = [
        "order_id",
        "client_id",
        "recipes",
        "product",
        "factory_id",
        "combined",
    ]

    def __init__(self, order_id: int, **kwargs):
        self.order_id = order_id
        self.combined = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def Order_list(self):  # gives all the ingredients needed in the order
        order_total = {}
        if type(self.recipes) == tuple:
            for dict_ in self.recipes:

                for key in dict_:

                    if key in order_total:
                        # add the value to the current total in the whole order
                        order_total[key] += dict_[key]
                    else:
                        # create a new entry if theres not currently a entry
                        order_total[key] = dict_[key]
        else:  # if there is only one recipe
            for key in self.recipes:
                if key in order_total:

                    order_total[key] += self.recipes[key]
                else:
                    order_total[key] = self.recipes[key]
        if type(self.product) != tuple:  # in case there are no additonal products
            pass
        elif len(self.product) > 1:
            for dict_p in self.product:
                for key_p in dict_p:

                    if key_p in order_total:

                        order_total[key_p] += dict_p[key_p]
                    else:
                        order_total[key_p] = dict_p[key_p]
        else:  # when there is only one entry
            for key_p in self.product:

                if key_p in order_total:

                    order_total[key_p] += self.product[key_p]
                else:

                    order_total[key_p] = self.product[key_p]
        self.combined = order_total

    def optimal_factory(self, test):

        eligible_list = []
        for factories in test["Factories"]:

            if test["Factories"][factories].Box_check(self.combined) == True:
                eligible_list.append(factories)
        eligible_factories = {
            your_key: test["Factories"][your_key] for your_key in eligible_list
        }
