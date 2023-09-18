from binpacking.model import Bin, Item
from itertools import combinations


class Preprocessor:
    def __init__(self, width: int, height: int, items: list[Item]):
        """
        Constructor
        """
        self.items = items
        self.Width = width
        self.Height = height

        # the minimized width/height of the bins calculated after processsing the
        # minimize bin function
        self.minimizedWidth = -1
        self.minimizedHeight = -1

        self.fullyIncompatible = []  # each item requires a bin to iteself
        self.largeItems = []  # each item requires a bin. stored as a list of Bins each bin containing a large item
        self.smallItems = []  # remaining items

        self.incompatibleItems = set()  # set of item pairs which cannot go together
        self.filtedItems = []

        self.processed = False

    def determineConflicts(self, items, W, H):
        """
        Finds all incompatible pairs in given item list according to the provide bin W and H
        and updates incompatible pairs set.
        """

        for i, itemI in enumerate(items):
            for j, itemJ in enumerate(self.items[i+1:]):
                if itemI.width + itemJ.width > W and itemI.height + itemJ.height > H:
                    self.incompatibleItems.add(frozenset((i, j)))

    def removeIncompatibleItems(self, items, W, H):
        """
        Finds and removes large items.
        Updates class variables of small, large and fully imcompatible
        """
        filtedItems = []
        removedItems = []
        # checking each item
        for i, item in enumerate(items):
            w = item.width
            h = item.height

            # removes items with the same size of the bin
            if w == W and h == H:
                removedItems.append(item)
                continue

            isFullyIncompatible = True  # true until proven otherwise

            # checks pairs of items
            for j, itemJ in enumerate(items):
                if i == j:
                    continue

                # if true then the item pair is incompatible
                if w + itemJ.width > W and h + itemJ.height > H:
                    continue

                isFullyIncompatible = False
                break

            # removes the item if it is incompatible with all others (i.e. a large item)
            if isFullyIncompatible:
                removedItems.append(item)
                continue

            filtedItems.append(item)

        self.fullyIncompatible = removedItems
        self.filtedItems = filtedItems

    def minimizeBins(self, items):
        """
        Shrinks the bin sizes based off maxium width and height items can be 
        stacked without exceeding the bin dimensions.
        Returns the minimized Width and Height
        """
        list_combinations = list()
        # creates all combination of items
        for n in range(len(items) + 1):
            list_combinations += list(combinations(items, n))

        W = 0  # min viable width required
        H = 0  # min viable height required
        for comb in list_combinations:
            curW = 0
            curH = 0
            for item in comb:
                curW += item.width
                curH += item.height

            # if width/height is greatest so far and within bounds
            if curW <= self.Width and curW > W:
                W = curW
            if curH <= self.Height and curH > H:
                H = curH
        self.minimizedHeight = H
        self.minimizedWidth = W

    def run(self):
        """
        Updates the class variables to contain an updated version of the incompatible items sets 
        as well as a list of the large items and remaing small items.

        Returns a list of bins containg each large item and 

        note we can do more preprocessing if necessary; figure out what small items can fit beside 
        large items.
        But this will likely involve a heuristic and could be costly to run
        """
        if self.processed == True:
            return self.largeItems, self.smallItems

        # removes all items which must be in its own bin
        self.removeIncompatibleItems(self.items, self.Width, self.Height)

        # determing the items are large enough to be in their own bin
        for item in self.filtedItems:
            if item.width > self.Width/2 and item.height > self.Height/2:
                bin = Bin(self.Width, self.Height)
                print(item.width)
                bin.add(0, 0, item.width, item.height)
                self.largeItems.append(bin)
            else:
                self.smallItems.append(item)

        self.processed = True
        return self.largeItems, self.smallItems
