import argparse
import math
import sys
import time
from binpacking import *


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

    if args.preprocess:
        print(f'\n{OKGREEN}Begin preprocess{ENDC}\n')

        preprocessor = Preprocessor(solver)

        # removes fully incompatible items and creates filtered item list (combination of large + small items)
        preprocessor.assignIncompatibleIndices()
        print(f'Incompatible items: {solver.incompatible_indices}')

        # fixes large items to their own bin
        preprocessor.assignLargeItemIndices()
        print(f'Large items: {solver.large_item_indices}')

        # fixes large items to their own bin
        preprocessor.assignLessThanLowerBoundIndices()
        print(f'Less than lower bound items: {solver.less_than_lower_bound_indices}')

        preprocessor.assignConflictIndices()
        print(f'Conflicting items: {solver.conflict_indices}')

    print(f'\nLower bound: {solver.lb}')
    print(f'Upper bound: {solver.ub}')

    print(f'Number of items: {len(solver.items)}')

    print(f'\n{OKGREEN}Begin solve{ENDC}\n')
    pre = time.time()

    indices = solver.solve()

    print(f'\n{OKGREEN}Done{ENDC}\n')

    print(f'Elapsed time: {time.time()-pre}')

    print('Found solution')
    print(f'Indexes: {indices}\n')

    print(f'Extracting solution')

    solution = Solver.extract(solver.model)

    for i, bin_dct in enumerate(solution):
        print(f'Bin: {i} Items: {bin_dct}')
    # print(f'Solution: {solution}\n')

    if args.plot == "box":
        print(f'Plotting solution')
        plot_box(width, height, solution, items, solver.incompatible_indices, args.instance)

    if args.plot == "grid":
        print(f'Plotting solution')
        plot_grid(width, height, solution, items, solver.incompatible_indices, args.instance)
