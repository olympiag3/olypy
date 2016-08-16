#!/bin/sh

# make sure we exist immediately when there's an error, for CI:
set -e

# if COVERAGE is set, use it, else python                                                                                                                     
if [ -z "$COVERAGE" ]; then COVERAGE=python; fi

echo roundtrips
echo

for f in data/g2/*
do
   [ -f $f ] && echo $f && $COVERAGE ../roundtrip.py --test $f
done

for f in data/g2/fact/*
do
   [ -f $f ] && echo $f && $COVERAGE ../roundtrip.py --test $f
done

echo PASS
exit 0

