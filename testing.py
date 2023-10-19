import argparse
import math
import sys
import time
from binpacking import *
import matplotlib.pyplot as plt
import numpy as np



results = []
skip_instances = [11,12,13,18]



for instance in range(18,20+1):
    print(instance)
    if instance in skip_instances:
        print('skipped')
        continue
    width, height, items = parse_data(instance)

    solver = Solver(width, height, items)
    preprocessor = Preprocessor(solver)

    solver.model.setParam('seed', 0)
    solver.model.setParam('MIPGAP', 0)

    pre = time.time()

    # Heuristic 
    
    ub, indices = heuristic.firstFitDecreasing(width, height, items)

    if solver.lb == ub:
        delta = time.time() - pre
        results.append((f'instance: {instance}, Items: {len(items)}', delta, 'Heuristic Solution'))
        print(f'done: {delta}')
        continue

    solver.ub = ub

    preprocessor.assignIncompatibleIndices()
    preprocessor.assignLargeItemIndices()
    preprocessor.assignConflictIndices()

    indices = solver.solve()
    delta = time.time() - pre
    results.append((f'instance: {instance}, Items: {len(items)}', delta, 'MIP Solution'))
    print(f'done: {delta}')

print(results) 
 

# print(f'Preprocessed Mean: {sum(preprocessedDelta)/len(preprocessedDelta)}')
# print(f'NonPreprocessed Mean: {sum(nonPreprocessedDelta)/len(nonPreprocessedDelta)}')
# print(f'Preproceed Times {preprocessedDelta}')
# print(f'Raw Times {nonPreprocessedDelta}')
# plt.scatter([i for i in range(1,len(preprocessedDelta)+1)],preprocessedDelta,
#              marker ='o', color = 'blue', label = 'preProcessed')
# plt.scatter([i for i in range(1,len(nonPreprocessedDelta)+1)], nonPreprocessedDelta, 
#              marker ='o', color = 'black', label = 'Not preProcessed')
# plt.legend(['pre-processed','raw'])
# plt.ylabel('Solving time(s)')
# ax = plt.gca()
# ax.get_xaxis().set_visible(False)
# plt.title(f'Times for {len(preprocessedDelta)} BPP with {20} items with and without preprocessing')
# plt.show()