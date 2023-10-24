import json
import argparse

from binpacking.model import Item


def parse_data(instance) -> tuple[int, int, list[Item]]:

    with open(f'./data/{instance}.json', 'r') as file:
        data = json.loads(file.read())

    bin = data['Objects'][0]
    W = int(bin['Length'])
    H = int(bin['Height'])

    items = []
    _items = []
    index = 0
    for item in data['Items']:
        for _ in range(0, int(item['Demand'])):
            width = int(item['Length'])
            height = int(item['Height'])

            _items.append(Item(index, width, height))
            index += 1

    _items.sort(key=lambda item: item.area, reverse=True)
    index = 0
    for item in _items:
        items.append(Item(index, item.width, item.height))
        index += 1

    return W, H, items


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
        "-s", "--subproblem",
        help="Plot the solutions",
        nargs="?",
        default="110",
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
        "--plot",
        help="Plot the solutions",
        nargs="?",
        default=None,
        const="grid"
    )

    return parser.parse_args()
