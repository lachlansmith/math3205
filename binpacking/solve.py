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

        print(lb)

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

        if m.status == GRB.OPTIMAL:
            # Count the number of bins used (same as the objective value)
            print("Number of bins used:", int(m.ObjVal))

            # Create a dictionary to store items in each bin
            itemsInBins = {b: [] for b in range(ub)}

            # Populate the itemsInBins dictionary based on the solution
            for t in T:
                for b in range(ub):
                    if X[b, t].x > 0.5:
                        itemsInBins[b].append(t)

            # Print the items in each bin
            for b in range(ub):
                print("Items in bin", b, ":", itemsInBins[b])

        else:
            print("Optimization did not result in an optimal solution.")

        sol = Solution(self.bins)

        return sol
