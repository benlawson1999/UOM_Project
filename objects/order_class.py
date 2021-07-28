class Order:
    def __init__(self, client_id, recipes, product):
        self.client_id = client_id  # id of the client who made the order
        self.recipes = recipes  # the recipes in the order
        self.product = product  # stand alone products
        self.combined = None

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
