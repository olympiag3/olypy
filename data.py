'''
Code that manipulates the in-memory Olympia database
'''

from oid import to_oid, to_int, allocate_oid

# uniq a list, order preserving
# see: https://www.peterbe.com/plog/uniqifiers-benchmark

def uniq_f11(seq):
    return list(_uniq_f11(seq))

def _uniq_f11(seq):
    seen = set()
    for x in seq:
        if x in seen:
            continue
        seen.add(x)
        yield x

def data_append(data, box, subbox, value):
    '''
    append value to data[box][subbox], doing what's needed to initialize things
    '''
    box = str(box)
    subbox = str(subbox)
    if not isinstance(value, list):
        value = [ value ]

    data[box] = data.get(box, {})
    l = data[box].get(subbox, [])
    [ l.append(str(v)) for v in value ]
    l = uniq_f11(l)
    data[box][subbox] = l

def data_remove(data, box, subbox, value):
    '''
    remove value to data[box][subbox]
    '''
    box = str(box)
    data[box] = data.get(box, {})
    l = data[box].get(subbox, [])
    try:
        l.remove(value)
        data[box][subbox] = l # only runs if value was in the list
    except ValueError:
        pass

def data_append2(data, box, subbox, key, value):
    '''
    append value to data[box][subbox][key], doing what's needed to initialize things
    '''
    box = str(box)
    subbox = str(subbox)
    key = str(key)
    if not isinstance(value, list):
        value = [ value ]

    data[box] = data.get(box, {})
    data[box][subbox] = data[box].get(subbox, {})
    l = data[box][subbox].get(key, [])
    [ l.append(str(v)) for v in value ] # XXX changeme to an extend
    l = uniq_f11(l)
    data[box][subbox][key] = l

def data_remove2(data, box, subbox, key, value):
    '''
    remove value from data[box][subbox][key]
    '''
    box = str(box)
    subbox = str(subbox)
    key = str(key)
    l = data[box].get(subbox,{}).get(key, [])
    try:
        l.remove(value)
        data[box][subbox][key] = l # only runs if value was in the list
    except ValueError:
        pass

def upsert_box(data, newbox, promote_children=True):
    '''
    As we parse turns going forward in time, we frequently run into boxes
    that we've seen before. Some are locations, which never move, and
    others are transient (buildings, characters.) We may have to destroy
    obsolete information.
    '''

    # if not the same type, destroy the previous thing
    oidint = newbox.keys()[0]
    old_firstline = box[oidint]['firstline'] # required
    _, old_kind, old_subkind = old_firstline.split(' ', maxsplit=2)
    new_firstline = newbox[oidint]['firstline'] # required
    _, new_kind, new_subkind = new_firstline.split(' ', maxsplit=2)
    if old_kind != new_kind:
        destroy_box(data, oidint, promote_children=promote_children)


    # copy over the name
    # destroy any interior structures that disappeared
    #  put existing structures in correct order
    # unlink any interior nobles that disappeared
    #  put remaining nobles in correct order
    # add any interior locations
    # add interior nobles
    # market report
    # do not be confused by
    #  hidden sub-locs disappearing/appearing; also fog
    #  tradegoods; opium less visible
    #  mid-turn trade vs. end-of-turn trade

def destroy_box(data, oidint, promote_children=True):
    '''
    Destroy a box that's become something different.
    '''
    unlink_box(data, oidint, promote_children=promote_children)
    # XXXv0 other links:
    # pledge chain - CM,pl is one-way so it needs a end-of-run fixup XXXv0
    # lord: CH,lo and previous lord CH,pl -- needs end-of-run fixup XXXv0
    # unique items - need to look at firstline - IT,un is where it is
    # creater of things like storms, artifacts - IM,ct
    # owner of storm - MI,sb {summoned by}
    # storm bound to a ship - ship has SL,bs ... and the storm has MI,bs=itself (?)

def link_box(data, who, where):
    whoint = to_int(str(who))
    unlink_box(data, whoint)
    whereint = to_int(str(where))
    data_append2(data, whoint, 'LI', 'wh', whereint)
    data_append2(data, whereint, 'LI', 'hl', whoint)

def unlink_box(data, oidint, promote_children=True):
    '''
    If I'm somewhere, remove me from that somewhere.
    If anyone is inside me, move them up.
    I may well end up nowhere... that will get cleaned up in the end.
    '''
    if data.get(oidint) is None:
        return
    wh = data[oidint].get('LI', {}).get('wh')
    hl = data[oidint].get('LI', {}).get('hl')

    if wh is not None:
        del data[oidint]['LI']['wh']
        other_hl = data.get(wh[0], {}).get('LI', {}).get('hl')
        if other_hl is not None:
            try:
                other_hl.remove(oidint)
                data[wh[0]]['LI']['hl'] = other_hl
            except ValueError:
                pass

    if promote_children and hl is not None:
        for h in hl:
            data_append(data, 'LI', 'hl', wh)
            data[h]['LI']['wh'] = wh

def data_newbox(data, oid_kind, firstline, oid=None, overwrite=False):
    '''
    Create a new box. Intended for generating QA libs, not for parsing turns.
    '''
    if oid:
        oidint = to_int(str(oid))
    else:
        oidint = allocate_oid(data, oid_kind) # e.g. NNNN
    if oidint in data:
        if not overwrite:
            raise ValueError( oidint + ' is already in data')
        # if I am not the same thing, destory the old thing
        if data[oidint]['firstline'] != firstline:
            destroy_box(data, oidint)
    data[oidint] = {}
    data[oidint]['firstline'] = [str(oidint) + ' ' + firstline]
    return oidint

structures = {
    # in-progress: bm, er, eg ... bm runs 0..4
    'roundship': {'type': 'ship', 'de': 10, 'er': 50000, 'ca': 25000,},
    'galley': {'type': 'ship', 'de': 20, 'er': 25000, 'ca': 5000,},
    'inn': {'de': 10, 'er': 30000,},
    'mine': {'de': 10, 'er': 50000, 'sd': 3, }, # depth is sd//3
    'temple': {'de': 10, 'er': 100000, 'te': 750},
    'tower': {'de': 40, 'er': 200000,},
    'castle': {'de': 50, 'er': 1000000,},
    'castle1': {'kind': 'castle', 'de': 55, 'er': 1000000, 'cl': 1,},
    'castle2': {'kind': 'castle', 'de': 60, 'er': 1000000, 'cl': 2,},
    'castle3': {'kind': 'castle', 'de': 65, 'er': 1000000, 'cl': 3,},
    'castle4': {'kind': 'castle', 'de': 70, 'er': 1000000, 'cl': 4,},
    'castle5': {'kind': 'castle', 'de': 75, 'er': 1000000, 'cl': 5,},
    'castle6': {'kind': 'castle', 'de': 80, 'er': 1000000, 'cl': 6,},
}

def add_structure(data, kind, where, name, progress=None, damage=None, defense=None, oid=None):
    if kind not in structures:
        raise ValueError
    whereint = to_int(where)
    if whereint not in data:
        raise ValueError('whereint ' + str(whereint) + ' is not in data')

    oidint = data_newbox(data, 'NNNN', structures[kind].get('type', 'loc') + ' ' + structures[kind].get('kind', kind), oid=oid)
    link_box(data, oidint, whereint)
    data[oidint]['na'] = [ name ]

    # fully-finished structure
    if 'ca' in structures[kind]:
        data_append2(data, oidint, 'SL', 'ca', structures[kind]['ca'])
    if 'cl' in structures[kind]:
        data_append2(data, oidint, 'SL', 'cl', structures[kind]['cl'])
    if 'sd' in structures[kind]:
        data_append2(data, oidint, 'SL', 'sd', structures[kind]['sd'])
    data_append2(data, oidint, 'SL', 'de', defense or structures[kind]['de'])
    if damage:
        data_append2(data, oidint, 'SL', 'da', damage)

    # XXX if under construction
    # remove ca if present
    # remove de
    #data_append2(data, oidint, 'SL', 'er', structures[kind]['er'])
    # compute eg
    # compute bm 0-4
    if progress:
        raise ValueError

def add_scroll(data, skill, loc, oid=None):
    oidint = data_newbox(data, 'CNNN', 'item scroll', oid=oid)
    locint = to_int(loc)
    skill = str(skill)

    data[oidint]['na'] = [ 'Scroll of '+skill ]
    data[oidint]['IT'] = {}
    data[oidint]['IT']['wt'] = [ 1 ]
    data[oidint]['IT']['un'] = [ locint ]
    data[oidint]['IM'] = {}
    data[oidint]['IM']['ms'] = [ skill ]

    data_append(data, locint, 'il', [ oidint, 1 ])

def add_potion(data, kind, im, loc, oid=None):
    oidint = data_newbox(data, 'CNNN', 'item 0', oid=oid)
    locint = to_int(loc)

    data[oidint]['na'] = [ 'Potion of '+kind ]
    data[oidint]['IT'] = {}
    data[oidint]['IT']['wt'] = [ 1 ]
    data[oidint]['IT']['un'] = [ locint ]
    data[oidint]['IM'] = im

    data_append(data, locint, 'il', [ oidint, 1 ])

