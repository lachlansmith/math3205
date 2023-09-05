from model import Bin, Item
from preprocess import *
from parse import *
from itertools import combinations

bin,items = Parser(r"C:\Users\joshu\Desktop\COMP3506\A1\math3205\data\1.json").parse_data()

preP = Preprocessor(bin,items)

preP.run()



sample_list = ['a', 'b', 'c']
list_combinations = list()
print(combinations(sample_list,len()))
for n in range(len(sample_list) + 1):
    list_combinations += list(combinations(sample_list, n))

print(list_combinations)

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





