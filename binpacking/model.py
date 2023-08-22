class Bin:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.area = w * h

    def __str__(self):
        return f'width: {self.width} height: {self.height} area: {self.area}'


class Item:
    def __init__(self, id, w, h):
        self.id = id
        self.width = w
        self.height = h
        self.area = w * h

    def __str__(self):
        return f'width: {self.width} height: {self.height} area: {self.area}'

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height

    def __lt__(self, other):
        return ((self.area, self.width) < (other.area, other.width))


class Solution:
    def __init__(self):
        pass
