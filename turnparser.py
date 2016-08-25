'''
Parse old Olympia text turns into an Olympia database, suitable for simming
'''

import re
import sys

from oid import to_int

# global state
current = {}
mapdata = {}

province_type = set(('mountain', 'plain', 'swamp', 'forest', 'desert', 'ocean', 'tunnel'))

directions = {'north': 1, 'east': 2, 'south': 3, 'west': 4, 'up': 5, 'down': 6}
inverted_directions = {'north': 3, 'east': 4, 'south': 1, 'west': 2, 'up': 6, 'down': 5}

structure_type = set(('castle', 'tower', 'galley', 'roundship', 'temple', 'mine', 'inn'))

geo_inventory = {
    'mountain': [ '78', '50', '10', '10', '96', '50', '101', '1', '275', '1' ],
    'plain': [ '51', '5', '10', '10', '96', '50', '101', '1', '275', '1' ],
    'swamp': [ '66', '1', '96', '50', '101', '1', '274', '1' ],
    'forest': [ '77', '30', '10', '10', '96', '50', '101', '1', '276', '1', '274', '1' ],
    'desert': [ '78', '10', '96', '50', '101', '1', '275', '1' ],
    'ocean': [ '59', '30', '87', '50', '274', '1', '275', '1', '276', '1' ],
    'cloud': [ '274', '1', '275', '1', '276', '1' ],
    'underground': [ '101', '1', '96', '50' ],
    'faery hill': [ ],
    'island': [ '59', '30' ],
    'ring of stones': [ ],
    'mallorn grove': [ '65', '2', '70', '2' ],
    'bog': [ '66', '4' ],
    'cave': [ '67', '2' ],
    'city': [ '10', '10', '294', '1', '277', '5', '96', '100', '101', '1' ],
    'lair': [ ],
    'graveyard': [ '31', '15', '273', '1' ],
    'ruins': [ ],
    'battlefield': [ ],
    'enchanted forest': [ ],
    'rocky hill': [ '78', '50' ],
    'circle of trees': [ '77', '5', '64', '3' ],
    'pits': [ '66', '4' ],
    'pasture': [ '51', '5' ],
    'oasis': [ ],
    'yew grove': [ '68', '5' ],
    'sand pit': [ '71', '1' ],
    'sacred grove': [ '77', '5' ],
    'poppy field': [ '93', '25' ],
    'tunnel': [ '101', '1', '96', '50' ],
    'sewer': [ ],
    'chamber': [ '101', '1', '96', '50' ],
}

# regions go from 58760-58999 ... and need to be in the correct order
# this dict is a list of every region which was observed to be after key r
region_after = {}

type_to_region = {
    'ocean': 'Great Sea', # if in main world
    'underground': 'Hades',
    'tunnel': 'Undercity',
    'cloud': 'Cloudlands',
}

has_6_directions = set(('tunnel', 'sewer'))

is_road_direction = set(('Secret pass', 'Secret route', 'Old road',
                         'Narrow channel', 'Rocky channel', 'Secret sea route',
                         'Underground'))

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
    '888': '21',
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
    'buy': '3',
    'sell': '2',
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
    return ret[1:] # discard header

def parse_inventory(text):
    temp = {}

    for line in text.split('\n'):
        m = re.match(r'\s+([\d,]+)\s+([\w ]+) \[(\d+)\]', line)
        if m:
            qty, name, ident = m.group(1,2,3)
            qty = qty.replace(',', '')
            ident = int(ident) # so we can sort on it
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
            if parts[0] == 'neutral':
                last = 'neutral'
                ret[last] = parts[1:]
            elif parts[0] == 'defend':
                last = 'defend'
                ret[last] = parts[1:]
            elif parts[0] == 'hostile':
                last = 'hostile'
                ret[last] = parts[1:]
            else: # continuation line
                ret[last].extend(parts)
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
        print('pieces is', pieces, file=sys.stderr)
        if len(pieces) != 4:
            continue
        trade, price, qty, item = pieces
        trade = trade_map.get(trade)
        if trade is None:
            continue
        qty = qty.replace(',', '')
        item = re.findall(r'\[(.*?)\]', item)
        ret.extend((trade, item[0], qty, price, '0', '0', '0', '0'))
    return ret

def parse_location_top(text):
# Forest [ah08], forest, in Acaren, wilderness
# The Dark Lands [bk76], forest, in Barun, wilderness
# Ocean [aq51], ocean, in Great Sea
# Forest [fn23], forest, in Faery
# Tunnel [vm89], tunnel, in Undercity
# Sewer [z581], sewer, in Plain [az99], hidden
# Graveyard [g462], graveyard, in province Forest [bw19]
# Rimmon [m19], city, in province Plain [bz28]
# Esnar [v96], port city, in province Plain [ar17]

    m = re.match(r'^([^[]{1,40}?) \[(.{3,6}?)\], ([^,]*?), in (.*)', text)
    loc_name, loc_id, kind, rest_str = m.group(1,2,3,4)
    # kind = terrain or 'city' or 'port city'
    # rest is a comma-separated list: region or province, hidden, wilderness|civ-N, safe haven
    rest = [s.strip() for s in rest_str.split(',')]

    loc_int = to_int(loc_id)


    # XXXv0
    return

def parse_routes_leaving(text):
#   South, to Forest [bx39], Ishdol, 2 days <== ocean->coast lacks terrain
#   West, swamp, to The Dark Lands [cv34], Teysel, 2 days <== this ocean->coast does have terrain?!
#   South, city, to Hornmar [g02], Olbradim, 1 day
#   South, to Swamp [ac21], Olbradim, impassable <== no terrain for city province
#   West, to Ocean [bw38], 3 days <== no terrain for ocean->ocean
#   East, underground, to Hades [rm21], hidden, 7 days
#   Underground, to Hades [hs70], Hades, hidden, 1 day <== no terrain for a special direction SL,lt
    # XXXv0
    return

def parse_inner_locations(text):
    # XXXv0
    return

def parse_market_report(text):
    # XXXv0
    return

def parse_seen_here(text):
    # XXXv0
    return

def analyze_regions(s, region_after):
    regions = []
    for line in s.split('\n'):
        if re.match(r'\s', line):
            print('skipping line', line.rstrip())
            continue
        reg = line.rstrip()
        print('line is', reg)
        for r in regions:
            print('r is <{}>'.format(r))
            if region_after.get(r) is None:
                region_after[r] = []
            try:
                region_after[r].index(reg)
            except ValueError:
                region_after[r].append(reg)
        regions.append(reg)

def match_line(text, word, capture=None):
    if capture is None:
        capture = r'(.*)'
    m = re.search(r'\s+'+word+'\s+'+capture, text, re.M)
    if not m:
        return None, # XXX this only works if the caller expects one result
    return m.groups()

def parse_turn_header(data, turn):
    m = re.search(r'^Olympia (.\S) turn (\d+)', turn, re.M)
    game = m.group(1)
    turn_num = m.group(2)

    m = re.search(r'^(?:Initial Position )?Report for (.{1,30}) \[(.{3,6})\]', turn, re.M)
    fact_name = m.group(1)
    fact_id = m.group(2)

    m = re.search(r'^Noble points:\s+(\d+) ', turn, re.M)
    nps = m.group(1)

    m = re.search(r'^The next five nobles formed will be:\s+(.*)', turn, re.M)
    next5 = m.group(1).split()

    m = re.search(r'(\d+) fast study days are left', turn, re.M)
    fast_study = m.group(1)

    m = re.search(r'^Location\s+Stack\n--------\s+-----\n(.*?)\n\n', turn, re.M | re.S)
    if m: # does not exist in the initial turn :/
        analyze_regions(m.group(1), region_after)

    # XXXv2 parse garr\s+where... to get cost of garrisons and complete garrison list (no fog, accurate castle info)

    factint = to_int(fact_id)
    fact = {}
    fact['firstline'] = [factint + ' player pl_regular']
    fact['na'] = [fact_name]

    pl = {}
    pl['np'] = [nps]
    pl['fs'] = [fast_study]
    pl['ft'] = ['1'] # first turn
    pl['lt'] = [turn_num] # last turn
    pl['kn'] = [] # to be filled in later
    pl['un'] = []
    pl['uf'] = next5
    fact['PL'] = pl

    data[factint] = fact # XXXv0 should be labled with turn
    return factint, turn_num, data

def parse_faction(text):
    '''
    claim, admit, hostile|defend|neutral
    '''
    ret = {}

    m = re.search(r'^Unclaimed items:\n\n(.*?)\n\n', text, re.M | re.S)
    unclaimed_items = parse_inventory(m.group(1))
    ret['il'] = unclaimed_items

    m = re.search(r'^Admit permissions:\n\n(.*?)\n\n', text, re.M | re.S)
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

loyalty_kind = {'Unsworn': 0, 'Contract':1, 'Oath':2, 'Fear':3, 'Npc':4, 'Summon':5}

def parse_character(name, ident, factident, text):
    loyalty, = match_line(text, 'Loyalty:')
    lkind = str(loyalty_kind[re.search(r'[A-Za-z]+', loyalty).group(0)])
    lrate = re.search(r'\d+', loyalty).group(0)

    health, = match_line(text, 'Health:')
    if 'getting worse' in health:
        sick = 1
    else:
        sick = 0
    health = re.search(r'\d+', health).group(0)
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
    current_aura, = match_line(text, 'Current aura:', capture=r'(\d+)')
    maximum_aura, = match_line(text, 'Maximum aura:', capture=r'(\d+)')

    m = re.search(r'Declared attitudes:\n(.*?)\n\n', text, re.M | re.S)
    attitudes = {}
    if m:
        attitudes = parse_attitudes(m.group(1))

    m = re.search(r'Skills known:\n(.*?)\n\n', text, re.M | re.S)
    skills = []
    if m:
        skills = parse_skills(m.group(1))

    m = re.search(r'Partially known skills:\n\n(.*?)\n\n', text, re.M | re.S)
    if m:
        skills_partial = parse_partial_skills(m.group(1))
        skills.extend(skills_partial)

    m = re.search(r'Inventory:\n(.*?)\n\n', text, re.M | re.S)
    inventory = []
    if m:
        inventory = parse_inventory(m.group(1))

    # TODOv2: scrolls

    m = re.search(r'^Pending trades:\n\n(.*?)\n\n', text, re.M | re.S)
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
    if attitudes.get('neutral'):
        ret['an'] = attitudes['neutral']
    if attitudes.get('defend'):
        ret['ad'] = attitudes['defend']
    if attitudes.get('hostile'):
        ret['ah'] = attitudes['hostile']

    ret['LI'] = {} # will get LI/wh eventually

    ch = {}
    ch['lo'] = [to_int(factident)]
    ch['he'] = [health]
    if sick:
        ch['si'] = [1]
    ch['lk'] = lkind
    ch['lr'] = lrate
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

# parse_top

# parse_leaving

# guess city province - city come before impassible province link on leaving
# guess terrain - ocean->coast, Hades, 
# guess region - 

    m = re.match(r'^(.*?)\n-------------', s)
    if not m:
        print('s is', s)
    parse_location_top(m.group(1))

    # XXXv2 location-days, e.g. enemy units I don't see at the end of the turn

    m = re.search(r'^Routes leaving .*?:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        parse_routes_leaving(m.group(1))

    m = re.search(r'^Inner locations:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        parse_inner_locations(m.group(1))

    m = re.search(r'^Market report:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        parse_market_report(m.group(1))

    m = re.search(r'^Seen here:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        parse_seen_here(m.group(1))

    m = re.search(r'^Ships docked at port:\n(.*?)\n\n', s, re.M | re.S)
    if m:
        parse_seen_here(m.group(1)) # same thing


    # XXXv0 do something with all this

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
                name, ident = m.group(1,2)
                data = parse_faction(s) # XXXv0 merge data with data
                break
            m = re.match(r'^Garrison log\n-------------', s)
            if m:
                data = parse_garrison_log(s)
                break
            m = re.match(r'^([^\[]{1,40}) \[(.{4,6})\]\n--------------', s)
            if m:
                name, ident = m.group(1,2)
                data = parse_character(name, ident, factint, s)
                break
            #m = re.match(r'^([^[]{1,40}?) \[(.{3,6}?)\], ([^,]*?), in (.*)\n-------------', s)
            m = re.search(r'\[.{3,6}?\].*?\n-------------', s)
            if m:
                data = parse_location(s)
                break

            # skip the rest: lore sheets, new players, order template
            break

    # XXXv0 form the above into characters and locations

    return data

def read_a_turn(f):
    turn = ''.join(f)
    turn.replace('\r\n', '\n')

    data = initial_parse(turn)

if __name__ == '__main__':
    with open('/home/lindahl/game/g4/oleg.099', 'r') as f:
        read_a_turn(f)

