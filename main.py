

import argparse
import binpacking as bpp


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--instance",
        help="File name of train/valid data",
        default=1,
        type=int
    )

    parser.add_argument(
        "--plot",
        help="Plot the solutions",
        type=str,
        # default="grid"
    )

    parser.add_argument(
        "--export",
        help="Export solution to either json or pdf",
        type=str
    )

    return parser.parse_args()


def create_problem(path: str):
    data = bpp.DataParser(path)

    return data.parse_data()


def plot_solution(sol: bpp.Solution, mode: str):
    plot = bpp.SolutionPlotter(sol)

    if mode == 'grid':
        plot.grid()


if __name__ == "__main__":
    args = parse_args()

    print(args)

    bin, items = create_problem(f'./data/{args.instance}.json')

    print(f'Bin')
    print(str(bin))
    print(f'Items')
    for item in items:
        print(str(item))

    solver = bpp.PackingSolver(bin, items)
    sol = solver.solve()

    if args.plot:
        plot_solution(sol, args.plot)
