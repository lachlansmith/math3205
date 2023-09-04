

from binpacking.model import Bin, Item


class Preprocessor:
    def __init__(self, bin: Item, items: list[Item]):
        self.bins = [Bin(bin.width, bin.height)]
        self.items = items

    def run(self) -> tuple[list[Bin], list[Item]]:
        """Here we need to strip out any items that are too big for the bin, and assign items
        more than half the area of the bin to their own bin."""

        return self.bins, self.items
