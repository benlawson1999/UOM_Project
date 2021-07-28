import pgeocode #may need to be installed at the copmmand line
from collections import Counter
class Factory:
     Fid_iter = itertools.count()
    #class of factory 
    def __init__(self,cost_weight,location):
        self.Factory_ID =  next(Factory.Fid_iter)
        self.SKU_types = None #list
        self.cost_weight = cost_weight #a multipler for how effiecent the factory is
        self.location = location #postcode of the factory
        self.fact_inv = None #dict of all the SKUs in the factory and their quantites
    
    def Box_check(self,box_in):
        #function to check if a factory can complete an order
        check = all(item in self.SKU_types for item in (box_in.keys()))
        #if this is true, see if they can do the order 
        if check == True:
          
            fact_box = {ingred: (self.fact_inv[ingred]-box_in[ingred]) for ingred in box_in}

            if all(value > 0 for value in fact_box.values()) == True:
                print("Factory",self.Factory_ID,"is eligible for this order")
            else:
                print("Factory",self.Factory_ID,"is not eligible for this order")
        else: 
             print("Factory",self.Factory_ID,"is not eligible for this order")
    
    def Cons_dist(self,order):
        #Function to find the Haversine distance between the factory and the order
        fact_dist = dist.query_postal_code(self.location, order.location)
        return fact_dist
    
    def SKU_Holding(self,inventory):
        #find all the unique items in the inventory and their quantites
        holding_total ={}

        for key in inventory:
                    
                    if key in holding_total:
                          #add the value to the current total in the whole factory
                        holding_total[key] += inventory[key]
                    else:
                        #create a new entry if theres not currently a entry
                        holding_total[key] = inventory[key]
        self.fact_inv = holding_total
        self.SKU_types = holding_total.keys()

  

def Factory_Dict(fact_list):
    fact_dict={}
    for i in fact_list:
        fact_dict[eval(i+".Factory_ID")] = eval(i)
    return fact_dict


for i in range(100):
    Fact_i =Factory((random.randint(50,200)/100),gb_pc._data["postal_code"][random.randint(0,27429)])
    Factories[i] = Fact_i
