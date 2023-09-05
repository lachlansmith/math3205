from model import Bin, Item
from preprocess import *
from parse import *

bin,items = Parser(r"C:\Users\joshu\Desktop\COMP3506\A1\math3205\data\1.json").parse_data()

preP = Preprocessor(bin,items)

preP.run()

counter = 0
print('\nincompatible items')
for item in preP.fullyIncompatible:
    print('Item: ',counter,'Attributes: ',item)
    counter += 1

print('\nlarge items')
for item in preP.largeItems:
    print('Item: ',counter,'Attributes: ',item)
    counter += 1

print('\nsmall items')
for item in preP.smallItems:
    print('Item: ',counter,'Attributes: ',item)
    counter += 1


