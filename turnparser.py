'''
Parse old Olympia text turns into an Olympia database, suitable for simming
'''

import re
import sys

from oid import to_int, to_oid, to_int_safely
import box
import data as db

global_days = {}

directions = {'north': 0, 'east': 1, 'south': 2, 'west': 3, 'up': 4, 'down': 5}
inverted_directions = {'north': 2, 'east': 3, 'south': 0, 'west': 1, 'up': 5, 'down': 4}

road_directions = set(('secret pass', 'secret route', 'old road',
                       'narrow channel', 'rocky channel', 'secret sea route',
                       'underground'))
special_directions = road_directions.union(set(('out',)))

route_annotations = set(('hidden', 'impassable', 'port', 'port city', 'safe haven'))

province_kinds = set(('mountain', 'plain', 'swamp', 'forest', 'desert', 'ocean',
                     'tunnel', 'chamber', 'cloud', 'underground'))
subloc_kinds = set(('island', 'ring of stones', 'mallorn grove', 'bog', 'cave',
                    'city', 'graveyard', 'ruins', 'battlefield', 'enchanted forest',
                    'rocky hill', 'circle of trees', 'pits', 'pasture', 'oasis',
                    'yew grove', 'sand pit', 'sacred grove', 'poppy field', 'lair',
                    'faery hill', 'sewer'))

structure_type = set(('castle', 'tower', 'galley', 'roundship', 'temple', 'mine', 'collapsed mine', 'inn'))

structure_er = {
    'castle':  '10000',
    'tower':    '2000',
    'galley':    '250',
    'roundship': '500',
    'temple':   '1000',
    'mine':      '500',
    'inn':       '300',
    'raft':       '45'}

geo_inventory = {
    # ordered same as mapgen.c
    'ocean': ['59', '30', '87', '50', '274', '1', '275', '1', '276', '1'],
    'forest': ['77', '30', '10', '10', '96', '50', '101', '1', '276', '1', '274', '1'],
    'swamp': ['66', '1', '96', '50', '101', '1', '274', '1'],
    'mountain': ['78', '50', '10', '10', '96', '50', '101', '1', '275', '1'],
    'plain': ['51', '5', '10', '10', '96', '50', '101', '1', '275', '1'],
    'desert': ['78', '10', '96', '50', '101', '1', '275', '1'],

    'island': ['59', '30'],
    'ring of stones': [],
    'mallorn grove': ['65', '2', '70', '2'],
    'bog': ['66', '4'],
    'cave': ['67', '2'],
    'city': ['10', '10', '294', '1', '277', '5', '96', '100', '101', '1'],
    # 'guild' -- generic name for non-land non-ocean sublocs
    'graveyard': ['31', '15', '273', '1'],
    'ruins': [],
    'battlefield': [],
    'enchanted forest': [],
    'rocky hill': ['78', '50'],
    'circle of trees': ['77', '5', '64', '3'],
    'pits': ['66', '4'],
    'pasture': ['51', '5'],
    'oasis': [],
    'yew grove': ['68', '5'],
    'sand pit': ['71', '1'],
    'sacred grove': ['77', '5'],
    'poppy field': ['93', '25'],
    'lair': [],

    # these are province-sized things in non-normal places
    'cloud': ['274', '1', '275', '1', '276', '1'],
    'underground': ['101', '1', '96', '50'],
    'tunnel': ['101', '1', '96', '50'],
    'chamber': ['101', '1', '96', '50'],

    # and two final special things that link normal-faery and normal-undercity
    'faery hill': [],
    'sewer': [],
}

# regions go from 58760-58999 ... and need to be in the correct order
# this dict is a list of every region which was observed to be after key r
# XXXv2 also get region order from parse_location_top order
region_after = {}
regions_set = set(('Great Sea', 'Hades', 'Undercity', 'Cloudlands'))

type_to_region = {
    'ocean': 'Great Sea',  # if in main world; ocean in Faery is in Faery region
    'underground': 'Hades',
    'tunnel': 'Undercity',
    'chamber': 'Undercity',
    'cloud': 'Cloudlands',
}

has_6_directions = set(('tunnel', 'sewer', 'chamber'))

skill_days = {
    '600': '21',
    '601': '14',
    '602': '14',
    '603': '14',
    '610': '21',
    '611': '28',
    '612': '28',
    '613': '14',
    '614': '14',
    '615': '21',
    '616': '14',
    '617': '14',
    '630': '28',
    '631': '14',
    '632': '14',
    '633': '14',
    '634': '14',
    '635': '28',
    '636': '14',
    '637': '21',
    '638': '28',
    '639': '21',
    '650': '28',
    '651': '21',
    '652': '28',
    '653': '28',
    '654': '28',
    '655': '14',
    '656': '14',
    '657': '21',
    '658': '21',
    '659': '21',
    '661': '21',
    '670': '28',
    '671': '14',
    '672': '21',
    '673': '14',
    '674': '21',
    '675': '21',
    '676': '14',
    '680': '21',
    '681': '14',
    '682': '14',
    '690': '28',
    '691': '21',
    '692': '21',
    '693': '21',
    '694': '21',
    '695': '14',
    '696': '21',
    '697': '28',
    '700': '21',
    '701': '14',
    '702': '14',
    '703': '14',
    '704': '14',
    '705': '14',
    '706': '14',
    '707': '14',
    '720': '21',
    '721': '14',
    '722': '14',
    '723': '14',
    '730': '21',
    '731': '14',
    '732': '14',
    '733': '14',
    '750': '35',
    '751': '28',
    '752': '28',
    '753': '21',
    '754': '28',
    '755': '28',
    '756': '28',
    '800': '28',
    '801': '14',
    '802': '14',
    '803': '14',
    '804': '21',
    '805': '21',
    '806': '21',
    '807': '14',
    '808': '21',
    '809': '21',
    '811': '21',
    '812': '21',
    '813': '21',
    '814': '21',
    '820': '35',
    '821': '21',
    '822': '21',
    '823': '21',
    '824': '21',
    '825': '21',
    '826': '21',
    '827': '21',
    '828': '21',
    '829': '21',
    '831': '28',
    '832': '21',
    '833': '21',
    '840': '35',
    '841': '21',
    '842': '21',
    '843': '14',
    '844': '21',
    '845': '21',
    '846': '21',
    '847': '21',
    '848': '21',
    '849': '21',
    '851': '21',
    '852': '21',
    '860': '35',
    '861': '14',
    '862': '14',
    '863': '21',
    '864': '14',
    '865': '14',
    '866': '14',
    '867': '21',
    '868': '21',
    '869': '14',
    '871': '14',
    '872': '21',
    '880': '43',
    '881': '14',
    '882': '21',
    '883': '21',
    '884': '21',
    '885': '21',
    '886': '14',
    '887': '14',
    '888': '14',
    '889': '21',
    '891': '28',
    '892': '14',
    '893': '21',
    '894': '21',
    '900': '42',
    '901': '21',
    '902': '21',
    '903': '21',
    '904': '21',
    '905': '21',
    '906': '21',
    '907': '28',
    '908': '21',
    '909': '21',
    '911': '28',
    '920': '42',
    '921': '28',
    '922': '28',
}

skill_experience = {
    'apprentice': '0',
    'journeyman': '5',
    'adept': '12',
    'master': '21',
    'grand master': '35',
}

trade_map = {
    'buy': '1',
    'sell': '2',
    'produce': '3',
    'consume': '4'
}

noble_ranks = {'lord': 10,
               'knight': 20,
               'baron': 30,
               'count': 40,
               'earl': 60,
               'marquess': 60,
               'duke': 70,
               'king': 80}

numbers = {'one': 1,
           'two': 2,
           'three': 3,
           'four': 4,
           'five': 5,
           'six': 6,
           'seven': 7,
           'eight': 8,
           'nine': 9,
           'ten': 10}

item_to_inventory = {
    'gold': '1',
    'peasant': '10',
    'worker': '11',
    'soldier': '12',
    'archer': '13',
    'knight': '14',
    'elite guard': '15',
    'pikeman': '16',
    'pikemen': '16',
    'blessed soldier': '17',
    'ghost warrior': '18',
    'sailor': '19',
    'swordsman': '20',
    'swordsmen': '20',
    'crossbowman': '21',
    'crossbowmen': '21',
    'elite archer': '22',
    'angry peasant': '23',
    'pirate': '24',
    'elf': '25',
    'elves': '25',
    'spirit': '26',
    'undead': '31',
    'savage': '32',
    'skeleton': '33',
    'barbarian': '34',
    'wild horse': '51',
    'riding horse': '52',
    'warmount': '53',
    'winged horse': '54',
    'nazgul': '55',
    'floatsam': '59',
    'battering ram': '60',
    'catapult': '61',
    'siege tower': '62',
    'ratspider venom': '63',
    'lana bark': '64',
    'avinia leaf': '65',
    'avinia leaves': '65',
    'spiny root': '66',
    'farrenstone': '67',
    'yew': '68',
    'elfstone': '69',
    'mallorn wood': '70',
    'pretus bones': '71',
    'longbow': '72',
    'plate armor': '73',
    'longsword': '74',
    'pike': '75',
    'ox': '76',
    'oxen': '76',
    'wood': '77',
    'stone': '78',
    'iron': '79',
    'leather': '80',
    'ratspider': '81',
    'mithril': '82',
    'gate crystal': '83',
    'blank scroll': '84',
    'crossbow': '85',
    'fish': '87',
    'opium': '93',
    'woven basket': '94',
    'clay pot': '95',
    'drum': '98',
    'hide': '99',
    'lead': '102',
    'pitch': '261',
    'centaur': '271',
    'minotaur': '272',
    'giant spider': '278',
    'rat': '279',
    'lion': '280',
    'giant bird': '281',
    'giant lizard': '282',
    'bandit': '283',
    'chimera': '284',
    'harpie': '285',
    'dragon': '286',
    'orc': '287',
    'gorgon': '288',
    'wolf': '289',
    'wolves': '289',
    'cyclops': '291',
    'giant': '292',
    'faerie': '293',
    'faeries': '293',
    'hound': '295'
}

mage_ranks = set(('conjurer', 'mage', 'wizard', 'sorcerer',
                  '6th black circle', '5th black circle', '4th black circle',
                  '3rd black circle', '2nd black circle', 'master of the black arts'))


def parse_an_id(text):
    '''
    Returns the first Olympia id
    '''
    m = re.search(r'\[(.{3,6})\]', text)
    if not m:
        raise ValueError('failed to find an id in '+text)
    return to_int(m.group(1))


def split_into_sections(text):
    dashes = '------------------------------------------------------------------------'
    sections = text.split(dashes)
    # we need to stick the last line of each group onto the previous group
    last = ''
    ret = []
    for s in sections:
        ret.append(last + '\n' + dashes + '\n' + s)
        lines = s.rstrip().split('\n')
        last = lines[-1]
    return ret[1:]  # discard header


wait_args = {'time': {'value': 0, 'nargs': 1},
             'day': {'value': 1, 'nargs': 1},
             'unit': {'value': 2, 'nargs': 1},
             'gold': {'value': 3, 'nargs': 1},
             'item': {'value': 4, 'nargs': 2},
             'flag': {'value': 5, 'nargs': 1, 'special': 1},
             'loc': {'value': 6, 'nargs': 1},
             'stack': {'value': 7, 'nargs': 1},
             'top': {'value': 8, 'nargs': 0},
             'ferry': {'value': 9, 'nargs': 1},
             'ship': {'value': 10, 'nargs': 1},
             'rain': {'value': 11, 'nargs': 0},
             'fog': {'value': 12, 'nargs': 0},
             'wind': {'value': 13, 'nargs': 0},
             'not': {'value': 14, 'nargs': 0},
             'owner': {'value': 15, 'nargs': 0},
             'raining': {'value': 11, 'nargs': 0},  # alias
             'foggy': {'value': 12, 'nargs': 0},  # alias
             'windy': {'value': 13, 'nargs': 0},  # alias
             'clear': {'value': 19, 'nargs': 0},
             'shiploc': {'value': 20, 'nargs': 1},
             'month': {'value': 21, 'nargs': 1},
             'turn': {'value': 22, 'nargs': 1}}


def parse_wait_args(order):
    '''
    Duplicates parsing in c1.c:parse_wait_args()
    '''
    args = order.split()  # on spaces
    ar = []
    assert args.pop(0) == 'wait'
    while len(args) > 0:
        arg = args.pop(0)
        if arg not in wait_args:
            raise ValueError('unknown WAIT arg of '+arg+' in order '+order)
        ar.append(wait_args[arg]['value'])
        nargs = wait_args[arg]['nargs']
        for _ in range(nargs):
            if 'special' in wait_args[arg]:
                ar.append(args.pop(0))  # flag blue
            else:
                ar.append(to_int(args.pop(0)))
        if 'special' in wait_args[arg]:
            # the next thing either doesn't exist, or is a unit, or is a wait name
            if len(args) > 0:
                if args[0] not in wait_args:
                    ar.append(to_oid(args.pop(0)))
    return ar


def generate_move_args(start_day, remaining, last_move_dest, where):
    '''
    ar: apparent-dest apprent-dir actual-dest road dest-hidden distance orig orig-hidden

    Right now we aren't setting all of these, just the easy ones.
    '''
    ar = ['0', '0', '0', '0', '0', '0', '0', '0']
    ar[2] = last_move_dest
    if remaining == '-1':
        raise ValueError('If I am moving, days remaining canot be unknown: '+remaining)
    ar[5] = str(31 - int(start_day) + int(remaining))
    ar[6] = where
    return ar


def split_order_args(order):
    '''
    Orders are allowed to have "" and '' in them. In this instance, we don't
    care what is in the quoted parts.
    '''
    order = re.sub(r'".*?"', '"foo"', order)
    order = re.sub(r"'.*?'", "'foo'", order)
    return order.split(' ')


order_canon = {'train': 'make',
               'torture': 'use 637',
               'sneak': 'use 639',
               'breed': 'use 654',
               'bribe': 'use 671',
               'raise': 'use 673',
               'rally': 'use 674',
               'incite': 'use 675',
               'bind': 'use 822',
               'trance': 'use 921',
               'wood': 'collect 77',
               'yew': 'collect 68',
               'mallorn': 'collect 70',
               'opium': 'collect 93',
               'stone': 'collect 78',
               'quarry': 'collect 78',
               'fish': 'collect 87',
               'catch': 'collect 51',
               'recruit': 'collect 10',
               'use 702': 'collect 77',
               'use 703': 'collect 68',
               'use 705': 'collect 70',
               'use 706': 'collect 93',
               'use 682': 'collect 78',
               'use 603': 'collect 87',
               'use 655': 'collect 51',
               'use 656': 'make 52',
               'use 657': 'make 53',
               'use 601': 'sail',
               'use 902': 'make 18',
               'go': 'move',
               'fly': 'move',
               'north': 'move n',
               'south': 'move s',
               'east': 'move e',
               'west': 'move w'}

order_canon_exact = {'n': 'move n',
                     's': 'move s',
                     'e': 'move e',
                     'w': 'move w',
                     'enter': 'move in',
                     'exit': 'move out',
                     'in': 'move in',
                     'out': 'move out'}


def canonicalize_order(order):
    for o in order_canon:
        if order.startswith(o):
            order = order.replace(o, order_canon[o], 1)
            break

    if order in order_canon_exact:
        order = order_canon_exact[order]

    return order


valid_orders = {'build': set(('poll',)),
                'collect': set(('poll',)),
                'explore': set(),
                'form': set(),
                'improve': set(('poll',)),
                'make': set(('poll',)),
                'move': set(),
                'pillage': set(),
                'quest': set(),
                'raze': set(('poll',)),
                'repair': set(('poll',)),
                'research': set(),
                'sail': set(('pri_4',)),
                'seek': set(('poll',)),
                'study': set(('poll',)),
                'terrorize': set(),
                'use': set(('poll', 'use_exp', 'use_skill')),
                'wait': set(('poll',))}


single_day_makes = set(('11', '19', '21', '12', '16', '20', '14', '15',
                        '13', '22', '72', '73', '74', '75', '85'))
single_day_collects = set(('10',))


def fake_order(order, start_day, remaining, last_move_dest, unit, data):
    # XXXv0 todo CH mo set to days_since_epoch + remaining for moves
    ret = {'li': [order],
           'wa': [remaining],
           'de': [str(31 - int(start_day))]}

    order = canonicalize_order(order)

    verb, _, rest = order.partition(' ')
    if verb not in valid_orders:
        raise ValueError('Unknown order verb in '+order)
    command = valid_orders[verb]

    ar = []

    if verb == 'wait':
        ar = parse_wait_args(order)
    elif verb == 'move' or verb == 'sail':
        where = data[unit]['LI']['wh'][0]
        ar = generate_move_args(start_day, remaining, last_move_dest, where)
    else:
        ar = [to_int_safely(x) for x in split_order_args(rest)]

    ar += ['0', '0', '0', '0', '0', '0', '0', '0']
    ar = ar[:8]

    if verb == 'collect':
        if ar[0] in single_day_collects:
            ar[3] = ret['de'][0]
    if verb == 'make':
        if ar[0] in single_day_makes:
            ar[3] = ret['de'][0]
        ar[2] = ar[1]  # apparently make item qty days doesn't really take a days argument

    if 'pri_4' in command:
        ret['pr'] = ['4']
    else:
        ret['pr'] = ['3']
    if 'use_skill' in command:
        # for whatever reason, the skill ID goes on the end of 'ar'
        ret['us'] = [ar.pop(0)]
        ar.append(ret['us'][0])
    if 'use_exp' in command:
        # XXXv2 it appears that currently a bug prevents this from having an effect
        # eventually should set it to novice=1 journey=2 teacher=3 master=4 grand=5
        ret['ue'] = ['1']
    if 'poll' in command:
        ret['po'] = ['1']
    ret['cs'] = ['2']  # state 2 = RUN
    ret['st'] = ['1']  # status = TRUE
    ret['ar'] = ar
    return ret


def parse_inventory(text, unit, data):
    temp = {}
    scroll_id = None

    grab_next = 0
    for line in text.split('\n'):
        if grab_next:
            grab_next = 0
            m = re.search(r'\s(.*?)\s\[(\d\d\d)\]', line)
            if m:
                box.subbox_overwrite(data, scroll_id, 'IM', 'ms', [m.group(2)])
            elif '???' in line:
                continue  # leave it faked
            else:
                raise ValueError('next line did not contain the scroll spell: '+line)
            continue

        m = re.match(r'\s+([\d,]+)\s+(.+?) \[(.{1,6}?)\]\s+([\d,]+)\s*(.*)?', line)
        if m:
            qty, name, ident, weight, rest = m.group(1, 2, 3, 4, 5)
            qty = qty.replace(',', '')
            weight = weight.replace(',', '')
            plus, what = 0, ''
            if rest:
                r = re.match(r'\+(\d+) (attack|defense|missile|aura)', rest)
                if r:
                    plus, what = r.group(1, 2)
                # not parsing: ride 150, cap 1,000, etcetc

            ident = to_int(ident)
            temp[int(ident)] = [ident, name, weight, qty, plus, what]

            if int(ident) > 399:
                make_fake_item(unit, ident, name, weight, plus, what, data)
            continue

        m = re.search(r'\s(\w.+)\s\[(.{4})\] permits study of the following skills', line)
        if m:
            name = m.group(1)
            scroll_id = to_int(m.group(2))
            data[scroll_id]['na'] = [name]  # removes 'Fake ' prefix
            data[scroll_id]['firstline'] = [scroll_id + ' item scroll']
            if 'fake' in data[scroll_id]:  # not present if ancient scroll
                del data[scroll_id]['fake']
            grab_next = 1

    ret = []
    keys = sorted(list(temp.keys()))
    for k in keys:
        ret.extend(temp[k])
    return ret


def reformat_inventory(inventory):
    '''
    Reformat a verbose inventory into what actually goes into the database
    '''
    ret = []
    for k in groups(inventory, 6):
        ret.extend([k[0], k[3]])
    return ret


artifact_kindmap = {'attack': 'ab', 'defense': 'db', 'missile': 'mb', 'aura': 'ba'}


def make_fake_item(unit, ident, name, weight, plus, what, data):
    '''
    Based on incomplete info, make a fake unique item.
    Used for things spotted in inventory.
    '''
    if ident in set(('401', '402', '403')):
        # created aready. transfer from old owner to me.
        old = data[ident]['IT']['un'][0]
        box.box_remove(data, old, 'il', ident)
        data[ident]['IT']['un'] = [unit]
    elif int(ident) < 10000:
        # dead body, ok, if you raise this dead body you will be disappointed
        data[ident] = {'firstline': [ident + ' item dead body'], 'na': ['dead body'],
                       'IT': {'pl': ['dead bodies'], 'wt': [weight], 'un': [unit]}}
        return
    else:
        if what in artifact_kindmap and weight == '10':
            # armor/weapon/aura item
            data[ident] = {'firstline': [ident + ' item artifact'],
                           'na': [name],
                           'IT': {'wt': [weight], 'un': [unit]},
                           'IM': {artifact_kindmap[what]: [plus]}}
        elif weight == '10':
            # aura item - held by non-mage. make it 1 point.
            # XXXv2 if it was ever held by a mage in the past, remember the value?
            data[ident] = {'firstline': [ident + ' item artifact'],
                           'na': [name],
                           'IT': {'wt': [weight], 'un': [unit]},
                           'IM': {'ba': ['1']}}
        elif weight == '5':  # ancient scroll
            data[ident] = {'firstline': [ident + ' item scroll'],
                           'na': [name],
                           'IT': {'wt': ['1'], 'un': [unit]}}  # type to be filled in later
        elif name == 'Orb' and weight == '1':
            data[ident] = {'firstline': [ident + ' item 0'],
                           'na': ['Fake Orb'],
                           'IT': {'wt': ['1'], 'un': [unit]},
                           'IM': {'uk': ['9']}}
        elif weight == '0':  # this is probably a bug! I hope it is not fixed
            data[ident] = {'firstline': [ident + ' item npc_token'],
                           'na': [name],
                           'IT': {'un': [unit]},  # g2 database agrees IT wt is not set
                           'IM': {'tn': ['1'], 'ti': ['33']}}  # IM ti is a lie, also needs PL un filled in
        elif int(weight) > 14:  # lightest tradegood is 15
            data[ident] = {'firstline': [ident + ' item tradegood'],
                           'na': [name],
                           'IT': {'pl': [name], 'wt': [weight], 'bp': ['100']}}
        elif weight == '1':  # probably a scroll or potion ... small chance of auraculum
            data[ident] = {'firstline': [ident + ' item 0'],  # if scroll, will eventually be 'item scroll'
                           'na': ['Fake '+name],
                           'IT': {'wt': ['1'], 'un': [unit]},
                           'fake': 'yes'}
        elif weight == '2':  # unusual weight -- auraculum or Palantir
            data[ident] = {'firstline': [ident + ' item palantir'],
                           'na': ['Fake '+name],
                           'IT': {'wt': ['2'], 'un': [unit]},
                           'fake': 'yes'}
        elif weight == '3':  # must be an auraculum
            data[ident] = {'firstline': [ident + ' item auraculum'],
                           'na': ['Fake '+name],
                           'IT': {'wt': ['3'], 'un': [unit]},
                           'fake': 'yes'}
        else:
            # in theory this might include 2/3 of auraculi, but, none of ours are 2 or 3?!
            raise ValueError('weight is '+weight)


def groups(iterable, n):
    '''
    They say Python is elegant, but then I have to do this.
    '''
    return zip(*[iter(iterable)]*n)


def parse_admit(text):
    ret = []
    for line in text.split('\n'):
        parts = line.split()
        if parts:
            if parts[0] != 'admit':
                ret[-1] += [to_int(p) for p in parts]
            else:
                ret.append([to_int(p) for p in parts[1:]])
    return ret


def parse_attitudes(text):
    last = ''
    ret = {}
    for line in text.split('\n'):
        parts = line.split()
        if parts:
            p0 = parts[0].lower()  # on g4 turn 20, some reports have uppercase
            if p0 == 'neutral':
                last = 'neutral'
                ret[last] = [to_int(p) for p in parts[1:]]
            elif p0 == 'defend':
                last = 'defend'
                ret[last] = [to_int(p) for p in parts[1:]]
            elif p0 == 'hostile':
                last = 'hostile'
                ret[last] = [to_int(p) for p in parts[1:]]
            else:  # continuation line
                ret[last].extend([to_int(p) for p in parts])
    return ret


def parse_skills(text):
    skill_exp_list = '|'.join(skill_experience.keys())
    skills_with = re.findall(r'\[(.*?)\], ('+skill_exp_list+')', text)
    skills_without = re.findall(r'\[(.*?)\]', text)
    d = {}
    for s in skills_without:
        d[s] = ('2', skill_days[s], '0', '0')
    for t in skills_with:
        s, e = t
        e = skill_experience[e]
        d[s] = ('2', skill_days[s], e, '0')
    ret = []
    for k in sorted(list(d.keys())):
        ret.append(k)
        ret.extend(d[k])
    return ret


def parse_partial_skills(text):
    skills = re.findall(r'\[(.*?)\], (\d+)/', text)
    ret = []
    for t in skills:
        s, p = t
        kind = '0'
        if p > '1':
            kind = '1'
        ret.extend((s, kind, p, '0', '0'))
    return ret


def parse_pending_trades(text):
    ret = []
    for line in text.split('\n'):
        pieces = line.split(maxsplit=3)
        if len(pieces) != 4:
            continue
        trade, price, qty, item = pieces
        trade = trade_map.get(trade)
        if trade is None:
            continue  # header lines
        qty = qty.replace(',', '')
        item = re.findall(r'\[(.*?)\]', item)
        ret.extend((trade, item[0], qty, price, '0', '0', '0', '0'))
    return ret


def make_locations_from_routes(routes, idint, region, data):
    for r in routes:
        dest = r['destination']
        kind = r['kind']
        dir = r['dir']
        if dir in inverted_directions:
            idir = inverted_directions[dir]
        else:
            idir = -99999
        if dest not in data:
            if kind in province_kinds:
                data[dest] = {'firstline': [dest + ' loc ' + kind],
                              'na': [r['name']],
                              'il': geo_inventory[kind],
                              'LI': {'wh': [region]},
                              'LO': {'pd': [0, 0, 0, 0]}}
                if 'impassable' in r:
                    pass  # city, or mountain/sea. Make the link anyway.
                if dir == 'out':
                    continue  # subloc out routes will be created elsewhere
                if dir.endswith(' road'):
                    continue  # roads are annoying to make. generally they're marked hidden GA rh 1. XXXv1
                if idir > 3:
                    data[dest]['LO']['pd'] = [0, 0, 0, 0, 0, 0]
                data[dest]['LO']['pd'][idir] = idint
            elif kind == 'city' or kind == 'port city':
                # figure out what province this city is in, there should be an impassable link
                prov = None
                for r in routes:
                    if r['dir'] == dir and 'impassable' in r:
                        prov = dest
                        break
                if prov is None:
                    raise ValueError('subiteration could not discover province of a city route, province '+idint)
                # the link is at the province, so don't make any LO here
                data[dest] = {'firstline': [dest + ' loc city'],
                              'na': [r['name']],
                              'il': geo_inventory['city'],
                              'LI': {'wh': [prov]}}
            elif kind in subloc_kinds or kind in structure_type:
                pass  # this only exists for visions of a castle, ship etc XXXv2
        else:
            # the destination exists, but this link may not
            if kind in province_kinds:
                if dir == 'out':
                    continue
                if dir.endswith(' road'):
                    continue  # XXXv1
                if idir > 3:
                    if len(data[dest]['LO']['pd']) < 6:
                        data[dest]['LO']['pd'].extend((0, 0))
                data[dest]['LO']['pd'][idir] = idint
            elif kind == 'city' or kind == 'port city':
                # link is at the province level
                pass

        if 'hidden' in r and not dir.endswith(' road'):
            print('setting LO hi for {}'.format(to_oid(dest)))
            box.subbox_overwrite(data, dest, 'LO', 'hi', ['1'])
            print('box is {}'.format(data[dest]))

        # XXXv2 what about roads?


def make_direction_routes(routes, idint, kind, data):
    '''
    make normal direction routes
    '''
    if kind == 'city' or kind == 'port city':
        return  # cities have no directions
    for r in routes:
        dir = r['dir']
        if dir in directions:
            dest = r['destination']
            if data[idint].get('LO', {}).get('pd') is None:  # non-province?
                box.subbox_overwrite(data, idint, 'LO', 'pd', [0, 0, 0, 0])
            if int(directions[dir]) > 3 and len(data[idint]['LO']['pd']) < 6:
                data[idint]['LO']['pd'].extend((0, 0))
            data[idint]['LO']['pd'][directions[dir]] = dest


def parse_location_top(text):
    '''
Forest [ah08], forest, in Acaren, wilderness
The Dark Lands [bk76], forest, in Barun, wilderness
Ocean [aq51], ocean, in Great Sea
Forest [fn23], forest, in Faery
Tunnel [vm89], tunnel, in Undercity
Sewer [z581], sewer, in Plain [az99], hidden
Graveyard [g462], graveyard, in province Forest [bw19]
Rimmon [m19], city, in province Plain [bz28]
Esnar [v96], port city, in province Plain [ar17]

Every location: Name, loc_id, kind, outer thing (region or province or ...)
Optional: civ-level (normal-world provinces only), hidden
 Things are either province-sized or sublocs
 Undercity chambers have civ levels? like normal provinces

Some things are lies. Sewer z581 connects to a city, not the province it's allegedly in.
This matters for things like visions, where we haven't seen the enclosing thing.
The main problem here is the kind of the enclosure, which can be renamed.

    '''

    m = re.match(r'^([^[]{1,40}?) \[(.{3,6}?)\], ([^,]*?), in (.*)', text)
    if not m:
        raise ValueError('Failed to find first line of location in text '+text)
    loc_name, loc_id, kind, rest_str = m.group(1, 2, 3, 4)
    loc_int = to_int(loc_id)
    # kind = terrain or 'city' or 'port city'
    # rest is a comma-separated list: region or province, hidden, wilderness|civ-N, safe haven
    rest = [s.strip() for s in rest_str.split(',')]
    enclosing = rest.pop(0)
    m = re.search(r'\[(.{3,6}?)\]', enclosing)
    if m:
        enclosing_id = m.group(1)
        enclosing_int = to_int(enclosing_id)
        region = 'Unknown'  # region is only unknown if it doesn't matter
    else:
        enclosing_id = ''
        enclosing_int = 0
        region = enclosing
        global regions_set
        regions_set.add(region)
    civ = 0
    safe_haven = 0
    hidden = 0
    if len(rest) > 1:
        for r in rest:
            if r == 'wilderness':
                civ = 0
                break
            m = re.match(r'civ-(\d)', r)
            if m:
                civ = m.group(1)
                break
            if r == 'safe haven':
                safe_haven = 1
                break
            if r == 'hidden':
                hidden = 1
                break
            raise ValueError('unknown rest in parse_location_top: {}, text is {}'.format(r, text))

    return [loc_name, loc_int, kind, enclosing_int, region, civ, safe_haven, hidden]  # make me a thingie


def parse_a_structure(parts):
    kind = parts.pop(0).strip()
    if kind.endswith('-in-progress'):
        kind = kind.replace('-in-progress', '')

    attr = {}
    SL = {}
    for p in parts:
        p = p.strip()
        if p.endswith('% completed'):
            SL['er'] = [structure_er[kind]]
            SL['eg'] = [str(int(int(structure_er[kind]) * int(p.replace('% completed', '')) / 100))]
        elif p.endswith('% damaged'):
            SL['da'] = [p.replace('% damage', '')]
        elif p.startswith('defense '):
            SL['df'] = [p.replace('defense ', '')]
        elif p.startswith('depth '):
            SL['sd'] = [int(p.replace('depth ', '')) * 3]
        elif p.startswith('level '):
            SL['cl'] = p.replace('level ', '')
        elif p.endswith('% loaded'):
            pass  # nothing useful to do with loaded %
        elif p.startswith('"') and p.endswith('"'):
            continue
        elif p == 'owner:':
            continue
        else:
            raise ValueError('Unknown structure part parsing {}'.format(p))
    attr['SL'] = SL
    return kind, attr


def parse_a_sublocation_route(parts):
    '''
   Wildefort [h63], port city, safe haven, 1 day
   Graveyard [m656], graveyard, hidden, 1 day
   Battlefield [j195], battlefield, hidden, 1 day
    '''
    kind = parts.pop(0).strip()
    if kind == 'port city':
        kind = 'city'

    if kind not in subloc_kinds:
        raise ValueError('invalid kind of a sublocation route, '+kind)

    attr = {}

    for p in parts:
        p = p.strip()
        if p == '1 day':
            continue
        elif p == 'hidden':
            attr['LO'] = {}
            attr['LO']['hi'] = ['1']
        elif p == 'safe haven':
            attr['SL'] = {}
            attr['SL']['sh'] = ['1']
        elif p == 'owner:':
            continue
        elif p == '""':
            continue
        else:
            raise ValueError('unknown part in a sublocation route: '+p)
    return kind, attr


def parse_a_character(parts):
    attr = {}
    CH = {}
    il = {}
    CM = {}
    MI = {}
    for p in parts:
        p = p.strip()
        if p in noble_ranks:
            CH['ra'] = [noble_ranks[p]]
        elif p.startswith('"') and p.endswith('"'):
            continue
        elif p == 'accompanied by:':
            continue
        elif p == 'prisoner':
            CH['pr'] = ['1']
        elif p == 'garrison':
            CM['dg'] = ['1']
            MI['ca'] = ['g']
            # controlling castle gc set elsewhere
            continue
        elif p == 'on guard':
            CH['gu'] = ['1']
            continue
        elif p == 'flying':
            continue
        elif p == 'priest':
            continue  # XXXv0
        elif p == 'demon lord':
            continue  # XXXv2 a thing you can summon
        elif p in mage_ranks:
            continue
        elif (p in item_to_inventory or
              p.endswith('s') and p[:-1] in item_to_inventory):
            continue  # npcs like savages, or controlled npcs like savage XXXv2
        elif p.startswith('number: '):
            continue  # definitely not a controlled npc
        else:
            if p.startswith('with '):
                p = p.replace('with ', '')
            if p.startswith('wearing '):
                p = p.replace('wearing ', 'one ')
            if p.startswith('wielding '):
                p = p.replace('wielding ', 'one ')
            count, _, item = p.partition(' ')
            count = count.replace(',', '')
            if count in numbers:
                count = numbers[count]
            try:
                count = int(count)
            except ValueError:
                raise ValueError('Error parsing count in '+p+', parts is '+repr(parts))
            if '[' in item:  # a unique item
                id = parse_an_id(item)
            else:
                if item not in item_to_inventory and item.endswith('s'):
                    if item[:-1] in item_to_inventory:
                        item = item[:-1]
                try:
                    id = item_to_inventory[item]
                except KeyError:
                    raise KeyError('invalid key with parts: '+repr(parts))
            il[id] = [str(count)]
    if len(il) > 0:
        attr['il'] = il
    if len(CH) > 0:
        attr['CH'] = CH
    if len(CM) > 0:
        attr['CM'] = CM
    if len(MI) > 0:
        attr['MI'] = MI
    return 'char', attr


def parse_a_structure_or_character(s, previous, last_depth, things):
    '''
    Parse a single structure or character.
    Place in stack context.
    '''
    # if it's mine, there's leading '*'. dump it.
    m = re.match(r'\s+\*', s)
    if m:
        s.replace('*', ' ', 1)

    depth = len(s) - len(s.lstrip(' '))

    parts = s.lstrip(' ').split(', ')  # needs the space due to 1,000+ soldiers etc

    first = parts.pop(0)
    m = re.match('(.*?) \[(.{3,6})\]', first)
    if not m:
        raise ValueError('failed to parse structure/char name in {}'.format(first))
    name, oid = m.group(1, 2)
    oidint = to_int(oid)

    if len(parts) > 0:
        second = parts[0].strip()
        if second in structure_type or second.endswith('-in-progress'):
            kind, thing = parse_a_structure(parts)
        elif second in route_annotations or second in subloc_kinds:
            kind, thing = parse_a_sublocation_route(parts)
            if 'hi' in thing.get('LO', {}):
                print('Subloc {} is hidden'.format(oid))  # XXXv0 this never fires
        else:
            kind, thing = parse_a_character(parts)
    else:
        # it was a naked character name, no inventory
        thing = {}
        kind = 'char'

    if kind == 'char':
        thing['firstline'] = [oidint + ' char 0']
    else:
        if kind == 'galley' or kind == 'roundship':
            loc = ' ship '
        else:
            loc = ' loc '
        if second.endswith('-in-progress'):
            kind = kind + '-in-progress'
        thing['firstline'] = [oidint + loc + kind]
    thing['na'] = [name]
    thing['LI'] = {}

    if last_depth is None or depth > last_depth:
        # I am *under* the previous thing
        where = previous
    elif depth == last_depth:
        # I am *after* the previous thing
        where = things[previous]['LI']['wh'][0]
    elif depth < last_depth:
        # I am *above* the previous thing
        where = things[previous]['LI']['wh'][0]
        where = things[where]['LI']['wh'][0]
    thing['LI']['wh'] = [where]
    box.subbox_append(things, where, 'LI', 'hl', [oidint])

    last_depth = depth

    things[oidint] = thing

    return oidint, last_depth


def parse_routes_leaving(text):
    '''
#   South, to Forest [bx39], Ishdol, 2 days <== ocean<->coast lacks terrain
#   West, to Ocean [bw38], 3 days <== ocean<->ocean lacks terrain, but Ocean can't be renamed
#   West, swamp, to The Dark Lands [cv34], Teysel, 2 days <== this ocean->coast does have terrain?!
#   South, city, to Hornmar [g02], Olbradim, 1 day
#   South, to Swamp [ac21], Olbradim, impassable <== no terrain for city province
#   East, underground, to Hades [rm21], hidden, 7 days
#   Up, to Sewer [z471], Grinter, hidden, 0 days
#   Down, to Tunnel [pz40], hidden, 5 days

#   Secret pass, to Forest [bw22], hidden, 8 days
#   Underground, to Hades [hs70], Hades, hidden, 1 day <== graveyard to hades, this is SL,lt
#   Forest, to The Dark Lands [cz66], Gothin, 1 day <== faery hill to normal world, this is SL,lt
#   To Plain [az03], Grinter, 1 day <== faery hill to normal world, SL,lt

# ship visions only
# 21:    To Osswid's Roundship [6014], 0 days


    1) Fill in outgoing routes from the current location
    2) Intuit boxes for all destinations, so we can fill in the half-seen parts of the map

    parts: direction, terrain, [Tt]o Name [loc], region, hidden, d days?
    '''

    ret = []
    for l in text.split('\n'):
        if ',' not in l:
            continue  # not a route
        # XXXv0 location banner -- should match more generally?
        if 'Notice to mortals' in l:
            continue
        if 'taking this route' in l:
            continue
        parts = l.split(',')
        attr = {}
        saw_loc = 0
        for p in parts:
            p = p.strip()
            if p.lower() in directions:
                attr['dir'] = p.lower()
            elif p.lower() in special_directions:
                attr['special_dir'] = p.lower()
            elif p in geo_inventory:
                attr['kind'] = p
            elif p in route_annotations:
                if p == 'hidden':
                    print('Route to {} is hidden'.format(to_oid(attr['destination'])))
                attr[p] = 1
            elif '[' in p:
                saw_loc = 1
                if p.startswith('to ') or p.startswith('To '):
                    p = p[3:]
                m = re.search('(.*?) \[(.{3,6})\]', p)
                if not m:
                    raise ValueError('failed to match loc in {}'.format(p))
                name, oid = m.group(1, 2)
                attr['name'] = name
                attr['destination'] = to_int(oid)
                if 'kind' not in attr:
                    if name.lower() in geo_inventory:
                        attr['kind'] = name.lower()
                    elif name == 'Hades':
                        attr['kind'] = 'underground'
                    elif '], 0 days' in l:
                        attr['kind'] = 'ship'  # only for visions of ships
                    else:
                        raise ValueError('no kind for link {}'.format(l))
            elif p.endswith(' day') or p.endswith(' days'):
                m = re.match(r'(\d+) days?$', p)
                if not m:
                    raise ValueError('could not parse days out of '+p)
                attr['days'] = m.group(1)
            elif p in regions_set:
                # regions are generally only visible on boundaries.
                # no region = link is to the same region
                attr['region'] = p
            elif saw_loc and p[0] == p[0].upper():
                # we don't know what this is, so let's guess it's a new region
                regions_set.add(p)
                attr['region'] = p
            elif not saw_loc and p[0] == p[0].upper() and p.lower() in geo_inventory:
                # Renamed provinces can lead with the geo
                attr['kind'] = p.lower()
            else:
                raise ValueError('unknown part of {} in line {}'.format(p, l))

        if 'dir' not in attr and 'special_dir' not in attr:
            # faery hill roads lack a direction to normal.
            #  SL,lt from fairy hill to normal; SL,lf from normal to faery hill
            # don't be fooled, faery hills in a normal province appear to be a subloc but that's a lie
            attr['dir'] = 'faery road'

        if 'dir' not in attr:
            if attr['special_dir'] == 'out':
                # a normal subloc
                attr['dir'] = 'out'
            elif attr['special_dir'] == 'underground':
                # Hades roads are 'Underground' direction
                #  SL,lt in graveyard to hades, SL,lf in hades province to graveyard
                attr['dir'] = 'hades road'
            else:
                # actual roads have 2 ids in 'road'
                #  kinda like a subloc, only GA tl points to the other end, GA,rh 1 for hidden
                #  yeah, the 2 things in 'road' don't directly refer to each other
                print('here we are and attr special_dir is', attr['special_dir'])
                attr['dir'] = 'road road'

        if 'destination' not in attr:
            raise ValueError('no destination parsed in'+l)
        if 'days' not in attr and 'impassable' not in attr:
            raise ValueError('no days parsed in'+l)

        if 'special_dir' in attr:
            del attr['special_dir']

        # dir, name, kind, target, days, region(optional), annotations
        ret.append(attr)

    return ret


def parse_inner_locations(idint, text, things):
    '''
   Faery hill [z777], faery hill, 1 day
   Island [g039], island, 1 day
   Wildefort [h63], port city, safe haven, 1 day
   Iche [n15], city, 1 day
   Atnerks' Mine [5948], mine, defense 10, depth 1
   Genius of Love [4415], castle, defense 70, level 4, owner:
      Tom [1753], baron, with 100 workers, six oxen, ten blessed soldiers,
      11 sailors, 122 swordsmen, 227 crossbowmen, seven elite
      archers, accompanied by:
         Eckhart [7584], prisoner
      Unclean University [7341], tower, defense 40
      Astronomy [6629], tower, defense 40, owner:
         Tom [5352]
   Rocky hill [b861], rocky hill, 1 day 
      New tower [6414], tower-in-progress, 57% completed, owner:
         Lazarus the Librarian [6832], "Boss of the BSTC"

    '''

    accumulation = ''
    last_depth = None
    previous = idint

    for l in text.split('\n'):
        l = re.sub('".*?"', '""', l)  # throw out all banners
        l = l.replace('*', ' ')  # XXXv0 don't confuse indentation parser with my characters
        parts = l.split(',')
        continuation = False
        if '[' not in parts[0]:
            continuation = True
        elif accumulation.endswith(','):
            continuation = True
        else:
            # is it an item?
            aparts = accumulation.split(',')
            alast = aparts[-1]
            if ' wearing' in alast or ' wielding' in alast:
                if ']' not in alast:
                    continuation = True

        if continuation:
            # continuation line
            accumulation += ' ' + l.lstrip(' ')
        else:
            if accumulation:
                previous, last_depth = parse_a_structure_or_character(accumulation, previous, last_depth, things)
            accumulation = l
    if accumulation:
        _, _ = parse_a_structure_or_character(accumulation, previous, last_depth, things)

    return things


def parse_market_report(text, include=None):
    ret = []
    for line in text.split('\n'):
        pieces = line.split(maxsplit=5)
        if len(pieces) != 6:
            continue
        trade, who, price, qty, weight, item = pieces
        trade = trade_map.get(trade)
        if trade is None:
            continue  # header lines
        if include is not None:
            if who == '?':  # hidden trader
                continue
            if to_int(who) != include:
                continue
        # if it's my noble, I'll get it in Pending trades
        # if it's not my noble, don't bother
        qty = qty.replace(',', '')
        item = re.findall(r'\[(.*?)\]', item)
        i = item[0]
        is_tradegood = 0
        if i[0].isalpha():
            is_tradegood = 1
            i = to_int(i)
        ret.extend((trade, i, qty, price, '0', '0', '0', '0'))
        # If a city buys/sells, it also produces/consumes 1 => 4, 2 => 3.
        if trade == '1':
            ret.extend(('4', i, qty, price, '0', '0', '0', '0'))
        if trade == '2' and is_tradegood:
            # XXXv2 set tradegoods turns left accurately
            ret.extend(('3', i, qty, price, '0', '0', '0', '36'))
        elif trade == '2':
            ret.extend(('3', i, qty, price, '0', '0', '0', '0'))
    # opium. I'm definintely not going to track, this, let's start
    # by having all cities buy 80 at 17 (max qty, min price)
    ret.extend(('1', '93', '80', '17', '0', '0', '0', '0'))
    ret.extend(('4', '93', '80', '17', '0', '0', '0', '0'))
    # XXXv2 have swamp cities not buy opium
    return ret


def parse_seen_here(text):
    # XXXv0
    return


def parse_ships_sighted(text):
    # XXXv0
    return


def analyze_regions(s, region_after):
    regions = set()
    for line in s.split('\n'):
        if re.match(r'\s', line):
            continue
        reg = line.rstrip()
        for r in regions:
            if region_after.get(r) is None:
                region_after[r] = []
            try:
                region_after[r].index(reg)
            except ValueError:
                region_after[r].append(reg)
        regions.add(reg)


def match_line(text, word, capture=None):
    if capture is None:
        capture = r'(.*)'
    m = re.search(r'\b'+word+'\s+'+capture, text, re.M)
    if not m:
        return None,  # caller expects a list
    return m.groups()


def remove_visions(s):
    '''
    Remove visions from a character report.
    It's hard to figure out where a vision ends, so we do it wrong.

    End is (1) different day (inaccurate) or (2) ' >' (repeat orbing)
    '''
    visions = []
    while True:
        m = re.search(r'^([ \d]\d:) (A vision|.*? receives a vision)', s, re.M)
        if m:
            day = m.group(1)
            kind = m.group(2)
            string = '^{} {} .*'.format(day, kind)
            string = string.replace('[', '\\[')
            string = string.replace(']', '\\]')
            clip = re.search(string, s, re.M | re.S)
            if clip:
                lines = clip.group(0).split('\n')
                wholeday = ''
                for l in lines:
                    if l.startswith(day):
                        wholeday += l + '\n'
                    else:
                        break
                s = s.replace(wholeday, '')
                visions = [wholeday]
                # XXXv2 further processing to split same-day orbs
        else:
            break

    return s, visions


def remove_days(s):
    '''
    Remove anything with a day
    '''
    lines = s.split('\n')
    days = ''
    nondays = ''
    for l in lines:
        m = re.match(r'[ \d]\d: ', l)
        if m:
            days += l + '\n'
        else:
            nondays += l + '\n'
    return nondays, days


def parse_turn_header(data, turn, everything):
    m = re.search(r'^Olympia (.\S) turn (\d+)', turn, re.M)
    # game = m.group(1)
    turn_num = m.group(2)

    m = re.search(r'^(?:Initial Position )?Report for (.{1,30}) \[(.{3,6})\]', turn, re.M)
    fact_name = m.group(1)
    fact_id = m.group(2)

    m = re.search(r'^Noble points:\s+(\d+) ', turn, re.M)
    nps = m.group(1)

    m = re.search(r'^The next five nobles formed will be:\s+(.*)', turn, re.M)
    next5 = m.group(1).split()
    if everything:
        for uf in next5:
            # destroy box first? XXXv0
            data[uf] = {'firstline': [uf + ' unform 0']}

    m = re.search(r'(\d+) fast study days are left', turn, re.M)
    if m:
        fast_study = m.group(1)
    else:
        fast_study = 0

    m = re.search(r'^Location\s+Stack\n--------\s+-----\n(.*?)\n\n', turn, re.M | re.S)
    if m:  # does not exist in the initial turn :/
        analyze_regions(m.group(1), region_after)

    # this is a complete garrison list (no fog) and accurate castle info
    # all it lacks is inventory, visible or not
    if everything:
        m = re.search(r'^  garr where  men cost  tax forw castle rulers\n[\- ]+\n(.*?)\n\n', turn, re.M | re.S)
        if m:
            analyze_garrison_list(m.group(1), data)

    factint = to_int(fact_id)

    if factint in data:
        kn = data[factint]['PL']['kn']
    else:
        kn = []

    fact = {}
    fact['firstline'] = [factint + ' player pl_regular']
    fact['na'] = [fact_name]

    pl = {}
    pl['np'] = [nps]
    pl['fs'] = [fast_study]
    pl['ft'] = ['1']  # first turn
    pl['lt'] = [turn_num]  # last turn
    pl['kn'] = kn
    pl['un'] = []
    pl['uf'] = next5
    fact['PL'] = pl

    data[factint] = fact
    return factint, turn_num, data


def create_garrison_player(data):
    data['207'] = {'firstline': ['207 player pl_silent'],
                   'na': ['Garrison units'],
                   'PL': {'pw': ['crusty7']}}
    # in the real game 207 has 'uf', however, I think we can safely leave it off


def parse_faction(text, factint, data):
    '''
    claim, admit, hostile|defend|neutral
    '''
    m = re.search(r'^Unclaimed items:\n\n(.*?)\n\n', text, re.M | re.S)
    if m:
        unclaimed_items = parse_inventory(m.group(1), factint, data)
        data[factint]['il'] = reformat_inventory(unclaimed_items)

    m = re.search(r'^Admit permissions:\n\n(.*?)\n\n', text, re.M | re.S)
    if m:
        admits = parse_admit(m.group(1))
        data[factint]['am'] = admits

    m = re.search(r'^Declared attitudes:\n(.*?)\n\n', text, re.M | re.S)
    if m:
        attitudes = parse_attitudes(m.group(1))
        if attitudes.get('neutral'):
            data[factint]['an'] = attitudes['neutral']
        if attitudes.get('defend'):
            data[factint]['ad'] = attitudes['defend']
        if attitudes.get('hostile'):
            data[factint]['ah'] = attitudes['hostile']


def analyze_garrison_list(text, data):
    lines = text.split('\n')
    for l in lines:
        pieces = l.split()
        garr = pieces[0]
        where = to_int(pieces[1])
        castle = to_int(pieces[6])
        firstline = garr + ' char garrison'

        il = ['12', '10']  # if we have to fake it
        if garr in data:
            if ' char garrison' in data[garr]['firstline'][0] and 'il' in data[garr]:
                il = data[garr]['il']

        LI = {'wh': [where]}
        CH = {'lo': ['207'], 'he': ['-1'], 'lk': ['4'], 'gu': ['1'], 'at': ['60'], 'df': ['60']}
        CM = {'dg': ['1']}
        MI = {'ca': ['g'], 'gc': [castle]}
        data[garr] = {'firstline': [firstline], 'il': il, 'LI': LI, 'CH': CH, 'CM': CM, 'MI': MI}
        box.subbox_append(data, '207', 'PL', 'un', [garr], dedup=True)

        # XXXv0 enable this when we are making garrisons from the location report
        # if where not in data:
        #     raise ValueError('garrison from list in loc that does not exist: '+where)
        # box.subbox_append(data, where, 'LI', 'hl', [garr], dedup=True)


def parse_garrison_log(text, data):
    # this is the daily details, not the list
    # XXXv2 need to track all give/get for all time to get hidden contents, esp gold
    pass


potion_to_uk = {'691': '2',  # heal
                '694': '1',  # slavery
                '696': '3'}  # death


def resolve_fake_items(data):
    for item in data:
        if ' item ' in data[item]['firstline'][0] and 'fake' in data[item]:
            oid = to_oid(item)
            for unit in global_days:
                if oid in global_days[unit]:
                    m = re.search(r'^[ \d]\d: (?:Created|Produced one) .*? \['+oid+r'\]\.?$', global_days[unit], re.M)
                    if m:
                        whole = m.group(0)
                        before, _, after = global_days[unit].partition(whole)
                        m = re.findall(r' \> use (\d+)(.*)', before, re.I)
                        if m:
                            # should be a list of tuples, let's grab the last one
                            what, rest = m[-1]
                            if what in potion_to_uk:
                                if data[item]['na'][0].startswith('Fake '):
                                    data[item]['na'] = [data[item]['na'][0][5:]]
                                box.subbox_overwrite(data, item, 'IM', 'uk', potion_to_uk[what])
                            elif what == '894':  # palantir
                                if data[item]['na'][0].startswith('Fake '):
                                    data[item]['na'] = [data[item]['na'][0][5:]]
                                if data[item]['IT']['wt'][0] != '2':
                                    raise ValueError('Wrong weight for palantir')
                                box.subbox_overwrite(data, item, 'IM', 'uk', ['4'])
                            elif what == '851':  # farcast
                                box.subbox_overwrite(data, item, 'IM', 'uk', ['5'])
                                assert len(m) > 1
                                for i in range(len(m)-2, -1, -1):
                                    what, rest = m[i]
                                    if what == '849':
                                        rest = rest.strip()
                                        box.subbox_overwrite(data, item, 'IM', 'pc', [to_int(rest)])
                                        break
                                else:
                                    raise ValueError('Could not find previous farcast to save')
                            elif what == '881':
                                if data[item]['na'][0].startswith('Fake '):
                                    data[item]['na'] = [data[item]['na'][0][5:]]
                                data[item]['firstline'] = [item + ' item auraculum']
                                rest = rest.strip()
                                strength = rest.partition(' ')[0]
                                try:
                                    strength = int(strength)
                                except:
                                    raise ValueError('Error parsing auraculum strength, use 881 '+rest)
                                box.subbox_overwrite(data, item, 'IM', 'au', strength)
                                box.subbox_overwrite(data, unit, 'CM', 'ar', item)
                            else:
                                raise ValueError('Failed to resolve unique item {} despite seeing creation'.format(oid))

                            if 'fake' in data[item]:
                                del data[item]['fake']

            if 'fake' in data[item]:  # did not see it being created
                if data[item]['IT']['wt'][0] == '2':
                    # auraculum or Palantir. Guess palantir.
                    box.subbox_overwrite(data, item, 'IM', 'uk', ['4'])


def resolve_regions(data):
    '''
    At this point all provinces are LI wh a region *string*
    Our info about the order of regions is in regions_set and region_after
    Use that to build an ordered list of regions
    Create the regions
    Change all the region strings in LI wh to integers
    '''


def remove_chars_and_ships(things):
    '''
    Most of the time we are only looking at 'loc' in the turn.
    '''
    nuke = []
    for i in things:
        if (' char ' in things[i]['firstline'][0] or
            ' ship ' in things[i]['firstline'][0]):
            db.unset_where(things, i)
            nuke.append(i)

    for i in nuke:
        del things[i]

loyalty_kind = {'Unsworn': 0, 'Contract': 1, 'Oath': 2, 'Fear': 3, 'Npc': 4, 'Summon': 5}


def parse_character(name, ident, factident, text, data):

    m = re.search(r'^\s+Location:\s+(.*)\n(\s+)(.*)$', text, re.M)
    if m:
        location, whitespace, rest = m.group(1, 2, 3)
        if len(whitespace) > 3:
            # I don't really need to do this since I'm only parsing the first location id
            location += ' ' + rest
        location = parse_an_id(location)
    else:
        raise ValueError('Did not find a location for character '+name+' '+ident)

    lkind, lrate = match_line(text, 'Loyalty:', capture=r'([A-Za-z]+)-(\d+)')
    lkind = str(loyalty_kind[lkind])

    stacked_under, = match_line(text, 'Stacked under:')
    if stacked_under is not None:
        stacked_under = parse_an_id(stacked_under)

    health, = match_line(text, 'Health:')
    if 'getting worse' in health:
        sick = 1
    else:
        sick = 0
    health = re.search(r'\d+|n/a', health).group(0)  # NPCs have health of 'n/a'

    attack, defense, missile = match_line(text, 'Combat:', capture=r'attack (\d+), defense (\d+), missile (\d+)')

    behind, = match_line(text, 'behind', capture=r'(\d+)')

    break_point, = match_line(text, 'Break point:', capture=r'(\d+)')

    concealed, = match_line(text, 'use  638 1')
    if concealed is not None and '(concealing self)' in concealed:
        concealed = 1
        print('Concealed character', ident, 'is actually in location', location)
        if stacked_under is not None:
            print('   and is stacked under', stacked_under)
        # XXXv0 place this hidden character
        # our turn's location data has already been parsed so it's safe to add me
    else:
        concealed = 0
        # we should already be placed in 'location' from earlier in this turn report, XXXv0 check it

    pledged_to, = match_line(text, 'Pledged to:')
    if pledged_to is not None:
        pledged_to_name, pledged_to = match_line(text, 'Pledged to:', capture=r'(.*?) \[(.{4,6})\]')

    current_aura, = match_line(text, 'Current aura:', capture=r'(\d+)')
    maximum_aura, = match_line(text, 'Maximum aura:', capture=r'(\d+)')

    # XXXv2 extract full data from max aura 161 (3+158) and construct a fake auraculum if needed
    aura_artifacts = 0
    plus, = match_line(text, 'Maximum aura:', capture=r'.*?\((.*)\)')
    if plus:
        native_aura, _, aura_artifacts = plus.partition('+')
        if _ != '+':
            raise ValueError('failed parsing Max Aura plus of '+plus)
        aura_artifacts = int(aura_artifacts)
        # XXXv0 eventually figure out if I have an auraculum & how big it is

    m = re.search(r'Declared attitudes:\n(.*?)\n\s*\n', text, re.M | re.S)
    attitudes = {}
    if m:
        attitudes = parse_attitudes(m.group(1))

    m = re.search(r'Skills known:\n(.*?)\n\s*\n', text, re.M | re.S)
    skills = []
    if m:
        skills = parse_skills(m.group(1))

    m = re.search(r'Partially known skills:\n(.*?)\n\s*\n', text, re.M | re.S)
    if m:
        skills_partial = parse_partial_skills(m.group(1))
        skills.extend(skills_partial)

    m = re.search(r'Inventory:\n(.*?)\n\n', text, re.M | re.S)
    inventory = []
    if m:
        inventory = parse_inventory(m.group(1), ident, data)
        inventory = reformat_inventory(inventory)

    m = re.search(r'^Pending trades:\n\n(.*?)\n\s*\n', text, re.M | re.S)
    trades = []
    if m:
        trades = parse_pending_trades(m.group(1))

    # XXXv2: location and stacked under... day 31 it comes from the map, but what about visions? fog/concealed?

    ret = {}
    iint = to_int(ident)
    ret['firstline'] = [iint + ' char 0']
    ret['na'] = [name]
    if len(inventory) > 0:
        ret['il'] = inventory
    if len(trades) > 0:
        ret['tl'] = trades

    ret['LI'] = {}  # will get LI/wh eventually
    print('monkey-patching unit {} LI wh to {}'.format(ident, location))
    ret['LI']['wh'] = [location]  # XXXv0 remove me, should already have been set

    ch = {}
    ch['lo'] = [to_int(factident)]
    ch['he'] = [health]
    if sick:
        ch['si'] = ['1']
    ch['lk'] = lkind
    ch['lr'] = lrate
    if attitudes.get('neutral'):
        ch['an'] = attitudes['neutral']
    if attitudes.get('defend'):
        ch['ad'] = attitudes['defend']
    if attitudes.get('hostile'):
        ch['ah'] = attitudes['hostile']
    if len(skills) > 0:
        ch['sl'] = skills
    if behind != '0':
        ch['bh'] = [behind]
    # guard?
    # time_flying XXXv2 - hard one
    ch['bp'] = [break_point]
    # rank
    ch['at'] = [attack]
    ch['df'] = [defense]
    ch['mi'] = [missile]
    # npc_prog ?!
    # contact XXXv2
    ret['CH'] = ch

    cm = {}
    if concealed:
        cm['hs'] = ['1']
    if pledged_to:
        cm['pl'] = to_int(pledged_to)
    if len(cm):
        ret['CM'] = cm

    # XXXv0 identity of my auraculum
    # in some previous turn report it is "Created %s" after a "use 881"
    # weight is a random number 1,3 -- 2 and 3 unique weights, 1 is ambiguous

    data[to_int(ident)] = ret
    box.subbox_append(data, factident, 'PL', 'un', ident, dedup=True)


def parse_location(s, factint, everything, data):

    m = re.match(r'^(.*?)\n-------------', s)
    if not m:
        raise ValueError('failed to parse location')
    top = m.group(1)
    if top == 'Lore sheets':
        return

    name, idint, kind, enclosing_int, region, civ, safe_haven, hidden = parse_location_top(top)
    if kind == 'port city':
        kind = 'city'

    if idint not in data:
        data[idint] = {'firstline': [idint + ' loc ' + kind],
                       'LI': {'wh': [enclosing_int or region]}}
        if kind in geo_inventory:
            data[idint]['il'] = geo_inventory[kind]
        if kind in province_kinds:
            box.subbox_append(data, idint, 'LO', 'pd', [0, 0, 0, 0])
        if safe_haven:
            box.subbox_overwrite(data, idint, 'SL', 'sh', ['1'])
        if hidden:
            box.subbox_overwrite(data, idint, 'LO', 'hi', ['1'])
            box.subbox_append(data, factint, 'PL', 'kn', idint, dedup=True)

    box.box_overwrite(data, idint, 'na', [name])

    controlling_castle, = match_line(s, 'Province controlled by', capture=r'.*?\[([0-9]{4})\]')

    m = re.search(r'^Routes leaving [^:]*?:\s?\n(.*?)\n\n', s, re.M | re.S)
    if m:
        routes = parse_routes_leaving(m.group(1))

        # Fixup: sewers incorrectly claim they are enclosed by the province... actually city subloc
        if kind == 'sewer':
            for r in routes:
                if r['dir'] == 'out':
                    enclosing_int = r['destination']
                    box.subbox_overwrite(data, idint, 'LI', 'wh', [enclosing_int])
                    break

        make_locations_from_routes(routes, idint, region, data)
        make_direction_routes(routes, idint, kind, data)

    things = {idint: {'LI': {}, 'firstline': ['fake']}}

    m = re.search(r'^Inner locations:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        parse_inner_locations(idint, m.group(1), things)
        # XXXv1 beware: faery hills are inner loc of faery, faery road in normal world
        # locations never change, however, they may be hidden to this faction
        # all buildings are here

    m = re.search(r'^Market report:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        market = parse_market_report(m.group(1), include=idint)
        box.box_overwrite(data, idint, 'tl', market)

    m = re.search(r'^Seen here:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        parse_inner_locations(idint, m.group(1), things)

    m = re.search(r'^Ships sighted:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        parse_inner_locations(idint, m.group(1), things)

    m = re.search(r'^Ships docked at port:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        parse_inner_locations(idint, m.group(1), things)

    # if a non-city garrison was seen, stick controlling_castle in
    # if it's my castle, I'll later fill in the correct gc from the garrison list
    if controlling_castle:
        for i in things:
            if 'ca' in things[i].get('MI', {}):
                box.subbox_overwrite(things, i, 'MI', 'gc', [controlling_castle])

    if not everything:
        remove_chars_and_ships(things)

    hl = things[idint].get('LI', {}).get('hl', [])
    del things[idint]

    for i in things:
        if 'hi' in things[i].get('LO', {}):
            box.subbox_append(data, factint, 'PL', 'kn', i, dedup=True)

    # XXXv0 do something with all this
    # stationary things can be destroyed / unplaced / created / placed at will
    # moving things (chars and ships) should be treated more carefully
    # for i in things:

    return


def parse_in_progress_orders(s, unit, data):
    lines = s.split('\n')
    unit = None
    for l in lines:
        divider = '   # > '
        if l.startswith('unit '):
            unit = l.partition(' ')[2].partition(' ')[0]
        elif l.startswith(divider):
            order_and_remaining = l[len(divider):]
            if '(still executing)' in order_and_remaining:
                order = order_and_remaining.replace('(still executing)', '').lower()
                remaining = '0'
            else:
                m = re.match(r'^(.*) \(executing for ([a-z0-9,]+) more days?\)', order_and_remaining)
                if m:
                    order, remaining = m.group(1, 2)
                    order = order.lower()
                    remaining = remaining.replace(',', '')
                else:
                    raise ValueError('Canot parse a remaining out of '+order_and_remaining)

            if not remaining.isdigit():
                remaining = str(numbers[remaining])
            if remaining == '0':
                remaining = '-1'

            # the following algo does the wrong thing for orders running more than 30 days. whatever.
            splits = global_days[unit].split(': > ')
            start_day = splits[-2][-3:]
            if not start_day.startswith('\n'):
                raise ValueError('Failed to parse an order day: '+start_day)
            start_day = int(start_day[1:])

            last_move_dest = to_int('aa01')
            m = re.search(r'(?:Flying|Travel|Sailing) to .*? \[(.*?)\] will take (?:.+) days?\.', splits[-1])
            if m:
                last_move_dest = to_int(m.group(1))

            co = fake_order(order, start_day, remaining, last_move_dest, unit, data)
            data[unit]['CO'] = co

def parse_turn(turn, data, everything=True):

    factint, turn_num, data = parse_turn_header(data, turn, everything)

    char_sections = {}
    in_progress_sections = {}

    for s in split_into_sections(turn):
        while True:
            m = re.match(r'^([^\[]{1,40}) \[(.{3})\]\n---------------', s)
            if m:
                name, ident = m.group(1, 2)
                parse_faction(s, factint, data)
                break
            m = re.match(r'^Garrison log\n-------------', s)
            if m:
                if not everything:
                    break
                parse_garrison_log(s, data)
                break
            m = re.match(r'^([^\[]{1,40}) \[(.{4,6})\]\n--------------', s)
            if m:
                name, ident = m.group(1, 2)

                # XXXv2visions need to be processed prior to *all* day 31 processing!
                # (which, currently, is not possible without a lot of rearrangement)
                s, visions = remove_visions(s)

                s, days = remove_days(s)
                if len(days):
                    if ident not in global_days:
                        global_days[ident] = ''
                    global_days[ident] += days

                if not everything:
                    break
                char_sections[ident] = [name, ident, factint, s]
                break
            m = re.search(r'\[.{3,6}?\].*?\n-------------', s)
            if m:
                parse_location(s, factint, everything, data)
                break

            m = re.search(r'^Order template\n------------', s)
            if m:
                if not everything:
                    break
                in_progress_sections[ident] = s
                break

            # skip the rest: lore sheets, new players
            break

    for i in char_sections:
        name, ident, factint, s = char_sections[i]
        parse_character(name, ident, factint, s, data)
    for i in in_progress_sections:
        parse_in_progress_orders(in_progress_sections[i], i, data)


def parse_turn_from_file(f, data):
    turn = ''.join(line.expandtabs() for line in f)
    turn.replace('\r\n', '\n')

    parse_turn(turn, data)

if __name__ == '__main__':
    data = {}
    for filename in sys.argv[1:]:
        print('\nbegin filename', filename, '\n')
        with open(filename, 'r') as f:
            parse_turn_from_file(f, data)

# XXXv2 storms from the location map
# It is raining.
#    Rain [144478], storm, strength 1
# XXXv2 storm owner from turn
# storm  kind  owner   loc  strength
# -----  ----  -----  ----  --------
# 82999  wind   8012  aq99     19
# XXXv2 walk global_days to find if it's bound
# XXXv2 random storms on map

# XXXv2 seek and contact

# XXXv0 unplace / promote_children harmful when it's a ship being unplaced

# XXXv0 hidden things don't move, so globally remember where they go

