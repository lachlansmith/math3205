import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from binpacking.model import Bin, Item


def plot_solution(width: int, height: int, sol: list[Bin], items: list[Item]):
    """[ { 5: (0,0), 17: (0,7) }, {} ] -> [ [ (0,0), (10,7), #FF0000 ], [ (0,7), (10,3), #00FF00] ]"""

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Bin width * number of bins used in the solution
    xlim = height*len(sol)

    ax.set_xlim((0, xlim))
    ax.set_ylim((0, height))
    ax.set_aspect('equal')
    plt.xticks(np.arange(0,xlim,2))

    for j,bin in enumerate(sol):
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
            fontsize=6, ha='center', va='center')
            
    plt.show()