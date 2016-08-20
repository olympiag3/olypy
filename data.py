'''
Code that manipulates the in-memory Olympia database
'''

from oid import to_oid, to_int, allocate_oid

def data_append(data, box, subbox, value):
    box = str(box)
    subbox = str(subbox)
    if not isinstance(value, list):
        value = [ value ]

    l = data[box].get(subbox, [])
    [ l.append(str(v)) for v in value ]
    data[box][subbox] = l

def data_append2(data, box, subbox, key, value):
    '''
    append value to the at data[box][subbox], doing what's needed to initialize things
    '''
    key = str(key)
    data[box] = data.get(box, {})
    data[box][subbox] = data[box].get(subbox, {})
    existing = data[box][subbox].get(key, [])
    existing.append(str(value))
    data[box][subbox][key] = existing

def data_newbox(data, oid_kind, firstline, oid=None):
    if oid:
        oidint = to_int(str(oid))
    else:
        oidint = allocate_oid(data, oid_kind) # e.g. NNNN
    if oidint in data:
        raise ValueError( oidint + ' is already in data')
    data[oidint] = {}
    data[oidint]['firstline'] = [str(oidint) + ' ' + firstline]
    return oidint

def place_new_unit(data, who, where):
    whoint = to_int(str(who))
    whereint = to_int(str(where))
    data_append2(data, whoint, 'LI', 'wh', whereint)
    data_append2(data, whereint, 'LI', 'hl', whoint)

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
    place_new_unit(data, oidint, whereint)
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

