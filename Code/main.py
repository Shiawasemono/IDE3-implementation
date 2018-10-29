import argparse
import DecisionTreeID
from anytree import Node, RenderTree

parser = argparse.ArgumentParser(description='ID3 Tree implementation')
parser.add_argument('input_filename', type = str, nargs = 1, help = 'Input CSV filename')
# parser.add_argument('input_record', type = str, nargs = 1, help = 'Input record filename')
args = parser.parse_args()

input_filename = args.input_filename[0]
# input_record = args.input_record[0]

tree = DecisionTreeID.DecisionTreeID(input_filename)
for pre, fill, node in RenderTree(tree):
    if 'id=' in node.name.split('\n')[1]: 
        print(len(pre))
        print("%s%s" % (pre, node.name.split('\n')[0]))
    else:
        print("%s%s" % (pre, node.name.split('\n')[0] + ' ' + node.name.split('\n')[1]))
