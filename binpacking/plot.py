from typing import Dict

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

from binpacking.model import Item


def plot_box(instance: int, sol: list[Dict[int, tuple[int, int]]], width: int, height: int, items: list[Item]):
    xlim = width*len(sol)

    fig = plt.figure(figsize=(len(sol), height/len(sol)))
    ax = fig.add_subplot(111)

    ax.set_xlim((0, xlim))
    ax.set_ylim((0, height))
    ax.set_aspect('equal')

    plt.xticks(np.arange(0, xlim + width, width))
    plt.yticks([0, height])
    plt.title(f"Instance {instance} Bins")
    plt.grid(color="black")

    for j, bin in enumerate(sol):
        rect = list(bin.items())
        for i in range(len(rect)):
            index = rect[i][0]
            x1, y1 = rect[i][1][0] + width*j, rect[i][1][1]
            x2, y2 = x1 + items[index].width, y1 + items[index].height

            color = matplotlib.colors.to_hex(
                [1.0 - (x2 - x1) / width, 1.0 - (y2 - y1) /
                 height, 1.0])

            rectPlot = matplotlib.patches.Rectangle((x1, y1), x2 - x1, y2 - y1, color=color)
            ax.add_patch(rectPlot)
            ax.annotate(index, (x1 + ((x2 - x1) / 2.0), y1 + ((y2 - y1) / 2.0)), color='w', weight='bold',
                        fontsize=8, ha='center', va='center')

    plt.show()


def plot_grid(instance: int, sol: list[Dict[int, tuple[int, int]]], width: int, height: int, items: list[Item]):

    fig = plt.figure()
    fig.suptitle(f"Instance {instance}")

    row = int(math.ceil(len(sol)/5))
    col = int(math.ceil(len(sol)/row))

    for j, bin in enumerate(sol):
        ax = fig.add_subplot(row, col, j+1)
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.set_aspect('equal')
        plt.title(f"Bin {j+1}")

        rect = list(bin.items())
        for i in range(len(rect)):
            index = rect[i][0]
            x1, y1 = rect[i][1][0], rect[i][1][1]
            x2, y2 = x1 + items[index].width, y1 + items[index].height

            color = matplotlib.colors.to_hex(
                [1.0 - (x2 - x1) / width, 1.0 - (y2 - y1) /
                 height, 1.0])

            rectPlot = matplotlib.patches.Rectangle((x1, y1), x2 - x1, y2 - y1, color=color)
            ax.add_patch(rectPlot)
            ax.annotate(index, (x1 + ((x2 - x1) / 2.0), y1 + ((y2 - y1) / 2.0)), color='w', weight='bold',
                        fontsize=10, ha='center', va='center')

    plt.show()
