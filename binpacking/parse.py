import json

from model import Item, Bin


class DataParser:
    def __init__(self, path) -> None:
        self.data = None

        with open(path, 'r') as file:
            self.data = json.loads(file.read())

    def parse_data(self):

        bin = self.data['Objects'][0]
        W = int(bin['Length'])
        H = int(bin['Height'])

        self.items = []
        itemId = 0
        for item in self.data['Items']:
            for _ in range(0, int(item['Demand'])):
                width = int(item['Length'])
                height = int(item['Height'])

                self.items.append(Item(itemId, width, height))
                itemId += 1

        self.bin = Bin(W, H)

        return self.bin, self.items
