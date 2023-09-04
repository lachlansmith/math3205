

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


if __name__ == "__main__":
    args = parse_args()

    print(args)

    parser = bpp.Parser(f'./data/{args.instance}.json')
    bin, items = parser.parse_data()

    print(f'Bin')
    print(str(bin))
    print(f'Items')
    for item in items:
        print(str(item))

    preprocessor = bpp.Preprocessor(bin, items)
    bins, items = preprocessor.run()

    solver = bpp.Solver(bins, items)
    sol = solver.solve()

    if args.plot:
        bpp.plot_solution(sol)
