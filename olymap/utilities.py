#!/usr/bin/python

import olypy.details as details
from collections import defaultdict
from olypy.oid import to_oid
from olymap.detail import long_type_to_display_type
from olymap.detail import long_kind_to_display_kind
from olymap.detail import rank_num_string
from olymap.detail import castle_ind
from olymap.detail import structure_kinds
from olymap.detail import use_key
from olypy.db import loop_here
import math


def get_item_names(box):
    itemz_name = box.get('na', [return_type(box).capitalize()])[0]
    itemz_plural = box['IT'].get('pl', [itemz_name])[0]
    return itemz_name, itemz_plural


def get_item_name(box):
    itemz_name, _ = get_item_names(box)
    return itemz_name


def get_item_plural(box):
    _, itemz_plural = get_item_names(box)
    return itemz_plural


# unit tested
def return_type(box):
    # return 3rd argument of firstlist
    firstline = return_firstline(box)
    _, _, sub_loc = firstline.split(' ', maxsplit=2)
    return sub_loc


def return_short_type(box):
    # return 3rd argument of firstlist
    firstline = return_firstline(box)
    _, _, sub_loc = firstline.split(' ', maxsplit=2)
    try:
        short_type = long_type_to_display_type[sub_loc]
    except KeyError:
        short_type = sub_loc
        # try kind
        if sub_loc not in details.subloc_kinds:
            if is_road_or_gate(box):
                if return_kind(box) == 'gate':
                    short_type = 'gate'
                else:
                    name = box['na'][0]
                    try:
                        short_type = long_kind_to_display_kind[name]
                    except KeyError:
                        print('missing short_type for {}'.format(name))
                        pass
        else:
            if len(short_type) > 7:
                print('missing short_type for {}'.format(sub_loc))
    return short_type


# unit tested
def return_kind(box):
    # return 2nd argument of firstlist
    firstline = return_firstline(box)
    _, kind, _ = firstline.split(' ', maxsplit=2)
    return kind


# unit tested
def return_unitid(box):
    # return 1st argument of firstlist
    firstline = return_firstline(box)
    unitid, _, _ = firstline.split(' ', maxsplit=2)
    return unitid


# unit tested
def return_firstline(box):
    # return firstlist from lib entry
    # firstline
    firstline = box['firstline'][0]
    return firstline


# unit tested
def xlate_rank(box):
    rank = 'undefined'
    if 'CH' in box and 'ra' in box['CH']:
        # could be a dict, but doing this for now because
        # rank can be a range??
        try:
            rank = rank_num_string[box['CH']['ra'][0]]
        except KeyError:
            pass
    return rank


# unit tested
def xlate_loyalty(box):
    # translate loyalty
    loyalty = 'Undefined'
    if 'CH' in box and 'lk' in box['CH']:
        if box['CH']['lk'][0] == '0':
            loyalty = 'Unsworn'
        elif box['CH']['lk'][0] == '1' and 'lr' in box['CH']:
            loyalty = 'Contract-' + box['CH']['lr'][0]
        elif box['CH']['lk'][0] == '2' and 'lr' in box['CH']:
            loyalty = 'Oath-' + box['CH']['lr'][0]
        elif box['CH']['lk'][0] == '3' and 'lr' in box['CH']:
            loyalty = 'Fear-' + box['CH']['lr'][0]
        elif box['CH']['lk'][0] == '4' and 'lr' in box['CH']:
            loyalty = 'Npc-' + box['CH']['lr'][0]
        elif box['CH']['lk'][0] == '5':
            loyalty = 'Summon'
        else:
            loyalty = 'Undefined'
    return loyalty


# unit tested
def is_fighter(box):
    attack = ''
    defense = ''
    missile = ''
    if 'IT' in box:
        if 'at' in box['IT']:
            attack = box['IT']['at'][0]
        if 'df' in box['IT']:
            defense = box['IT']['df'][0]
        if 'mi' in box['IT']:
            missile = box['IT']['mi'][0]
    if attack != '' or defense != '' or missile != '' or return_unitid(box) == '18':
        return True
    return False


# unit tested
def is_magician(box):
    if box.get('CM', {}).get('im', [None]):
        if box.get('CM', {}).get('im', [None])[0] == '1':
            return True
    return False


# unit tested
def is_char(box):
    if return_kind(box) == 'char':
        return True
    return False


# unit tested
def is_graveyard(box):
    if is_loc(box) and return_type(box) == 'graveyard':
        return True
    return False


# unit tested
def is_faeryhill(box):
    if is_loc(box) and return_type(box) == 'faery hill':
        return True
    return False


# unit tested
def is_loc(box):
    if return_kind(box) == 'loc':
        return True
    return False


# unit tested
def is_item(box):
    if return_kind(box) == 'item':
        return True
    return False


# unit tested
def is_ship(box):
    if return_kind(box) == 'ship':
        return True
    return False


# unit tested
def is_player(box):
    if return_kind(box) == 'player':
        return True
    return False


# unit tested
def is_city(box):
    if is_loc(box) and return_type(box) == 'city':
        return True
    return False


# unit tested
def is_skill(box):
    if return_kind(box) == 'skill':
        return True
    return False


# unit tested
def is_garrison(box):
    if is_char(box) and return_type(box) == 'garrison':
        return True
    return False


# unit tested
def is_castle(box):
    if is_loc(box) and return_type(box) == 'castle':
        return True
    return False


# unit tested
def is_region(box):
    if is_loc(box) and return_type(box) == 'region':
        return True
    return False


# unit tested
def is_road_or_gate(box):
    if 'GA' in box:
        if 'tl' in box['GA']:
            return True
    return False


def resolve_all_pledges(data):
    ret = defaultdict(list)
    for unit in data:
        unit_box = data[unit]
        if is_char(unit_box):
            pl = data[unit].get('CM', {}).get('pl', [None])[0]
            if pl and pl is not [None]:
                ret[pl].append(unit)
    return ret


def resolve_castles(data):
    ret2 = defaultdict(list)
    for unit in data:
        unit_rec = data[unit]
        if is_castle(unit_rec):
            pl = data[unit]
            if pl:
                ret2[region(unit, data)].append(unit)
    ret = defaultdict(list)
    for reg in ret2:
        castle_list = ret2[reg]
        i = 0
        for castle in castle_list:
            ret[castle].append(castle_ind[i])
            i = i + 1
    return ret


def resolve_bound_storms(data):
    ret = defaultdict(list)
    for unit in data:
        unit_box = data[unit]
        if is_ship(unit_box):
            pl = data[unit].get('SL', {}).get('bs', [None])[0]
            if pl and pl is not [None]:
                ret[pl].append(unit)
    return ret


def resolve_all_prisoners(data):
    ret = defaultdict(list)
    for unit in data:
        unit_box = data[unit]
        if is_char(unit_box):
            pl = data[unit].get('CH', {}).get('pr', [None])[0]
            if pl and pl is not [None]:
                ret[data[unit].get('LI', {}).get('wh', [None])[0]].append(unit)
    return ret


def resolve_hidden_locs(data):
    ret = defaultdict(list)
    for unit in data:
        unit_box = data[unit]
        if is_player(unit_box):
            pl = data[unit].get('PL', {}).get('kn', None)
            if pl and pl is not None:
                for loc in pl:
                    try:
                        loc_rec = data[loc]
                    except KeyError:
                        pass
                    else:
                        if is_loc(loc_rec):
                            ret[loc].append(unit)
    return ret


def resolve_teaches(data):
    ret = defaultdict(list)
    for unit in data:
        unit_box = data[unit]
        if is_city(unit_box):
            pl = data[unit].get('SL', {}).get('te', None)
            if pl and pl is not None:
                for skill in pl:
                    ret[skill].append(unit)
    return ret


def resolve_child_skills(data):
    ret = defaultdict(list)
    for unit in data:
        unit_box = data[unit]
        if is_skill(unit_box):
            pl = data[unit].get('SK', {}).get('rs', None)
            if pl and pl is not None:
                for skill in pl:
                    ret[skill].append(unit)
    return ret


def resolve_garrisons(data):
    ret = defaultdict(list)
    for unit in data:
        unit_box = data[unit]
        if is_garrison(unit_box):
            pl = data[unit].get('MI', {}).get('gc', None)
            if pl and pl is not None:
                for skill in pl:
                    ret[skill].append(unit)
    return ret


def resolve_skills_known(data):
    ret = defaultdict(list)
    for unit in data:
        unit_box = data[unit]
        if is_char(unit_box):
            pl = data[unit].get('CH', {}).get('sl', None)
            if pl and pl is not None:
                for skill in range(0, len(pl), 5):
                    ret[pl[skill]].append(unit)
    for row in ret:
        ret[row].sort()
    return ret


def resolve_trades(data):
    ret = defaultdict(list)
    for unit in data:
        unit_box = data[unit]
        if is_city(unit_box):
            pl = data[unit].get('tl', None)
            if pl is not None:
                for goods in range(0, len(pl), 8):
                    if int(pl[(goods + 1)]) >= 300:
                        if pl[goods] in {'1', '2'}:
                            ret[pl[(goods + 1)]].append([unit, pl[goods]])
    return ret


# unit tested
def loc_depth(loc_type):
    if loc_type == 'region':
        return 1
    elif loc_type in details.province_kinds:
        return 2
    # line below contains code to work around issue in details.subloc_kinds
    elif loc_type in details.subloc_kinds and loc_type != 'sewer':
        return 3
    # details.structure_type does not include 'in-progress' or could use it
    elif loc_type in structure_kinds:
        return 4
    return 0


# unit tested
def region(who, data):
    v = data[who]
    while (int(who) > 0 and
            (not is_loc(v) or loc_depth(return_type(v)) != 1)):
        v = data[v['LI']['wh'][0]]
        who = return_unitid(v)
    return who


# unit tested
def province(who, data):
    v = data[who]
    if loc_depth(return_type(v)) == 1:
        return 0
    while (int(who) > 0 and
            (not is_loc(v) or loc_depth(return_type(v)) != 2)):
        v = data[v['LI']['wh'][0]]
        who = return_unitid(v)
    return who


def top_ruler(k, data):
    cont = True
    while cont:
        top_dog = k
        try:
            v = data[k]
        except KeyError:
            return top_dog
        if 'CM' in v and 'pl' in v['CM']:
                k = v['CM']['pl'][0]
        else:
            cont = False
    return top_dog


# unit tested
def calc_exit_distance(box1, box2):
    if box1 is None or box2 is None:
        return 0
    if return_type(box1) == 'pit' or return_type(box2) == 'pit':
        return 28
    if loc_depth(return_type(box1)) > loc_depth(return_type(box2)):
        tmp = box1
        box1 = box2
        box2 = tmp
    box1_return_type = return_type(box1)
    box2_return_type = return_type(box2)
    # w_d = loc_depth(box1_return_type)
    d_d = loc_depth(box2_return_type)
    if d_d == 4:
        return 0
    if d_d == 3:
        return 1
    if is_ocean(box1) and not is_ocean(box2):
        return 2
    if not is_ocean(box1) and is_ocean(box2):
        return 2
    #
    # skipping province logic for now
    #
    if is_ocean(box2):
        return 3
    elif is_mountain(box2):
        return 10
    elif box2_return_type == 'forest':
        return 8
    elif box2_return_type == 'swamp':
        return 14
    elif box2_return_type == 'desert':
        return 8
    elif box2_return_type == 'plain':
        return 7
    elif box2_return_type == 'underground':
        return 7
    elif box2_return_type == 'cloud':
        return 7
    elif box2_return_type == 'tunnel':
        return 5
    elif box2_return_type == 'chamber':
        return 5
    return 0


# unit tested
def is_port_city(box, data):
    if not is_city(box):
        return False
    province = data[box['LI']['wh'][0]]
    if is_mountain(province):
        return False
    province_list = province['LO']['pd']
    for pd in province_list:
        if int(pd) > 0:
            dest_box = data[pd]
            if is_ocean(dest_box):
                return True
    return False


# unit tested
def province_has_port_city(box, data):
    if 'LI' in box and 'hl' in box['LI']:
        here_list = box['LI']['hl']
        for here in here_list:
            try:
                here_box = data[here]
            except KeyError:
                pass
            else:
                if is_port_city(here_box, data):
                    return here
    return None


# unit tested
def is_priest(box):
    if 'CH' in box:
        if 'sl' in box['CH']:
            skills_list = box['CH']['sl']
            if len(skills_list) > 0:
                for skill in range(0, len(skills_list), 5):
                    if skills_list[skill] == '750':
                        if skills_list[skill + 1] == '2':
                            return True
    return False


# unit tested
def xlate_magetype(box, data):
    if is_magician(box):
        max_aura = get_max_aura(box)
        auraculum_aura = 0
        if get_auraculum_id(box) is not None:
            auraculum_box = data[get_auraculum_id(box)]
            auraculum_aura = get_auraculum_aura(auraculum_box)
            if auraculum_aura is None:
                auraculum_aura = 0
            else:
                auraculum_aura = int(auraculum_aura)
        mage_level = max_aura + auraculum_aura
        if mage_level <= 5:
            return None
        elif mage_level <= 10:
            return 'Conjurer'
        elif mage_level <= 15:
            return 'Mage'
        elif mage_level <= 20:
            return 'Wizard'
        elif mage_level <= 30:
            return 'Sorcerer'
        elif mage_level <= 40:
            return '6th Black Circle'
        elif mage_level <= 50:
            return '5th Black Circle'
        elif mage_level <= 60:
            return '4th Black Circle'
        elif mage_level <= 70:
            return '3rd Black Circle'
        elif mage_level <= 80:
            return '2nd Black Circle'
        else:
            return 'Master of the Black Arts'
        return ''
    else:
        return None


# unit tested
def xlate_use_key(k):
    try:
        ret = use_key[k]
    except KeyError:
        ret = 'undefined'
    return ret


def calc_ship_pct_loaded(data, k, box):
    if not is_ship(box):
        return 0
    total_weight = 0
    damaged = get_ship_damage(box)
    level = 0
    seen_here_list = loop_here(data, k, False, True)
    list_length = len(seen_here_list)
    if list_length > 1:
        for un in seen_here_list:
            char = data[un]
            if is_char(char):
                unit_type = '10'
                if 'CH' in char and 'ni' in char['CH']:
                    unit_type = char['CH']['ni'][0]
                base_unit = data[unit_type]
                item_weight = get_item_weight(base_unit)
                total_weight = total_weight + item_weight
                if 'il' in char:
                    item_list = char['il']
                    for itm in range(0, len(item_list), 2):
                        itemz = data[item_list[itm]]
                        item_weight = get_item_weight(itemz)
                        qty = int(item_list[itm + 1])
                        total_weight = total_weight + int(qty * item_weight)
    ship_capacity = get_ship_capacity(box)
    actual_capacity = ship_capacity - ((ship_capacity * damaged) // 100)
    pct_loaded = math.floor((total_weight * 100) / actual_capacity)
    return pct_loaded


def get_name(box, data, qty=None):
    if 'na' in box:
        name = box['na'][0]
        if qty and qty > 1:
            name = get_item_plural(box)
    else:
        name = return_type(box)
        if name.islower():
            name = name.capitalize()
    if name == 'Ni':
        name = data[box['CH']['ni'][0]]['na'][0].capitalize()
    return name


def get_oid(k):
    return to_oid(k)


def get_type(box, data):
    if return_type(box) == 'ni':
        # char_type = box['na'][0].lower()
        type = data[box['CH']['ni'][0]]['na'][0]
    else:
        type = return_type(box)
    return type


# unit tested
def is_absorb_aura_blast(box):
    if 'CH' in box and 'sl' in box['CH']:
        skills_list = box['CH']['sl']
        if int(len(skills_list)) > 0:
            for skill in range(0, len(skills_list), 5):
                if skills_list[skill] == '909':
                    if skills_list[skill + 1] == '2':
                        return True
    return False


# unit tested
def is_prisoner(box):
    if 'CH' in box and 'pr' in box['CH'] and box['CH']['pr'][0] == '1':
        return True
    return False


# unit tested
def is_on_guard(box):
    if 'CH' in box and  'gu' in box['CH'] and box['CH']['gu'][0] == '1':
        return True
    return False


# unit tested
def is_concealed(box):
    if 'CH' in box and 'hs' in box['CH'] and box['CH']['hs'][0] == '1':
        return True
    return False


def loop_here2(data, where, level=0, fog=False, into_city=False, char_only=False, kind=None):
    '''
    Make a list of everything here: chars, structures, sublocs. Do not descend into big sublocs (cities)
    If fog, make a list of only the visible things
    (caller responsible for making sure that fog=True only for provinces)
    '''
    hls = []
    if 'LI' in data[where] and 'hl' in data[where]['LI']:
        for w in data[where]['LI']['hl']:
            w_box = data[w]
            if kind is None or (kind is not None and level == 0 and return_kind(data[w]) == kind):
                pass
            else:
                continue
            if char_only and not is_char(w_box):
                continue
            if fog and is_char(w_box):
                continue
            hls.append([w, level])
            firstline = data[w]['firstline'][0]
            if ' loc city' in firstline and not into_city:
                # do not descend into cities
                continue
            [hls.append(x) for x in loop_here2(data, w, level + 1)]
    return hls


# unit tested
def get_who_has(box, data):
    who_has_id = box.get('IT', {}).get('un', [None])[0]
    if who_has_id is not None:
        who_has_box = data[who_has_id]
        who_has_dict = {'id': who_has_id,
                        'oid': to_oid(who_has_id),
                        'name': get_name(who_has_box, data)}
        return who_has_dict
    return None


# unit tested
def is_prominent(box):
    if box.get('IT', {}).get('pr', [None])[0] == '1':
        return True
    return False


# unit tested
def is_hidden(box):
    if box.get('LO', {}).get('hi', [None])[0] == '1':
        return True
    return False


# unit tested
def is_impassable(box1, box2, direction, data):
    if (is_ocean(box1) and is_mountain(box2)) or \
       (is_mountain(box1) and is_ocean(box2)) or \
       (is_ocean(box1) and not is_ocean(box2) and province_has_port_city(box2, data) is not None) and \
       direction.lower() not in details.road_directions:
        return True
    return False


# unit tested
def get_use_key(box):
    return box.get('IM', {}).get('uk', [None])[0]


# unit tested
def is_projected_cast(box):
    projected_cast = get_use_key(box)
    if projected_cast is None or projected_cast != '5':
        return False
    return True


# unit tested
def is_orb(box):
    orb = get_use_key(box)
    if orb is None or orb != '9':
        return False
    return True


# unit tested
def is_man_item(box):
    if box.get('IT', {}).get('mu', [None])[0] == '1':
        return True
    return False


# unit tested
def is_ocean(box):
    if is_loc(box) and return_type(box) == 'ocean':
        return True
    return False


# unit tested
def is_mountain(box):
    if is_loc(box) and return_type(box) == 'mountain':
        return True
    return False


# unit tested
def get_auraculum_aura(box):
    return int(box.get('IM', {}).get('au', ['0'])[0])


# unit tested
def get_max_aura(box):
    return int(box.get('CM', {}).get('ma', ['0'])[0])


# unit tested
def get_auraculum_id(box):
    return box.get('CM', {}).get('ar', [None])[0]


# unit tested
def get_ship_capacity(v):
    return int(v.get('SL', {}).get('ca', ['0'])[0])


# unit tested
def get_ship_damage(v):
    return int(v.get('SL', {}).get('da', [0])[0])


# unit tested
def get_item_weight(box):
    return int(box.get('IT', {}).get('wt', ['0'])[0])
