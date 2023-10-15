from gurobipy import *
# The ortools constraint programmer
from ortools.sat.python import cp_model

from binpacking.model import Bin
from binpacking.exception import IncompatibleBinException

from binpacking.colours import *


class SubproblemSolver:
    def __init__(self, verbose=False):
        self.model = Model("BSP")

        if not verbose:
            self.model.setParam("OutputFlag", 0)

    def solve(self, bin: Bin):
        """Here we solve the sub problem, which is to find the optimal placement of items in a single bin."""

        # return self.solveORtools(bin)
        # Define parameters
        N = range(len(bin.items))

        # x,y positions of item n in bin
        X = {n: self.model.addVar(vtype=GRB.INTEGER) for n in N}
        Y = {n: self.model.addVar(vtype=GRB.INTEGER) for n in N}

        K = range(0, 4)
        delta = {(i, j, k): self.model.addVar(vtype=GRB.BINARY) for i in N for j in N for k in K}

        # pre assignment constraints

        # fix largest item (max area) to 0,0 in the grid
        if bin.items:
            max_item_index = bin.items.index(max(bin.items, key=lambda item: item.area))
            FixLargestItem = (
                self.model.addConstr(X[max_item_index] == 0),
                self.model.addConstr(Y[max_item_index] == 0)
            )

        # adds constraint for equal items that one item must be place before the other
        EqualItemSymmetryBreaking = {
            (i, j): self.model.addConstr(X[i] <= X[j])
            for i in N for j in N[i:]
            if bin.items[i].width == bin.items[j].width and bin.items[i].height == bin.items[j].height
        }

        # problem constraints

        ItemPlacementWithinBin = {
            n: [
                self.model.addConstr(X[n] >= 0),
                self.model.addConstr(Y[n] >= 0),
                self.model.addConstr(X[n] + bin.items[n].width <= bin.width),
                self.model.addConstr(Y[n] + bin.items[n].height <= bin.height)
            ]
            for n in N
        }

        ItemPlacementAndNoOverlap = {
            (i, j): [
                self.model.addConstr(X[i] + bin.items[i].width <= X[j] + bin.width * delta[i, j, 0]),
                self.model.addConstr(X[j] + bin.items[j].width <= X[i] + bin.width * delta[i, j, 1]),
                self.model.addConstr(Y[i] + bin.items[i].height <= Y[j] + bin.height * delta[i, j, 2]),
                self.model.addConstr(Y[j] + bin.items[j].height <= Y[i] + bin.height * delta[i, j, 3]),
                self.model.addConstr(quicksum(delta[i, j, k] for k in K) <= 3)
            ]
            for i in N
            for j in range(i+1, len(bin.items))
        }

        self.model.optimize()

        if self.model.status == GRB.OPTIMAL:
            return {bin.items[n].index: (int(X[n].x), int(Y[n].x)) for n in N}
        else:
            raise IncompatibleBinException(bin)
