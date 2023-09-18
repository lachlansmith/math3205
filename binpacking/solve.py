import sys

from gurobipy import *

from binpacking.subproblem import SubproblemSolver
from binpacking.model import Bin, Item
from binpacking.exception import NonOptimalSolutionException, IncompatibleBinException


class Solver:
    def __init__(self):
        self.env = Env(empty=True)
        # self.env.setParam("OutputFlag", 0)
        self.env.setParam("LazyConstraints", 1)
        self.env.start()

        self.model = Model("Main problem", env=self.env)

    @staticmethod
    def cut(model, b, indices):
        model.cbLazy(quicksum(model._X[b, i] for i in indices) <= len(indices) - 1)

    @staticmethod
    def callback(model, where):
        if where == GRB.Callback.MIPSOL:
            ub = model._ub
            Y = model.cbGetSolution(model._Y)
            X = model.cbGetSolution(model._X)

            subproblem = SubproblemSolver()

            for b in range(ub):
                if Y[b] < 0.5:
                    break

                bin = Bin(model._width, model._height)

                for i in range(ub):
                    if X[b, i] > 0.5:
                        bin.items.append(model._items[i])

                indices = frozenset(bin.indices())

                if indices in model._feasible:
                    continue

                if indices in model._infeasible:
                    Solver.cut(model, b, indices)
                    continue

                try:
                    subproblem.solve(bin)
                    model._feasible.add(indices)
                except IncompatibleBinException:
                    Solver.cut(model, b, indices)
                    model._infeasible.add(indices)

    @staticmethod
    def extract(model):

        width = model._width
        height = model._height
        items = model._items
        ub = model._ub
        X = model._X
        Y = model._X

        I = range(len(items))

        subproblem = SubproblemSolver()

        solution = []

        for b in range(ub):
            if Y[b].x < 0.5:
                break

            bin = Bin(width, height)

            # Populate the items
            for i in I:
                if X[b, i].x > 0.5:
                    bin.items.append(items[i])

            try:
                solution.append(subproblem.solve(bin))
            except IncompatibleBinException as e:
                print(e)
                sys.exit()

        return solution

    def solve(self, width: int, height: int, bins: list[Bin], items: list[Item]) -> list[Bin]:
        """Here we solve the problem using Gurobi."""

        area = width * height
        ub = len(items)
        I = range(len(items))

        # item i is assigned to bin b
        X = {(b, i): self.model.addVar(vtype=GRB.BINARY) for i in I for b in range(ub)}

        # bin b is open
        Y = {b: self.model.addVar(vtype=GRB.BINARY) for b in range(ub)}

        self.model.setObjective(quicksum(Y[b] for b in range(ub)), GRB.MINIMIZE)

        EachItemUsedOnce = {
            i: self.model.addConstr(quicksum(X[b, i] for b in range(ub)) == 1)
            for i in I}

        SumOfAreasLessThanBinArea = {
            b: self.model.addConstr(quicksum(items[i].area * X[b, i] for i in I) <= area * Y[b])
            for b in range(ub)}

        PreviousBinOpen = {
            b: self.model.addConstr(Y[b + 1] <= Y[b])
            for b in range(ub - 1)}

        self.model._width = width
        self.model._height = height
        self.model._infeasible = set()
        self.model._feasible = set()
        self.model._ub = ub
        self.model._X = X
        self.model._Y = Y
        self.model._items = items

        self.model.optimize(Solver.callback)

        # Create a dictionary to store items in each bin

        if self.model.status == GRB.OPTIMAL:
            return Solver.extract(self.model)
        else:
            raise NonOptimalSolutionException('Failed to find optimal solution')
