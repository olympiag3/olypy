import sys
import argparse

from oio import read_lib, write_lib
import dbck

parser = argparse.ArgumentParser(description='copy an Olympia lib for QA purposes')
parser.add_argument('inputlib', help='input Olympia lib directory')
parser.add_argument('outputlib', help='output Olympia lib directory')
parser.add_argument('--problems', help='expected number of problems', type=int, default=0)

args = parser.parse_args()

data = read_lib(args.inputlib)

problems = dbck.check_db(data)
if problems:
    print('dbck found {} problems'.format(problems))
assert problems == args.problems

write_lib(data, args.outputlib)
