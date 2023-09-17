from gurobipy import *

from binpacking.model import Bin
from binpacking.exception import IncompatibleBinException


class SubproblemSolver:
    def __init__(self):

        self.env = Env(empty=True)
        self.env.setParam("OutputFlag", 0)
        self.env.start()

    def solve(self, bin: Bin):
        """Here we solve the sub problem, which is to find the optimal placement of items in a single bin."""

        m = Model(env=self.env)

        # Define parameters
        N = range(len(bin.items))
        K = range(0, 4)

        # x,y positions of item n in bin
        X = {n: m.addVar(vtype=GRB.INTEGER) for n in N}
        Y = {n: m.addVar(vtype=GRB.INTEGER) for n in N}

        delta = {(i, j, k): m.addVar(vtype=GRB.BINARY) for i in N for j in N for k in K}

        # Constraint: Item placement within bin dimensions
        ItemPlacementWithinBin = {
            n: [
                m.addConstr(X[n] >= 0),
                m.addConstr(Y[n] >= 0),
                m.addConstr(X[n] + bin.items[n].width <= bin.width),
                m.addConstr(Y[n] + bin.items[n].height <= bin.height)
            ]
            for n in N
        }

        # Constraint: Item placement and prevent overlaps (width and height)
        ItemPlacementAndNoOverlap = {
            (i, j): [
                m.addConstr(X[i] + bin.items[i].width <= X[j] + bin.width * delta[i, j, 0]),
                m.addConstr(X[j] + bin.items[j].width <= X[i] + bin.width * delta[i, j, 1]),
                m.addConstr(Y[i] + bin.items[i].height <= Y[j] + bin.height * delta[i, j, 2]),
                m.addConstr(Y[j] + bin.items[j].height <= Y[i] + bin.height * delta[i, j, 3]),
                m.addConstr(quicksum(delta[i, j, k] for k in K) <= 3)
            ]
            for i in N
            for j in range(i+1, len(bin.items))
        }

        m.optimize()

        if m.status == GRB.OPTIMAL:
            return {bin.items[n].index: (int(X[n].x), int(Y[n].x)) for n in N}
        else:
            raise IncompatibleBinException(bin)
