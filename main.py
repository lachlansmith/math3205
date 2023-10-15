import time
from binpacking import *
import binpacking.heuristic as heuristic


if __name__ == "__main__":
    args = parse_args()

    width, height, items = parse_data(args.instance)
    solver = Solver(width, height, items, verbose=int(args.verbose))

    def debug(str):
        if int(args.verbose) > 0:
            print(str)

    print(f'\n\n{BOLD}Instance {args.instance}{ENDC}\n')

    debug(f'\nBin: {(width, height)}')
    dimensions = {i: (item.width, item.height) for i, item in enumerate(items)}
    debug(f'Items: {dimensions}\n')

    debug(f'{BOLD}# of items: {len(solver.items)}{ENDC}')

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
        debug(f'\n{BOLD}{OKGREEN}Heuristic{ENDC}')

        ub, indices = heuristic.firstFitDecreasing(width, height, items)

        print(f'\nHeuristic solution: {indices}\n')
        print(f'{BOLD}# bins used: {len(indices)}{ENDC}')

        if solver.lb != ub:
            debug('\nSolution non-optimal')
            solver.ub = ub
        else:
            debug('\nSolution optimal')

        if solver.lb == ub or args.plot == 'heuristic':
            print(f'\nElapsed time: {time.time() - pre} seconds')
            if args.extract or args.plot:
                solution = Solver.extract(width, height, items, indices)

                print(f'\nExtracting heuristic solution')
                for i, bin_dct in enumerate(solution):
                    print(f'Bin: {i} Items: {bin_dct}')

                print()

                if args.plot:
                    print(f'Plotting heuristic solution')
                    plot_box(args.instance, solution, width, height, items)

            quit()

    if args.preprocess:
        debug(f'\n{BOLD}{OKGREEN}Preprocess{ENDC}\n')

        preprocessor = Preprocessor(solver)
        preprocessor.run()

        if args.preprocess == 'all':
            preprocessor.assignIndices()
        else:
            def assign(position):
                return len(args.preprocess) > position and bool(int(args.preprocess[position]))

            # assigns incompatible items so that the solver ignores them
            if assign(0):
                preprocessor.assignIncompatibleIndices()

            # fixes large items to their own bin
            if assign(1):
                preprocessor.assignLargeItemIndices()

            # prevents conflicting items from ever being assigned to the same bin
            if assign(2):
                preprocessor.assignConflictIndices()

        debug(f'Incompatible indices: {solver.incompatible_indices}\n')
        debug(f'Large indices: {solver.large_item_indices}\n')
        debug(f'Conflicting indices: {solver.conflict_indices}')

    debug(f'\n{BOLD}{OKGREEN}Solve{ENDC}\n')

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
