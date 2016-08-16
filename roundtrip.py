'''
Round-trip Olympia files, to test reading and writing
'''

import sys
import argparse
from formatters import write_oly_file, read_oly_file

parser = argparse.ArgumentParser(description='roundtrip Olympia files')
#parser.add_argument('--config', action='append')
parser.add_argument('inputfile', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Olympia file to be read')
parser.add_argument('outputfile', nargs='?', default=sys.stdout, type=argparse.FileType('w'), help='the file where output is written')

args = parser.parse_args()

data = read_oly_file(args.inputfile)
write_oly_file(data)

args.outputfile.close()


