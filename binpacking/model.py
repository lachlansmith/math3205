
class Bin:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.area = w * h
        self.items = []

    def __str__(self):
        return f'width: {self.width} height: {self.height} area: {self.area}'

    def indices(self):
        return [item.index for item in self.items]

class Item:
    def __init__(self, index, w, h):
        self.index = index
        self.width = w
        self.height = h
        self.area = w * h

    def __str__(self):
        return f'width: {self.width} height: {self.height} area: {self.area}'
