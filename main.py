

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


def plot_solution(sol: bpp.Solution, mode: str):
    plt = bpp.SolutionPlotter(sol)

    if mode == 'interactive':
        plt.interactive_plot()

    if mode == 'grid':
        plt.grid_plot()


def export_solution(sol: bpp.Solution, format: str):
    exp = bpp.SolutionExporter(sol)

    if format == 'json':
        json = exp.json()

    if format == 'pdf':
        pdf = exp.pdf()


if __name__ == "__main__":
    args = parse_args()

    bin, items = create_problem(args.file_path)

    solver = bpp.PackingSolver(bin, items)
    sol = solver.solve()

    print(solver.elapsed_time)

    if args.plot:
        plot_solution(sol, args.plot)

    if args.export:
        export_solution(sol, args.export)
