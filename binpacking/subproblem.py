from gurobipy import *

from binpacking.model import Bin
from binpacking.exception import IncompatibleBinException


class SubproblemSolver:
    def __init__(self, verbose=False):

        env = Env(empty=True)
        if not verbose:
            env.setParam("OutputFlag", 0)
        env.start()

        self.model = Model("Subproblem", env=env)

    def solve(self, bin: Bin):
        """Here we solve the sub problem, which is to find the optimal placement of items in a single bin."""

        # Define parameters
        N = range(len(bin.items))
        K = range(0, 4)

        # x,y positions of item n in bin
        X = {n: self.model.addVar(vtype=GRB.INTEGER) for n in N}
        Y = {n: self.model.addVar(vtype=GRB.INTEGER) for n in N}

        delta = {(i, j, k): self.model.addVar(vtype=GRB.BINARY) for i in N for j in N for k in K}

        # Constraint: Item placement within bin dimensions
        ItemPlacementWithinBin = {
            n: [
                self.model.addConstr(X[n] >= 0),
                self.model.addConstr(Y[n] >= 0),
                self.model.addConstr(X[n] + bin.items[n].width <= bin.width),
                self.model.addConstr(Y[n] + bin.items[n].height <= bin.height)
            ]
            for n in N
        }

        # Constraint: Item placement and prevent overlaps (width and height)
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
