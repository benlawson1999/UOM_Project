class Client:
    def __init__(self, client_id, postcode, tenure, income, age, churn_chance):
        self.client_id = client_id
        self.postcode = postcode
        self.tenure = tenure
        self.income = income
        self.age = age
        self.churn_chance = churn_chance
