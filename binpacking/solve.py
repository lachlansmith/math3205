from gurobipy import *
from binpacking.model import Bin, Item
from binpacking.exception import NonOptimalException


class Solver:
    def __init__(self, width: int, height: int, bins: list[Bin], items: list[Item]):
        self.width = width
        self.height = height
        self.area = width * height
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

        ub = len(self.items)

        env = Env(empty=True)
        env.setParam("OutputFlag", 0)
        env.start()

        m = Model(env=env)

        # item t is assigned to bin b
        X = {(b, t): m.addVar(vtype=GRB.BINARY) for t in range(ub) for b in range(ub)}

        # bin b is open
        Y = {b: m.addVar(vtype=GRB.BINARY) for b in range(ub)}

        m.setObjective(quicksum(Y[b] for b in range(ub)), GRB.MINIMIZE)

        EachItemUsedOnce = {
            t: m.addConstr(quicksum(X[b, t] for b in range(ub)) == 1)
            for t in range(ub)}

        SumOfAreasLessThanBinArea = {
            b: m.addConstr(quicksum(self.items[t].area * X[b, t] for t in range(ub)) <= self.area * Y[b])
            for b in range(ub)}

        PreviousBinOpen = {
            b: m.addConstr(Y[b + 1] <= Y[b])
            for b in range(ub - 1)}

        m.optimize()

        # Create a dictionary to store items in each bin
        bins = []

        if m.status == GRB.OPTIMAL:
            for b in range(ub):
                if Y[b].x > 0.5:
                    bins.append(Bin(self.width, self.height))

                    # Populate the items
                    for t in range(ub):
                        if X[b, t].x > 0.5:
                            bins[b].items.append(t)
        else:
            raise NonOptimalException('Indices optimsation failed')

        return bins
