import argparse
import math
import sys
import time
from binpacking import *
import matplotlib.pyplot as plt
import numpy as np
import stopit
import pandas as pd

results = []
skip_instances = [11,17,13,18]

 

for instance in range(1,20+1):
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
    with stopit.ThreadingTimeout(120) as to_ctx_mgr: 
        assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
        indices = solver.solve()

    delta = time.time() - pre
    if to_ctx_mgr.state == to_ctx_mgr.EXECUTED:
        results.append([instance, len(items), delta, True])
    elif to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT:
        results.append([instance, len(items), delta, False])
    
    print(f'done: {delta}')


columns = ['Instance', 'Items', 'Time', 'Found Solution']

df = pd.DataFrame(results,columns = columns)
print(df)
#df.to_csv('Subproblem_Testing_ORTools.csv', index=False)
 