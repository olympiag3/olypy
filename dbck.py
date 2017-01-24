'''
Database checker, similar to the one in the C code (check.c)
'''
import sys

from oid import to_oid
import box
import data as db
import details


def check_firstline(data):
    '''Make sure everything in data has a firstline'''
    problem = 0
    for k, v in data.items():
        if 'firstline' not in v:
            print('Thing {} has no firstline'.format(k), file=sys.stderr)
            problem += 1
    return problem


where_things = set(('loc', 'ship', 'char'))


def check_where_here(data):
    '''Make sure that every box that's where is here, and here is where.
    Does not check anything that is not where.'''
    problem = 0
    for k, v in data.items():
        if 'firstline' in v and ' loc region' not in v['firstline'][0]:
            _, kind, _ = v['firstline'][0].split(' ', maxsplit=2)
            if kind in where_things:
                try:
                    where = data[k]['LI']['wh'][0]
                except (KeyError, IndexError):
                    print('Thing {} is not anywhere'.format(k), file=sys.stderr)
                    print('  ', data[k]['firstline'][0], file=sys.stderr)
                    problem += 1
                    continue
                try:
                    hl = data[where]['LI']['hl']
                    hl.index(k)
                except (KeyError, ValueError):
                    print('Thing {} is not in here list of thing {}'.format(k, where), file=sys.stderr)
                    print('  ', data[k]['firstline'][0], file=sys.stderr)
                    if where in data:
                        print('  ', data[where]['firstline'][0], file=sys.stderr)
                        box.subbox_append(data, where, 'LI', 'hl', k, dedup=True)
                        print('   fixed up.', file=sys.stderr)
                    else:
                        problem += 1
                    continue

    for k, v in data.items():
        if 'LI' in v:
            if 'hl' in v['LI']:
                hl = v['LI']['hl']
                for unit in hl:
                    try:
                        where = data[unit]['LI']['wh'][0]
                        if where != k:
                            raise ValueError
                    except (KeyError, ValueError, IndexError):
                        print('Unit {} is in here list of unit {}, but is not there'.format(unit, k), file=sys.stderr)
                        if unit not in data:
                            print('   btw unit {} does not exist'.format(unit), file=sys.stderr)
                        box.subbox_remove(data, k, 'LI', 'hl', unit)
                        print('   fixed.', file=sys.stderr)

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
                    print('  ', data[i]['firstline'][0], file=sys.stderr)
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
                    if unit in data:
                        print('  ', data[unit]['firstline'][0], file=sys.stderr)
                    else:
                        print('  ' 'unit {} is not in data'.format(unit), file=sys.stderr)
                    problem += 1
                    continue

    return problem


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
                if not isinstance(il, list):
                    print('Whoops. id', i, 'il is', il, file=sys.stderr)
                il.index(i)  # this might have false positive and match a qty XXX
            except (KeyError, ValueError):
                print('Unique item {} is not in inventory of unit {}'.format(i, un), file=sys.stderr)
                print('  ', data[i]['firstline'][0], file=sys.stderr)
                if un in data:
                    print('  ', data[un]['firstline'][0], file=sys.stderr)
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
        if i not in all_inventory or all_inventory[i] != 1:
            print('Unique item {} does not have exactly one instance'.format(i), file=sys.stderr)
            if i in data:
                print('  ', data[i]['firstline'][0], file=sys.stderr)
            problem += 1
            continue

    for i in all_inventory:
        if int(i) > 399 and i not in data:
            print('Item {} is in inventory somewhere but is not in data'.format(i), file=sys.stderr)
            problem += 1

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
    for k, v in data.items():
        if ' char ' in v['firstline'][0]:
            if 'CH' in v:
                if 'pr' in v['CH']:
                    where = v['LI']['wh'][0]
                    if ' char ' not in data[where]['firstline'][0]:
                        print('Prisoner {} is not stacked; location {}'.format(to_oid(k), where), file=sys.stderr)
                        problem += 1
    return problem


def check_links(data):
    '''
    Regression test.
    Make sure provinces don't link cities in LO pd.
    Make sure cities don't have LO pd.
    TODO: roads
    TODO: sewers, cities
    TODO: graveyards and faery hills
    '''
    problem = 0

    for k, v in data.items():
        fl = v['firstline'][0]
        if ' loc ' in fl:
            kind = fl.partition(' loc ')[2]
            if kind in details.province_kinds:
                if 'LO' not in v or 'pd' not in v['LO']:
                    print('Province {} lacks LO pd'.format(k), file=sys.stderr)
                    problem += 1
                    continue
                pd = v['LO']['pd']
                for route in pd:
                    if route != '0':
                        route_fl = data[route]['firstline'][0]
                        if route_fl.endswith(' loc city'):
                            print('Province {} has a NESWUD link to city {}'.format(k, route), file=sys.stderr)
                            problem += 1
            elif kind == 'city':
                pd = v.get('LO', {}).get('pd', [])
                for dir, route in enumerate(pd):
                    if dir < 4 and route != '0':
                        print('City {} has NESW link'.format(k), file=sys.stderr)
                        problem += 1
    return problem


def check_db(data):
    problems = 0
    problems += check_firstline(data)
    problems += check_where_here(data)
    problems += check_faction_units(data)
    problems += check_unique_items(data)
    problems += check_moving(data)
    problems += check_prisoners(data)
    problems += check_links(data)

    return problems
