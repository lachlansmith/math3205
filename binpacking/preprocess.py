

from binpacking.model import Bin, Item, Solution


class PackingPreprocessor:
    def __init__(self, bin: Bin, items: list[Item]):
        self.bins = [bin]
        self.items = items

    def run(self) -> tuple[Bin, list[Item]]:
        """Here we need to strip out any items that are too big for the bin, and assign items
        more than half the area of the bin to their own bin."""

        return self.bins, self.items
