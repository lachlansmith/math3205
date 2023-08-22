from gurobipy import *

from binpacking.model import Bin, Item, Solution


class PackingSolver:
    def __init__(self, bin: Bin, items: list[Item]):
        self.bins = [bin]
        self.items = items

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

        model = Model()

        X = {(i, j): model.addVar(vtype=GRB.BINARY) for i in self.bins for j in self.items}
        Y = {i: model.addVar(vtype=GRB.BINARY) for i in self.bins}

        for j in self.items:
            model.addConstr(quicksum(X[i, j] for i in self.bins) == 1)

        for i in self.items:
            model.addConstr(quicksum(self.items[j].area * X[i, j] for j in self.items) <= self.bins[j].area * Y[i])

        model.optimize(self.callback)

        return self.extract(sol)
