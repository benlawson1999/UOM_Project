class Inventory:
    # inventory for a given factory
    def _init_(self):
        self.SKU_dict = None

    def Form_dict(self, SKU_list):
        # form a dictonary from the list of all SKU in the factory
        self.SKU_dict = dict(Counter((SKU_list)))
