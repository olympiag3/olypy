#!/usr/bin/python

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import get_oid, get_name, get_type, to_oid, get_who_has, get_use_key, get_auraculum_aura
import pathlib
from jinja2 import Environment, PackageLoader, select_autoescape


def build_complete_item_dict(k, v, data, trade_chain):
    who_has_oid, who_has_name = get_who_has(v, data)
    dead_body_id, dead_body_name = get_dead_body(v, data)
    may_study_id, may_study_name = get_may_study(v, data)
    item_dict = {'oid' : get_oid(k),
                 'name' : get_name(v, data),
                 'type' : get_type(v, data),
                 'plural' : get_plural(v, data)[0],
                 'animal' : get_animal(v)[0],
                 'attack' : get_attack(v)[0],
                 'attack_bonus' : get_attack_bonus(v)[0],
                 'aura' : get_auraculum_aura(v),
                 'aura_bonus' : get_aura_bonus(v),
                 'dead_body_oid' : dead_body_id,
                 'dead_body_name' : dead_body_name,
                 'defense' : get_defense(v)[0],
                 'defense_bonus' : get_defense_bonus(v)[0],
                 'fly_capacity' : get_fly_capacity(v)[0],
                 'land_capacity' : get_land_capacity(v)[0],
                 'lore' : get_lore(v)[0],
                 'man_item': get_man_item(v)[0],
                 'may_study_oid' : may_study_id,
                 'may_study_name' : may_study_name,
                 'missile' : get_missile(v)[0],
                 'missile_bonus' : get_missile_bonus(v)[0],
                 'project_cast' : get_project_cast(v, data),
                 'prominent' : get_prominent(v)[0],
                 'ride_capacity' : get_ride_capacity(v)[0],
                 'unit': get_unit(v, data),
                 'use_key' : get_use_key(v),
                 'weight' : get_weight(v)[0],
                 'who_has_oid' : who_has_oid,
                 'who_has_name' : who_has_name,
                 'trade_good' : get_trade_good(k, v, data, trade_chain),
                 'magic_info': get_magic_item(data, k, v)}
    return item_dict


def build_basic_item_dict(k, v, data, trade_chain):
    who_has_oid, who_has_name = get_who_has(v, data)
    item_dict = {'id': k,
                 'oid' : get_oid(k),
                 'name' : get_name(v, data),
                 'type' : get_type(v, data),
                 'plural' : get_plural(v, data)[0],
                 'animal' : get_animal(v)[0],
                 'attack' : get_attack(v)[0],
                 'attack_bonus' : get_attack_bonus(v)[0],
                 'aura' : get_auraculum_aura(v),
                 'aura_bonus' : get_aura_bonus(v),
                 'defense' : get_defense(v)[0],
                 'defense_bonus' : get_defense_bonus(v)[0],
                 'fly_capacity' : get_fly_capacity(v)[0],
                 'land_capacity' : get_land_capacity(v)[0],
                 'man_item': get_man_item(v)[0],
                 'missile' : get_missile(v)[0],
                 'missile_bonus' : get_missile_bonus(v)[0],
                 'project_cast': get_project_cast(v, data),
                 'prominent': get_prominent(v)[0],
                 'ride_capacity' : get_ride_capacity(v)[0],
                 'unit': get_unit(v, data),
                 'use_key' : get_use_key(v),
                 'weight' : get_weight(v)[0],
                 'who_has_oid' : who_has_oid,
                 'who_has_name' : who_has_name,
                 'trade_good' : get_trade_good(k, v, data, trade_chain),
                 'magic_info': get_magic_item(data, k, v)}
    return item_dict


def get_animal(v):
    return v.get('IT', {}).get('an', [None])


def get_attack(v):
    return v.get('IT', {}).get('at', [None])


def get_attack_bonus(v):
    return v.get('IM', {}).get('ab', [None])


def get_aura_bonus(v):
    return v.get('IM', {}).get('ba', [None])[0]


def get_capacities(v):
    return v.get('IT', {}).get('lc', [0]), v.get('IT', {}).get('rc', [0]), v.get('IT', {}).get('fc', [0])


def get_dead_body(v, data):
    oid =  v.get('PL', {}).get('un', [None])
    if oid[0] is not None:
        dead_body_rec = data[oid[0]]
        dead_body_name = get_name (dead_body_rec, data)
        return to_oid(oid[0]), dead_body_name
    return None, None


def get_defense(v):
    return v.get('IT', {}).get('de', [None])


def get_defense_bonus(v):
    return v.get('IM', {}).get('db', [None])


def get_fly_capacity(v):
    return v.get('IT', {}).get('fc', [None])


def get_land_capacity(v):
    return v.get('IT', {}).get('lc', [None])


def get_lore(v):
    return v.get('IM', {}).get('lo', [None])


def get_man_item(v):
    return v.get('IT', {}).get('mu', [None])


def get_may_study(v, data):
    oid = v.get('IM', {}).get('ms', [None])
    if oid[0] is not None:
        skill_rec = data[oid[0]]
        skill_name = get_name(skill_rec, data)
        return to_oid(oid[0]), skill_name
    return None, None


def get_missile(v):
    return v.get('IT', {}).get('mi', [None])


def get_missile_bonus(v):
    return v.get('IM', {}).get('mb', [None])


def get_plural(v, data):
    plural = v.get('IT', {}).get('pl', [None])
    if plural[0] is None:
        plural = [get_name(v, data)]
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
                region_name = get_name(region_rec, data)
            except KeyError:
                region_id = None
                region_oid = None
                region_name = None
            projected_dict = {'id': projected_cast_id,
                              'oid': to_oid(projected_cast_id),
                              'name': get_name(projected_cast_rec, data),
                              'kind': u.return_kind(projected_cast_rec),
                              'region_id': region_id,
                              'region_oid': region_oid,
                              'region_name': region_name}
        except KeyError:
            projected_dict = {'id': None,
                              'oid': to_oid(projected_cast_id)}
        return projected_dict
    return None


def get_prominent(v):
    return v.get('IT', {}).get('pr', [None])


def get_ride_capacity(v):
    return v.get('IT', {}).get('rc', [None])


def get_unit(v, data):
    unit_id = v.get('IT', {}).get('un', [None])[0]
    if unit_id is not None:
        unit_rec = data[unit_id]
        unit_dict = {'id': unit_id,
                     'oid': to_oid(unit_id),
                     'name': get_name(unit_rec, data),
                     'kind': u.return_kind(unit_rec)}
        return unit_dict
    return None


def get_weight(v):
    return v.get('IT', {}).get('wt', [None])


def get_trade_good(k, v, data, trade_chain):
    buy_list = []
    sell_list = []
    if trade_chain is not None and u.return_type(v) == 'tradegood':
        trade_list = trade_chain[k]
        if len(trade_list) > 0:
            for loc in trade_list:
                loc_rec = data[loc[0]]
                if loc[1] == '1':
                    buy_entry = {'id': loc[0],
                                 'oid': to_oid(loc[0]),
                                 'name': get_name(loc_rec, data)}
                    buy_list.append(buy_entry)
                else:
                    sell_entry = {'id': loc[0],
                                 'oid': to_oid(loc[0]),
                                 'name': get_name(loc_rec, data)}
                    sell_list.append(sell_entry)
            trade_dict = {'buy': buy_list,
                          'sell': sell_list}
            return trade_dict
    return None


def get_magic_item(data, item_id, item_rec):
    item_type = u.return_type(item_rec)
    if item_type == '0':
        if 'IM' in item_rec and 'uk' in item_rec['IM']:
            use_key = item_rec['IM']['uk'][0]
            if use_key == '2':
                magic_type = 'Healing Potion'
                magic_dict = {'oid': to_oid(item_id),
                              'name': get_name(item_rec, data),
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
                        loc_name = get_name(location, data)
                        loc_id = to_oid(u.return_unitid(location))
                else:
                    loc_id = '(no id)'
                    loc_oid = '(no id)'
                magic_type = 'Projected Cast'
                magic_dict = {'oid': to_oid(item_id),
                              'name': get_name(item_rec, data),
                              'loc_name': loc_name,
                              'loc_kind': loc_kind,
                              'loc_id': loc_id,
                              'loc_oid': loc_oid,
                              'magic_type': magic_type}
                return magic_dict
    elif item_type == 'scroll':
        skill_name = 'unknown'
        required_study = ''
        required_name = ''
        skill_id = ''
        scroll_id = to_oid(item_id)
        if 'IM' in item_rec and 'ms' in item_rec['IM']:
            skill_id = to_oid(item_rec['IM']['ms'][0])
            try:
                skill = data[item_rec['IM']['ms'][0]]
            except KeyError:
                skill_name = 'unknown'
            else:
                skill_name = get_name(skill, data)
            if 'SK' in skill and 'rs' in skill['SK']:
                try:
                    skill2 = data[skill['SK']['rs'][0]]
                except KeyError:
                    required_name = 'unknown'
                else:
                    required_name = skill2.get('na', ['unknown'])[0]
                    required_study = to_oid(skill['SK']['rs'][0])
        magic_type = 'Scroll'
        magic_dict = {'oid': scroll_id,
                      'name': skill_name,
                      'skill_id': skill_id,
                      'required_study': required_study,
                      'required_name': required_name,
                      'magic_type': magic_type}
        return magic_dict
    elif item_type == 'artifact':
        artifact_dict = {'attack': get_attack_bonus(item_rec)[0],
                         'defense': get_defense_bonus(item_rec)[0],
                         'missile': get_missile_bonus(item_rec)[0],
                         'aura': get_aura_bonus(item_rec)}
        magic_type = 'Artifact'
        magic_dict = {'oid': to_oid(item_id),
                      'name': get_name(item_rec, data),
                      'magic_type': magic_type,
                      'artifact_dict': artifact_dict}
        return magic_dict
    elif item_type == 'dead body':
        magic_type = 'Dead Body'
        db_oid, db_name = get_dead_body(item_rec, data)
        magic_dict = {'oid': to_oid(item_id),
                      'name': get_name(item_rec, data),
                      'magic_type': magic_type,
                      'dead_oid': db_oid,
                      'dead_name': db_name}
        return magic_dict
    elif item_type == 'npc_token':
        magic_type = 'NPC_Token'
        npc_oid, npc_name = get_dead_body(item_rec, data)
        magic_dict = {'oid': to_oid(item_id),
                      'name': get_name(item_rec, data),
                      'magic_type': magic_type,
                      'npc_oid': npc_oid,
                      'npc_name': npc_name}
        return magic_dict
    elif item_type == 'auraculum':
        magic_type = 'Auraculum'
        magic_dict = {'oid': to_oid(item_id),
                      'name': get_name(item_rec, data),
                      'magic_type': magic_type,
                      'aura': get_auraculum_aura(item_rec)}
        return magic_dict
    return None
