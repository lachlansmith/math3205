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

    @staticmethod
    def cut(m, b, indices):
        m.cbLazy(quicksum(m._X[b, i] for i in indices) <= len(indices) - 1)

    @staticmethod
    def callback(m, where):
        if where == GRB.Callback.MIPSOL:
            ub = m._ub
            Y = m.cbGetSolution(m._Y)
            X = m.cbGetSolution(m._X)

            subproblem = SubproblemSolver()

            for b in range(ub):
                if Y[b] < 0.5:
                    break

                bin = Bin(m._width, m._height)

                for i in range(ub):
                    if X[b, i] > 0.5:
                        bin.items.append(m._items[i])

                indices = frozenset(bin.indices())

                if indices in m._feasible:
                    continue

                if indices in m._infeasible:
                    Solver.cut(m, b, indices)
                    continue

                try:
                    subproblem.solve(bin)
                    m._feasible.add(indices)
                except IncompatibleBinException:
                    Solver.cut(m, b, indices)
                    m._infeasible.add(indices)

    @staticmethod
    def extract(m):

        width = m._width
        height = m._height
        items = m._items
        ub = m._ub
        X = m._X
        Y = m._X

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

        m = Model(env=self.env)

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

        m._width = width
        m._height = height
        m._infeasible = set()
        m._feasible = set()
        m._ub = ub
        m._X = X
        m._Y = Y
        m._items = items

        m.optimize(Solver.callback)

        # Create a dictionary to store items in each bin

        if m.status == GRB.OPTIMAL:
            return Solver.extract(m)
        else:
            raise NonOptimalSolutionException('Failed to find optimal solution')
