from gurobipy import *
#The ortools constraint programmer
from ortools.sat.python import cp_model

from binpacking.model import Bin
from binpacking.exception import IncompatibleBinException

from binpacking.colours import *


class SubproblemSolver:
    def __init__(self, verbose=False):

        env = Env(empty=True)
        if not verbose:
            env.setParam("OutputFlag", 0)
        env.start()

        self.model = Model("Subproblem", env=env)
        self.fixed_x = []
        self.fixed_y = []


    def solveORtools(self,bin: Bin):
        """
        Solves the subproblem but using ortools
        """
        model = cp_model.CpModel()
        solver = cp_model.CpSolver()

        N = range(len(bin.items))

        #creating variables
        #X and Y position for the item n 
        X = {n: model.NewIntVar(0, bin.width - bin.items[n].width, f'{bin.items[n].index}: X position') for n in N}
        Y = {n: model.NewIntVar(0, bin.height - bin.items[n].height, f'{bin.items[n].index}: Y position') for n in N}

        #Width and Height inverval variables for the item n 
    
        X_interval = [model.NewIntervalVar(X[n], bin.items[n].width, X[n]+bin.items[n].width, f'{bin.items[n].index}: X interval') for n in N] # {n: model.NewIntervalVar(X[n], bin.items[n].width, X[n]+bin.items[n].width, f'{bin.items[n].index}: X interval') for n in N}
        Y_interval = [model.NewIntervalVar(Y[n], bin.items[n].height, Y[n]+bin.items[n].height, f'{bin.items[n].index}: Y interval') for n in N] #{n: model.NewIntervalVar(Y[n], bin.items[n].height, Y[n]+bin.items[n].height, f'{bin.items[n].index}: Y interval') for n in N}
        
        model.AddNoOverlap2D(X_interval, Y_interval)

        status = solver.Solve(model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return {bin.items[n].index: (int(solver.Value(X[n])), int(solver.Value(Y[n]))) for n in N}
        else:
            raise IncompatibleBinException(bin)




    








    def solve(self, bin: Bin):
        """Here we solve the sub problem, which is to find the optimal placement of items in a single bin."""


        return self.solveORtools(bin)
        # Define parameters
        N = range(len(bin.items))
        

        # x,y positions of item n in bin
        X = {n: self.model.addVar(vtype=GRB.INTEGER) for n in N}
        Y = {n: self.model.addVar(vtype=GRB.INTEGER) for n in N}

        K = range(0, 4)
        delta = {(i, j, k): self.model.addVar(vtype=GRB.BINARY) for i in N for j in N for k in K}

        ItemPlacementWithinBin = {
            n: [
                self.model.addConstr(X[n] >= 0),
                self.model.addConstr(Y[n] >= 0),
                self.model.addConstr(X[n] + bin.items[n].width <= bin.width),
                self.model.addConstr(Y[n] + bin.items[n].height <= bin.height)
            ]
            for n in N
        }

        ItemPlacementAndNoOverlap = {
            (i, j): [
                self.model.addConstr(X[i] + bin.items[i].width <= X[j] + bin.width * delta[i, j, 0]),
                self.model.addConstr(X[j] + bin.items[j].width <= X[i] + bin.width * delta[i, j, 1]),
                self.model.addConstr(Y[i] + bin.items[i].height <= Y[j] + bin.height * delta[i, j, 2]),
                self.model.addConstr(Y[j] + bin.items[j].height <= Y[i] + bin.height * delta[i, j, 3]),
                self.model.addConstr(quicksum(delta[i, j, k] for k in K) <= 3)
            ]
            for i in N
            for j in range(i+1, len(bin.items))
        }

        self.model.optimize()

        if self.model.status == GRB.OPTIMAL:
            return {bin.items[n].index: (int(X[n].x), int(Y[n].x)) for n in N}
        else:
            raise IncompatibleBinException(bin)
