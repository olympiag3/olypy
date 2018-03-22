#!/usr/bin/python

from collections import defaultdict
from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import get_oid, get_name, get_subkind
import pathlib
from jinja2 import Environment, PackageLoader, select_autoescape


def get_strength(v):
    return v.get('MI', {}).get('ss', [0])[0]


def build_complete_storm_dict(k, v, data, storm_chain):
    storm_dict = {'oid': get_oid(k),
                  'name': get_name(v),
                  'subkind': get_subkind(v, data),
                  'kind': 'storm',
                  'strength': get_strength(v),
                  'loc': build_loc_dict(v, data),
                  'ship': build_ship_dict(k, data, storm_chain)}
    return storm_dict


def build_basic_storm_dict(k, v, data):
    storm_dict = {'oid': get_oid(k),
                  'name': get_name(v),
                  'subkind': get_subkind(v, data),
                  'kind': 'storm',
                  'strength': get_strength(v)}
    return storm_dict


def build_loc_dict(v, data):
    loc_id = v['LI']['wh'][0]
    loc_rec = data[loc_id]
    loc_dict = {'oid': get_oid(loc_id),
                'name': get_name(loc_rec),
                'subkind': get_subkind(loc_rec, data)}
    return loc_dict


def get_bound_ship(k, storm_chain):
    ship_list = storm_chain[k]
    if len(ship_list) > 0:
        return ship_list[0]
    else:
        return None


def build_ship_dict(k, data, storm_chain):
    ship_id = get_bound_ship(k, storm_chain)
    if ship_id is not None:
        ship_rec = data[ship_id]
        ship_dict = {'id': ship_id,
                     'oid': get_oid(ship_id),
                     'name': get_name(ship_rec)}
    else:
        ship_dict = None
    return ship_dict
