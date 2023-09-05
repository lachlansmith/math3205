

from binpacking.model import Bin, Item


class Preprocessor:
    def __init__(self, bin: Item, items: list[Item]):
        self.bins = []
        self.items = items
        self.Width = bin.width
        self.Height = bin.height

        self.incompatibleItems = set()
        

        self.RemovedItems = []
        self.FixItemToBin = []
        self.BinDomains = []

        self.processedItems = []

    def DetermineConflicts(self,items,W,H):
        """
        Finds all incompatible pairs in given item list according to the provide bin W and H
        and updates incompatible pairs set.
        """
        
        for i, itemI in enumerate(items):
            for j, itemJ in enumerate(self.items[i+1:]):
                if itemI.width + itemJ.width > W and itemI.height + itemJ.height > H:
                    self.IncompatibleItems.add(frozenset((i, j)))


    def RemoveLargeItems(self, items, H, W):
        """
        Finds and removes large items.
        Returns a list of remaining 'small' items
        """
        filteredItemIndices = []
        #checking each item
        for i, item in enumerate(items):
            w = item.width
            h = item.height

            #removes items with the same size of the bin
            if w == W and h == H:
                self.RemovedItems.append(Item(i, w, h))
                continue
            
            isFullyIncompatible = True #true until proven otherwise

            #checks pairs of items
            for j, itemJ in enumerate(items):
                if i == j:
                    continue
                
                #if true then pair is incompatible
                if w + itemJ.width > W and h + itemJ.height > H:
                    continue

                isFullyIncompatible = False
                break
                
            #removes the item if it is incompatible with all others (i.e. a large item)
            if isFullyIncompatible:
                self.RemovedItems.append(Item(w, h))
                continue

            filteredItemIndices.append(i)

        newItems = []
        for i in filteredItemIndices:
            newItems.append(Item(items[i].width, items[i].height))

        return newItems
        

    def run(self) -> tuple[list[Bin], list[Item]]:
        """
        Here we need to strip out any items that are too big for the bin, and assign items
        more than half the area of the bin to their own bin.
        """
        
        

        #shrinking bins
        #first find the largest W* s.t. W* = max(z=sum())




        #Creates own bin for items with widths or heights >= 1/2 * W
        # for item in self.items:
        #     if item.width >= self.Width/2: 
        #         new_bin = Bin(self.Width,self.Height) 
        #         new_bin.add(0,0,item.width,item.height) #adds large item to new bin
        #         self.bins.append(new_bin)
        #     elif item.height >= self.Height/2:
        #         new_bin = Bin



        return self.bins, self.items
