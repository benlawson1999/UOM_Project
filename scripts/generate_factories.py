from objects.factory_class import Factory
import json
import sys
from pathlib import Path

sys.path.append(str(Path(".").absolute().parent))


def generate_factories(data):
    """Code to generate factories"""

    return [
        Factory(
            Factory_ID=key,
            cost_weight=list(value.values())[0],
            location=list(value.values())[1],
            fact_inv=list(value.values())[2],
        )
        for key, value in data.items()
    ]


if __name__ == "__main__":
    with open("../data/config_factories.json") as fh:
        data = json.load(fh)

    examples = generate_factories(data)
    print(examples)
