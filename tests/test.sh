#!/bin/sh

# make sure we exist immediately when there's an error, for CI:
set -e

# if COVERAGE is set, use it, else python                                                                                                                     
if [ -z "$COVERAGE" ]; then COVERAGE=python; fi

echo roundtrips
echo

for f in data/g2/*
do
   [ -f $f ] && echo $f && $COVERAGE ../scripts/roundtriplib --test $f
done

for f in data/g2/fact/*
do
   [ -f $f ] && echo $f && $COVERAGE ../scripts/roundtriplib --test --player $f
done

echo
echo copylib
echo

rm -rf data/test-temporary
mkdir data/test-temporary
mkdir data/test-temporary/fact

$COVERAGE ../scripts/copylib --problems 81 data/g2 data/test-temporary

diff -r -q data/g2 data/test-temporary
rm -rf data/test-temporary

echo

echo PASS
exit 0

