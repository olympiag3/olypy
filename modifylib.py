'''
Modify an existing lib directory to have a lot of additional stuff
'''

import argparse

from oid import to_oid, to_int, allocate_oid
from oio import read_lib, write_lib
from data import link_box, add_structure, add_scroll, add_potion

parser = argparse.ArgumentParser(description='read an Olympia lib')

parser.add_argument('libdir', help='Olympia lib directory')
args = parser.parse_args()

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

link_box(data, 1100, 1001)
link_box(data, 1101, 1100)
link_box(data, 1102, 'c18')
link_box(data, 1103, 1005)
link_box(data, 1104, 1001)
link_box(data, 1105, 1006)

link_box(data, 2100, 2001)
link_box(data, 3100, 3001)
link_box(data, 4100, 4001)

# fix mage aura, add 1100 auraculum
# copy chars to other factions

# make list of hidden stuff, make 1/2 of it randomly visible to each faction
# (do this after you finish creating more stuff...)

newlibdir = args.libdir.replace('mapgen', 'modified')
if newlibdir == args.libdir:
    raise ValueError

write_lib(data, newlibdir)
