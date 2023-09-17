from gurobipy import *

from binpacking.model import Bin, Item


class SubproblemSolver:
    def __init__(self, env):
        self.env = env

    def solve(self, bin: Bin) -> list[Bin]:
        """Here we solve the sub problem, which is to find the optimal placement of items in a single bin."""

        m = Model(env=self.env)

        # Define parameters
        N = range(len(bin.items))
        K = range(0,4)
       

        # Whether item b has been placed in bin
        Z = {n: m.addVar(vtype=GRB.BINARY) for n in N}

        # x,y positions of item n in bin
        X = {n: m.addVar(vtype=GRB.INTEGER) for n in N}
        Y = {n: m.addVar(vtype=GRB.INTEGER) for n in N}

        delta = {(i,j,k): m.addVar(vtype=GRB.BINARY) for i in N for j in N for k in K}

        # #Set objective function: minimize wasted space
        # m.setObjective(
        #     quicksum(
        #         (bin.width - X[n] - bin.items[n].width)**2 +
        #         (bin.height - Y[n] - bin.items[n].height)**2
        #         for n in N
        #     ),
        #     GRB.MINIMIZE
        # )


        #Constraint: Item placement within bin dimensions
        ItemPlacementWithinBin = {
            n: [
                m.addConstr(X[n] >= 0),
                m.addConstr(Y[n] >= 0),
                m.addConstr(X[n] + bin.items[n].width <= bin.width),
                m.addConstr(Y[n] + bin.items[n].height <= bin.height)
            ]
            for n in N
        }

        # Constraint: Item placement and prevent overlaps (width and height)
        ItemPlacementAndNoOverlap = {
            (i, j): [
                m.addConstr(X[i] +  bin.items[i].width <= X[j] + bin.width*delta[i,j,0]),
                m.addConstr(X[j] +  bin.items[j].width <= X[i] + bin.width*delta[i,j,1]),
                m.addConstr(Y[i] +  bin.items[i].height <= Y[j] + bin.height*delta[i,j,2]),
                m.addConstr(Y[j] +  bin.items[j].height <= Y[i] + bin.height*delta[i,j,3]),
                m.addConstr(quicksum(delta[i,j,k] for k in K) <= 3)
            ]
            for i in N
            for j in range(i+1,len(bin.items))
        }


        # ItemPlacementAndNoOverlap = {
        #     (i, j): [
        #         m.addConstr(X[i] + Z[i] * bin.items[i].width <= X[j] + Z[j] * bin.items[j].width),
        #         m.addConstr(X[j] + Z[j] * bin.items[j].width <= X[i] + Z[i] * bin.items[i].width),
        #         m.addConstr(Y[i] + Z[i] * bin.items[i].height <= Y[j] + Z[j] * bin.items[j].height),
        #         m.addConstr(Y[j] + Z[j] * bin.items[j].height <= Y[i] + Z[i] * bin.items[i].height)
        #     ]
        #     for i in N
        #     for j in range(i+1,len(bin.items))
        # }

        m.optimize()
        for n in N:
            print('item ',n,(bin.items[n].width,bin.items[n].height)) #,'placed',(X[n].x,Y[n].x)
        print()

        
        if m.status == GRB.OPTIMAL:
            for n in N:
                print(f"Item {n} {(bin.items[n].width, bin.items[n].height)}")
                print(f'Placed X = {X[n].x}, Y = {Y[n].x}')
                if Z[n].x > 0.5:
                    print("Item placed in the bin")
                else:
                    print("Item not placed in the bin")

            print([delta[0,1,k].x for k in K])

            print(f"Total Wasted Space: {m.objVal}")
        else:

            raise NonOptimalException('Placement optimsation failed')
