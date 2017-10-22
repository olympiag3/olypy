import sys
import os
import pathlib

import olymap


if len(sys.argv) < 3:
    raise ValueError('usage: make-oly-map inlib outdir')

libdir = sys.argv[1]
outdir = sys.argv[2]

if not os.path.isdir(libdir):
    raise ValueError('inlib must exist and be a directory')
if not os.path.isdir(outdir):
    pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

olymap.make_map(libdir, outdir)
