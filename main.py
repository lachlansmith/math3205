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
        "--verbose",
        help="Print gurobi output",
        action="store_true"
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

    print(f'{BOLD}Instance {args.instance}{ENDC}\n')

    parser = Parser(f'./data/{args.instance}.json')
    width, height, items = parser.parse_data()

    print(f'Bin: {(width, height)}')
    dimensions = {i: (item.width, item.height) for i, item in enumerate(items)}
    print(f'Items: {dimensions}')

    if args.preprocess:

        print(f'\n{OKGREEN}Begin preprocess{ENDC}\n')

        preprocessor = Preprocessor(width, height, items)
        bins, items = preprocessor.run()

        print(f'Allocated {len(bins)} bin{"s" if len(bins) != 1 else ""}')
        print(f'Indexes: {[bin.items for bin in bins]}')
    else:
        bins = [Bin(width, height)]

    ub = len(items)
    lb = int(math.ceil(sum([items[t].area for t in range(ub)]) / (width * height)))
    print(f'\nLower bound: {lb}')
    print(f'Upper bound: {ub}')

    print(f'\n{OKGREEN}Begin solve{ENDC}\n')

    solver = Solver(args.verbose)

    solver.lb = lb
    solver.ub = ub
    solver.fixed_indices = []

    indices = solver.solve(width, height, items)

    print('\nFound solution')
    print(f'Indexes: {indices}\n')

    print(f'Extracting solution')
    solution = Solver.extract(solver.model)

    print(f'Solution: {solution}\n')

    if args.plot:
        plot_solution(width, height, solution, items)
