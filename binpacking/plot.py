import matplotlib
import matplotlib.pyplot as plt

from binpacking.model import Solution


class SolutionPlotter:
    def __init__(self, sol: Solution) -> None:
        self.solution = sol

    def grid(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlim((0, self.solution.bin.width))
        ax.set_ylim((0, self.solution.bin.width))
        ax.set_aspect('equal')

        for i, rect in enumerate(self.solution.items):
            bottomLeft = rect[0]
            topRight = rect[1]

            x1, y1 = bottomLeft[0], bottomLeft[1]
            x2, y2 = topRight[0], topRight[1]

            color = rect[2]

            rectPlot = matplotlib.patches.Rectangle((x1, y1), x2 - x1, y2 - y1, color=color)
            ax.add_patch(rectPlot)

            ax.annotate(i, (x1 + ((x2 - x1) / 2.0), y1 + ((y2 - y1) / 2.0)), color='b', weight='bold',
                        fontsize=6, ha='center', va='center')

        plt.show()
