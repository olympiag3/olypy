'''
Given a set of turn reports, build a game database.

Strategy:

* Group turns by turns

* Moving from past to present, generate location data up to N-1
* Generate full data from last turn only
* In-progress orders

* Harder 1
* Think about hidden locations and routes?
* Parse characters as I go, move and mutate them

* Harder 2
* location data from visions/scrys - pre-day-31 stuff
* tradegoods in visions/scrys - confusing compared to day 31

* Harder 3 - global knowledge
** garrison hidden inventory
** scroll / potion types
** dead bodies / dead body location
** priestly state, visions done and prep
'''

import sys
import os
import re
import time

import turnparser
import oio
import dbck

filelist = sys.argv[1:]
turn_files = {}

os.makedirs('lib/fact', exist_ok=False)
os.makedirs('lib/spool', exist_ok=False)
os.makedirs('lib/orders', exist_ok=False)

for f in filelist:
    m = re.search('(\d{2,})', f)
    if not m:
        raise ValueError('Cannot parse turn number out of file '+f)
    t = m.groups(1)[0]
    tf = turn_files.get(t, [])
    tf.append(f)
    turn_files[t] = tf

sorted_turns = sorted(list(turn_files.keys()))
last_turn = sorted_turns[-1]
print('Last turn is:', last_turn)
data = {}

turnparser.create_garrison_player(data)
turnparser.create_independent_player(data)

for t in sorted_turns:
    if t == last_turn:
        everything = True
    else:
        everything = False

    for f in turn_files[t]:
        contents = ''
        print('\nprocessing', f, '\n')
        with open(os.path.expanduser(f), 'r') as fd:
            for line in fd:
                contents += line.expandtabs()
        turnparser.parse_turn(contents, data, everything=everything)

turnparser.resolve_characters(data, last_turn)
turnparser.resolve_garrisons(data)

c0 = time.clock()
turnparser.resolve_fake_items(data)
print('resolve fake items took {} seconds'.format(time.clock() - c0))
turnparser.resolve_bound_storms(data)

c0 = time.clock()
turnparser.resolve_regions(data)
print('resolve regions took {} seconds'.format(time.clock() - c0))

c0 = time.clock()
problems = dbck.check_db(data)
print('Database check found {} problems'.format(problems))
print('Check took {} seconds'.format(time.clock() - c0))

oio.write_lib(data, 'lib')

# subprocess module introduced in 3.5, so don't use it yet
tar = 'tar cjf lib.{}.tar.bz2 lib'.format(last_turn)
ret = os.system(tar)

if ret != 0:
    raise ValueError('{} exited with error value {}'.format(tar, ret))
