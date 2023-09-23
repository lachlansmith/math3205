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
        "--plotbox",
        help="Plot the solutions",
        action="store_true"
    )

    parser.add_argument(
        "--plotgrid",
        help="Plot the solutions",
        action="store_true"
    )

    parser.add_argument(
        "--export",
        help="Export solution to either json or pdf",
        type=str
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

    if args.preprocess:
        print(f'\n{OKGREEN}Begin preprocess{ENDC}\n')

        preprocessor = Preprocessor(solver)
    
        #removes fully incompatible items and creates filtered item list (combination of large + small items)
        preprocessor.removeIncompatibleItems()
        if len(solver.incompatible_indices):
            print('Found incompatible items')
            print(f'Incompatible items: {solver.incompatible_indices}')

        # fixes large items to their own bin
        preprocessor.fixLargeItemIndices()
        if len(solver.fixed_indices):
            print('Found large items')
            print(f'Large items: {[i for indices in solver.fixed_indices for i in indices]}')

    print(f'\nLower bound: {solver.lb}')
    print(f'Upper bound: {solver.ub}')

    print(f'Number of items: {len(solver.items)}')

    print(f'\n{OKGREEN}Begin solve{ENDC}\n')

    indices = solver.solve()

    print(f'\n{OKGREEN}Done{ENDC}\n')

    print('Found solution')
    print(f'Indexes: {indices}\n')

    print(f'Extracting solution')

    pre = time.time()

    solution = Solver.extract(solver.model)

    print(f'Elapsed time: {time.time()-pre}')

    for i, bin_dct in enumerate(solution):
        print(f'Bin: {i} Items: {bin_dct}')
    # print(f'Solution: {solution}\n')

    if args.plotbox:
        print(f'Plotting solution')
        plot_box(width, height, solution, items, solver.incompatible_indices, args.instance)
    if args.plotgrid:
        print(f'Plotting solution')
        plot_grid(width, height, solution, items, solver.incompatible_indices, args.instance)

