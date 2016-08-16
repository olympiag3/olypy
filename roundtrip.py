'''
Round-trip Olympia files, to test reading and writing
'''

import sys
import argparse
from contextlib import redirect_stdout
from io import StringIO

from formatters import write_oly_file, read_oly_file

parser = argparse.ArgumentParser(description='roundtrip Olympia files')
parser.add_argument('--test', action='store_true')
parser.add_argument('inputfile', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Olympia file to be read')
parser.add_argument('outputfile', nargs='?', default=sys.stdout, type=argparse.FileType('w'), help='the file where output is written')

args = parser.parse_args()

if args.test:
    lines = [line for line in args.inputfile]
    data, orig_order = read_oly_file(lines)
    in_string = ''.join(lines)

    out_string = StringIO()
    with redirect_stdout(out_string):
        write_oly_file(data, orig_order)
    out_string = out_string.getvalue()

    if in_string == out_string:
        exit(0)
    else:
        exit(1)

data, orig_order = read_oly_file(args.inputfile)
write_oly_file(data, orig_order)
args.outputfile.close()


