import sys
import olymap


libdir = ''
outdir = ''
if len(sys.argv) > 1:
    libdir = sys.argv[1]
    if len(sys.argv) > 2:
        outdir = sys.argv[2]
olymap.make_map(libdir, outdir)
