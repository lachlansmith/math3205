from functools import reduce

from gurobipy import *

from binpacking.subproblem import SubproblemSolver
from binpacking.model import Bin, Item
from binpacking.exception import NonOptimalSolutionException, IncompatibleBinException


class Solver:
    def __init__(self, env):
        self.env = env

    @staticmethod
    def cut(model, b, indices):
        model.cbLazy(quicksum(model._X[b, i] for i in indices) <= len(indices) - 1)

    @staticmethod
    def callback(model, where):
        if where == GRB.Callback.MIPSOL:
            ub = model._ub
            Y = model.cbGetSolution(model._Y)
            X = model.cbGetSolution(model._X)

            solver = SubproblemSolver()

            for b in range(ub):
                if Y[b] < 0.5:
                    break

                bin = Bin(model._width, model._height)

                for i in range(ub):
                    if X[b, i] > 0.5:
                        bin.items.append(model._items[i])

                indices = frozenset(bin.indices())

                if len(indices) == 0:
                    continue

                if indices in model._feasible:
                    continue

                if indices in model._infeasible:
                    Solver.cut(model, b, indices)
                    continue

                try:
                    solver.solve(bin)
                    model._feasible.add(indices)
                except IncompatibleBinException:
                    Solver.cut(model, b, indices)
                    model._infeasible.add(indices)

    def solve(self, width: int, height: int, bins: list[Bin], items: list[Item]) -> list[Bin]:
        """Here we solve the problem using Gurobi."""

        m = Model(env=self.env)

        m._infeasible = set()
        m._feasible = set()

        area = width * height
        ub = len(items)
        I = range(len(items))

        # item i is assigned to bin b
        X = {(b, i): m.addVar(vtype=GRB.BINARY) for i in I for b in range(ub)}

        # bin b is open
        Y = {b: m.addVar(vtype=GRB.BINARY) for b in range(ub)}

        m.setObjective(quicksum(Y[b] for b in range(ub)), GRB.MINIMIZE)

        EachItemUsedOnce = {
            i: m.addConstr(quicksum(X[b, i] for b in range(ub)) == 1)
            for i in I}

        SumOfAreasLessThanBinArea = {
            b: m.addConstr(quicksum(items[i].area * X[b, i] for i in I) <= area * Y[b])
            for b in range(ub)}

        PreviousBinOpen = {
            b: m.addConstr(Y[b + 1] <= Y[b])
            for b in range(ub - 1)}

        m._ub = ub
        m._X = X
        m._Y = Y
        m._items = items

        m.optimize(Solver.callback)

        # Create a dictionary to store items in each bin

        if m.status == GRB.OPTIMAL:
            solution = []
            for b in range(ub):
                if Y[b].x < 0.5:
                    break

                solution.append(Bin(width, height))

                # Populate the items
                for i in I:
                    if X[b, i].x > 0.5:
                        solution[b].items.append(items[i])

            return solution
        else:
            raise NonOptimalSolutionException('Failed to find optimal solution')
