from typing import Dict

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from binpacking.model import Item


def plot_solution(width: int, height: int, sol: list[Dict[int, tuple[int, int]]], items: list[Item], incompatible: list[Item]):
    xlim = width*len(sol)

    fig = plt.figure(figsize=(len(sol), height/len(sol)), dpi=100)
    ax = fig.add_subplot(111)

    ax.set_xlim((0, xlim))
    ax.set_ylim((0, height))
    ax.set_aspect('equal')

    plt.xticks(np.arange(0, xlim + width, width))
    plt.yticks([0, height])
    plt.title("Instance ... Bins")

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
    
    
    if not len(incompatible):
        plt.xlabel(f"Incompatible items: {' '.join(incompatible)}")
    plt.show()


def plot_grid(width: int, height: int, sol: list[Dict[int, tuple[int, int]]], items: list[Item]):
    pass


def plot_single(width: int, height: int, sol: list[Dict[int, tuple[int, int]]], items: list[Item]):

    for j, bin in enumerate(sol):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.set_aspect('equal')

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
        
        plt.title(f"Bin {j + 1}")
    plt.show()
