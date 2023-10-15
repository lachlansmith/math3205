
from binpacking.model import Item


def firstFitDecreasing(width: int, height: int, items: list[Item]):
    width_remaining = []
    height_remaining = []
    bins = []
    for item in items:
        
        placed = False
        for j, bin in enumerate(bins):
            if item.width <= width_remaining[j]:
                if len(bin):
                
                    if item.height <= items[bin[0]].height:
                        width_remaining[j] -= item.width
                        height_remaining[j] -= item.height
                        bin.append(item.index)

                        placed = True
                        break

            if not placed and item.height <= height_remaining[j]:
                # width_remaining[j] -= item.width
                height_remaining[j] -= item.height
                bin.append(item.index)

                placed = True
                break

        if not placed:
            width_remaining.append(width - item.width)
            height_remaining.append(height - item.height)
            bins.append([item.index])

    return len(bins), bins

def firstFitDecreasingSubProblem(width: int, height: int, items: list[Item]):
    width_remaining = []
    height_remaining = []
    bins = []
    
    for item in items:
        
        placed = False
        for j, items2 in enumerate(bins):
            if item.width <= width_remaining[j]:
                if len(items2):
                    if item.height <= items2[0].height:
                        width_remaining[j] -= item.width
                        height_remaining[j] -= item.height
                        items2.append(item)

                        placed = True
                        break

            if not placed and item.height <= height_remaining[j]:
                # width_remaining[j] -= item.width
                height_remaining[j] -= item.height
                items2.append(item)

                placed = True
                break

        if not placed:
            width_remaining.append(width - item.width)
            height_remaining.append(height - item.height)
            bins.append([item])

    return len(bins), bins
