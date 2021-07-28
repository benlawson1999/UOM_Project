import sys
from pathlib import Path

sys.path.append(str(Path(".").absolute().parent))

import pgeocode
import random
from objects.Factory_Class import Factory


def generate_factories():
    """Code to generate a factory"""
    gb_pc = pgeocode.GeoDistance("GB")
    return Factory(
        cost_weight=(random.randint(50, 200) / 100),
        location=gb_pc._data["postal_code"][random.randint(0, 27429)],
    )


if __name__ == "__main__":
    Factory = generate_factories()
    print(Factory)
