#!/usr/bin/python

import olypy.details as details
from collections import defaultdict
from olypy.oid import to_oid
from olymap.detail import long_type_to_display_type
from olymap.detail import long_kind_to_display_kind
from olymap.detail import rank_num_string
from olymap.detail import castle_ind
from olymap.detail import loc_types
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
                        pass
    return short_type


def return_kind(box):
    # return 2nd argument of firstlist
    firstline = return_firstline(box)
    _, kind, _ = firstline.split(' ', maxsplit=2)
    return kind


def return_unitid(box):
    # return 1st argument of firstlist
    firstline = return_firstline(box)
    unitid, _, _ = firstline.split(' ', maxsplit=2)
    return unitid


def return_firstline(box):
    # return firstlist from lib entry
    # firstline
    firstline = box['firstline'][0]
    return firstline


# def chase_structure(k, data, level, seen_here_list):
#     try:
#         z = data[k]
#     except KeyError:
#         return seen_here_list
#     else:
#         seen_here_list.append((return_unitid(z), level))
#         if 'LI' in z:
#             if 'hl' in z['LI']:
#                 level = level + 1
#                 for here in z['LI']['hl']:
#                     seen_here_list = chase_structure(here, data, level, seen_here_list)
#     return seen_here_list


def xlate_rank(v):
    rank = 'undefined'
    if 'CH' in v and 'ra' in v['CH']:
        # could be a dict, but doing this for now because
        # rank can be a range??
        try:
            rank = rank_num_string[v['CH']['ra'][0]]
        except KeyError:
            pass
    return rank


def xlate_loyalty(v):
    # translate loyalty
    loyalty = 'Undefined'
    if 'CH' in v and 'lk' in v['CH']:
        if v['CH']['lk'][0] == '0':
            loyalty = 'Unsworn'
        elif v['CH']['lk'][0] == '1' and 'lr' in v['CH']:
            loyalty = 'Contract-' + v['CH']['lr'][0]
        elif v['CH']['lk'][0] == '2' and 'lr' in v['CH']:
            loyalty = 'Oath-' + v['CH']['lr'][0]
        elif v['CH']['lk'][0] == '3' and 'lr' in v['CH']:
            loyalty = 'Fear-' + v['CH']['lr'][0]
        elif v['CH']['lk'][0] == '4' and 'lr' in v['CH']:
            loyalty = 'Npc-' + v['CH']['lr'][0]
        elif v['CH']['lk'][0] == '5':
            loyalty = 'Summon'
        else:
            loyalty = 'Undefined'
    return loyalty


def is_fighter(item_record, item_id):
    attack = ''
    defense = ''
    missile = ''
    if 'at' in item_record['IT']:
        attack = item_record['IT']['at'][0]
    if 'df' in item_record['IT']:
        defense = item_record['IT']['df'][0]
    if 'mi' in item_record['IT']:
        missile = item_record['IT']['mi'][0]
    if attack != '' or defense != '' or missile != '' or item_id == '18':
        return True
    return False


def is_magician(char_record):
    if 'CM' in char_record:
        if 'im' in char_record['CM']:
            if char_record['CM']['im'][0] == '1':
                return True
    return False


def is_char(data, unit):
    if return_kind(data[unit]) == 'char':
        return True
    return False


def is_graveyard(data, unit):
    if return_type(data[unit]) == 'graveyard':
        return True
    return False


def is_faeryhill(data, unit):
    if return_type(data[unit]) == 'faery hill':
        return True
    return False


def is_loc(data, unit):
    if return_kind(data[unit]) == 'loc':
        return True
    return False


def is_item(data, unit):
    if return_kind(data[unit]) == 'item':
        return True
    return False


def is_ship(data, unit):
    if return_kind(data[unit]) == 'ship':
        return True
    return False


def is_player(data, unit):
    if return_kind(data[unit]) == 'player':
        return True
    return False


def is_city(data, unit):
    if return_type(data[unit]) == 'city':
        return True
    return False


def is_skill(data, unit):
    if return_kind(data[unit]) == 'skill':
        return True
    return False


def is_garrison(data, unit):
    if return_type(data[unit]) == 'garrison':
        return True
    return False


def is_castle(data, unit):
    if return_type(data[unit]) == 'castle':
        return True
    return False


def is_region(data, unit):
    if return_type(data[unit]) == 'region':
        return True
    return False


def is_road_or_gate(loc_record):
    if 'GA' in loc_record:
        if 'tl' in loc_record['GA']:
            return True
    return False


def resolve_all_pledges(data):
    ret = defaultdict(list)
    for unit in data:
        if is_char(data, unit):
            pl = data[unit].get('CM', {}).get('pl', [None])[0]
            if pl and pl is not [None]:
                ret[pl].append(unit)
    return ret


def resolve_castles(data):
    ret2 = defaultdict(list)
    for unit in data:
        if is_castle(data, unit):
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
        if is_ship(data, unit):
            pl = data[unit].get('SL', {}).get('bs', [None])[0]
            if pl and pl is not [None]:
                ret[pl].append(unit)
    return ret


def resolve_all_prisoners(data):
    ret = defaultdict(list)
    for unit in data:
        if is_char(data, unit):
            pl = data[unit].get('CH', {}).get('pr', [None])[0]
            if pl and pl is not [None]:
                ret[data[unit].get('LI', {}).get('wh', [None])[0]].append(unit)
    return ret


def resolve_hidden_locs(data):
    ret = defaultdict(list)
    for unit in data:
        if is_player(data, unit):
            pl = data[unit].get('PL', {}).get('kn', None)
            if pl and pl is not None:
                for loc in pl:
                    try:
                        loc_rec = data[loc]
                    except KeyError:
                        pass
                    else:
                        if return_kind(loc_rec) == 'loc':
                            ret[loc].append(unit)
    return ret


def resolve_teaches(data):
    ret = defaultdict(list)
    for unit in data:
        if is_city(data, unit):
            pl = data[unit].get('SL', {}).get('te', None)
            if pl and pl is not None:
                for skill in pl:
                    ret[skill].append(unit)
    return ret


def resolve_child_skills(data):
    ret = defaultdict(list)
    for unit in data:
        if is_skill(data, unit):
            pl = data[unit].get('SK', {}).get('rs', None)
            if pl and pl is not None:
                for skill in pl:
                    ret[skill].append(unit)
    return ret


def resolve_garrisons(data):
    ret = defaultdict(list)
    for unit in data:
        if is_garrison(data, unit):
            pl = data[unit].get('MI', {}).get('gc', None)
            if pl and pl is not None:
                for skill in pl:
                    ret[skill].append(unit)
    return ret


def resolve_skills_known(data):
    ret = defaultdict(list)
    for unit in data:
        if is_char(data, unit):
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
        if is_city(data, unit):
            pl = data[unit].get('tl', None)
            if pl is not None:
                for goods in range(0, len(pl), 8):
                    if int(pl[(goods + 1)]) >= 300:
                        if pl[goods] in {'1', '2'}:
                            ret[pl[(goods + 1)]].append([unit, pl[goods]])
    return ret


def loc_depth(loc_type):
    if loc_type == 'region':
        return 1
    elif loc_type in details.province_kinds:
        return 2
    elif loc_type in details.subloc_kinds:
        return 3
    # details.structure_type does not include 'in-progress' or could use it
    elif loc_type in loc_types:
        return 4
    return 0


def region(who, data):
    v = data[who]
    while (int(who) > 0 and
            (return_kind(v) != 'loc' or loc_depth(return_type(v)) != 1)):
        v = data[v['LI']['wh'][0]]
        who = return_unitid(v)
    return who


def province(who, data):
    v = data[who]
    if loc_depth(return_type(v)) == 1:
        return 0
    while (int(who) > 0 and
            (return_kind(v) != 'loc' or loc_depth(return_type(v)) != 2)):
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


def calc_exit_distance(loc1, loc2):
    if loc1 is None or loc2 is None:
        return 0
    if return_type(loc1) == 'pit' or return_type(loc2) == 'pit':
        return 28
    if loc_depth(return_type(loc1)) > loc_depth(return_type(loc2)):
        tmp = loc1
        loc1 = loc2
        loc2 = tmp
    loc1_return_type = return_type(loc1)
    loc2_return_type = return_type(loc2)
    # w_d = loc_depth(loc1_return_type)
    d_d = loc_depth(loc2_return_type)
    if d_d == 4:
        return 0
    if d_d == 3:
        return 1
    if loc1_return_type == 'ocean' and loc2_return_type != 'ocean':
        return 2
    if loc1_return_type != 'ocean' and loc2_return_type == 'ocean':
        return 2
    #
    # skipping province logic for now
    #
    if loc2_return_type == 'ocean':
        return 3
    elif loc2_return_type == 'mountain':
        return 10
    elif loc2_return_type == 'forest':
        return 8
    elif loc2_return_type == 'swamp':
        return 14
    elif loc2_return_type == 'desert':
        return 8
    elif loc2_return_type == 'plain':
        return 7
    elif loc2_return_type == 'underground':
        return 7
    elif loc2_return_type == 'cloud':
        return 7
    elif loc2_return_type == 'tunnel':
        return 5
    elif loc2_return_type == 'chamber':
        return 5
    return 0


def is_port_city(loc, data):
    if return_type(loc) != 'city':
        return False
    province = data[loc['LI']['wh'][0]]
    if return_type(province) == 'mountain':
        return False
    province_list = province['LO']['pd']
    for pd in province_list:
        if int(pd) > 0:
            dest_loc = data[pd]
            if return_type(dest_loc) == 'ocean':
                return True
    return False


def province_has_port_city(loc, data):
    if 'LI' in loc and 'hl' in loc['LI']:
        here_list = loc['LI']['hl']
        for here in here_list:
            try:
                here_loc = data[here]
            except KeyError:
                pass
            else:
                if is_port_city(here_loc, data):
                    return here
    return None


def is_priest(v):
    if 'CH' in v:
        if 'sl' in v['CH']:
            skills_list = v['CH']['sl']
            if len(skills_list) > 0:
                for skill in range(0, len(skills_list), 5):
                    if skills_list[skill] == '750':
                        if skills_list[skill + 1] == '2':
                            return True
    return False


def xlate_magetype(v, data):
    if is_magician(v):
        max_aura = 0
        auraculum_aura = 0
        if 'CM' in v and 'ma' in v['CM']:
            max_aura = int(v['CM']['ma'][0])
            if 'ar' in v['CM']:
                auraculum = data[v['CM']['ar'][0]]
                auraculum_id = v['CM']['ar'][0]
                if 'IM' in auraculum and 'au' in auraculum['IM']:
                    auraculum_aura = int(auraculum['IM']['au'][0])
            mage_level = max_aura + auraculum_aura
            if mage_level <= 5:
                return ''
            elif mage_level <= 10:
                return 'conjurer'
            elif mage_level <= 15:
                return 'mage'
            elif mage_level <= 20:
                return 'wizard'
            elif mage_level <= 30:
                return 'sorcerer'
            elif mage_level <= 40:
                return '6th black circle'
            elif mage_level <= 50:
                return '5th black circle'
            elif mage_level <= 60:
                return '4th black circle'
            elif mage_level <= 70:
                return '3rd black circle'
            elif mage_level <= 80:
                return '2nd black circle'
            else:
                return 'master of the black arts'
        return ''
    else:
        return None


def xlate_use_key(k):
    try:
        ret = use_key[k]
    except KeyError:
        ret = 'undefined'
    return ret


def calc_ship_pct_loaded(data, k, v):
    if return_kind(v) != 'ship':
        return 0
    total_weight = 0
    try:
        damaged = int(v['SL']['da'][0])
    except KeyError:
        damaged = 0
    level = 0
    seen_here_list = loop_here(data, k, False, True)
    list_length = len(seen_here_list)
    if list_length > 1:
        for un in seen_here_list:
            char = data[un]
            if return_kind(char) == 'char':
                unit_type = '10'
                if 'CH' in char and 'ni' in char['CH']:
                    unit_type = char['CH']['ni'][0]
                base_unit = data[unit_type]
                if 'IT' in base_unit and 'wt' in base_unit['IT']:
                    item_weight = int(base_unit['IT']['wt'][0]) * 1
                    total_weight = total_weight + item_weight
                if 'il' in char:
                    item_list = char['il']
                    for itm in range(0, len(item_list), 2):
                        itemz = data[item_list[itm]]
                        try:
                            item_weight = int(itemz['IT']['wt'][0])
                        except KeyError:
                            item_weight = int(0)
                        qty = int(item_list[itm + 1])
                        total_weight = total_weight + int(qty * item_weight)
    ship_capacity = int(v['SL']['ca'][0])
    actual_capacity = int(ship_capacity - ((ship_capacity * damaged) / 100))
    pct_loaded = math.floor((total_weight * 100) / actual_capacity)
    return pct_loaded


def get_name(v, data, qty=None):
    if 'na' in v:
        name = v['na'][0]
        if qty and qty > 1:
            name = get_item_plural(v)
    else:
        name = return_type(v)
        if name.islower():
            name = name.capitalize()
    if name == 'Ni':
        name = data[v['CH']['ni'][0]]['na'][0].capitalize()
    return name


def get_oid(k):
    return to_oid(k)


def get_type(v, data):
    if return_type(v) == 'ni':
        # char_type = v['na'][0].lower()
        type = data[v['CH']['ni'][0]]['na'][0]
    else:
        type = return_type(v)
    return type


def is_absorb_aura_blast(v, data):
    if 'CH' in v and 'sl' in v['CH']:
        skills_list = v['CH']['sl']
        if int(len(skills_list)) > 0:
            for skill in range(0, len(skills_list), 5):
                if skills_list[skill] == '909':
                    if skills_list[skill + 1] == '2':
                        return True
    return False


def is_prisoner(v):
    if 'CH' in v and 'pr' in v['CH'] and v['CH']['pr'][0] == '1':
        return True
    return False


def is_on_guard(v):
    if 'CH' in v and  'gu' in v['CH'] and v['CH']['gu'][0] == '1':
        return True
    return False


def is_concealed(v):
    if 'CH' in v and 'hs' in v['CH'] and v['CH']['hs'][0] == '1':
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
            if kind is None or (kind is not None and level == 0 and return_kind(data[w]) == kind):
                pass
            else:
                continue
            if char_only and not is_char(data, w):
                continue
            if fog and is_char(data, w):
                continue
            hls.append([w, level])
            firstline = data[w]['firstline'][0]
            if ' loc city' in firstline and not into_city:
                # do not descend into cities
                continue
            [hls.append(x) for x in loop_here2(data, w, level + 1)]
    return hls


def get_who_has(item_rec, data):
    if 'un' in item_rec['IT']:
        who_has = item_rec['IT']['un'][0]
        who_rec = data[who_has]
        name = get_name(who_rec, data)
        if name == 'Ni':
            name = data[who_rec['CH']['ni'][0]]['na'][0].capitalize()
        return to_oid(who_has), name
    return None, None


def is_prominent(v):
    if v.get('IT', {}).get('pr', [None])[0] == '1':
        return True
    else:
        return False


def is_hidden(v):
    if v.get('LO', {}).get('hi', [None])[0] == '1':
        return True
    else:
        return False


def is_impassable(loc1, loc2, direction, data):
    if (return_type(loc1) == 'ocean' and return_type(loc2) == 'mountain') or \
       (return_type(loc1) == 'mountain' and return_type(loc2) == 'ocean') or \
       (return_type(loc1) == 'ocean' and return_type(loc2) != 'ocean' and province_has_port_city(loc2, data) is not None) and \
       direction.lower() not in details.road_directions:
        return True
    else:
        return False


def get_use_key(v):
    return v.get('IM', {}).get('uk', [None])


def is_projected_cast(v):
    projected_cast = get_use_key(v)[0]
    if projected_cast is None or projected_cast != '5':
        return False
    else:
        return True


def is_orb(v):
    orb = get_use_key(v)[0]
    if orb is None or orb != '9':
        return False
    else:
        return True


def is_man_item(v):
    if 'IT' in v and 'mu' in v['IT']:
        if v['IT']['mu'][0] == '1':
            return True
    return False
