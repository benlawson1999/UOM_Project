import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))

import json
from objects.Example import Example

def generate_examples(data):
    """Code to generate examples
    """

    return [Example(foo = key, bar = value) for key, value in data.items()]

if __name__ == '__main__':
    with open('../data/config_example.json') as fh:
        data = json.load(fh)

    examples = generate_examples(data)
    print(examples)
