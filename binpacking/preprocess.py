from itertools import combinations

from binpacking.model import Bin, Item
from binpacking.solve import Solver


from gurobipy import *
from math import floor, ceil


class Preprocessor:
    def __init__(self, solver: Solver):
        """
        Constructor
        """
        self.solver = solver
        self.items = solver.items
        self.width = solver.width
        self.height = solver.height

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

    def assignIncompatibleIndices(self):
        """
        Finds and removes large items.
        Updates class variables of small, large and fully imcompatible
        Also updates solvers list of incompatible incides
        """
        filtedItems = []
        removedItems = []
        # checking each item
        for i, item in enumerate(self.items):
            w = item.width
            h = item.height

            # removes items with the same size of the bin
            if w == self.width and h == self.height:
                removedItems.append(item)
                continue

            isFullyIncompatible = True  # true until proven otherwise

            # checks pairs of items
            for j, itemJ in enumerate(self.items):
                if i == j:
                    continue

                # if true then the item pair is incompatible
                if w + itemJ.width > self.width and h + itemJ.height > self.height:
                    continue

                isFullyIncompatible = False
                break

            # removes the item if it is incompatible with all others (i.e. a extra large item)
            if isFullyIncompatible:
                removedItems.append(item)
                continue

            filtedItems.append(item)

        self.fullyIncompatible = removedItems
        self.filtedItems = filtedItems

        # updates solvers incompatible indices
        for item in removedItems:
            self.solver.incompatible_indices.append(item.index)

    def assignLargeItemIndices(self):
        """
        Updates the fixed indicies list in the solver.
        This function does not removed full imcompatible indicies and that should be run first
        """
        for item in self.filtedItems:
            if item.width > self.width / 2 and item.height > self.height / 2:
                self.solver.large_item_indices.append([item.index])

    def assignConflictIndices(self):
        """
        Finds all incompatible pairs in given item list according to the provide bin W and H
        and returns set of infeasible pairs type set(frozenset([indexi, indexj]))
        """

        for i, itemI in enumerate(self.items):
            for j, itemJ in enumerate(self.items[i + 1:]):
                if itemI.width + itemJ.width > self.width and itemI.height + itemJ.height > self.height:
                    self.solver.conflict_indices.append([itemI.index, itemJ.index])

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
            if curW <= self.width and curW > W:
                W = curW
            if curH <= self.height and curH > H:
                H = curH
        self.minimizedHeight = H
        self.minimizedWidth = W

        return W, H

    def upperbound(self):
        """
        Finds a upperbound for the number of bins
        Excludes the removed items
        """
        pass

    def lowerbound(self, items):
        """
        Finds a lowerbound for the number of bins.
        Excludes the removed items
        """
        U = range(0, 3)
        K = range(1, self.Area/2+1)

        lowerbound = max(ceil(
            sum(self.dff(u, item.width, k, items) * self.dff(u, item.height, k, items) for item in items) / (
                self.dff(u, self.width, k, items) * self.dff(u, self.height, k, items)))
            for u in U for v in U for k in K for l in K)

    def dff(self, fn, x, k, items):
        """
        Returns the value from the DFF numbered fn with the parameters
        x (width / height of items or bin)
        k paramter in range [1,C/2]
        C bin area
        items items to find lower bound from
        """
        if fn == 0:
            return self.dff0(x, k)
        elif fn == 1:
            return self.dff1(x, k, items)
        elif fn == 0:
            return self.dff2(x, k)
        else:
            raise ValueError('DFF parameter fn should be (0,1,2)')

    def dff0(self, x, k):
        C = self.Area
        if x > C-k:
            return C
        elif C-k >= x and x >= k:
            return x
        else:
            return 0

    def knapsack(self, C: int, items: list) -> int:
        """
        Solve the cardinaility knapsack problem for the given bin area C and 
        list of items.
        Returns maximum number of items which can fit in A.
        NOTE packing feasiblity not considered 
        """

        m = Model()
        I = range(0, len(items))

        # if item i is placed
        X = {i: m.addVar(vtype=GRB.BINARY) for i in range(0, len(items))}

        # maximize number of items chosen
        m.setObjective(quicksum(X[i] for i in I), GRB.MAXIMIZE)

        # total area of the items must be less than the bins area
        m.addConstr(quicksum(X[i]*items[i].area for i in I) <= C)

        m.optimize()
        # for i in I:
        #     if round(X[i].x) == 1:
        #         print(f'item, {items[i]} placed')

        return m.objVal

    def dff1(self, x, k, items) -> int:
        # TODO I should be basing the knapsack problem off 1 Dimension (either width or height) not area
        # and the items to be consdered J should be with the widths or heights k <= item(width or height) <= C/2
        # only takes items
        C = self.Area
        if x > C/2:
            return self.knapsack(C, items) - self.knapsack(C-x, items)
        elif C/2 <= x and x >= k:
            return 1
        else:
            return 0

    def dff2(self, x, k) -> int:
        C = self.Area
        if x > C/2:
            return 2*(floor(C/k)-floor((C-x)/k))
        elif x == C/2:
            return floor(C/k)
        elif x < C/2:
            return 2*floor(x/k)

    def run(self):
        """
        Updates the class variables to contain an updated version of the incompatible items sets 
        as well as a list of the large items and remaing small items.

        Returns a list of bins containg each large item and a list of the remaing small items

        note we can do more preprocessing if necessary; figure out what small items can fit beside 
        large items.
        But this will likely involve a heuristic and could be costly to run
        """
        # NOTE I will try and only use this run method once all of the preprocessing is working
        if self.processed == True:
            return self.largeItems, self.smallItems

        # removes all items which must be in its own bin
        self.removeIncompatibleItems(self.items, self.width, self.height)

        # determing the items are large enough to be in their own bin
        for item in self.filtedItems:
            if item.width > self.width/2 and item.height > self.height/2:
                bin = Bin(self.width, self.height)
                bin.items.append(item)
                self.largeItems.append(bin)
            else:
                self.smallItems.append(item)

        self.processed = True
        return self.largeItems, self.smallItems
