import argparse
import math
import sys
import time
from binpacking import *
import matplotlib.pyplot as plt
import numpy as np

parser = Parser()
preprocessFlag = True
preprocessedDelta = []
nonPreprocessedDelta = []
instance = 1
width, height, items = parser.parse_data(instance)






items = [Item(0,5,5), Item(1,4,3), Item(2,1,3)]

solver = Solver(10, 10, items)
bins, indices = firstFitDecreasing(10, 10, items)
print(indices)
indices = solver.solve()
sol = Solver.extract(10,10, items, indices)
plot_grid(0, width, height, sol, items)
quit()
#plot_items(items)

solver = Solver(width, height, items) 


preprocessor = Preprocessor(solver) 
#preprocessor.incompatibleItems()
preprocessor.assignLargeItemIndices()

indices = solver.solve()
solution = Solver.extract(solver.model)
plot_grid(width, height, solution, items, solver.incompatible_indices, instance)




quit()
###This file is used for testing the 2D-bin packing model###
for instance in range(1,10+1):
    print(instance)
    width, height, items = parser.parse_data(instance)
    N = len(items)
    if N <= 20:

        #solving with preprocessing
        pre = time.time()
        solver = Solver(width, height, items)

        preprocessor = Preprocessor(solver)
        preprocessor.removeIncompatibleItems()
        preprocessor.fixLargeItemIndices()

        indices = solver.solve()
        preprocessedDelta.append(time.time() - pre)

        #solving without preprocessing
        pre = time.time()
        solver = Solver(width, height, items)

        indices = solver.solve()
        nonPreprocessedDelta.append(time.time() - pre)
      

print(f'Preprocessed Mean: {sum(preprocessedDelta)/len(preprocessedDelta)}')
print(f'NonPreprocessed Mean: {sum(nonPreprocessedDelta)/len(nonPreprocessedDelta)}')
print(f'Preproceed Times {preprocessedDelta}')
print(f'Raw Times {nonPreprocessedDelta}')
plt.scatter([i for i in range(1,len(preprocessedDelta)+1)],preprocessedDelta,
             marker ='o', color = 'blue', label = 'preProcessed')
plt.scatter([i for i in range(1,len(nonPreprocessedDelta)+1)], nonPreprocessedDelta, 
             marker ='o', color = 'black', label = 'Not preProcessed')
plt.legend(['pre-processed','raw'])
plt.ylabel('Solving time(s)')
ax = plt.gca()
ax.get_xaxis().set_visible(False)
plt.title(f'Times for {len(preprocessedDelta)} BPP with {20} items with and without preprocessing')
plt.show()