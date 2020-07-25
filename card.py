from egiftcard import get_card
from tabulate import tabulate
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("file")
parser.add_argument("-f", "--full", help="output all information", action="store_true")

args = parser.parse_args()

with open(args.file) as f:
    lines = f.read().splitlines()

if args.full:
  x = tabulate(sorted([get_card(line) for line in lines]))
else:
  x = tabulate([get_card(line)[2:] for line in lines])
print(x)