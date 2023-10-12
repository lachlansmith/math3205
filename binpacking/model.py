
class Bin:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.area = w * h
        self.items = []

    def indices(self):
        return [item.index for item in self.items]


class Item:
    def __init__(self, index, w, h):
        self.index = index
        self.width = w
        self.height = h
        self.area = w * h
