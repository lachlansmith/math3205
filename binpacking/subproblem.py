from gurobipy import *

from binpacking.model import Bin, Item


class SubproblemSolver:
    def __init__(self, bin: Bin, items: list[Item]):
        self.bin = bin
        self.items = items

    def solve(self) -> list[Bin]:
        """Here we solve the sub problem, which is to find the optimal placement of items in a single bin."""

        m = Model()

        # Define parameters
        Wb = 10  # Width of the bin
        Hb = 8   # Height of the bin
        n = 3    # Number of items

        W = [3, 2, 1]  # Width of each item
        H = [2, 4, 3]  # Height of each item

        # Create binary decision variables for item placement
        Z = {t: m.addVar(vtype=GRB.BINARY) for t in range(n)}

        # Create decision variables for item positions
        X = {t: m.addVar(vtype=GRB.INTEGER) for t in range(n)}
        Y = {t: m.addVar(vtype=GRB.INTEGER) for t in range(n)}

        # Set objective function: minimize wasted space
        m.setObjective(quicksum((Wb - X[i] - Z[i] * W[i])**2 + (Hb - Y[i] - Z[i] * H[i])**2 for i in range(n)), GRB.MINIMIZE)

        # Constraint: Each item is placed once or not at all
        EachItemPlacedOnce = {
            i: m.addConstr(quicksum(Z[i] for i in range(n)) == 1)
            for i in range(n)
        }

        # Constraint: Item placement within bin dimensions
        ItemPlacementWithinBin = {
            i: [
                m.addConstr(X[i] >= 0),
                m.addConstr(Y[i] >= 0),
                m.addConstr(X[i] + Z[i] * W[i] <= Wb),
                m.addConstr(Y[i] + Z[i] * H[i] <= Hb)
            ]
            for i in range(n)
        }

        # Constraint: Item placement and prevent overlaps (width and height)
        ItemPlacementAndNoOverlap = {
            (i, j): [
                m.addConstr(X[i] + Z[i] * W[i] <= X[j] + (1 - Z[j]) * W[j]),
                m.addConstr(X[j] + Z[j] * W[j] <= X[i] + (1 - Z[i]) * W[i]),
                m.addConstr(Y[i] + Z[i] * H[i] <= Y[j] + (1 - Z[j]) * H[j]),
                m.addConstr(Y[j] + Z[j] * H[j] <= Y[i] + (1 - Z[i]) * H[i])
            ]
            for i in range(n)
            for j in range(i + 1, n)
        }

        m.optimize()

        if m.status == GRB.OPTIMAL:

            for i in range(n):
                print(f"Item {i} (Width: {W[i]}, Height: {H[i]})")
                if Z[i].X == 1:
                    print("Item placed in the bin")
                else:
                    print("Item not placed in the bin")

            print(f"Total Wasted Space: {m.objVal}")
        else:
            print("No optimal solution found.")
