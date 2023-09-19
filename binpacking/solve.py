import math
from typing import Dict

from gurobipy import *

from binpacking.subproblem import SubproblemSolver
from binpacking.model import Bin, Item
from binpacking.exception import NonOptimalSolutionException, BadSolutionException, IncompatibleBinException


class Solver:
    def __init__(self, width: int, height: int, items: list[Item], verbose=True):
        env = Env(empty=True)
        if not verbose:
            env.setParam("OutputFlag", 0)
        env.setParam("LazyConstraints", 1)
        env.start()

        self.model = Model("Main problem", env=env)

        self.width = width
        self.height = height
        self.area = width * height
        self.items = items
        self.lb = int(math.ceil(sum(item.area for item in items) / self.area))
        self.ub = len(items)
        self.incompatible_indices = []
        self.fixed_indices = []

    @staticmethod
    def cut(model, b, indices):
        model.cbLazy(quicksum(model._X[b, i] for i in indices) <= len(indices) - 1)

    @staticmethod
    def callback(model, where):
        if where == GRB.Callback.MIPSOL:
            ub = model._ub
            Y = model.cbGetSolution(model._Y)
            X = model.cbGetSolution(model._X)

            for b in range(ub):
                if Y[b] < 0.5:
                    break

                bin = Bin(model._width, model._height)

                for i in range(len(model._items)):
                    if X[b, i] > 0.5:
                        bin.items.append(model._items[i])

                indices = frozenset(bin.indices())

                if indices in model._feasible:
                    continue

                if indices in model._infeasible:
                    Solver.cut(model, b, indices)
                    continue

                subproblem = SubproblemSolver()

                try:
                    subproblem.solve(bin)
                    model._feasible.add(indices)
                except IncompatibleBinException:
                    Solver.cut(model, b, indices)
                    model._infeasible.add(indices)

    @staticmethod
    def extract(model) -> list[Dict[int, tuple[int, int]]]:

        width = model._width
        height = model._height
        items = model._items
        ub = model._ub
        X = model._X
        Y = model._Y

        I = range(len(items))

        solution = []

        for b in range(ub):
            if Y[b].x < 0.5:
                break

            bin = Bin(width, height)

            # Populate the items
            for i in I:
                if X[b, i].x > 0.5:
                    bin.items.append(items[i])

            subproblem = SubproblemSolver()

            try:
                solution.append(subproblem.solve(bin))
            except IncompatibleBinException as e:
                raise BadSolutionException(e.bin)

        return solution

    def solve(self) -> list[list[int]]:
        """Here we solve the problem using Gurobi."""

        I = range(len(self.items))

        # item i is assigned to bin b
        X = {(b, i): self.model.addVar(vtype=GRB.BINARY) for i in I for b in range(self.ub)}

        # bin b is open
        Y = {b: self.model.addVar(vtype=GRB.BINARY) for b in range(self.ub)}

        self.model.setObjective(quicksum(Y[b] for b in range(self.ub)), GRB.MINIMIZE)

        CompatibleItemsUsedOnce = {
            i: self.model.addConstr(quicksum(X[b, i] for b in range(self.ub)) == 1)
            for i in I if i not in self.incompatible_indices}

        IncompatibleItemsNotUsed = {
            i: self.model.addConstr(quicksum(X[b, i] for b in range(self.ub)) == 0)
            for i in self.incompatible_indices}

        SumOfAreasLessThanBinArea = {
            b: self.model.addConstr(quicksum(self.items[i].area * X[b, i] for i in I) <= self.area * Y[b])
            for b in range(self.ub)}

        PreviousBinOpen = {
            b: self.model.addConstr(Y[b + 1] <= Y[b])
            for b in range(self.ub - 1)}

        FixedItemIndices = {
            (b, i): self.model.addConstr(X[b, i] == 1)
            for b, indices in enumerate(self.fixed_indices)
            for i in indices
        }

        self.model._width = self.width
        self.model._height = self.height
        self.model._infeasible = set()
        self.model._feasible = set()
        self.model._ub = self.ub
        self.model._X = X
        self.model._Y = Y
        self.model._items = self.items

        self.model.optimize(Solver.callback)

        if self.model.status == GRB.OPTIMAL:
            arr = []
            for b in range(self.ub):
                if Y[b].x < 0.5:
                    break

                indices = []
                for i in I:
                    if X[b, i].x > 0.5:
                        indices.append(i)

                arr.append(indices)

            return arr
        else:
            raise NonOptimalSolutionException('Failed to find optimal solution')