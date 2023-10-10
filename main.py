import argparse
import math
import sys
import time
from binpacking import *
import binpacking.heuristic as heuristic


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--instance",
        help="File name of train/valid data",
        default=1,
        type=int
    )

    parser.add_argument(
        "--preprocess",
        help="Preprocess the data",
        action="store_true"
    )

    parser.add_argument(
        "--heuristic",
        help="Plot the solutions",
        nargs="?",
        default=None,
        const="lifted"
    )

    parser.add_argument(
        "--verbose",
        help="Print gurobi output",
        action="store_true"
    )

    parser.add_argument(
        "--subproblem",
        help="Attempt to solve the subproblem for each bin",
        action="store_true"
    )

    parser.add_argument(
        "--plot",
        help="Plot the solutions",
        nargs="?",
        default=None,
        const="box"
    )

    return parser.parse_args()


def plot(args, width, height, items, solution):

    if args.plot == "box":
        plot_box(args.instance, width, height, solution, items)

    if args.plot == "grid":
        plot_grid(args.instance, width, height, solution, items)


if __name__ == "__main__":
    args = parse_args()

    print(f'{BOLD}Instance {args.instance}{ENDC}\n')

    parser = Parser()
    width, height, items = parser.parse_data(args.instance)

    print(f'Bin: {(width, height)}')
    dimensions = {i: (item.width, item.height) for i, item in enumerate(items)}
    print(f'Items: {dimensions}\n')

    solver = Solver(width, height, items, verbose=args.verbose)

    if args.subproblem:
        print(f'\n{OKGREEN}Attempting subproblem{ENDC}\n')
        subproblemSolver = SubproblemSolver(True)
        temp_bin = Bin(10, 10)
        for i in range(0, 10):
            temp_bin.items.append(items[i])

        max_item = max(temp_bin.items, key=lambda item: item.area)
        print(f'Max item {max_item}')

        # solved_dct = subproblemSolver.solve(temp_bin)
        # plot_solution(temp_bin.width,temp_bin.height,[solved_dct], items, [])
        print('done')
        quit()

    print()

    print(f'Lower bound: {solver.lb}')
    print(f'Upper bound: {solver.ub}')
    print(f'Number of items: {len(solver.items)}\n')

    if args.heuristic:
        print(f'{OKGREEN}Begin heuristic{ENDC}\n')

        ub, indices = heuristic.firstFitDecreasing(width, height, items)

        try:

            solution = Solver.extract(width, height, items, indices)

            print('Found heuristic solution')
            print(f'Indexes: {indices}\n')

            print(f'Plotting heuristic solution')
            plot(args, width, height, items, solution)

        except BadSolutionException:
            print(f'Found better upper bound: {ub}\n')
            solver.ub = ub

    if args.preprocess:
        print(f'{OKGREEN}Begin preprocess{ENDC}\n')

        preprocessor = Preprocessor(solver)

        # removes fully incompatible items and creates filtered item list (combination of large + small items)
        preprocessor.assignIncompatibleIndices()
        print(f'Incompatible indices: {solver.incompatible_indices}\n')

        # fixes large items to their own bin
        preprocessor.assignLargeItemIndices()
        print(f'Large indices: {solver.large_item_indices}\n')

        # fixes large items to their own bin
        preprocessor.assignLessThanLowerBoundIndices()
        print(f'Less than lower bound indices: {solver.less_than_lower_bound_indices}\n')

        preprocessor.assignConflictIndices()
        print(f'Conflicting indices: {solver.conflict_indices}\n')

    print(f'{OKGREEN}Begin solve{ENDC}\n')

    pre = time.time()

    indices = solver.solve()

    print(f'\n{OKGREEN}Done{ENDC}\n')

    print(f'Elapsed time: {time.time()-pre}')

    print('Found solution')
    print(f'Indexes: {indices}\n')

    print(f'Extracting solution')

    solution = Solver.extract(width, height, items, indices)

    for i, bin_dct in enumerate(solution):
        print(f'Bin: {i} Items: {bin_dct}')
    # print(f'Solution: {solution}\n')

    if args.plot:
        print(f'Plotting solution')
        plot(args, width, height, items, solution)
