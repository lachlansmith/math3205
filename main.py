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
        help="Preprocess the data",
        action="store_true"
    )

    parser.add_argument(
        "--preprocess",
        help="Preprocess the data",
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

    if args.verbose:
        print(f'{BOLD}Instance {args.instance}{ENDC}\n')

    parser = Parser(f'./data/{args.instance}.json')
    bin, items = parser.parse_data()

    if args.verbose:
        print(f'Bin: {(bin.width, bin.height)}')
        indexes = {i: (item.width, item.height) for i, item in enumerate(items)}
        print(f'Items: {indexes}')
        ub = len(items)
        lb = int(math.ceil(sum([items[t].area for t in range(ub)]) / bin.area))
        print(f'\nLower bound: {lb}')
        print(f'Upper bound: {ub}')

    if args.preprocess:
        if args.verbose:
            print(f'\n{OKGREEN}Begin preprocess{ENDC}\n')

        preprocessor = Preprocessor(bin, items)
        bins, items = preprocessor.run()

        if args.verbose:
            print(f'Allocated {len(bins)} bin{"s" if len(bins) != 1 else ""}')
            print(f'Indexes: {[bin.items for bin in bins]}')
    else:
        bins = [Bin(bin.width, bin.height)]

    if args.verbose:
        print(f'\n{OKGREEN}Begin solve{ENDC}\n')

    try:
        solver = Solver(bin.width, bin.height, bins, items)
        sol = solver.solve()
    except NonOptimalException as e:
        print(e)
        sys.exit()

    if args.verbose:
        print('Found solution')
        print(f'Indexes: {[bin.items for bin in sol]}')

    if args.plot:
        plot_solution(sol)
