import argparse


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
        help="Plot the solutions",
        nargs="?",
        default="0",
        const="1"
    )

    parser.add_argument(
        "-p", "--preprocess",
        help="Plot the solutions",
        nargs="?",
        default=None,
        const="all"
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
