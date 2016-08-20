'''
Read an entire lib directory
'''

import argparse

from oid import to_oid, to_int, allocate_oid
from formatters import read_players, write_players, read_lib, write_lib

parser = argparse.ArgumentParser(description='read an Olympia lib')

parser.add_argument('libdir', help='Olympia lib directory')
args = parser.parse_args()

def data_append(data, box, subbox, value):
    if not isinstance(value, list):
        value = [ value ]

    l = data[box].get(subbox, [])
    [ l.append(v) for v in value ]
    data[box][subbox] = l

def data_append2(data, box, subbox, key, value):
    '''
    append value to the at data[box][subbox], doing what's needed to initialize things
    '''
    data[box] = data.get(box, {})
    data[box][subbox] = data[box].get(subbox, {})
    existing = data[box][subbox].get(key, [])
    existing.append(value)
    data[box][subbox][key] = existing

def data_newbox(data, oid_kind, firstline, oid=None):
    if oid:
        oidint = to_int(oid)
    else:
        oidint = allocate_oid(data, oid_kind) # e.g. NNNN
    if oidint in data:
        raise ValueError( oidint + ' is already in data')
    data[oidint] = {}
    data[oidint]['firstline'] = [str(oidint) + ' ' + firstline]
    return oidint

def place_new_unit(data, oidint, whereint):
    data_append2(data, oidint, 'LI', 'wh', whereint)
    data_append2(data, whereint, 'LI', 'hl', oidint)

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

    data[oidint]['na'] = [ 'Scroll of '+skill ]
    data[oidint]['IT'] = {}
    data[oidint]['IT']['wt'] = [ 1 ]
    data[oidint]['IT']['un'] = [ locint ]
    data[oidint]['IM'] = {}
    data[oidint]['IM']['ms'] = [ skill ]

    data_append(data, locint, 'il', [ oidint, 1 ])

def add_scrolls(data):
    ownerprefix = { 'aa1': [ 'a', 'b', 'c', 'd', 'e', ],
                    'ff1': [ 'f', 'g', 'h', 'i', 'j', ],
                    'kk1': [ 'k', 'l', 'm', 'n', 'o', ],
                    'pp1': [ 'p', 'q', 'r', 's', 't', ],
    }
    skills = [ '600', '610', '630', '636', '637', '638', '639', '650', '657', '658', 
               '659', '661', '670', '675', '676', '680', '690', '693', '694', '695', 
               '696', '697', '700', '706', '707', '720', '723', '730', '750', '753', 
               '754', '755', '756', '800', '807', '808', '809', '811', '812', '813', 
               '814', '820', '825', '826', '827', '828', '829', '831', '832', '833', 
               '840', '843', '844', '845', '846', '847', '848', '849', '851', '852', 
               '860', '864', '865', '866', '867', '868', '869', '871', '872', '880', 
               '885', '886', '887', '888', '889', '891', '892', '893', '894', '900', 
               '904', '905', '906', '907', '908', '909', '911', '921', '922',
    ]
    for owner in ownerprefix:
        for prefix in ownerprefix[owner]:
            for skill in skills:
                oid = prefix + skill
                add_scroll(data, skill, owner, oid=oid)

def add_potion(data, kind, im, loc, oid=None):
    oidint = data_newbox(data, 'CNNN', 'item 0', oid=oid)
    locint = to_int(loc)

    data[oidint]['na'] = [ 'Potion of '+kind ]
    data[oidint]['IT'] = {}
    data[oidint]['IT']['wt'] = [ 1 ]
    data[oidint]['IT']['un'] = [ locint ]
    data[oidint]['IM'] = im

    data_append(data, locint, 'il', [ oidint, 1 ])

def add_potions(data):
    ownerprefix = { 'aa1': [ 'a', ],
                    'ff1': [ 'f', ],
                    'kk1': [ 'k', ],
                    'pp1': [ 'p', ],
    }
    ct = { 'aa1': '1001', 'ff1': '2001', 'kk1': '3001', 'pp1': '4001' }
    farcasts = {
        'aa1': [ 'aa08', 'aa08', 'c43', 'c43', '2001', '2001', ],
        'ff1': [],
        'kk1': [],
        'pp1': [],
    }
    for owner in ownerprefix:
        for prefix in ownerprefix[owner]:
            for r in range(500,510):
                oid = prefix + str(r)
                add_potion(data, 'heal', {'uk': [2]}, owner, oid=oid)
            for r in range(510,512):
                oid = prefix + str(r)
                add_potion(data, 'death', {'uk': [1]}, owner, oid=oid)
            for r in range(520,522):
                oid = prefix + str(r)
                im = {'uk': [3]}
                im['ct'] = [ ct[owner] ]
                add_potion(data, 'slavery', im, owner, oid=oid)
            count = 530
            for pc in farcasts[owner]:
                oid = prefix + str(count)
                count += 1
                im = {'uk': [5], 'pc': [to_int(pc)]}
                add_potion(data, 'farcast '+pc, im, owner, oid=oid)

def place_char(data, who, where):
    whoint = to_int(str(who))
    whereint = to_int(str(where))
    data_append2(data, whoint, 'LI', 'wh', whereint)
    data_append2(data, whereint, 'LI', 'hl', whoint)

data = read_lib(args.libdir)

add_scrolls(data)
add_potions(data)
#add_storms(data)

add_structure(data, 'castle6', 'c18', 'Aachen Castle', oid='1001')
add_structure(data, 'tower', '1001', 'Aachen Tower', oid='1002')
add_structure(data, 'tower', 'c18', 'Aachen Outer Tower', oid='1003')
add_structure(data, 'tower', 'aa01', 'Aachen Outside Tower', oid='1004')
add_structure(data, 'temple', 'c18', 'Aachen Temple', oid='1005')
add_structure(data, 'mine', 'aa01', 'Aachen Mine', oid='1006')

# XXX structures for other factions
add_structure(data, 'castle6', 'c43', 'Flugel Castle', oid='2001')
add_structure(data, 'castle6', 'k20', 'Koeln Castle', oid='3001')
add_structure(data, 'castle6', 'w65', 'Paschen Castle', oid='4001')

# add_garrison(loc, castle, oid=oid)

place_char(data, 1100, 1001)
place_char(data, 1101, 1100)
place_char(data, 1102, 'c18')
place_char(data, 1103, 1005)
place_char(data, 1104, 1001)
place_char(data, 1105, 1006)

place_char(data, 2100, 2001)
place_char(data, 3100, 3001)
place_char(data, 4100, 4001)

# fix mage aura, add 1100 auraculum
# copy chars to other factions

# make list of hidden stuff, make 1/2 of it randomly visible to each faction
# (do this after you finish creating more stuff...)

newlibdir = args.libdir.replace('mapgen', 'modified')
if newlibdir == args.libdir:
    raise ValueError

write_lib(data, newlibdir)
