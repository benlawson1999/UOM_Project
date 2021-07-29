import pgeocode  

gb_pc = pgeocode.GeoDistance("GB")


class Factory:
    __slots__=["Factory_ID","cost_weight","location","fact_inv"]

    # class of factory
    def __init__(self, Factory_ID, **kwags):
        self.Factory_ID = Factory_ID,
        for key, value in kwags.items():
            setattr(self,key,value)
       
      
   

    def Box_check(self, box_in):
        # function to check if a factory can complete an order
        check = all(item in self.fact_inv.keys() for item in (box_in.keys()))
        # if this is true, see if they can do the order
        if check == True:

            fact_box = {
                ingred: (self.fact_inv[ingred] - box_in[ingred]) for ingred in box_in
            }

            if all(value > 0 for value in fact_box.values()) == True:
                print("Factory", self.Factory_ID, "is eligible for this order")
            else:
                print("Factory", self.Factory_ID,
                      "is not eligible for this order")
        else:
            print("Factory", self.Factory_ID, "is not eligible for this order")

    def Cons_dist(self, order):
        # Function to find the Haversine distance between the factory and the order
        fact_dist = gb_pc.query_postal_code(self.location, order.location)
        return fact_dist

    def SKU_Holding(self, inventory):
        # find all the unique items in the inventory and their quantites
        holding_total = {}

        for key in inventory:

            if key in holding_total:
                # add the value to the current total in the whole factory
                holding_total[key] += inventory[key]
            else:
                # create a new entry if theres not currently a entry
                holding_total[key] = inventory[key]
        self.fact_inv = holding_total
        self.SKU_types = holding_total.keys()


def Factory_Dict(fact_list):
    fact_dict = {}
    for i in fact_list:
        fact_dict[eval(i + ".Factory_ID")] = eval(i)
    return fact_dict
