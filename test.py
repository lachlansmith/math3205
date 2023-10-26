import time
import multiprocessing
import os
from binpacking import *
import binpacking.heuristic as heuristic


def run(instance):

    width, height, items = parse_data(instance)
    solver = Solver(width, height, items, verbose=2)

    print(f'\n\n{BOLD}Instance {instance}{ENDC}\n')

    pre = time.time()

    ub, indices = heuristic.firstFitDecreasing(width, height, items)

    if solver.lb == ub:

        print(f'\nElapsed time: {time.time() - pre} seconds\n')
        solution = Solver.extract(width, height, items, indices)

        with open(f'./solutions/{instance}.json', 'w') as fp:
            json.dump(solution, fp)

        return

    else:
        solver.ub = ub

    preprocessor = Preprocessor(solver)
    preprocessor.run()

    preprocessor.assignIncompatibleIndices()
    preprocessor.assignLargeItemIndices()
    preprocessor.assignConflictIndices()

    print(f'Lower bound: {solver.lb}')
    print(f'Upper bound: {solver.ub}\n')

    indices = solver.solve()

    solution = Solver.extract(width, height, items, indices)

    with open(f'./stats/{instance}.json', 'w') as fp:
        json.dump({
            "solves": len(solver.model._infeasible) + len(solver.model._feasible)
        }, fp)


if __name__ == "__main__":

    for instance in range(501):
        if os.path.isfile(f'./solutions/{instance}.json'):
            p = multiprocessing.Process(target=run, args=[instance])
            p.start()

            p.join(300)

            if p.is_alive():
                p.kill()

                p.join()
