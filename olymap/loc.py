#!/usr/bin/python

import math

from olypy.oid import to_oid
import olymap.utilities as u
import olypy.details as details
import olymap.detail as detail
from operator import itemgetter
from olymap.utilities import get_oid, get_name, get_subkind, to_oid, loop_here2, get_who_has
from olymap.utilities import calc_ship_pct_loaded, is_impassable, calc_exit_distance, get_item_weight
from olymap.char import get_items_list, get_wearable_wielding, get_inventory, build_basic_char_dict
from olymap.ship import build_basic_ship_dict
from olymap.storm import build_basic_storm_dict


pd_directions = {0: 'North', 1: 'East', 2: 'South', 3: 'West', 4: 'Up', 5: 'Down'}


def build_basic_loc_dict(k, v, data, garrisons_chain=None):
    loc_dict = {'oid': to_oid(k),
                'name': get_name(v),
                'subkind': get_subkind(v, data),
                'kind': u.return_kind(v),
                'where': get_where_info(v, data),
                'hidden': u.is_hidden(v),
                'structure': get_structure_info(v),
                'seen_here': get_here_list(k, v, data),
                'region': get_region(k, data),
                'garrisons': get_garrisons(k, v, data, garrisons_chain),}
    return loc_dict


def get_where_info(v, data):
    where_id = v.get('LI', {}).get('wh', None)
    if where_id is not None:
        try:
            where_rec = data[where_id[0]]
        except KeyError:
            where_dict = None
        else:
            where_dict = {'id': where_id[0],
                          'oid': to_oid(where_id[0]),
                          'name': get_name(where_rec),
                          'subkind': get_subkind(where_rec, data)}
    else:
        where_dict = None
    return where_dict


def get_safe_haven(v):
    safe_haven = v.get('SL', {}).get('sh', [None])
    return safe_haven[0]


def get_civ_level(k, v, data):
    civ_level = None
    if not u.is_ocean(v) and u.loc_depth(u.return_subkind(v)) == 2 \
    and data[u.region(k, data)]['na'][0] != 'faery' and data[u.region(k, data)]['na'][0] != 'hades':
        civ_level = 'wilderness'
        if 'LO' in v and 'lc' in v['LO']:
            if v['LO']['lc'][0] == '0':
                civ_level = 'wilderness'
            else:
                civ_level = 'civ-' + v['LO']['lc'][0]
    return civ_level


def get_barrier(k, v, data):
    barrier = v.get('LO', {}).get('ba', [None])
    if barrier[0] is not None and barrier[0] != '0':
        barrier_dict = {'oid': to_oid(k),
                        'name': get_name(v)}
        return barrier_dict
    else:
        return None


def get_shroud(k, v, data):
    shroud = v.get('LO', {}).get('sh', [None])
    if shroud[0] is not None and shroud[0] != '0':
        shroud_dict = {'oid': to_oid(k),
                       'name': get_name(v)}
        return shroud_dict
    else:
        return None


def get_controlled_by(v, data):
    controlled_dict = {}
    here_list = v.get('LI', {}).get('hl', [None])
    if here_list[0] is not None and len(here_list) > 0:
        for loc in here_list:
            garrison_rec = data[loc] # looking for garrisons
            if u.is_garrison(garrison_rec):
                castle = garrison_rec.get('MI', {}).get('gc', [None])
                if castle[0] is not None and castle[0] != '0':
                    castle_rec = data[castle[0]]
                    castle_name = castle_rec['na'][0]
                    castle_oid = to_oid(castle[0])
                    castle_type = u.return_subkind(castle_rec)
                    castle_loc_id = castle_rec['LI']['wh'][0]
                    castle_loc_rec = data[castle_loc_id]
                    castle_loc_type = get_subkind(castle_loc_rec, data)
                    if castle_loc_type == 'city':  # in a city
                        castle_loc_id = castle_loc_rec['LI']['wh'][0]
                        castle_loc_rec = data[castle_loc_id]
                    castle_loc_oid = to_oid(castle_loc_id)
                    castle_loc_name = castle_loc_rec['na'][0]
                    # calculate top of pledge chain
                    castle_here_list = castle_rec.get('LI', {}).get('hl', [None])
                    ruled_by_dict = None
                    if castle_here_list[0] is not None:
                        top_guy_box = u.top_ruler(data[castle_here_list[0]], data)
                        if top_guy_box is not None:
                            ruled_by_dict = {'id': u.return_unitid(top_guy_box),
                                             'oid': to_oid(u.return_unitid(top_guy_box)),
                                             'name': get_name(top_guy_box)}
                    controlled_dict = {'oid': castle_oid,
                                       'name': castle_name,
                                       'subkind': castle_type,
                                       'loc_oid': castle_loc_oid,
                                       'loc_name': castle_loc_name,
                                       'ruled_by_dict': ruled_by_dict}
    return controlled_dict


def get_destinations(k, v, data):
    dest_list = []
    if 'LO' in v and 'pd' in v['LO']:
        pd_list = v['LO']['pd']
        i = int(0)
        for pd in pd_list:
            if pd != '0':
                direction = pd_directions[i]
                pd_rec = data[pd]
                region_id = u.region(pd, data)
                region_rec = data[region_id]
                if u.province_has_port_city(pd_rec, data) is not None:
                    city_rec = data[u.province_has_port_city(pd_rec, data)]
                    to_dict = create_loc_to_dict_entry(data, direction, city_rec, v, region_rec)
                    dest_list.append(to_dict)
                to_dict = create_loc_to_dict_entry(data, direction, pd_rec, v, region_rec)
                dest_list.append(to_dict)
                # see if port city so show province also
                if u.is_port_city(pd_rec, data):
                    prov_rec = data[u.province(pd, data)]
                    to_dict = create_loc_to_dict_entry(data, direction, prov_rec, v, region_rec)
                    dest_list.append(to_dict)
            i = i + 1
    if u.return_subkind(v) not in details.province_kinds:
        if 'LI' in v and 'wh' in v['LI']:
            out_id = v['LI']['wh'][0]
            out_rec = data[out_id]
            region_id = u.region(out_id, data)
            region_rec = data[region_id]
            to_dict = create_loc_to_dict_entry(data, 'Out', out_rec, v, region_rec)
            dest_list.append(to_dict)
    if 'LI' in v and 'hl' in v['LI']:
        here_list = v['LI']['hl']
        for here in here_list:
            here_record = data[here]
            if u.is_road_or_gate(here_record):
                to_id = here_record['GA']['tl'][0]
                to_rec = data[to_id]
                region_id = u.region(to_id, data)
                region_rec = data[region_id]
                if u.return_kind(here_record) == 'gate':
                    direction = 'Gate'
                else:
                    direction = get_name(here_record)
                to_dict = create_loc_to_dict_entry(data, direction, to_rec, here_record, region_rec)
                dest_list.append(to_dict)
    if 'SL' in v and 'lt' in v['SL']:
        link_id = v['SL']['lt'][0]
        link_rec = data[link_id]
        region_id = u.region(link_id, data)
        region_rec = data[region_id]
        to_dict = create_loc_to_dict_entry(data, get_subkind(link_rec, data).title(), link_rec, v, region_rec)
        dest_list.append(to_dict)
    region_id = u.region(k, data)
    region_rec = data[region_id]
    dest_dict = {'id': k,
                 'oid': to_oid(k),
                 'name': get_name(v),
                 'subkind': get_subkind(v, data),
                 'region_oid': to_oid(region_id),
                 'region_name': get_name(region_rec),
                 'dest': dest_list}
    return dest_dict


def create_loc_to_dict_entry(data, direction, to_loc_rec, from_loc_rec, region_rec):
    to_dict = {'id': u.return_unitid(to_loc_rec),
               'oid': to_oid(u.return_unitid(to_loc_rec)),
               'name': get_name(to_loc_rec),
               'subkind': get_subkind(to_loc_rec, data),
               'is_port': u.is_port_city(to_loc_rec, data),
               'prov_port': u.province_has_port_city(to_loc_rec, data),
               'region_oid': to_oid(u.return_unitid(region_rec)),
               'region_name': get_name(region_rec),
               'direction': direction,
               'barrier': get_barrier(u.return_unitid(to_loc_rec), to_loc_rec, data),
               'distance': u.calc_exit_distance(from_loc_rec, to_loc_rec),
               'impassable': is_impassable(from_loc_rec, to_loc_rec, direction, data)}
    return to_dict


def get_routes_out(k, v, data):
    routes_out_list = []
    if not u.is_city(v):
        dest_dict = get_destinations(k, v, data)
    else:
        dest_list = []
        host_prov_id = v['LI']['wh'][0]
        host_prov_rec = data[host_prov_id]
        # If city is in a mountain, can't move from city to ocean
        if not u.is_mountain(host_prov_rec):
            dest_loc_list = host_prov_rec['LO']['pd']
            i = int(0)
            for pd in dest_loc_list:
                if pd != '0':
                    pd_loc = data[pd]
                    if u.is_ocean(pd_loc):
                        pd_name = pd_loc['na'][0]
                        pd_loc_id = u.return_unitid(pd_loc)
                        pd_rec = data[pd_loc_id]
                        direction = pd_directions[i]
                        region_id = u.region(pd_loc_id, data)
                        region_rec = data[region_id]
                        to_dict = create_loc_to_dict_entry(data, direction, pd_rec, v, region_rec)
                        dest_list.append(to_dict)
                i = i + 1
        region_id = u.region(host_prov_id, data)
        region_rec = data[region_id]
        direction = 'Out'
        to_dict = create_loc_to_dict_entry(data, direction, host_prov_rec, v, region_rec)
        dest_list.append(to_dict)
        region_id = u.region(k, data)
        region_rec = data[region_id]
        dest_dict = {'id': k,
                     'oid': to_oid(k),
                     'name': get_name(v),
                     'subkind': get_subkind(v, data),
                     'region_oid': to_oid(region_id),
                     'region_name': get_name(region_rec),
                     'dest': dest_list}
    return dest_dict


def get_defense(v):
    defense = v.get('SL', {}).get('de', [None])
    return defense[0]


def get_damage(v):
    damage = v.get('SL', {}).get('da', [0])
    return damage[0]


def get_effort_given(v):
    effort_given = v.get('SL', {}).get('eg', [None])
    if effort_given[0] is not None:
        return int(effort_given[0])
    else:
        return None


def get_effort_required(v):
    effort_required = v.get('SL', {}).get('er', [None])
    if effort_required[0] is not None:
        return int(effort_required[0])
    else:
        return None


def get_depth(v):
    depth = v.get('SL', {}).get('sd', [None])
    if depth[0] is not None:
        return int(depth[0])
    else:
        return None


def get_level(v):
    level = v.get('SL', {}).get('cl', [None])
    return level[0]


def get_completed(v):
    effort_required = get_effort_required(v)
    effort_given = get_effort_given(v)
    if effort_required is not None:
        if effort_given is None:
            effort_given = 0
        return (effort_given // effort_required) * 100
    return None


def get_structure_info(v):
    structure_dict = {'defense': get_defense(v),
                      'damage': get_damage(v),
                      'effort_given': get_effort_given(v),
                      'effort_required': get_effort_required(v),
                      'completed': get_completed(v),
                      'depth': get_depth(v),
                      'level': get_level(v)}
    if structure_dict['defense'] is None and structure_dict['effort_given'] is None and structure_dict['effort_required'] is None and structure_dict['completed'] is None and structure_dict['depth'] is None and structure_dict['level'] is None:
        return None
    return structure_dict


def get_skills_taught(v, data):
    skills_taught_list = []
    if 'SL' in v and 'te' in v['SL']:
        skills_list = v['SL']['te']
        if len(skills_list) > 0:
            for skill in skills_list:
                skill_rec = data[skill]
                skills_dict = {'oid': to_oid(skill),
                               'name': get_name(skill_rec)}
                skills_taught_list.append(skills_dict)
    return skills_taught_list


def get_markets(k, v, data, trade_chain):
    markets_list = []
    trade_list = []
    if 'tl' in v:
        trade_list = v['tl']
    # load city/character trades
    if len(trade_list) > 0:
        # city trades
        for trade in range(0, len(trade_list), 8):
            if trade_list[trade] in {'1', '2'}:
                item_rec = data[trade_list[trade+1]]
                trade_recip = trade_chain[trade_list[trade + 1]]
                recip_list = []
                if len(trade_recip) > 0:
                    for recip in trade_recip:
                        if recip[0] != k:
                            recip_type = recip[1]
                            if recip_type != trade_list[trade]:
                                recip_loc = recip[0]
                                recip_rec = data[recip_loc]
                                recip_name = get_name(recip_rec)
                                recip_trade_list = recip_rec['tl']
                                for recip in range(0, len(recip_trade_list), 8):
                                    if recip_trade_list[recip + 1] == trade_list[trade+1]:
                                        if recip_trade_list[recip] in {'1', '2'}:
                                            recip_qty = recip_trade_list[recip + 2]
                                            recip_price = recip_trade_list[recip + 3]
                                recip_dict = {'loc_id': recip_loc,
                                              'loc_oid': to_oid(recip_loc),
                                              'name': recip_name,
                                              'qty': recip_qty,
                                              'price': recip_price}
                                recip_list.append(recip_dict)
                market_dict = {'subkind': trade_list[trade],
                               'item_id': trade_list[trade + 1],
                               'item_oid': to_oid(trade_list[trade + 1]),
                               'item_name': get_name(item_rec),
                               'item_weight': get_item_weight(item_rec),
                               'who_id': k,
                               'who_oid': to_oid(k),
                               'who_name': get_name(v),
                               'who_qty': trade_list[trade + 2],
                               'who_price': trade_list[trade + 3],
                               'recip_list': recip_list}
                markets_list.append(market_dict)
        # character trades - needs to be recursive
        seen_here_list = loop_here2(data, k, 0, False, False, True)
        if len(seen_here_list) > 1:
            for un in seen_here_list[1:]:
                charac_rec = data[un[0]]
                if u.return_kind(charac_rec) == 'char':
                    if 'tl' in charac_rec:
                        trade_list = charac_rec['tl']
                        if len(trade_list) > 0:
                            # character trades
                            for trade in range(0, len(trade_list), 8):
                                if trade_list[trade] in {'1', '2'}:
                                    item_rec = data[trade_list[trade + 1]]
                                    trade_recip = trade_chain[trade_list[trade + 1]]
                                    recip_list = []
                                    if len(trade_recip) > 0:
                                        for recip in trade_recip:
                                            if recip[0] != k:
                                                recip_type = recip[1]
                                                if recip_type != trade_list[trade]:
                                                    recip_loc = recip[0]
                                                    recip_rec = data[recip_loc]
                                                    recip_name = get_name(recip_rec)
                                                    recip_trade_list = recip_rec['tl']
                                                    for recip in range(0, len(recip_trade_list), 8):
                                                        if recip_trade_list[recip + 1] == trade_list[trade + 1]:
                                                            if recip_trade_list[recip] in {'1', '2'}:
                                                                recip_qty = recip_trade_list[recip + 2]
                                                                recip_price = recip_trade_list[recip + 3]
                                                    recip_dict = {'loc_id': recip_loc,
                                                                  'loc_oid': to_oid(recip_loc),
                                                                  'name': recip_name,
                                                                  'qty' : recip_qty,
                                                                  'price' : recip_price}
                                                    recip_list.append(recip_dict)
                                    market_dict = {'subkind': trade_list[trade],
                                                   'item_id': trade_list[trade + 1],
                                                   'item_oid': to_oid(trade_list[trade + 1]),
                                                   'item_name': get_name(item_rec),
                                                   'item_weight': get_item_weight(item_rec),
                                                   'who_id': un[0],
                                                   'who_oid': to_oid(un[0]),
                                                   'who_name': get_name(charac_rec),
                                                   'who_qty': trade_list[trade + 2],
                                                   'who_price': trade_list[trade + 3],
                                                   'recip_list' : recip_list}
                                    markets_list.append(market_dict)
    sorted_list = sorted(markets_list, key=itemgetter('subkind', 'item_oid', 'who_oid'))
    return sorted_list


def get_here_list(k, v, data):
    inner_list_final = []
    seen_list_final = []
    ships_list_final = []
    storms_list_final = []
    if 'LI' in v and 'hl' in v['LI']:
        inner_list = loop_here2(data, k, 0, False, True, False, 'loc')
        seen_list = loop_here2(data, k, 0, False, False, False, 'char')
        ship_list = loop_here2(data, k, 0, False, False, False, 'ship')
        storm_list = loop_here2(data, k, 0, False, False, False, 'storm')
        if len(inner_list) > 0:
            for here in inner_list:
                here_rec = data[here[0]]
                if u.is_loc(here_rec):
                    inner_dict = build_basic_loc_dict(here[0], here_rec, data)
                    inner_dict.update({'level': here[1]})
                    inner_list_final.append(inner_dict)
                elif u.is_char(here_rec):
                    inner_dict = build_basic_char_dict(here[0], here_rec, data, True)
                    inner_dict.update({'level': here[1]})
                    inner_list_final.append(inner_dict)
                elif u.return_kind(here_rec) == 'storm':
                    inner_dict = build_basic_storm_dict(here[0], here_rec, data)
                    inner_dict.update({'level': here[1]})
                    inner_list_final.append(inner_dict)
                elif u.is_ship(here_rec):
                    inner_dict = build_basic_ship_dict(here[0], here_rec, data)
                    inner_dict.update({'level': here[1]})
                    inner_list_final.append(inner_dict)
                # else:
                #     print('here_list unknown {} {}'.format(here[0], u.return_kind(here_rec)))
        if len(seen_list) > 0:
            for seen in seen_list:
                seen_rec = data[seen[0]]
                seen_dict = build_basic_char_dict(seen[0], seen_rec, data, True)
                seen_dict.update({'level': seen[1]})
                seen_list_final.append(seen_dict)
        if len(ship_list) > 0:
            for ship in ship_list:
                ship_rec = data[ship[0]]
                if u.is_ship(ship_rec):
                    ship_dict = build_basic_ship_dict(ship[0], ship_rec, data)
                    ship_dict.update({'level': ship[1]})
                    ships_list_final.append(ship_dict)
                elif u.is_char(ship_rec):
                    ship_dict = build_basic_char_dict(ship[0], ship_rec, data, True)
                    ship_dict.update({'level': ship[1]})
                    ships_list_final.append(ship_dict)
                else:
                    print('ship_list unknown {}'.format(ship[0]))
        if len(storm_list) > 0:
            for storm in storm_list:
                storm_rec = data[storm[0]]
                storm_dict = build_basic_storm_dict(storm[0], storm_rec, data)
                storm_dict.update({'level': storm[1]})
                storms_list_final.append(storm_dict)
    if 'SL' in v and 'lf' in v['SL']:
        here = v['SL']['lf'][0]
        here_rec = data[here]
        if u.is_loc(here_rec):
            inner_dict = build_basic_loc_dict(here, here_rec, data)
            inner_dict.update({'level': 0})
            inner_list_final.append(inner_dict)
    here_dict = {'id': k,
                 'oid': to_oid(k),
                 'inner': inner_list_final,
                 'seen': seen_list_final,
                 'ships': ships_list_final,
                 'storms': storms_list_final}
    return here_dict


def get_hidden_access(k, v, data, hidden_chain):
    hidden_access_list = []
    if u.is_hidden(v) or u.region(k, data) in {'faery', 'hades'}:
        # PL/kn
        try:
            hidden_list = hidden_chain[k]
        except:
            pass
        else:
            if len(hidden_list) > 0:
                for hidden in hidden_list:
                    hidden_rec = data[hidden]
                    hidden_dict = {'oid': to_oid(hidden),
                                   'name': get_name(hidden_rec)}
                    hidden_access_list.append(hidden_dict)
    return hidden_access_list


def get_garrisons(k, v, data, garrisons_chain):
    garrisons_list = None
    if garrisons_chain is not None:
        garrisons_list = []
        if u.is_castle(v):
            garrison_list = garrisons_chain[k]
            if len(garrison_list) > 0:
                province_list = []
                for garrison in garrison_list:
                    province_rec = data[garrison]
                    province_list.append([province_rec['LI']['wh'][0], garrison])
                province_list.sort()
                for province in province_list:
                    garrison_rec = data[province[1]]
                    garrison_dict = get_character_info(province[1], garrison_rec, data, True)
                    garrisons_list.append(garrison_dict)
    return garrisons_list


def get_character_info(k, v, data, print_province):
    char_dict = {}
    province_oid = None
    if print_province:
        if 'LI' in v and 'wh' in v['LI']:
            province_rec = data[v['LI']['wh'][0]]
            province_oid = to_oid(v['LI']['wh'][0])
    character_dict = build_basic_char_dict(k, v, data, True)
    character_dict.update({'province_oid': province_oid})
    return character_dict


def build_complete_loc_dict(k, v, data, garrisons_chain, hidden_chain, trade_chain, instance, inst_dict, map_matrices):
    loc_dict = {'oid': to_oid(k),
                'name': get_name(v),
                'subkind': get_subkind(v, data),
                'kind': 'loc',
                'where': get_where_info(v, data),
                'safe_haven': get_safe_haven(v),
                'hidden': u.is_hidden(v),
                'civ_level': get_civ_level(k, v, data),
                'barrier': get_barrier(k, v, data),
                'shroud': get_shroud(k, v, data),
                'anchor': get_map_anchor(v, k, data, instance, inst_dict, map_matrices),
                'controlled_by': get_controlled_by (v, data),
                'routes_out': get_routes_out(k, v, data),
                'structure': get_structure_info(v),
                'skills': get_skills_taught(v, data),
                'markets': get_markets(k, v, data, trade_chain),
                'seen_here': get_here_list(k, v, data),
                'hidden_access': get_hidden_access(k, v, data, hidden_chain),
                'garrisons': get_garrisons(k, v, data, garrisons_chain),
                'region': get_region(k, data)}
    return loc_dict


def get_region(k, data):
    region_id = u.region(k, data)
    region_rec = data[region_id]
    region_dict = {'id': region_id,
                   'oid': to_oid(region_id),
                   'name': get_name(region_rec)}
    return region_dict


def get_map_anchor(v, k, data, instance, inst_dict, map_matrices):
    if u.return_subkind(v) in ['tunnel', 'chamber']:
        return None
    dimensions = inst_dict[instance]
    region = u.region(k, data)
    region_rec = data[region]
    province = u.province(k, data)
    if province == 0:
        return None
    province_rec = data[province]
    custom = False
    save_rec = []
    save_world = ''
    try:
        save_rec = map_matrices[region_rec['na'][0].lower()]
    except KeyError:
        try:
            save_rec = dimensions[region_rec['na'][0].lower()]
        except KeyError:
            for world in dimensions:
                world_rec = dimensions[world]
                if world_rec[0] <= int(province) < world_rec[0] + (world_rec[2] * 100):
                    save_rec = world_rec
                    save_world = world
                    break
        else:
            save_world = region_rec['na'][0].lower()
    else:
        save_world = region_rec['na'][0].lower()
        custom = True
    # if len(save_rec) == 0:
    #     print('error {} {}'.format(to_oid(k),
    #                                u.return_subkind(v)))
    if len(save_rec) > 0 and not custom:
        world_rec = save_rec
        world = save_world
        x_coord = int(10 * math.floor((int(province) % 100) / 10))
        if x_coord >= world_rec[1] - 10:
            x_coord = world_rec[1] - 20
        y_coord = int(1000 * math.floor(int(province) / 1000))
        if y_coord >= world_rec[0] + (world_rec[2] * 100) - 1000:
            y_coord = world_rec[0] + (world_rec[2] * 100) - 2000
            if y_coord < world_rec[0]:
                y_coord = world_rec[0]
        final_coord = y_coord + x_coord
        if final_coord < world_rec[0]:
            final_coord = world_rec[0]
        anchor_string = world + '_map_leaf_' + to_oid(final_coord)
        return anchor_string
    if len(save_rec) > 0 and custom:
        world_rec = save_rec
        world = save_world
        for xx in range(0, len(save_rec[0])):
            for yy in range(0,len(save_rec)):
                if save_rec[yy][xx] == province:
                    xxx = int(math.floor(xx / 10)) * 10
                    yyy = int(math.floor(yy / 10)) * 10
                    final_coord = save_rec[yyy][xxx]
                    break
        anchor_string = world + '_map_leaf_' + to_oid(final_coord)
        return anchor_string
    return None


def get_road_here(v):
    if 'GA' in v and 'rh' in v['GA']:
        if v['GA']['rh'][0] == '1':
            return True
    return False


def get_gate_here(v):
    if 'GA' in v:
        if 'rh' in v['GA']:
            if v['GA']['rh'][0] == '1':
                return False
            else:
                return True
        else:
            return True
    return False


def get_gate_start_end(v, data):
    if get_road_here(v) or get_gate_here(v):
        from_loc_dict = None
        if 'LI' in v and 'wh' in v['LI']:
            from_loc_id = v['LI']['wh'][0]
            from_loc_rec = data[from_loc_id]
            from_loc_name = get_name(from_loc_rec)
            from_loc_dict = {'id': from_loc_id,
                             'oid': to_oid(from_loc_id),
                             'name': from_loc_name}
        to_loc_dict = None
        if 'GA' in v and 'tl' in v['GA']:
            to_loc_id = v['GA']['tl'][0]
            to_loc_rec = data[to_loc_id]
            to_loc_name = get_name(to_loc_rec)
            to_loc_dict = {'id': to_loc_id,
                           'oid': to_oid(to_loc_id),
                           'name': to_loc_name}
        gate_start_end_dict = {'from': from_loc_dict,
                               'to': to_loc_dict}
        return gate_start_end_dict
    return None
