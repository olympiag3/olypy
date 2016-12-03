'''
Parse old Olympia text turns into an Olympia database, suitable for simming
'''

import re
import sys

from oid import to_int

# global state
current = {}
mapdata = {}

directions = {'north': 1, 'east': 2, 'south': 3, 'west': 4, 'up': 5, 'down': 6}
inverted_directions = {'north': 3, 'east': 4, 'south': 1, 'west': 2, 'up': 6, 'down': 5}

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

structure_type = set(('castle', 'tower', 'galley', 'roundship', 'temple', 'mine', 'inn'))

structure_er = {
    'castle':  10000,
    'tower':    2000,
    'galley':    250,
    'roundship': 500,
    'temple':   1000,
    'mine':      500,
    'inn':       300,
    'raft':       45}

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
    #'guild' -- generic name for non-land non-ocean sublocs
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
# XXXv0 also get region order from parse_location_top order
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

name_to_inventory = {
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
    'giant biard': '281',
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
    'faery': '293',
    'faeries': '293',
    'hound': '295'
}


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


def parse_inventory(text):
    temp = {}

    for line in text.split('\n'):
        m = re.match(r'\s+([\d,]+)\s+([\w ]+) \[(\d+)\]', line)
        if m:
            qty, name, ident = m.group(1, 2, 3)
            qty = qty.replace(',', '')
            ident = int(ident)  # so we can sort on it
            temp[ident] = qty

    keys = sorted(list(temp.keys()))
    ret = []
    for k in keys:
        ret.extend((str(k), temp[k]))
    return ret


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
            print('unknown rest in parse_location_top:', r, 'text is', text)

    return [loc_name, loc_int, kind, enclosing_int, region, civ, safe_haven, hidden]  # make me a thingie


def parse_a_structure(parts):
    kind = parts.pop(0).strip()
    in_progress = False
    if kind.endswith('-in-progress'):
        in_progress = True
        kind = kind.replace('-in-progress', '')

    attr = {}
    SL = {}
    for p in parts:
        p = p.strip()
        if p.endswith('% completed'):
            SL['er'] = [structure_er[kind]]
            SL['eg'] = [int(structure_er[kind] * int(p.replace('% completed', '')) / 100)]
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
            pass
        elif p == 'owner:':
            pass
        else:
            raise ValueError('Unknown structure part parsing {}'.format(p))
    attr['SL'] = SL
    return attr


def parse_a_character(parts):
    attr = {}
    CH = {}
    il = {}
    for p in parts:
        p = p.strip()
        if p in noble_ranks:
            CH['ra'] = [noble_ranks[p]]
        elif p.startswith('"') and p.endswith('"'):
            pass
        elif p == 'accompanied by:':
            pass
        elif p == 'prisoner':
            CH['pr'] = [1]
        else:
            if p.startswith('with '):
                p = p.replace('with ', '')
            count, _, name = p.partition(' ')
            if count in numbers:
                count = numbers[count]
            count = int(count)
            if name not in name_to_inventory and name.endswith('s'):
                if name[:-1] in name_to_inventory:
                    name = name[:-1]
            id = name_to_inventory[name]
            il[id] = [count]
    if len(il) > 0:
        attr['il'] = il
    if len(CH) > 0:
        attr['CH'] = CH
    return attr

def parse_a_structure_or_character(s, stack, last_depth):
    '''
    Parse a single structure or character.
    Place in stack context.
    '''
    depth = len(s) - len(s.lstrip(' '))

    parts = s.lstrip(' ').split(',')

    first = parts.pop(0)
    m = re.match('(.*?) \[(.{3,6})\]', first)
    if not m:
        print('ack! s=', s)
        raise ValueError('failed to parse structure/char name in {}'.format(first))
    name, oid = m.group(1, 2)
    oidint = to_int(oid)

    if len(parts) > 0:
        second = parts[0].strip()
        if second in structure_type or second.endswith('-in-progress'):
            thing = parse_a_structure(parts)
        else:
            thing = parse_a_character(parts)
    else:
        # it was a naked character name, no inventory
        thing = {}

    if last_depth is None:
        last_depth = depth
    if depth == last_depth:
        stack.append(oidint)
    elif depth > last_depth:
        stack.append('down')
        stack.append(oidint)
    elif depth < last_depth:
        stack.append('up')
        stack.append(oidint)
    last_depth = depth

    return oidint, thing, last_depth


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
                print('unknown part of', p, 'in line', l)
        if 'dir' not in attr and 'special_dir' not in attr:
            # faery hill roads lack a direction to normal.
            #  SL,lt from fairy hill to normal, SL,lf from normal to faery hill
            #  don't be fooled, faery hills in a normal province appear to be a subloc but that's a lie
            attr['dir'] = 'faery road'
        if 'dir' not in attr:
            if attr['special_dir'] == 'out':
                # a normal subloc
                attr['dir'] = 'out'
            elif attr['special_dir'] == 'underground':
                # Hades roads are 'Underground' direction
                #  SL,lt in graveyard to hades, SL,lf in hades province to graveyard
                attr['dir'] = 'hades road'
            # actual roads have 2 ids in 'road'
            #  kinda like a subloc, only GA tl points to the other end, GA,rh 1 for hidden
            #  yeah, the 2 things in 'road' don't directly refer to each other
            attr['dir'] = 'road'

        if 'destination' not in attr:
            raise ValueError('no destination parsed in'+l)
        if 'days' not in attr and 'impassable' not in attr:
            raise ValueError('no days parsed in'+l)

        if 'special_dir' in attr:
            del attr['special_dir']

        # dir, name, kind, target, days, region(optional), annotations
        ret.append(attr)

    return ret


def parse_inner_locations(text):
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

    things = {}
    stack = []
    accumulation = ''
    last_depth = None

    for l in text.split('\n'):
        l = l.replace('\t', '        ')  # 1 tab = 8 spaces
        print('l=', l)
        first, _, _ = l.partition(',')
        if '[' not in first:
            # continuation line
            accumulation += ' ' + l.lstrip(' ')
        else:
            if accumulation:
                oidint, thing, last_depth = parse_a_structure_or_character(accumulation, stack, last_depth)
                things[oidint] = thing
            accumulation = l
    if accumulation:
        oidint, thing, _ = parse_a_structure_or_character(accumulation, stack, last_depth)
        things[oidint] = thing

    return stack, things


def parse_market_report(text):
    ret = []
    for line in text.split('\n'):
        pieces = line.split(maxsplit=5)
        if len(pieces) != 6:
            continue
        trade, who, price, qty, weight, item = pieces
        trade = trade_map.get(trade)
        if trade is None:
            continue  # header lines
        # XXXv0 discard all entries for who != city
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
    m = re.search(r'\s+'+word+'\s+'+capture, text, re.M)
    if not m:
        return None,  # XXX this only works if the caller expects one result
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
                # XXX further processing to split same-day orbs
        else:
            break

    return s, visions


def parse_turn_header(data, turn):
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

    m = re.search(r'(\d+) fast study days are left', turn, re.M)
    if m:
        fast_study = m.group(1)
    else:
        fast_study = 0

    m = re.search(r'^Location\s+Stack\n--------\s+-----\n(.*?)\n\n', turn, re.M | re.S)
    if m:  # does not exist in the initial turn :/
        analyze_regions(m.group(1), region_after)

    # XXXv2 parse garr\s+where... to get cost of garrisons and complete garrison list (no fog, accurate castle info)

    factint = to_int(fact_id)
    fact = {}
    fact['firstline'] = [factint + ' player pl_regular']
    fact['na'] = [fact_name]

    pl = {}
    pl['np'] = [nps]
    pl['fs'] = [fast_study]
    pl['ft'] = ['1']  # first turn
    pl['lt'] = [turn_num]  # last turn
    pl['kn'] = []  # to be filled in later
    pl['un'] = []
    pl['uf'] = next5
    fact['PL'] = pl

    data[factint] = fact  # XXXv0 should be labled with turn
    return factint, turn_num, data


def parse_faction(text):
    '''
    claim, admit, hostile|defend|neutral
    '''
    ret = {}

    m = re.search(r'^Unclaimed items:\n\n(.*?)\n\n', text, re.M | re.S)
    if m:
        unclaimed_items = parse_inventory(m.group(1))
        ret['il'] = unclaimed_items

    m = re.search(r'^Admit permissions:\n\n(.*?)\n\n', text, re.M | re.S)
    if m:
        admits = parse_admit(m.group(1))
        ret['am'] = admits

    m = re.search(r'^Declared attitudes:\n(.*?)\n\n', text, re.M | re.S)
    if m:
        attitudes = parse_attitudes(m.group(1))
        if attitudes.get('neutral'):
            ret['an'] = attitudes['neutral']
        if attitudes.get('defend'):
            ret['ad'] = attitudes['defend']
        if attitudes.get('hostile'):
            ret['ah'] = attitudes['hostile']

    return ret


def parse_garrison_log(text):
    # XXXv2
    # need to track all give/get for all time to get hidden contents, esp gold
    return {}

loyalty_kind = {'Unsworn': 0, 'Contract': 1, 'Oath': 2, 'Fear': 3, 'Npc': 4, 'Summon': 5}


def parse_character(name, ident, factident, text):
    # dead characters have no loyalty
    # TODOv2 make a body... but it's hard to figure out where to put the body
    loyalty, = match_line(text, 'Loyalty:')
    if loyalty is None:
        return

    m = re.search(r'[A-Za-z]+', loyalty)
    lkind = str(loyalty_kind[m.group(0)])
    lrate = re.search(r'\d+', loyalty).group(0)

    health, = match_line(text, 'Health:')
    if 'getting worse' in health:
        sick = 1
    else:
        sick = 0
    health = re.search(r'\d+|n/a', health).group(0)  # NPCs have health of 'n/a'
    attack, defense, missile = match_line(text, 'attack', capture=r'(\d+), defense (\d+), missile (\d+)')
    behind, = match_line(text, 'behind', capture=r'(\d+)')
    break_point, = match_line(text, 'Break point:', capture=r'(\d+)')
    concealed, = match_line(text, 'use  638 1')
    if concealed is not None and '(concealing self)' in concealed:
        concealed = 1
    else:
        concealed = 0
    pledged_to, = match_line(text, 'Pledged to:')
    if pledged_to is not None:
        pledged_to_name, pledged_to = match_line(text, 'Pledged to:', capture=r'(.*?) \[(.{4,6})\]')
    # XXXv2 Pledged to us: ...
    current_aura, = match_line(text, 'Current aura:', capture=r'(\d+)')
    maximum_aura, = match_line(text, 'Maximum aura:', capture=r'(\d+)')

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
        inventory = parse_inventory(m.group(1))

    # TODOv2: scrolls

    m = re.search(r'^Pending trades:\n\n(.*?)\n\s*\n', text, re.M | re.S)
    trades = []
    if m:
        trades = parse_pending_trades(m.group(1))

    # TODOv2: location and stacked under... day 31 it comes from the map, but what about visions? fog/concealed?

    ret = {}
    iint = to_int(ident)
    ret['firstline'] = [iint + ' char 0']
    ret['na'] = [name]
    if len(inventory) > 0:
        ret['il'] = inventory
    if len(trades) > 0:
        ret['tl'] = trades

    ret['LI'] = {}  # will get LI/wh eventually

    ch = {}
    ch['lo'] = [to_int(factident)]
    ch['he'] = [health]
    if sick:
        ch['si'] = [1]
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
    # prisoner
    # moving - hard one
    # behind
    # guard
    # time_flying XXXv2 - hard one
    if break_point:
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
        cm['hs'] = [1]
    if pledged_to:
        cm['pl'] = to_int(pledged_to)
    if len(cm):
        ret['CM'] = cm

    return ret


def parse_location(s):

    m = re.match(r'^(.*?)\n-------------', s)
    if not m:
        print('failed to parse location, s is', s)
    top = m.group(1)
    if top == 'Lore sheets':
        return
    name, idint, kind, enclosing_int, region, civ, safe_haven, hidden = parse_location_top(top)

    m = re.search(r'^Routes leaving [^:]*?:\s?\n(.*?)\n\n', s, re.M | re.S)
    if m:
        routes = parse_routes_leaving(m.group(1))

    # XXXv0 if it's a sewer, update enclosing_int to be the city
    # the city id can be found in routes.

    m = re.search(r'^Inner locations:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        stack, things = parse_inner_locations(m.group(1))

    m = re.search(r'^Market report:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        market = parse_market_report(m.group(1))

    m = re.search(r'^Seen here:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        stack, things = parse_inner_locations(m.group(1))

    m = re.search(r'^Ships sighted:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        stack, things = parse_inner_locations(m.group(1))

    m = re.search(r'^Ships docked at port:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        stack, things = parse_inner_locations(m.group(1))

    # XXXv0 do something with all this
    # when constructing actual routes,
    #  faery hills are NOT a subloc of a normal province, they're a road
    #   they are a normal subloc on the faery side

    return


def parse_turn(turn):

    data = {}

    factint, turn_num, data = parse_turn_header(data, turn)

    current['factint'] = factint
    current['turn'] = turn_num

    for s in split_into_sections(turn):
        while True:
            m = re.match(r'^([^\[]{1,40}) \[(.{3})\]\n---------------', s)
            if m:
                name, ident = m.group(1, 2)
                data = parse_faction(s)  # XXXv0 merge data with data
                break
            m = re.match(r'^Garrison log\n-------------', s)
            if m:
                data = parse_garrison_log(s)
                break
            m = re.match(r'^([^\[]{1,40}) \[(.{4,6})\]\n--------------', s)
            if m:
                name, ident = m.group(1, 2)
                s, visions = remove_visions(s)
                # TODOv2 do something with visions
                data = parse_character(name, ident, factint, s)
                break
            m = re.search(r'\[.{3,6}?\].*?\n-------------', s)
            if m:
                data = parse_location(s)
                break

            # skip the rest: lore sheets, new players, order template
            break

    # XXXv0 form the above into characters and locations

    return data


def parse_turn_from_file(f):
    turn = ''.join(f)
    turn.replace('\r\n', '\n')

    data = parse_turn(turn)

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        print('\nbegin filename', filename, '\n')
        with open(filename, 'r') as f:
            parse_turn_from_file(f)
