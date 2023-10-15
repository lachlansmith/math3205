import argparse
import math
import sys
import time
from binpacking import *
import binpacking.heuristic as heuristic


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "-i", "--instance",
        help="File name of train/valid data",
        default=1,
        type=int
    )

    parser.add_argument(
        "-p", "--preprocess",
        help="Preprocess the data",
        action="store_true"
    )

    parser.add_argument(
        "-h", "--heuristic",
        help="Plot the solutions",
        action="store_true"
    )

    parser.add_argument(
        "-v", "--verbose",
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
        const="grid"
    )

    return parser.parse_args()


def plot(args, width, height, items, solution):

    if args.plot == "box":
        plot_box(args.instance, width, height, solution, items)

    if args.plot == "grid":
        plot_grid(args.instance, width, height, solution, items)


if __name__ == "__main__":
    args = parse_args()

    parser = Parser()
    width, height, items = parser.parse_data(args.instance)
    solver = Solver(width, height, items, verbose=args.verbose)

    print(f'\n\n{BOLD}Instance {args.instance}{ENDC}\n')

    print(f'\nBin: {(width, height)}')
    dimensions = {i: (item.width, item.height) for i, item in enumerate(items)}
    print(f'Items: {dimensions}\n')

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

    print(f'{BOLD}# of items: {len(solver.items)}{ENDC}\n')

    if args.heuristic:
        print(f'{BOLD}{OKGREEN}Heuristic{ENDC}\n')

        ub, indices = heuristic.firstFitDecreasing(width, height, items)

        print(f'Heuristic solution: {indices}\n')
        print(f'{BOLD}# bins used: {len(indices)}{ENDC}\n')

        if solver.lb == ub:
            solution = Solver.extract(width, height, items, indices)

            print('Solution optimal\n')

            print(f'Extracting heuristic solution')
            for i, bin_dct in enumerate(solution):
                print(f'Bin: {i} Items: {bin_dct}')

            print()

            if args.plot:
                print(f'Plotting heuristic solution')
                plot(args, width, height, items, solution)

            quit()

        else:
            print('Solution non-optimal\n')
            solver.ub = ub

    if args.preprocess:
        print(f'{BOLD}{OKGREEN}Preprocess{ENDC}\n')

        preprocessor = Preprocessor(solver)
        preprocessor.run()

        # assigns incompatible items so that the solver ignores them
        preprocessor.assignIncompatibleIndices()
        print(f'Incompatible indices: {solver.incompatible_indices}\n')

        # fixes large items to their own bin
        preprocessor.assignLargeItemIndices()
        print(f'Large indices: {solver.large_item_indices}\n')

        # prevents conflicting items from ever being assigned to the same bin
        preprocessor.assignConflictIndices()
        print(f'Conflicting indices: {solver.conflict_indices}\n')

    print(f'{BOLD}{OKGREEN}Solve{ENDC}\n')

    print(f'Lower bound: {solver.lb}')
    print(f'Upper bound: {solver.ub}\n')

    pre = time.time()

    indices = solver.solve()

    print(f'\n{BOLD}{OKGREEN}Done{ENDC}\n')

    print(f'Elapsed time: {round(time.time() - pre, 3)} seconds\n')

    solution = Solver.extract(width, height, items, indices)

    print(f'Solver solution: {indices}\n')
    print(f'{BOLD}# bins used: {len(indices)}{ENDC}\n')

    print(f'Extracting solver solution')

    for i, bin_dct in enumerate(solution):
        print(f'Bin: {i} Items: {bin_dct}')

    print()

    if args.plot:
        print(f'Plotting solver solution')
        plot(args, width, height, items, solution)
