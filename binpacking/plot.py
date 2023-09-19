from typing import Dict

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from binpacking.model import Item


def plot_solution(width: int, height: int, sol: list[Dict[int, tuple[int, int]]], items: list[Item]):

    # Bin width * number of bins used in the solution
    xlim = width*len(sol)

    # scaling plot display size
    fig = plt.figure(figsize=(xlim/6, height/2))
    ax = fig.add_subplot(111)

    ax.set_xlim((0, xlim))
    ax.set_ylim((0, height))
    ax.set_aspect('equal')


    xtick_locations = np.arange(0, xlim + 1, 5)
    bin_labels = [f"Bin {i+1}" for i in range(len(sol))]
    xtick_labels = []

    for i in range(0, len(sol)*2 - 1, 2):
        xtick_labels.append(str(xtick_locations[i]))
        xtick_labels.append(f"{xtick_locations[i+1]} \n {bin_labels[int(i/2)]}")
    # adding bin labels
    xtick_labels.append(str(xtick_locations[-1]))

    plt.xticks(xtick_locations, xtick_labels)
    plt.yticks(np.arange(0, height + 1, 2))
    plt.title("Instance ... Bins")

    for j, bin in enumerate(sol):
        rect = list(bin.items())
        for i in range(len(rect)):
            index = rect[i][0]
            x1, y1 = rect[i][1][0] + 10*j, rect[i][1][1]
            x2, y2 = x1 + items[index].width, y1 + items[index].height

            color = matplotlib.colors.to_hex(
                [1.0 - (x2 - x1) / width, 1.0 - (y2 - y1) /
                 height, 1.0])

            rectPlot = matplotlib.patches.Rectangle((x1, y1), x2 - x1, y2 - y1, color=color)
            ax.add_patch(rectPlot)
            ax.annotate(index, (x1 + ((x2 - x1) / 2.0), y1 + ((y2 - y1) / 2.0)), color='w', weight='bold',
                        fontsize=10, ha='center', va='center')

    plt.show()