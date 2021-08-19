import numpy as np
class Client:
    __slots__ = [
        "client_id",
        "postcode",
        "tenure",
        "income",
        "age",
        "churn_chance",
        "optimal_distance",
    ]

    def __init__(self, client_id: int, **kwargs):
        self.client_id = client_id
        for key, value in kwargs.items():
            setattr(self, key, value)

    def optimal_distance_calc(self, factories_dict: dict):
        all_distances = np.array([])
        for factory in factories_dict.values():
            all_distances = np.append(
                all_distances,
                (factory.consumer_distance(self.postcode)),
            )
        self.optimal_distance = np.min(all_distances)
