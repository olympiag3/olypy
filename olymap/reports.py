#!/usr/bin/python
import math

from collections import defaultdict
from olypy.oid import to_oid
from olypy.oid import to_int
import olymap.utilities as u
from olymap.utilities import get_oid, get_name, get_subkind, get_who_has
import olymap.maps as maps
import pathlib
from olypy.db import loop_here
from jinja2 import Environment, PackageLoader, select_autoescape
import olymap
from olymap.ship import build_basic_ship_dict
from olymap.item import build_basic_item_dict, get_magic_item
from olymap.player import build_complete_player_dict
from olymap.loc import build_basic_loc_dict, get_road_here, get_gate_here, get_gate_start_end, get_where_info, get_region
from olymap.char import build_basic_char_dict, get_items_list, get_loc


def ship_report(data, outdir):
    ship_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_ship(unit_box):
            ship_list.append(unit)
    sort_ship_list = sorted(ship_list, key=lambda x:int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_ship_report.html'), 'w')
    template = olymap.env.get_template('master_ship_report.html')
    ship = build_ship_dict(sort_ship_list, data)
    outf.write(template.render(ship=ship))


def build_ship_dict(ship_list, data):
    ship = []
    for ship_id in ship_list:
        ship_rec = data[ship_id]
        ship_entry = build_basic_ship_dict(ship_id, ship_rec, data)
        ship.append(ship_entry)
    return ship


def item_report(data, trade_chain, outdir):
    item_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_item(unit_box):
            item_list.append(unit)
    # item_list.sort()
    # for unit in item_list:
    sort_item_list =  sorted(item_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_item_report.html'), 'w')
    template = olymap.env.get_template('master_item_report.html')
    itemz = build_item_dict(sort_item_list, data, trade_chain)
    outf.write(template.render(itemz=itemz))


def build_item_dict(item_list, data, trade_chain):
    itemz = []
    for item_id in item_list:
        item_rec = data[item_id]
        item_entry = build_basic_item_dict(item_id, item_rec, data, trade_chain)
        item_entry.update({'magic_item': get_magic_item(data, item_id, item_rec)})
        itemz.append(item_entry)
    return itemz


def player_report(data, outdir):
    player_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_player(unit_box):
            player_list.append(unit)
    sort_player_list =  sorted(player_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_player_report.html'), 'w')
    template = olymap.env.get_template('master_player_report.html')
    player = build_player_dict(sort_player_list, data)
    outf.write(template.render(player=player))


def build_player_dict(player_list, data):
    player = []
    for player_id in player_list:
        player_rec = data[player_id]
        player_entry = build_complete_player_dict(player_id, player_rec, data)
        player.append(player_entry)
    return player


def healing_potion_report(data, outdir):
    healing_potion_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_item(unit_box) and u.get_use_key(unit_box) == '2':
            healing_potion_list.append(unit)
    # healing_potion_list.sort()
    # for unit in healing_potion_list:
    sort_healing_potion_list = sorted(healing_potion_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_healing_potion_report.html'), 'w')
    template = olymap.env.get_template('master_healing_potion_report.html')
    healing_potion = build_item_dict(sort_healing_potion_list, data, None)
    outf.write(template.render(healing_potion=healing_potion))


def orb_report(data, outdir):
    orb_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_item(unit_box):
            item_rec = data[unit]
            if u.is_orb(item_rec):
                orb_list.append(unit)
    # orb_list.sort()
    # for unit in orb_list:
    sort_orb_list = sorted(orb_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_orb_report.html'), 'w')
    template = olymap.env.get_template('master_orb_report.html')
    orb = build_item_dict(sort_orb_list, data, None)
    outf.write(template.render(orb=orb))


def projected_cast_potion_report(data, outdir):
    projected_cast_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_item(unit_box):
            item_rec = data[unit]
            if u.is_projected_cast(item_rec):
                projected_cast_list.append(unit)
    # projected_cast_list.sort()
    # for unit in projected_cast_list:
    sort_projected_cast_list = sorted(projected_cast_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_projected_cast_report.html'), 'w')
    template = olymap.env.get_template('master_projected_cast_report.html')
    projected_cast = build_item_dict(sort_projected_cast_list, data, None)
    outf.write(template.render(projected_cast=projected_cast))


def location_report(data, outdir):
    location_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_loc(unit_box):
            location_list.append(unit)
    # location_list.sort()
    # for unit in location_list:
    sort_location_list = sorted(location_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_location_report.html'), 'w')
    template = olymap.env.get_template('master_location_report.html')
    loc = build_loc_dict(sort_location_list, data, True, None)
    outf.write(template.render(loc=loc))


def build_loc_dict(loc_list, data, nbr_men_flag=False, garrisons_chain=None, port_city_flag=False, nbr_provinces_flag=False):
    loc = []
    for loc_id in loc_list:
        loc_rec = data[loc_id]
        loc_entry = build_basic_loc_dict(loc_id, loc_rec, data, garrisons_chain)
        if nbr_men_flag == True:
            nbrmen, _, _ = maps.count_stuff(loc_rec, data)
            loc_entry.update({'nbr_men': nbrmen})
        if port_city_flag == True:
            port_city = u.is_port_city(loc_rec, data)
            loc_entry.update({'port_city': port_city})
        if nbr_provinces_flag == True:
            nbr_provinces = 0
            if 'LI' in loc_rec:
                if 'hl' in loc_rec['LI']:
                    nbr_provinces = len(loc_rec['LI']['hl'])
            loc_entry.update({'nbr_provinces': nbr_provinces})
        loc.append(loc_entry)
    return loc


def skill_xref_report(data, teaches_chain, outdir):
    skill_list = sorted(list(teaches_chain))
    sort_skill_xref_list = []
    for unit in skill_list:
        city_list = teaches_chain[unit]
        if len(city_list) > 0 and unit is not None:
            skill_rec = data[unit]
            for city in city_list:
                city_rec = data[city]
                where_rec = data[city_rec['LI']['wh'][0]]
                loc_dict = {'id': city,
                            'oid': to_oid(city),
                            'name': get_name(city_rec)}
                sort_skill_xref_dict = {'id': unit,
                                        'oid': to_oid(unit),
                                        'name': get_name(skill_rec),
                                        'loc_dict': loc_dict,
                                        'where_dict': get_where_info(city_rec, data),
                                        'region_dict': get_region(city, data)}
                sort_skill_xref_list.append(sort_skill_xref_dict)
    outf = open(pathlib.Path(outdir).joinpath('master_skill_xref_report.html'), 'w')
    template = olymap.env.get_template('master_skill_xref_report.html')
    loc = sort_skill_xref_list
    outf.write(template.render(loc=loc))


def trade_report(data, trade_chain, outdir):
    trade_list = sorted(list(trade_chain))
    sort_trade_list = []
    for unit in trade_list:
        city_list = trade_chain[unit]
        if len(city_list) > 0 and unit is not None:
            item_rec = data[unit]
            sell_list = []
            buy_list = []
            for city in city_list:
                city_id = city[0]
                city_rec = data[city_id]
                region_id = u.region(city_id, data)
                region_rec = data[region_id]
                if city[1] == '1':
                    buy_dict = {'id': city_id,
                                'oid': to_oid(city_id),
                                'name': get_name(city_rec),
                                'region_oid': to_oid(region_id),
                                'region_name': get_name(region_rec)}
                    buy_list.append(buy_dict)
                else:
                    sell_dict = {'id': city_id,
                                 'oid': to_oid(city_id),
                                 'name': get_name(city_rec),
                                 'region_oid': to_oid(region_id),
                                 'region_name': get_name(region_rec)}
                    sell_list.append(sell_dict)
            trade_entry = {'id': unit,
                           'oid': to_oid(unit),
                           'name': get_name(item_rec),
                           'buy_list': buy_list,
                           'sell_list': sell_list}
            sort_trade_list.append((trade_entry))
    outf = open(pathlib.Path(outdir).joinpath('master_trade_report.html'), 'w')
    template = olymap.env.get_template('master_trade_report.html')
    loc = sort_trade_list
    outf.write(template.render(loc=loc))


def road_report(data, outdir):
    road_list = []
    for unit in data:
        if u.is_road_or_gate(data[unit]):
            unit_rec = data[unit]
            if get_road_here(unit_rec) == True:
                road_list.append(unit)
    # road_list.sort()
    # for road in road_list:
    sort_road_list =  sorted(road_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_road_report.html'), 'w')
    template = olymap.env.get_template('master_road_report.html')
    loc = build_road_dict(sort_road_list, data)
    outf.write(template.render(loc=loc))


def build_road_dict(loc_list, data):
    loc = []
    for loc_id in loc_list:
        loc_rec = data[loc_id]
        loc_entry = build_basic_loc_dict(loc_id, loc_rec, data)
        loc_entry.update({'road': get_gate_start_end(loc_rec, data)})
        loc.append(loc_entry)
    return loc


def gate_report(data, outdir):
    gate_list = []
    for unit in data:
        if u.is_road_or_gate(data[unit]):
            unit_rec = data[unit]
            if get_gate_here(unit_rec) == True:
                gate_list.append(unit)
    # road_list.sort()
    # for road in road_list:
    sort_gate_list =  sorted(gate_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_gate_report.html'), 'w')
    template = olymap.env.get_template('master_gate_report.html')
    loc = build_road_dict(sort_gate_list, data)
    outf.write(template.render(loc=loc))


def character_report(data, outdir):
    character_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_char(unit_box):
            character_list.append(unit)
    # character_list.sort()
    # for unit in character_list:
    sort_character_list =  sorted(character_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_character_report.html'), 'w')
    template = olymap.env.get_template('master_character_report.html')
    char = build_char_dict(sort_character_list, data)
    outf.write(template.render(char=char))


def build_char_dict(char_list, data):
    char = []
    for char_id in char_list:
        char_rec = data[char_id]
        char_entry = build_basic_char_dict(char_id, char_rec, data)
        char.append(char_entry)
    return char


def graveyard_report(data, outdir):
    graveyard_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_graveyard(unit_box):
            graveyard_list.append(unit)
    # graveyard_list.sort()
    # for unit in graveyard_list:
    sort_graveyard_list = []
    for unit in sorted(graveyard_list, key=lambda x: int(x)):
        graveyard_rec = data[unit]
        # SL/lt
        if 'SL' in graveyard_rec and 'lt' in graveyard_rec['SL']:
            target_id = graveyard_rec['SL']['lt'][0]
            target_rec = data[target_id]
            target_dict = {'id': target_id,
                           'oid': to_oid(target_id),
                           'name': get_name(target_rec)}
        else:
            target_rec = None
            target_dict = None
            target_region_dict = None
        sort_graveyard_dict = {'id:' : unit,
                               'oid': to_oid(unit),
                               'name': get_name(graveyard_rec),
                               'where_dict': get_where_info(graveyard_rec, data),
                               'region_dict': get_region(unit, data),
                               'target_dict': target_dict}
        sort_graveyard_list.append((sort_graveyard_dict))
    outf = open(pathlib.Path(outdir).joinpath('master_graveyard_report.html'), 'w')
    template = olymap.env.get_template('master_graveyard_report.html')
    loc = sort_graveyard_list
    outf.write(template.render(loc=loc))


def faeryhill_report(data, outdir):
    faeryhill_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_faeryhill(unit_box):
            faeryhill_list.append(unit)
    # faeryhill_list.sort()
    # for unit in faeryhill_list:
    sort_faeryhill_list = []
    for unit in sorted(faeryhill_list, key=lambda x: int(x)):
        faeryhill_rec = data[unit]
        # SL/lt
        if 'SL' in faeryhill_rec and 'lt' in faeryhill_rec['SL']:
            target_id = faeryhill_rec['SL']['lt'][0]
            target_rec = data[target_id]
            target_dict = {'id': target_id,
                           'oid': to_oid(target_id),
                           'name': get_name(target_rec)}
            target_region_dict = get_region(target_id, data)
        else:
            target_rec = None
            target_dict = None
            target_region_dict = None
        sort_faeryhill_dict = {'id:' : unit,
                               'oid': to_oid(unit),
                               'name': get_name(faeryhill_rec),
                               'where_dict': get_where_info(faeryhill_rec, data),
                               'region_dict': get_region(unit, data),
                               'target_dict': target_dict,
                               'target_region_dict': target_region_dict}
        sort_faeryhill_list.append((sort_faeryhill_dict))
    outf = open(pathlib.Path(outdir).joinpath('master_faeryhill_report.html'), 'w')
    template = olymap.env.get_template('master_faeryhill_report.html')
    loc = sort_faeryhill_list
    outf.write(template.render(loc=loc))


def castle_report(data, outdir, garrisons_chain):
    castle_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_castle(unit_box):
            castle_list.append(unit)
    # castle_list.sort()
    # for unit in castle_list:
    sort_castle_list = sorted(castle_list, key=lambda x: int(x))
    # nbrmen, _, _ = maps.count_stuff(castle, data)
    outf = open(pathlib.Path(outdir).joinpath('master_castle_report.html'), 'w')
    template = olymap.env.get_template('master_castle_report.html')
    loc = build_loc_dict(sort_castle_list, data, True, garrisons_chain)
    outf.write(template.render(loc=loc))


def city_report(data, outdir):
    city_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_city(unit_box):
            city_list.append(unit)
    # city_list.sort()
    # for unit in city_list:
    sort_city_list = sorted(city_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_city_report.html'), 'w')
    template = olymap.env.get_template('master_city_report.html')
    loc = build_loc_dict(sort_city_list, data, True, None, True)
    outf.write(template.render(loc=loc))


def region_report(data, outdir):
    region_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_region(unit_box):
            region_list.append(unit)
    # region_list.sort()
    # for unit in region_list:
    sort_region_list = sorted(region_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_region_report.html'), 'w')
    template = olymap.env.get_template('master_region_report.html')
    loc = build_loc_dict(sort_region_list, data, False, None, False, True)
    outf.write(template.render(loc=loc))


def mage_report(data, outdir):
    mage_list = []
    for unit in data:
        unit_rec = data[unit]
        if u.is_magician(unit_rec):
            mage_list.append(unit)
    # mage_list.sort()
    # for unit in mage_list:
    sort_mage_list = sorted(mage_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_mage_report.html'), 'w')
    template = olymap.env.get_template('master_mage_report.html')
    char = build_char_dict(sort_mage_list, data)
    outf.write(template.render(char=char))


def priest_report(data, outdir):
    priest_list = []
    for unit in data:
        if u.is_priest(data[unit]):
            priest_list.append(unit)
    # priest_list.sort()
    # for unit in priest_list:
    sort_priest_list = sorted(priest_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_priest_report.html'), 'w')
    template = olymap.env.get_template('master_priest_report.html')
    char = build_char_dict(sort_priest_list, data)
    outf.write(template.render(char=char))


def gold_report(data, outdir):
    character_list = []
    for unit in data:
        unit_box = data[unit]
        if u.is_char(unit_box):
            character_list.append(unit)
    # character_list.sort()
    # for unit in character_list:
    sort_gold_list = []
    for unit in sorted(character_list, key=lambda x: int(x)):
        character_rec = data[unit]
        items_list = get_items_list(character_rec, data, False, '1')
        if items_list != []:
            if int(items_list[0]['qty']) > 10000:
                gold_dict = {'id': unit,
                             'oid': to_oid(unit),
                             'name': get_name(character_rec),
                             'loc': get_loc(character_rec, data),
                             'qty': int(items_list[0]['qty'])}
                sort_gold_list.append(gold_dict)
    outf = open(pathlib.Path(outdir).joinpath('master_gold_report.html'), 'w')
    template = olymap.env.get_template('master_gold_report.html')
    char = sort_gold_list
    outf.write(template.render(char=char))
