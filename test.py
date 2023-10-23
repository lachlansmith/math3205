import time
import multiprocessing
import os
import signal
from binpacking import *
import binpacking.heuristic as heuristic

# difficult = [27, 33, 37, 41, 43, 44, 46, 61, 63, 64, 68, 71, 72]

# the 60s / 70s are failing to start (maybe todo with defining constraints?)


def run(instance):

    width, height, items = parse_data(instance)
    solver = Solver(width, height, items, verbose=2)

    print(f'\n\n{BOLD}Instance {instance}{ENDC}\n')

    pre = time.time()

    ub, indices = heuristic.firstFitDecreasing(width, height, items)

    if solver.lb == ub:

        print(f'\nElapsed time: {time.time() - pre} seconds\n')
        solution = Solver.extract(width, height, items, indices)

        with open(f'./Solutions/{instance}.json', 'w') as fp:
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

    with open(f'./Solutions/{instance}.json', 'w') as fp:
        json.dump(solution, fp)


if __name__ == "__main__":

    difficult = []

    with open(f'./Solutions/difficult.json', 'r') as fp:
        difficult = json.loads(fp.read())

    for instance in range(501):

        if os.path.isfile(f'./Solutions/{instance}.json') or instance in difficult:
            continue

        p = multiprocessing.Process(target=run, args=[instance])
        p.start()

        p.join(120)

        if p.is_alive():
            p.kill()

            p.join()

            difficult.append(instance)
            with open(f'./Solutions/difficult.json', 'w') as fp:
                json.dump(difficult, fp)
