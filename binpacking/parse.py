import json

from binpacking.model import Item


def parse_data(instance) -> tuple[int, int, list[Item]]:

    with open(f'./data/{instance}.json', 'r') as file:
        data = json.loads(file.read())

    bin = data['Objects'][0]
    W = int(bin['Length'])
    H = int(bin['Height'])

    items = []
    _items = []
    index = 0
    for item in data['Items']:
        for _ in range(0, int(item['Demand'])):
            width = int(item['Length'])
            height = int(item['Height'])

            _items.append(Item(index, width, height))
            index += 1

    _items.sort(key=lambda item: item.area, reverse=True)
    index = 0
    for item in _items:
        items.append(Item(index, item.width, item.height))
        index += 1

    return W, H, items
