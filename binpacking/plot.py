import matplotlib
import matplotlib.pyplot as plt

from binpacking.model import Bin, Item


def plot_solution(self, sol: list[Bin], items: list[Item]):
    """[ { 5: (0,0), 17: (0,7) } ] -> [ [ (0,0), (10,7), #FF0000 ], [ (0,7), (10,3), #00FF00] ]"""

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_xlim((0, sol.bin.width * sol.ub))
    ax.set_ylim((0, sol.bin.height))
    ax.set_aspect('equal')

    for i, rect in enumerate(sol.items):
        x1, y1 = rect[0]
        x2, y2 = rect[1]

        color = rect[2]

        rectPlot = matplotlib.patches.Rectangle((x1, y1), x2 - x1, y2 - y1, color=color)
        ax.add_patch(rectPlot)

        ax.annotate(i, (x1 + ((x2 - x1) / 2.0), y1 + ((y2 - y1) / 2.0)), color='b', weight='bold',
                    fontsize=6, ha='center', va='center')

    plt.show()
