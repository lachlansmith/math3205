import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from binpacking.model import Solution


def plot_solution(sol: Solution):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    BinWidth = 10

    # Bin width * number of bins used in the solution
    xlim = BinWidth*len(sol.rectangles)

    ax.set_xlim((0, xlim))
    ax.set_ylim((0, BinWidth))
    ax.set_aspect('equal')
    plt.xticks(np.arange(0,xlim,2))

    for i in range(len(sol.rectangles)):
        for j, rect in enumerate(sol.rectangles[i]):
            bottomLeft = rect[0]
            topRight = rect[1]

            x1, y1 = bottomLeft[0] + 10*i, bottomLeft[1]
            x2, y2 = topRight[0] + 10*i, topRightp[1]

            color = rect[2]

            rectPlot = matplotlib.patches.Rectangle((x1, y1), x2 - x1, y2 - y1, color=color)
            ax.add_patch(rectPlot)
            ax.annotate(j, (x1 + ((x2 - x1) / 2.0), y1 + ((y2 - y1) / 2.0)), color='w', weight='bold',
            fontsize=6, ha='center', va='center')

    plt.show()