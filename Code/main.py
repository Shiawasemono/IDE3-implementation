import argparse
import DecisionTreeID
from anytree import Node, RenderTree

parser = argparse.ArgumentParser(description='ID3 Tree implementation')
parser.add_argument('input_filename', type = str, nargs = 1, help = 'Input CSV filename')
args = parser.parse_args()

input_filename = args.input_filename[0]

tree = DecisionTreeID.DecisionTreeID(input_filename)