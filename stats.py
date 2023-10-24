import os
import re

from binpacking import *

if __name__ == "__main__":

    classes = {n: 0 for n in range(1, 11)}
    items = {20: 0, 40: 0, 60: 0, 80: 0, 100: 0}
    total = 0

    for instance in range(500):

        if os.path.isfile(f'./solutions/{instance}.json'):

            with open(f'./data/{instance}.json', 'r') as file:
                data = json.loads(file.read())

                result = re.search('^CLASS(.*)_(.*)_(.*)$', data['Name'])

                cls = int(result.group(1))
                amount = int(result.group(2))

                classes[cls] += 1
                items[amount] += 1
                total += 1

    print(classes)
    print(items)
    print(total)
