import argparse
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
        "-v", "--verbose",
        help="Print gurobi output",
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
        "-e", "--extract",
        help="Plot the solutions",
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


if __name__ == "__main__":
    args = parse_args()

    width, height, items = parse_data(args.instance)
    solver = Solver(width, height, items, verbose=bool(int(args.verbose) > 1))

    def debug(str):
        if int(args.verbose) > 0:
            print(str)

    print(f'\n\n{BOLD}Instance {args.instance}{ENDC}\n\n')

    debug(f'Bin: {(width, height)}')
    dimensions = {i: (item.width, item.height) for i, item in enumerate(items)}
    debug(f'Items: {dimensions}\n')

    debug(f'{BOLD}# of items: {len(solver.items)}{ENDC}\n')

    if args.subproblem:
        debug(f'\n{OKGREEN}Attempting subproblem{ENDC}\n')
        subproblemSolver = SubproblemSolver(True)
        temp_bin = Bin(10, 10)
        for i in range(0, 10):
            temp_bin.items.append(items[i])

        max_item = max(temp_bin.items, key=lambda item: item.area)
        debug(f'Max item {max_item}')

        # solved_dct = subproblemSolver.solve(temp_bin)
        # plot_solution(temp_bin.width,temp_bin.height,[solved_dct], items, [])
        debug('done')
        quit()

    pre = time.time()

    if args.heuristic:
        debug(f'{BOLD}{OKGREEN}Heuristic{ENDC}\n')

        ub, indices = heuristic.firstFitDecreasing(width, height, items)

        print(f'Heuristic solution: {indices}\n')
        print(f'{BOLD}# bins used: {len(indices)}{ENDC}\n')

        if solver.lb == ub:
            debug('Solution optimal\n')

            debug(f'Elapsed time: {time.time() - pre} seconds\n')
        else:
            debug('Solution non-optimal\n')
            solver.ub = ub

        if solver.lb == ub or args.plot == 'heuristic':
            if args.extract or args.plot:
                solution = Solver.extract(width, height, items, indices)

                print(f'Extracting heuristic solution')
                for i, bin_dct in enumerate(solution):
                    print(f'Bin: {i} Items: {bin_dct}')

                print()

                if args.plot:
                    print(f'Plotting heuristic solution')
                    plot_box(args.instance, solution, width, height, items)

            quit()

    if args.preprocess:
        debug(f'{BOLD}{OKGREEN}Preprocess{ENDC}\n')

        preprocessor = Preprocessor(solver)
        preprocessor.run()

        # assigns incompatible items so that the solver ignores them
        preprocessor.assignIncompatibleIndices()
        debug(f'Incompatible indices: {solver.incompatible_indices}\n')

        # fixes large items to their own bin
        preprocessor.assignLargeItemIndices()
        debug(f'Large indices: {solver.large_item_indices}\n')

        # prevents conflicting items from ever being assigned to the same bin
        preprocessor.assignConflictIndices()
        debug(f'Conflicting indices: {solver.conflict_indices}\n')

    debug(f'{BOLD}{OKGREEN}Solve{ENDC}\n')

    debug(f'Lower bound: {solver.lb}')
    debug(f'Upper bound: {solver.ub}\n')

    indices = solver.solve()

    debug(f'\n{BOLD}{OKGREEN}Done{ENDC}\n')

    solution = Solver.extract(width, height, items, indices)

    print(f'Solver solution: {indices}\n')
    print(f'{BOLD}# bins used: {len(indices)}{ENDC}\n')

    print(f'Elapsed time: {time.time() - pre} seconds\n')

    if args.extract or args.plot:
        print(f'Extracting solver solution')

        for i, bin_dct in enumerate(solution):
            print(f'Bin: {i} Items: {bin_dct}')

        print()

        if args.plot:
            print(f'Plotting solver solution')

            if args.plot == "box":
                plot_box(args.instance, solution, width, height, items)

            if args.plot == "grid":
                plot_grid(args.instance, solution, width, height, items)
