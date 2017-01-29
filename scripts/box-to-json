'''
Given a file of Olympia boxes, or a directory containing a complete
Olympia game database, read it, and output a specified box (or the
whole thing) as JSON.
'''

import sys
import os
import json

import olypy.formatters as formatters
import olypy.oio as oio

if len(sys.argv) > 1:
    filename = sys.argv[1]
if len(sys.argv) > 2:
    box = sys.argv[2]
else:
    box = None

data = {}

if os.path.isdir(filename):
    data = oio.read_lib(filename)
else:
    data = formatters.read_oly_file(filename)

if box is not None:
    data = data[box]

print(json.dumps(data))
