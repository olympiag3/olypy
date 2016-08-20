# olypy

[![Build Status](https://travis-ci.org/olympiag3/olypy.svg?branch=master)](https://travis-ci.org/olympiag3/olypy) [![Coverage Status](https://coveralls.io/repos/github/olympiag3/olypy/badge.svg?branch=master)](https://coveralls.io/github/olympiag3/olypy?branch=master) [![Apache License 2.0](https://img.shields.io/github/license/olympiag3/olypy.svg)](LICENSE)

olypy is a collection of code related to the game Olympia, which
currently lives in SVN (yuck) at

https://sourceforge.net/projects/olympiag3/

olypy is intended to support:

* Generating a game database for testing the Olympia code
* Actual end-to-end tests of the Olympia code
* Generating a game database from turn output to support simulations for players

## Installing

Clone the repo. Note that Python 3.4+ is required; use penv if your
system Python is old.

## Generating the QA database

`make defaultlib`

## Running Olympia tests

You need a compiled Olympia binary with support for the 'assert'
command.

```
cd sim; python run-tests.py
```

Tests are YAML files. Here's an example:

```
description: test move-related things
lib: defaultlib
aa1 orders: |
 unit 1102  # A2 in Aachen [c18]
   # test movement delays
   claim 10 20
   assert item 10 20 not item 10 21 # exactly 20
   move out # 2 days
   assert day 3 not day 4
   drop 10 1
   move c18
   assert day 4 not day 5
```

