import json

from binpacking.model import Bin, Item


class Parser:
    def __init__(self) -> None:
        self.data = None

    def parse_data(self, instance) -> tuple[int, int, list[Item]]:

        with open(f'./data/{instance}.json', 'r') as file:
            self.data = json.loads(file.read())

        bin = self.data['Objects'][0]
        W = int(bin['Length'])
        H = int(bin['Height'])

        self.items = []
        index = 0
        for item in self.data['Items']:
            for _ in range(0, int(item['Demand'])):
                width = int(item['Length'])
                height = int(item['Height'])

                self.items.append(Item(index, width, height))
                index += 1

        return W, H, self.items
