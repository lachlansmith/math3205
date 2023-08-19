

import argparse
import binpacking as bpp


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file-path",
        help="File name of train/valid data",
        required=True
    )

    parser.add_argument(
        "--plot",
        help="Plot the solutions",
        action="store_false"
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


if __name__ == "__main__":

    args = parse_args()
    bin, items = create_problem(args.file_path)

    solver = bpp.PackingSolver(bin, items)

    sol = solver.solve()

    print(solver.elapsed_time)

    if args.plot:
        plt = bpp.SolutionPlotter(sol)

        if args.plot == 'interactive':
            plt.interactive_plot()

        if args.plot == 'grid':
            plt.grid_plot()

    if args.export:
        exp = bpp.SolutionExporter(sol)

        if args.export == 'json':
            json = exp.json()

        if args.export == 'pdf':
            pdf = exp.pdf()
