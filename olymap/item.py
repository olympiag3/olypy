#!/usr/bin/python

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import get_oid, get_name, get_subkind, to_oid, get_who_has, get_use_key
from olymap.utilities import get_auraculum_aura, get_item_weight


def build_complete_item_dict(k, v, data, trade_chain):
    item_dict = {'oid' : get_oid(k),
                 'name' : get_name(v),
                 'subkind' : get_subkind(v, data),
                 'plural' : get_plural(v),
                 'animal' : get_animal(v),
                 'attack' : get_item_attack(v),
                 'aura' : get_auraculum_aura(v),
                 'dead_body_dict': get_dead_body(v, data),
                 'defense' : get_item_defense(v),
                 'fly_capacity' : get_fly_capacity(v),
                 'land_capacity' : get_land_capacity(v),
                 'lore' : get_lore(v),
                 'man_item': get_man_item(v),
                 'may_study_dict': get_may_study(v, data),
                 'missile' : get_item_missile(v),
                 'project_cast' : get_project_cast(v, data),
                 'prominent' : get_prominent(v),
                 'ride_capacity' : get_ride_capacity(v),
                 'use_key' : get_use_key(v),
                 'weight' : get_item_weight(v),
                 'who_has_dict': get_who_has(v, data),
                 'trade_good' : get_trade_good(k, v, data, trade_chain),
                 'magic_info': get_magic_item(data, k, v)}
    return item_dict


def build_basic_item_dict(k, v, data, trade_chain):
    item_dict = {'id': k,
                 'oid' : get_oid(k),
                 'name' : get_name(v),
                 'subkind' : get_subkind(v, data),
                 'plural' : get_plural(v),
                 'animal' : get_animal(v),
                 'attack' : get_item_attack(v),
                 'aura' : get_auraculum_aura(v),
                 'defense' : get_item_defense(v),
                 'fly_capacity' : get_fly_capacity(v),
                 'land_capacity' : get_land_capacity(v),
                 'man_item': get_man_item(v),
                 'missile' : get_item_missile(v),
                 'project_cast': get_project_cast(v, data),
                 'prominent': get_prominent(v),
                 'ride_capacity' : get_ride_capacity(v),
                 'use_key' : get_use_key(v),
                 'weight' : get_item_weight(v),
                 'who_has_dict': get_who_has(v, data),
                 'trade_good' : get_trade_good(k, v, data, trade_chain),
                 'magic_info': get_magic_item(data, k, v)}
    return item_dict


# unit tested
def get_animal(box):
    animal = box.get('IT', {}).get('an', [None])[0]
    if animal == '1':
        return True
    return None


# unit tested
def get_item_attack(v):
    return v.get('IT', {}).get('at', [None])[0]


# unit tested
def get_attack_bonus(v):
    return int(v.get('IM', {}).get('ab', ['0'])[0])


# unit tested
def get_aura_bonus(v):
    return v.get('IM', {}).get('ba', [None])[0]


def get_dead_body(v, data):
    dead_body_id =  v.get('PL', {}).get('un', [None])[0]
    if dead_body_id is not None:
        dead_body_box = data[dead_body_id]
        dead_body_dict = {'id': dead_body_id,
                          'oid': to_oid(dead_body_id),
                          'name': get_name(dead_body_box)}
        return dead_body_dict
    return None


# unit tested
def get_item_defense(v):
    return v.get('IT', {}).get('de', [None])[0]


# unit tested
def get_defense_bonus(v):
    return int(v.get('IM', {}).get('db', ['0'])[0])


# unit tested
def get_fly_capacity(v):
    return v.get('IT', {}).get('fc', [None])[0]


# init tested
def get_land_capacity(v):
    return v.get('IT', {}).get('lc', [None])[0]


# unit tested
def get_lore(v):
    return v.get('IM', {}).get('lo', [None])[0]


# unit tested
def get_man_item(box):
    man_item = box.get('IT', {}).get('mu', [None])[0]
    if man_item == '1':
        return True
    return None


# unit tested
def get_item_missile(v):
    return v.get('IT', {}).get('mi', [None])[0]


# unit tested
def get_missile_bonus(v):
    return int(v.get('IM', {}).get('mb', ['0'])[0])


# unit tested
def get_plural(v):
    plural = v.get('IT', {}).get('pl', [None])[0]
    if plural is None:
        plural = get_name(v)
    return plural


def get_project_cast(v, data):
    projected_cast = v.get('IM', {}).get('pc', [None])
    projected_cast_id = projected_cast[0]
    if projected_cast_id is not None:
        try:
            projected_cast_rec = data[projected_cast_id]
            try:
                region_id = u.region(projected_cast_id, data)
                region_rec = data[region_id]
                region_oid = to_oid(region_id)
                region_name = get_name(region_rec)
            except KeyError:
                region_id = None
                region_oid = None
                region_name = None
            projected_dict = {'id': projected_cast_id,
                              'oid': to_oid(projected_cast_id),
                              'name': get_name(projected_cast_rec),
                              'kind': u.return_kind(projected_cast_rec),
                              'region_id': region_id,
                              'region_oid': region_oid,
                              'region_name': region_name}
        except KeyError:
            projected_dict = {'id': None,
                              'oid': to_oid(projected_cast_id)}
        return projected_dict
    return None


# unit tested
def get_prominent(box):
    prominent = box.get('IT', {}).get('pr', [None])[0]
    if prominent == '1':
        return True
    return None


# unit tested
def get_ride_capacity(v):
    return v.get('IT', {}).get('rc', [None])[0]


def get_trade_good(k, v, data, trade_chain):
    buy_list = []
    sell_list = []
    if trade_chain is not None and u.return_subkind(v) == 'tradegood':
        trade_list = trade_chain[k]
        if len(trade_list) > 0:
            for loc in trade_list:
                loc_rec = data[loc[0]]
                if loc[1] == '1':
                    buy_entry = {'id': loc[0],
                                 'oid': to_oid(loc[0]),
                                 'name': get_name(loc_rec)}
                    buy_list.append(buy_entry)
                else:
                    sell_entry = {'id': loc[0],
                                 'oid': to_oid(loc[0]),
                                 'name': get_name(loc_rec)}
                    sell_list.append(sell_entry)
            trade_dict = {'buy': buy_list,
                          'sell': sell_list}
            return trade_dict
    return None


def get_magic_item(data, item_id, item_rec):
    item_type = u.return_subkind(item_rec)
    if item_type == '0':
        if 'IM' in item_rec and 'uk' in item_rec['IM']:
            use_key = item_rec['IM']['uk'][0]
            if use_key == '2':
                magic_type = 'Healing Potion'
                magic_dict = {'oid': to_oid(item_id),
                              'name': get_name(item_rec),
                              'magic_type': magic_type}
                return magic_dict
            elif use_key == '5':
                loc_kind = 'unknown'
                loc_name = 'target'
                loc_id = ''
                if 'IM' in item_rec and 'pc' in item_rec['IM']:
                    loc_id = item_rec['IM']['pc'][0]
                    try:
                        location = data[loc_id]
                    except KeyError:
                        loc_kind = 'unknown'
                        loc_name = 'target'
                        loc_oid = to_oid(loc_id)
                    else:
                        loc_oid = to_oid(loc_id)
                        if u.return_kind(location) != 'loc':
                            loc_kind = u.return_kind(location)
                        else:
                            loc_kind = 'location'
                        loc_name = get_name(location)
                        loc_id = to_oid(u.return_unitid(location))
                else:
                    loc_id = '(no id)'
                    loc_oid = '(no id)'
                magic_type = 'Projected Cast'
                magic_dict = {'oid': to_oid(item_id),
                              'name': get_name(item_rec),
                              'loc_name': loc_name,
                              'loc_kind': loc_kind,
                              'loc_id': loc_id,
                              'loc_oid': loc_oid,
                              'magic_type': magic_type}
                return magic_dict
    elif item_type == 'scroll':
        magic_type = 'Scroll'
        # need to get skill_name
        magic_dict = {'oid': to_oid(item_id),
                      'name': get_name(item_rec),
                      'magic_type': magic_type,
                      'scroll_dict': get_may_study(item_rec, data)}
        return magic_dict
    elif item_type == 'artifact':
        magic_type = 'Artifact'
        magic_dict = {'oid': to_oid(item_id),
                      'name': get_name(item_rec),
                      'magic_type': magic_type,
                      'artifact_dict': get_item_bonuses(item_rec)}
        return magic_dict
    elif item_type == 'dead body':
        magic_type = 'Dead Body'
        magic_dict = {'oid': to_oid(item_id),
                      'name': get_name(item_rec),
                      'magic_type': magic_type,
                      'dead_body_dict': get_dead_body(item_rec, data)}
        return magic_dict
    elif item_type == 'npc_token':
        magic_type = 'NPC_Token'
        magic_dict = {'oid': to_oid(item_id),
                      'name': get_name(item_rec),
                      'magic_type': magic_type,
                      'dead_body_dict': get_dead_body(item_rec, data)}
        return magic_dict
    elif item_type == 'auraculum':
        magic_type = 'Auraculum'
        magic_dict = {'oid': to_oid(item_id),
                      'name': get_name(item_rec),
                      'magic_type': magic_type,
                      'aura': get_auraculum_aura(item_rec)}
        return magic_dict
    return None


# unit tested
def get_item_bonuses(box):
       artifact_dict = {'attack_bonus': get_attack_bonus(box),
                        'defense_bonus': get_defense_bonus(box),
                        'missile_bonus': get_missile_bonus(box),
                        'aura_bonus': get_aura_bonus(box)}
       return artifact_dict


def get_may_study(box, data):
    skill_id = box.get('IM', {}).get('ms', [None])[0]
    if skill_id is not None:
        try:
            skill_box = data[skill_id]
        except:
            return None
        skill_dict = {'id': skill_id,
                      'oid': to_oid(skill_id),
                      'name': get_name(skill_box),
                      'required_dict' : get_required_study(skill_box, data)}
        return skill_dict
    return None


def get_required_study(box, data):
    skill_id = box.get('SK', {}).get('rs', [None])[0]
    if skill_id is not None:
        try:
            skill_box = data[skill_id]
        except:
            return None
        skill_dict = {'id': skill_id,
                      'oid': to_oid(skill_id),
                      'name': get_name(skill_box)}
        return skill_dict
    return None
