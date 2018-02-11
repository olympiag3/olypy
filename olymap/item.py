#!/usr/bin/python

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor, get_oid, get_name, get_type, to_oid, loop_here2, get_who_has
import pathlib
from jinja2 import Environment, PackageLoader, select_autoescape


def build_complete_item_dict(k, v, data, trade_chain):
    who_has_id, who_has_name = get_who_has(v, data)
    dead_body_id, dead_body_name = get_dead_body(v, data)
    may_study_id, may_study_name = get_may_study(v, data)
    item_dict = {'oid' : get_oid(k),
                 'name' : get_name(v, data),
                 'type' : get_type(v, data),
                 'plural' : get_plural(v, data)[0],
                 'animal' : get_animal(v)[0],
                 'attack' : get_attack(v)[0],
                 'attack_bonus' : get_attack_bonus(v)[0],
                 'aura' : get_aura(v)[0],
                 'aura_bonus' : get_aura_bonus(v)[0],
                 'dead_body_oid' : dead_body_id,
                 'dead_body_name' : dead_body_name,
                 'defense' : get_defense(v)[0],
                 'defense_bonus' : get_defense_bonus(v)[0],
                 'fly_capacity' : get_fly_capacity(v)[0],
                 'land_capacity' : get_land_capacity(v)[0],
                 'lore' : get_lore(v)[0],
                 'may_study_oid' : may_study_id,
                 'may_study_name' : may_study_name,
                 'missile' : get_missile(v)[0],
                 'missile_bonus' : get_missile_bonus(v)[0],
                 'project_cast' : get_project_cast(v)[0],
                 'prominent' : get_prominent(v)[0],
                 'ride_capacity' : get_ride_capacity(v)[0],
                 'use_key' : get_use_key(v)[0],
                 'weight' : get_weight(v)[0],
                 'who_has_oid' : who_has_id,
                 'who_has_name' : who_has_name,
                 'trade_good' : get_trade_good(k, v, data, trade_chain)}
    return item_dict


def get_animal(v):
    return v.get('IT', {}).get('an', [None])


def get_attack(v):
    return v.get('IT', {}).get('at', [None])


def get_attack_bonus(v):
    return v.get('IM', {}).get('ab', [None])


def get_aura(v):
    return v.get('IM', {}).get('au', [None])


def get_aura_bonus(v):
    return v.get('IM', {}).get('ba', [None])


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


def get_project_cast(v):
    return v.get('IM', {}).get('pc', [None])


def get_prominent(v):
    return v.get('IT', {}).get('pr', [None])


def get_ride_capacity(v):
    return v.get('IT', {}).get('rc', [None])


def get_use_key(v):
    return v.get('IM', {}).get('uk', [None])


def get_weight(v):
    return v.get('IT', {}).get('wt', [None])


def get_trade_good(k, v, data, trade_chain):
    if u.return_type(v) == 'tradegood':
        trade_list = trade_chain[k]
        if len(trade_list) > 0:
            first = True
            ret = ''
            for loc in trade_list:
                loc_rec = data[loc[0]]
                if not first:
                    ret = ret + '<br>'
                first = False
                if loc[1] == '1':
                    ret = ret + 'buy: '
                else:
                    ret = ret + 'sell: '
                ret = ret + loc_rec['na'][0] + ' [' + anchor(to_oid(loc[0])) + ']'
            return ret
    return None