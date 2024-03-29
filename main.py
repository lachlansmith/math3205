import time
from binpacking import *
import binpacking.heuristic as heuristic


if __name__ == "__main__":
    args = parse_args()

    width, height, items = parse_data(args.instance)
    solver = Solver(width, height, items, verbose=int(args.verbose))

    solver.model.setParam('seed', 0)
    solver.model.setParam('MIPGAP', 0)

    # configure the subproblem
    if args.subproblem[0] == '1':
        subproblem.UseHeuristic = True
    else:
        subproblem.UseHeuristic = False

    if args.subproblem[1] == '1':
        subproblem.MinimizeBins = True
    else:
        subproblem.MinimizeBins = False

    if args.subproblem[2] == '1':
        subproblem.UseORTools = True
    else:
        subproblem.UseORTools = False

    def debug(str):
        if int(args.verbose) > 0:
            print(str)

    print(f'\n\n{BOLD}Instance {args.instance}{ENDC}\n')

    debug(f'\nBin: {(width, height)}')
    dimensions = {i: (item.width, item.height) for i, item in enumerate(items)}
    debug(f'Items: {dimensions}\n')

    debug(f'{BOLD}# of items: {len(solver.items)}{ENDC}')

    pre = time.time()

    if args.heuristic:
        debug(f'\n{BOLD}{OKGREEN}Heuristic{ENDC}')

        ub, indices = heuristic.firstFitDecreasing(width, height, items)

        if solver.lb != ub:
            debug(f'\nHeuristic solution: {indices}\n')
            debug(f'{BOLD}# bins used: {len(indices)}{ENDC}')

            debug('\nSolution non-optimal')
            solver.ub = ub
        else:
            print(f'\nHeuristic solution: {indices}\n')
            print(f'{BOLD}# bins used: {len(indices)}{ENDC}')

            debug('\nSolution optimal')

        if solver.lb == ub or args.plot == 'heuristic':
            print(f'\nElapsed time: {time.time() - pre} seconds\n')
            if args.extract or args.plot:
                solution = Solver.extract(width, height, items, indices)

                print(f'Extracting heuristic solution')
                for i, bin_dct in enumerate(solution):
                    print(f'Bin: {i} Items: {bin_dct}')

                print()

                if args.plot:
                    print(f'Plotting heuristic solution')
                    plot_box(args.instance, solution, width, height, items)

                if args.extract:
                    with open(f'./Solutions/{args.instance}.json', 'w') as fp:
                        json.dump(solution, fp)

            quit()

    if args.preprocess:
        debug(f'\n{BOLD}{OKGREEN}Preprocess{ENDC}')

        preprocessor = Preprocessor(solver)
        preprocessor.run()

        def assign(position):
            return args.preprocess == 'all' or (len(args.preprocess) > position and bool(int(args.preprocess[position])))

        # assigns incompatible items so that the solver ignores them
        if assign(0):
            preprocessor.assignIncompatibleIndices()
            debug(f'\nIncompatible indices: {solver.incompatible_indices}')

        # fixes large items to their own bin
        if assign(1):
            preprocessor.assignLargeItemIndices()
            debug(f'\nLarge indices: {solver.large_item_indices}')

        # prevents conflicting items from ever being assigned to the same bin
        if assign(2):
            preprocessor.assignConflictIndices()
            debug(f'\nConflicting indices: {solver.conflict_indices}')

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

        if args.extract:
            with open(f'./Solutions/{args.instance}.json', 'w') as fp:
                json.dump(solution, fp)
