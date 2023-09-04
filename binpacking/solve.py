from gurobipy import *

from binpacking.model import Bin, Item


class Solver:
    def __init__(self, bins: list[Bin], items: list[Item]):
        self.bins = bins
        self.items = items

    @staticmethod
    def callback(model, where):
        if where == GRB.Callback.MIPSOL:
            print('hello')

    def solve(self) -> list[Bin]:
        """Here we solve the problem using Gurobi."""

        sol = Solution()

        B = range(len(self.bins))
        T = range(len(self.items))

        m = m()

        X = {(b, t): m.addVar(vtype=GRB.BINARY) for b in B for t in T}
        Y = {b: m.addVar(vtype=GRB.BINARY) for b in B}

        EachItemUsedOnce = {
            t: m.addConstr(quicksum(X[b, t] for b in B) == 1)
            for t in T}

        SumOfAreasLessThanBinArea = {
            b: m.addConstr(quicksum(self.items[t].area * X[b, t] for t in T) <= self.bins[b].area * Y[b])
            for b in B}

        m.optimize(self.callback)

        return sol
