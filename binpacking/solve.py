from gurobipy import *

from binpacking.model import Bin, Item, Solution


class PackingSolver:
    def __init__(self, bin: Bin, items: list[Item]):
        self.bins = [bin]
        self.items = items

    @staticmethod
    def callback(model, where):
        if where == GRB.Callback.MIPSOL:
            print('hello')

    def extract(model) -> Solution:
        itemIndicesArray = []
        itemsInBinArray = []
        for b, binVariables in enumerate(model._Bins):
            area = 0.0
            itemsInBin = []
            itemIndices = []
            for i, x in enumerate(model._VarsX[b]):
                xVal = x.x
                if xVal < 0.5:
                    continue

                item = model._Items[i]

                area += item.Weight
                itemsInBin.append(item)
                itemIndices.append(i)

            itemIndices.sort()

            if area > model._Bins[b].WeightLimit:
                raise ValueError('Capacity constraints violated')

            itemIndicesArray.append(itemIndices)
            itemsInBinArray.append(itemsInBin)

        return itemIndicesArray, itemsInBinArray

    def solve(self) -> Solution:

        sol = Solution()

        B = range(len(self.bins))
        T = range(len(self.items))

        model = Model()

        X = {(b, t): model.addVar(vtype=GRB.BINARY) for b in B for t in T}
        Y = {b: model.addVar(vtype=GRB.BINARY) for b in B}

        for t in T:
            model.addConstr(quicksum(X[b, t] for b in B) == 1)

        for b in B:
            model.addConstr(quicksum(self.items[t].area * X[b, t] for t in T) <= self.bins[b].area * Y[b])

        model.optimize(self.callback)

        return sol
