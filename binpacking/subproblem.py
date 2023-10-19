from gurobipy import *
# The ortools constraint programmer
from ortools.sat.python import cp_model

from binpacking.model import Bin, Item
from binpacking.heuristic import firstFitDecreasingSubProblem
from binpacking.exception import IncompatibleBinException

from binpacking.colours import *
from typing import Tuple, List, Dict
from itertools import combinations


class SubproblemSolver:
    def __init__(self, verbose=False):
        self.model = Model("BSP")

        if not verbose:
            self.model.setParam("OutputFlag", 0)

        self.fixed_x = []
        self.fixed_y = []

        self.userORTools = False

        self.ortool_model = cp_model.CpModel()
        self.ortool_solver = cp_model.CpSolver()


    def minimizeBin(self, bin: Bin) -> Tuple[int,int]:
        """
        Returns the bins minimized width and height (W, H)
        """
        list_combinations = list()
        items = bin.items
        # creates all combination of items
        for n in range(len(items) + 1):
            list_combinations += list(combinations(items, n))

        W = 0  # min viable width required
        H = 0  # min viable height required
        for comb in list_combinations:
            curW = 0
            curH = 0
            for item in comb:
                curW += item.width
                curH += item.height

            # if width/height is greatest so far and within bounds
            if curW <= bin.width and curW > W:
                W = curW
            if curH <= bin.height and curH > H:
                H = curH

        return W, H

    def solveORtools(self, bin: Bin):
        """
        Solves the subproblem but using ortools

        Note imperically this was found to perform worse then the gurobi cp solver. Don't know why 
        or tools should be better at overlap problems like this one. Was imperically found worse on all 
        instances but a complicated problem that shows this the best is instance 250. On my personal computer
        it took 26 seconds for the or tools sovler to find the optimal solution and 16 seconds using gurobi 
        """
        W, H = self.minimizeBin(bin)

        # Imperically this was found to be no better then the gurobi solver with the additonal no-overlap constraint 

        N = range(len(bin.items))

        # creating variables
        # X and Y position for the item n
        X = {n: self.ortool_model.NewIntVar(0, W - bin.items[n].width, f'{bin.items[n].index}: X position') for n in N}
        Y = {n: self.ortool_model.NewIntVar(0, H - bin.items[n].height, f'{bin.items[n].index}: Y position') for n in N}

        # Width and Height inverval variables for the item n

        X_interval = [self.ortool_model.NewIntervalVar(X[n], bin.items[n].width, X[n]+bin.items[n].width, f'{bin.items[n].index}: X interval') for n in N]
        Y_interval = [self.ortool_model.NewIntervalVar(Y[n], bin.items[n].height, Y[n]+bin.items[n].height, f'{bin.items[n].index}: Y interval') for n in N]

        # Prevents overlapping rectangles
        self.ortool_model.AddNoOverlap2D(X_interval, Y_interval)

        # assign max item
        if bin.items:
            max_item_index = bin.items.index(max(bin.items, key=lambda item: item.area))
            FixLargestItem = (
                self.ortool_model.Add(X[max_item_index] == 0),
                self.ortool_model.Add(Y[max_item_index] == 0)
            )

        # order identical items
        EqualItemSymmetryBreaking = {(i,j): 
                                     self.ortool_model.Add(X[i] <= X[j])
                                     for i in N for j in N[i:]
                                     if bin.items[i].width == bin.items[j].width and bin.items[i].height == bin.items[j].height}


        status = self.ortool_solver.Solve(self.ortool_model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return {bin.items[n].index: (int(self.ortool_solver.Value(X[n])), int(self.ortool_solver.Value(Y[n]))) for n in N}
        else:
            raise IncompatibleBinException(bin)
  
    def constraint_program(self, bin: Bin) -> Dict[int, Tuple[int, int]]:
        """
        Solve the subproblem using a gurobi constraint program. 
        Returns a Dictonary where the key is the item index and the value is the 
        x y position of the item
        """

        W, H = self.minimizeBin(bin)
        # Define parameters
        N = range(len(bin.items))

        # x,y positions of item n in bin
        X = {n: self.model.addVar(vtype=GRB.INTEGER) for n in N}
        Y = {n: self.model.addVar(vtype=GRB.INTEGER) for n in N}

        K = range(0, 4)
        delta = {(i, j, k): self.model.addVar(vtype=GRB.BINARY) for i in N for j in N for k in K}

        # problem constraints

        ItemPlacementWithinBin = {
            n: [
                self.model.addConstr(X[n] >= 0),
                self.model.addConstr(Y[n] >= 0),
                self.model.addConstr(X[n] + bin.items[n].width <= W),
                self.model.addConstr(Y[n] + bin.items[n].height <= H)
            ]
            for n in N
        }

        ItemPlacementAndNoOverlap = {
            (i, j): [
                self.model.addConstr(X[i] + bin.items[i].width <= X[j] + W * delta[i, j, 0]),
                self.model.addConstr(X[j] + bin.items[j].width <= X[i] + W * delta[i, j, 1]),
                self.model.addConstr(Y[i] + bin.items[i].height <= Y[j] + H * delta[i, j, 2]),
                self.model.addConstr(Y[j] + bin.items[j].height <= Y[i] + H * delta[i, j, 3]),
                self.model.addConstr(quicksum(delta[i, j, k] for k in K) <= 3)
            ]
            for i in N
            for j in range(i+1, len(bin.items))
        }

        #adds constraint for equal items that one item must be place before the other
        EqualItemSymmetryBreaking = {(i, j): 
                                     self.model.addConstr(X[i] <= X[j]) 
                                     for i in N for j in N[i:] 
                                     if bin.items[i].width == bin.items[j].width and bin.items[i].height == bin.items[j].height}


        #fix largest item (max area) to 0,0 in the grid
        if bin.items:
            max_item_index = bin.items.index(max(bin.items, key = lambda item: item.area))
            FixingLargestItem = (
                self.model.addConstr(X[max_item_index] == 0), 
                self.model.addConstr(Y[max_item_index] == 0))

        self.model.optimize()

        if self.model.status == GRB.OPTIMAL:
            return {bin.items[n].index: (int(X[n].x), int(Y[n].x)) for n in N}
        else:
            raise IncompatibleBinException(bin)
   
    def solve(self, bin: Bin):
        """
        Here we solve the sub problem, which is to find the optimal placement of items in a single bin.

        Implementataion first tries a first fit heuristic then uses a constraint program if the heuristic fails
        """
        
        bins_used, bins = firstFitDecreasingSubProblem(bin.width, bin.height, bin.items)

        if bins_used == 1:
            return 'FEASIBLE'
        
        if not self.userORTools:
            return self.constraint_program(bin)
        else:
            return self.solveORtools(bin)
