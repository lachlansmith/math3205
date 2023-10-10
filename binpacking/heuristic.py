
from binpacking.model import Item


def firstFitDecreasing(width: int, items: list[Item]):
    """
    Finds a upperbound for the number of bins
    Excludes the removed items
    """

    bin_space = [width]
    bins = [[]]
    for item in items:
        placed = False
        for j, bin in enumerate(bins):
            if item.width <= bin_space[j]:
                bin_space[j] -= item.width
                bin.append(item.index)

                placed = True
                break

        if not placed:
            bin_space.append(width - item.width)
            bins.append([item.index])

    return len(bins), bins
