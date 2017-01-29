#!/usr/bin/env python

import sys

from olypy.oid import to_oid, to_int

for oid in sys.argv[1:]:
    if oid.isdigit():
        oidint = int(oid)
    else:
        oidint = to_int(oid)
    print('{}: {}'.format(to_oid(oidint), oidint))
