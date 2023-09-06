from binpacking.model import Bin, Item
from binpacking.preprocess import *
from binpacking.parse import *
from itertools import combinations


# sample_list = ['a', 'b', 'c']
# list_combinations = list()
# for n in range(len(sample_list) + 1):
#     list_combinations += list(combinations(sample_list, n))

# print(list_combinations)

parser = Parser(r"C:\Users\joshu\OneDrive\Desktop\MATH3205\Project\math3205\data\1.json")
bin, items = parser.parse_data()

preP = Preprocessor(bin,items)

preP.minimizeBins()



# counter = 0
# print('\nincompatible items')
# for item in preP.fullyIncompatible:
#     print('Item: ',counter,'Attributes: ',item)
#     counter += 1

# print('\nlarge items')
# for item in preP.largeItems:
#     print('Item: ',counter,'Attributes: ',item)
#     counter += 1

# print('\nsmall items')
# for item in preP.smallItems:
#     print('Item: ',counter,'Attributes: ',item)
#     counter += 1







