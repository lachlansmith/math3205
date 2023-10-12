from typing import Dict

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

from binpacking.model import Item

def plot_items(items: list[Item]):


    width, height = 10, 10
    xlim = sum([item.width for item in items])

    fig = plt.figure(figsize=(sum([item.width for item in items]), height))
    ax = fig.add_subplot(111)

    plt.title(f'Items {[item.index for item in items]}')

    ax.set_xlim((0, xlim))
    ax.set_ylim((0, max([item.height for item in items])))
    ax.set_aspect('equal')

    x, y = 0, 0
    for item in items:
        index = item.index

        x1, y1 = x, 0
        x2, y2 = x1 + item.width, y1 + item.height

        color = matplotlib.colors.to_hex(
                    [1.0 - (x2 - x1) / width, 1.0 - (y2 - y1) /
                    height, 1.0])

        rectPlot = matplotlib.patches.Rectangle((x1, y1), x2 - x1, y2 - y1, color=color)
        ax.add_patch(rectPlot)
        ax.annotate(index, (x1 + ((x2 - x1) / 2.0), y1 + ((y2 - y1) / 2.0)), color='w', weight='bold',
                    fontsize=8, ha='center', va='center')
        
        x = x2
        
    plt.show()

def plot_box(instance: int, width: int, height: int, sol: list[Dict[int, tuple[int, int]]], items: list[Item], incompatible: list[Item] = []):
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

    if len(incompatible):
        plt.xlabel(f"Incompatible items: {' '.join(incompatible)}")
    plt.show()


def plot_grid(instance: int, width: int, height: int, sol: list[Dict[int, tuple[int, int]]], items: list[Item], incompatible: list[Item] = []):

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
