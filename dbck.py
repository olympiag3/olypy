'''
Database checker, similar to the one in the C code (check.c)
'''
import sys

from oid import to_oid


def check_where_here(data):
    "Make sure that every box that's where is here, and here is where."
    problem = 0
    for i in data:
        if 'LI' in data[i]:
            if 'wh' in data[i]['LI']:
                where = data[i]['LI']['wh'][0]
                try:
                    hl = data[where]['LI']['hl']
                    hl.index(i)
                except KeyError:
                    print('Unit {} is not in here list of unit {}'.format(i, where), file=sys.stderr)
                    problem += 1
                    continue

    for i in data:
        if 'LI' in data[i]:
            if 'hl' in data[i]['LI']:
                hl = data[i]['LI']['hl']
                for unit in hl:
                    try:
                        where = data[unit]['LI']['wh'][0]
                        if where != i:
                            raise ValueError
                    except (KeyError, ValueError):
                        print('Unit {} is in here list of unit {}, but is not there'.format(unit, i), file=sys.stderr)
                        problem += 1
                        continue

    return problem


def check_faction_units(data):
    "If a box is in a faction, make sure it's on the faction's unit list and vice versa."
    problem = 0
    for i in data:
        if 'CH' in data[i]:
            if 'lo' in data[i]['CH']:
                fact = data[i]['CH']['lo'][0]
                try:
                    un = data[fact]['PL']['un']
                    un.index(i)
                except (KeyError, ValueError):
                    print('Unit {} is in faction {} but not vice versa'.format(i, fact), file=sys.stderr)
                    problem += 1
                    continue

    for i in data:
        if ' player ' in data[i]['firstline'][0] and 'un' in data[i]['PL']:
            for unit in data[i]['PL']['un']:
                try:
                    lo = data[unit]['CH']['lo'][0]
                    if lo != i:
                        raise ValueError
                        print('lo {} i {}'.format(lo, i), file=sys.stderr)
                except (KeyError, ValueError):
                    print('Unit {} is not in faction {}'.format(unit, i), file=sys.stderr)
                    problem += 1
                    continue

    return problem


def sweep_independent_units(data):
    '''Move any unit not in a faction to being unsworn and owned by faction 100 (independent player)'''
    return 0


def check_unique_items(data):
    "Make sure unique items exist on exactly one inventory list, somewhere."
    problem = 0
    all_unique_items = {}
    for i in data:
        if int(i) > 399 and ' item ' in data[i]['firstline'][0]:
            if ' item tradegood' in data[i]['firstline'][0]:
                continue
            all_unique_items[i] = 1
            try:
                un = None
                un = data[i]['IT']['un'][0]
                il = data[un]['il']
                il.index(i)  # this might have false positive and match a qty XXX
            except (KeyError, ValueError):
                print('Unique item {} is not in inventory of unit {}'.format(i, un), file=sys.stderr)
                problem += 1
                continue

    all_inventory = {}
    for i in data:
        if 'il' in data[i]:
            il = data[i]['il'].copy()
            while len(il) > 0:
                item = il.pop(0)
                qty = int(il.pop(0))
                all_inventory[item] = all_inventory.get(item, 0) + qty

    for i in all_unique_items:
        if all_inventory[i] != 1:
            print('Unique item {} does not have exactly one instance'.format(i), file=sys.stderr)
            problem += 1
            continue

    return problem


def check_moving(data):
    '''
    Make sure moving stack leaders have a running command cs=2
    If I'm a moving non-stack-leader make sure my mo == stack leader mo
    '''
    return 0


def check_prisoners(data):
    "Make sure prisoners are stacked under another character"
    problem = 0
    for i in data:
        if ' char ' in data[i]['firstline'][0]:
            if 'CH' in data[i]:
                if 'pr' in data[i]['CH']:
                    where = data[i]['LI']['wh'][0]
                    if ' char ' not in data[where]['firstline'][0]:
                        print('Prisoner {} is not stacked under a character.'.format(to_oid(i)))
                        problem += 1
    return problem


def check_db(data):
    problems = 0
    problems += check_where_here(data)
    problems += check_faction_units(data)
    problems += sweep_independent_units(data)
    problems += check_unique_items(data)
    problems += check_moving(data)
    problems += check_prisoners(data)

    return problems
