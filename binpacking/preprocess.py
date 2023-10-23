from itertools import combinations

import math

from binpacking.model import Bin, Item
from binpacking.solve import Solver


from gurobipy import *


class Preprocessor:
    def __init__(self, solver: Solver):
        """
        Constructor
        """
        self.solver = solver

        self.incompatible_items = []
        self.compatible_items = []

    def assignIncompatibleIndices(self):
        """
        Finds and removes large items.
        Updates class variables of small, large and fully imcompatible
        Also updates solvers list of incompatible incides
        """

        self.solver.incompatible_indices = [item.index for item in self.incompatible_items]

    def assignLargeItemIndices(self):
        """
        Updates the fixed indicies list in the solver.
        This function does not removed full imcompatible indicies and that should be run first
        """

        self.solver.large_item_indices = [
            item.index
            for item in self.compatible_items
            if item.width > math.ceil(self.solver.width / 2) and item.height > math.ceil(self.solver.height / 2)
        ]

    def assignConflictIndices(self):
        """
        Finds all incompatible pairs in given item list according to the provide bin W and H
        and returns set of infeasible pairs type set(frozenset([indexi, indexj]))
        """

        self.solver.conflict_indices = [
            [itemI.index, itemJ.index]
            for i, itemI in enumerate(self.compatible_items)
            for j, itemJ in enumerate(self.compatible_items[i + 1:])
            if itemI.width + itemJ.width > self.solver.width and itemI.height + itemJ.height > self.solver.height
        ]

    def run(self):
        """
        Finds and removes large items.
        Updates class variables of small, large and fully imcompatible
        Also updates solvers list of incompatible incides
        """

        self.incompatible_items = []
        self.compatible_items = []

        # checking each item
        for i, item in enumerate(self.solver.items):
            w = item.width
            h = item.height

            # removes items with the same size of the bin
            if w == self.solver.width and h == self.solver.height:
                self.incompatible_items.append(item)
                continue

            isFullyIncompatible = True  # true until proven otherwise

            # checks pairs of items
            for j, itemJ in enumerate(self.solver.items):
                if i == j:
                    continue

                # if true then the item pair is incompatible
                if w + itemJ.width > self.solver.width and h + itemJ.height > self.solver.height:
                    continue

                isFullyIncompatible = False
                break

            # removes the item if it is incompatible with all others (i.e. a extra large item)
            if isFullyIncompatible:
                self.incompatible_items.append(item)
                continue

            self.compatible_items.append(item)
