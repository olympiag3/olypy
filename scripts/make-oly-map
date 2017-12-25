import sys
import os
import pathlib

import olymap


if len(sys.argv) < 4:
    raise ValueError('usage: make-oly-map inlib outdir instance')

libdir = sys.argv[1]
outdir = sys.argv[2]
instance = sys.argv[3]

if not os.path.isdir(libdir):
    raise ValueError('inlib must exist and be a directory')
if not os.path.isdir(outdir):
    pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
if not instance in ['g2', 'g4', 'qa']:
    raise ValueError('instance: must be g2, g4 or qa')

olymap.make_map(libdir, outdir, instance)
