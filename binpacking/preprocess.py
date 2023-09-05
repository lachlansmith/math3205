from binpacking.model import Bin, Item
from itertools import combinations


class Preprocessor:
    def __init__(self, bin: Bin, items: list[Item]):
        """
        Constructor
        """
        self.items = items
        self.Width = bin.width
        self.Height = bin.height

        self.fullyIncompatible = []  # each item requires a bin to iteself
        self.largeItems = []  # each item requires a bin (bin,item) #add large item to its own bin
        self.smallItems = []  # remaining items

        self.bins = []  # pre allocated bins

        self.incompatibleItems = set()  # set of item pairs which cannot go together

        self.filtedItems = []

        self.processed = False

        self.processedItems = []

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

    def minimizeWidth(self):

        combinations()

    def run(self):
        """
        Updates the class variables to contain an updated version of the incompatible items sets 
        as well as a list of the large items and remaing small items.

        note we can do more preprocessing if necessary; figure out what small items can fit beside 
        large items.
        But this will likely involve a heuristic and could be costly to run
        """

        if self.processed == True:
            return
        self.removeIncompatibleItems(self.items, self.Width, self.Height)
        self.determineConflicts(self.items, self.Width, self.Height)
        for item in self.filtedItems:
            if item.width > self.Width/2 and item.height > self.Height/2:
                self.largeItems.append(item)
            else:
                self.smallItems.append(item)
        self.processed = True
        # return list of bins
