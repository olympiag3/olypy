'''
Round-trip Olympia files, to test reading and writing
'''

import sys
import argparse
from contextlib import redirect_stdout
from io import StringIO

from formatters import write_oly_file, read_oly_file, write_player

parser = argparse.ArgumentParser(description='roundtrip Olympia files')
parser.add_argument('--test', action='store_true')
parser.add_argument('--player', action='store_true')
parser.add_argument('inputfile', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Olympia file to be read')
parser.add_argument('outputfile', nargs='?', default=sys.stdout, type=argparse.FileType('w'), help='the file where output is written')

args = parser.parse_args()

if args.test:
    lines = [line for line in args.inputfile]
    data = read_oly_file(lines)
    in_string = ''.join(lines)

    out_string = StringIO()

    with redirect_stdout(out_string):
        if args.player:
            box, _ = in_string.split(' ', maxsplit=1)
            write_player(data, box)
        else:
            write_oly_file(data)

    out_string = out_string.getvalue()

    if in_string == out_string:
        exit(0)
    else:
        exit(1)

# note - does not handle the order of player files!
data = read_oly_file(args.inputfile)
write_oly_file(data)
args.outputfile.close()


