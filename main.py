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

    env = Env(empty=True)
    if not args.verbose:
        env.setParam("OutputFlag", 0)
    env.start()

    print(f'{BOLD}Instance {args.instance}{ENDC}\n')

    parser = Parser(f'./data/{args.instance}.json')
    bin, items = parser.parse_data()

    print(f'Bin: {(bin.width, bin.height)}')
    indexes = {i: (item.width, item.height) for i, item in enumerate(items)}
    print(f'Items: {indexes}')
    ub = len(items)
    lb = int(math.ceil(sum([items[t].area for t in range(ub)]) / bin.area))
    print(f'\nLower bound: {lb}')
    print(f'Upper bound: {ub}')

    if args.preprocess:

        print(f'\n{OKGREEN}Begin preprocess{ENDC}\n')

        preprocessor = Preprocessor(bin, items)
        bins, items = preprocessor.run()

        print(f'Allocated {len(bins)} bin{"s" if len(bins) != 1 else ""}')
        print(f'Indexes: {[bin.items for bin in bins]}')
    else:
        bins = [Bin(bin.width, bin.height)]

        print(f'\n{OKGREEN}Begin solve{ENDC}\n')

    try:
        solver = Solver(env)
        sol = solver.solve(bin.width, bin.height, bins, items,)
    except NonOptimalException as e:
        print(e)
        sys.exit()

    print('Found solution')
    print(f'Indexes: {[[item.index for item in bin.items] for bin in sol]}')

    if args.subproblem:
        # for bin in sol:
        problem = SubproblemSolver(env)
        subsol = problem.solve(sol[0])

    if args.plot:
        plot_solution(sol)
