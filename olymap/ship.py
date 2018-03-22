#!/usr/bin/python
import math
from collections import defaultdict

from olymap.utilities import get_oid, get_name, get_subkind, to_oid, loop_here2, get_ship_damage
from olypy.db import loop_here
from olymap.utilities import calc_ship_pct_loaded
from olymap.storm import build_basic_storm_dict
from olymap.char import build_basic_char_dict


def get_complete(v):
    effort_given = int(v.get('SL', {}).get('eg', [0])[0])
    effort_required = int(v.get('SL', {}).get('er', [0])[0])
    if effort_required > 0:
        complete = (effort_given / effort_required) * 100
    elif effort_required == 0 and effort_given == 0:
        complete = 100
    else:
        complete = 0
    return complete


def get_load(k, v, data):
    return calc_ship_pct_loaded(data, k, v)


def get_defense(v):
    return v.get('SL', {}).get('de', [0])


def build_loc_dict(v, data):
    loc_id = v['LI']['wh'][0]
    loc_rec = data[loc_id]
    loc_dict = {'id': loc_id,
                'oid': get_oid(loc_id),
                'name': get_name(loc_rec),
                'subkind': get_subkind(loc_rec, data)}
    return loc_dict


def get_owner(v):
    owner_id = v.get('LI', {}).get('hl', [None])[0]
    if owner_id is not None:
        return owner_id
    return None


def build_owner_dict(v, data):
    if get_owner(v) is not None:
        owner_id = get_owner(v)
        owner_rec = data[owner_id]
        owner_dict = {'id': owner_id,
                      'oid': get_oid(owner_id),
                      'name': get_name(owner_rec)}
    else:
        owner_dict = None
    return owner_dict


def get_bound_storm(v):
    return v.get('SL', {}).get('bs', [None])[0]


def build_storm_dict(v, data):
    if get_bound_storm(v) is not None:
        storm_id = get_bound_storm(v)
        storm_rec = data[storm_id]
        storm_dict = build_basic_storm_dict(storm_id, storm_rec, data)
    else:
        storm_dict = None
    return storm_dict


def build_seenhere_dict(k, v, data, instance, pledge_chain, prisoner_chain):
    stack_list = []
    stack_list = loop_here2(data, k)
    # print (stack_list)
    seen_here = []
    # here_list =  v.get('LI', {}).get('hl', [None])
    if len(stack_list) > 0:
        for characters in stack_list:
            char_rec = data[characters[0]]
            seen_entry = build_basic_char_dict(characters[0], char_rec, data, True)
            seen_entry.update({'level': characters[1]})
            seen_here.append(seen_entry)
    return seen_here


def build_non_prominent_items_dict(k, v, data):
    npi_list = []
    seen_here_list = loop_here(data, k, False, True)
    list_length = len(seen_here_list)
    if list_length > 1:
        for un in seen_here_list:
            unit_rec = data[un]
            if 'il' in unit_rec:
                item_list = unit_rec['il']
                for items in range(0, len(item_list), 2):
                    item_rec = data[item_list[items]]
                    if 'IT' in item_rec and 'pr' in item_rec['IT'] and item_rec['IT']['pr'][0] == '1':
                        pass
                    else:
                        if int(item_list[items + 1]) > 0:
                            weight = 0
                            qty = int(item_list[items + 1])
                            if 'wt' in item_rec['IT']:
                                weight = int(item_rec['IT']['wt'][0])
                            total_weight = int(qty * weight)
                            if total_weight > 0:
                                npi_entry = {'possessor_oid': to_oid(un),
                                             'possessor_name': unit_rec['na'][0],
                                             'item_oid': to_oid(item_list[items]),
                                             'item_name': item_rec['na'][0],
                                             'qty': qty,
                                             'weight': total_weight}
                                npi_list.append(npi_entry)
    return npi_list


def build_basic_ship_dict(k, v, data):
    ship_dict = {'oid': get_oid(k),
                 'name': get_name(v),
                 'subkind': get_subkind(v, data),
                 'kind': 'ship',
                 'complete': get_complete(v),
                 'load': get_load(k, v, data),
                 'defense': get_defense(v)[0],
                 'damage': get_ship_damage(v),
                 'owner': build_owner_dict(v, data),
                 'storm': build_storm_dict(v, data),
                 'loc': build_loc_dict(v, data)}
    return ship_dict


def build_complete_ship_dict(k, v, data, instance, pledge_chain, prisoner_chain):
    ship_dict = {'oid': get_oid(k),
                 'name': get_name(v),
                 'subkind': get_subkind(v, data),
                 'kind': 'kind',
                 'complete': get_complete(v),
                 'load': get_load(k, v, data),
                 'defense': get_defense(v)[0],
                 'damage': get_ship_damage(v),
                 'owner': build_owner_dict(v, data),
                 'storm': build_storm_dict(v, data),
                 'seen_here': build_seenhere_dict(k, v, data, instance, pledge_chain, prisoner_chain),
                 'non_prominent_items': build_non_prominent_items_dict(k, v, data),
                 'loc': build_loc_dict(v, data)}
    return ship_dict
