from oio import read_lib, write_lib

import sys

inputlib = sys.argv[1]
outputlib = sys.argv[2]

data = read_lib(inputlib)
write_lib(data, outputlib)
