class Bin:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.size = w * h


class Item:
    def __init__(self, id, w, h):
        self.id = id
        self.width = w
        self.height = h
        self.size = w * h

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height

    def __lt__(self, other):
        return ((self.size, self.width) < (other.size, other.width))


class Solution:
    def __init__(self):
        pass
