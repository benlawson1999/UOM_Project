class Client:
    __slots__ = ["client_id", "postcode", "tenure", "income", "age", "churn_chance"]
    def __init__(self, client_id, **kwags):
        self.client_id = client_id
        for key, value in kwags.items():
            setattr(self,key,value)
            
