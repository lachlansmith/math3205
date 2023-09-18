import argparse
import math
import sys
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
        "--subproblem",
        help="Attempt to solve the subproblem for each bin",
        action="store_true"
    )

    parser.add_argument(
        "--plot",
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

    solver = Solver()

    print(f'\n{BOLD}Instance {args.instance}{ENDC}\n')

    parser = Parser()
    width, height, items = parser.parse_data(args.instance)

    print(f'Bin: {(width, height)}')
    dimensions = {i: (item.width, item.height) for i, item in enumerate(items)}
    print(f'Items: {dimensions}')

    if args.preprocess:
        print(f'\n{OKGREEN}Begin preprocess{ENDC}\n')

        preprocessor = Preprocessor(solver, width, height, items)

        preprocessor.removeIncompatibleItems()
        if len(solver.incompatible_indices):
            print('Found incompatible items')
            print(f'Incompatible items: {solver.incompatible_indices}')

        preprocessor.fixLargeItemIndices()
        if len(solver.fixed_indices):
            print('Found large items')
            print(f'Large items: {[i for indices in solver.fixed_indices for i in indices]}')

    print(f'\nLower bound: {solver.lb}')
    print(f'Upper bound: {solver.ub}')

    print(f'\n{OKGREEN}Begin solve{ENDC}\n')

    indices = solver.solve(width, height, items)

    print(f'\n{OKGREEN}Done{ENDC}\n')

    print('Found solution')
    print(f'Indexes: {indices}\n')

    print(f'Extracting solution')
    solution = Solver.extract(solver.model)

    print(f'Solution: {solution}\n')

    if args.plot:
        print(f'Plotting solution')
        plot_solution(width, height, solution, items)
