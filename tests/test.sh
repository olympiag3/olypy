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
   [ -f $f ] && echo $f && $COVERAGE ../roundtrip.py --test --player $f
done

echo
echo copylib
echo

rm -rf data/test-temporary
mkdir data/test-temporary
mkdir data/test-temporary/fact
$COVERAGE ../copylib.py data/g2 data/test-temporary
diff -u data/g2/system data/test-temporary/system # temporary to find my bug
diff -r -q data/g2 data/test-temporary
rm -rf data/test-temporary

echo

echo PASS
exit 0

