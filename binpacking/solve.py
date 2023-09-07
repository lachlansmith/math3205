from gurobipy import *
import math

from binpacking.model import Bin, Item, Solution


class Solver:
    def __init__(self, bins: list[Bin], items: list[Item]):
        self.bins = bins
        self.items = items

    @staticmethod
    def AddCut(items, itemVariables, bins, model):
        for b in bins:
            expr = gp.LinExpr()
            for i in items:
                expr += itemVariables[b][i]

            model.cbLazy(expr <= len(items) - 1)

    @staticmethod
    def callback(model, where):
        if where == GRB.Callback.MIPSOL:
            pass
            # for b in bins:
            #     expr = gp.LinExpr()
            #     for i in items:
            #         expr += itemVariables[b][i]

            #     model.cbLazy(expr <= len(items) - 1)

    def solve(self) -> list[Bin]:
        """Here we solve the problem using Gurobi."""

        B = range(len(self.bins))
        T = range(len(self.items))

        lb = int(math.ceil(sum([self.bins[b].area for b in B]) / self.bins[0].area))
        ub = len(self.items)

        m = Model()

        # item t is assigned to bin b
        X = {(b, t): m.addVar(vtype=GRB.BINARY) for t in T for b in range(ub)}

        # bin b is open
        Y = {b: m.addVar(vtype=GRB.BINARY) for b in range(ub)}

        m.setObjective(quicksum(Y[b] for b in range(ub)), GRB.MINIMIZE)

        EachItemUsedOnce = {
            t: m.addConstr(quicksum(X[b, t] for b in range(ub)) == 1)
            for t in T}

        SumOfAreasLessThanBinArea = {
            b: m.addConstr(quicksum(self.items[t].area * X[b, t] for t in T) <= self.bins[0].area * Y[b])
            for b in range(ub)}

        m.optimize()

        print(m.ObjVal)

        # for t in T:

        sol = Solution(self.bins)

        return sol
