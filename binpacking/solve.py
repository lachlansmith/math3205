import math
from typing import Dict

from gurobipy import *

from binpacking.subproblem import SubproblemSolver
from binpacking.model import Bin, Item
from binpacking.exception import NonOptimalSolutionException, BadSolutionException, IncompatibleBinException


class Solver:
    def __init__(self, width: int, height: int, items: list[Item], verbose=False):
        self.model = Model("BMP")

        if not verbose:
            self.model.setParam("OutputFlag", 0)

        self.model.setParam("LazyConstraints", 1)

        self.model._verbose = verbose

        self.width = width
        self.height = height
        self.area = width * height
        self.items = items
        self.lb = int(math.ceil(sum(item.area for item in items) / self.area))
        self.ub = len(items)
        self.large_item_indices = []
        self.less_than_lower_bound_indices = []
        self.incompatible_indices = []
        self.conflict_indices = []

    @staticmethod
    def cut(model, b, indices):
        model.cbLazy(quicksum(model._X[b, i] for i in indices) <= len(indices) - 1)

    @staticmethod
    def report(model):
        print(f'Aborts: {model._aborts}')
        print(f'Cuts: {model._cuts}')
        print(f'Feasible sets: {len(model._feasible)}')
        print(f'Infeasible sets: {len(model._infeasible)}', end='\r\033[3A')

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
                    model._aborts += 1
                    continue

                if indices in model._infeasible:
                    Solver.cut(model, b, indices)

                    model._cuts += 1
                    model._aborts += 1

                    continue

                subproblem = SubproblemSolver()

                try:
                    subproblem.solve(bin)
                    model._feasible.add(indices)

                    if not model._verbose:
                        Solver.report(model)

                except IncompatibleBinException:
                    Solver.cut(model, b, indices)
                    model._infeasible.add(indices)

                    model._cuts += 1

                    if not model._verbose:
                        Solver.report(model)

    @staticmethod
    def extract(width: int, height: int, items: list[Item], bins: list[list[int]]) -> list[Dict[int, tuple[int, int]]]:

        solution = []

        for b, indices in enumerate(bins):

            bin = Bin(width, height)

            # Populate the items
            for i in indices:
                bin.items.append(items[i])

            subproblem = SubproblemSolver()

            try:
                solution.append(subproblem.solve(bin))
            except IncompatibleBinException:
                raise BadSolutionException(f"Solution wasn't able to be extracted due to an incompatible bin {b}")

        return solution

    def solve(self) -> list[list[int]]:
        """Here we solve the problem using Gurobi."""

        I = range(len(self.items))

        # item i is assigned to bin b
        X = {(b, i): self.model.addVar(vtype=GRB.BINARY) for i in I for b in range(self.ub)}

        # bin b is open
        Y = {b: self.model.addVar(vtype=GRB.BINARY) for b in range(self.ub)}

        self.model.setObjective(quicksum(Y[b] for b in range(self.ub)), GRB.MINIMIZE)

        # pre assignment constraints

        FixLargeItemIndices = {
            (b, i): self.model.addConstr(X[b, i] == 1)
            for b, indices in enumerate(self.large_item_indices)
            for i in indices
        }

        FixLessThanLowerBoundIndices = {
            (b, i): self.model.addConstr(X[b, i] == 0)
            for b in range(self.lb) for i in I if b > i
        }

        PreventIncompatibleItemIndices = {
            i: self.model.addConstr(quicksum(X[b, i] for b in range(self.ub)) == 0)
            for i in self.incompatible_indices
        }

        PreventConflictingItemIndices = {
            b: self.model.addConstr(quicksum(X[b, i] for i in indices) <= 1)
            for indices in self.conflict_indices for b in range(self.ub)
        }

        # problem constraints

        SumOfAreasLessThanBinArea = {
            b: self.model.addConstr(quicksum(self.items[i].area * X[b, i] for i in I) <= self.area * Y[b])
            for b in range(self.ub)}

        ItemsUsedOnce = {
            i: self.model.addConstr(quicksum(X[b, i] for b in range(self.ub)) == 1)
            for i in I if i not in self.incompatible_indices}

        PreviousBinOpen = {
            b: self.model.addConstr(Y[b + 1] <= Y[b])
            for b in range(self.ub - 1)}

        self.model._width = self.width
        self.model._height = self.height
        self.model._infeasible = set()
        self.model._feasible = set()
        self.model._ub = self.ub
        self.model._X = X
        self.model._Y = Y
        self.model._items = self.items
        self.model._cuts = 0
        self.model._aborts = 0

        # add preprocess cuts here?

        self.model.optimize(Solver.callback)

        if self.model._verbose:
            Solver.report(self.model)

        print('\033[3B')

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
