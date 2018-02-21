#!/usr/bin/python
import math

from collections import defaultdict
from olypy.oid import to_oid
from olypy.oid import to_int
import olymap.utilities as u
from olymap.utilities import anchor, get_oid, get_name, get_type, get_who_has
import olymap.maps as maps
import pathlib
from olypy.db import loop_here
from jinja2 import Environment, PackageLoader, select_autoescape
from olymap.ship import build_basic_ship_dict
from olymap.item import build_basic_item_dict
from olymap.player import build_complete_player_dict
from olymap.loc import build_basic_loc_dict, get_road_here, get_gate_here, get_gate_start_end
from olymap.char import build_basic_char_dict


def ship_report(data, outdir):
    ship_list = []
    for unit in data:
        if u.is_ship(data, unit):
            ship_list.append(unit)
    sort_ship_list = sorted(ship_list, key=lambda x:int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_ship_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_ship_report.html')
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
        if u.is_item(data, unit):
            item_list.append(unit)
    # item_list.sort()
    # for unit in item_list:
    sort_item_list =  sorted(item_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_item_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_item_report.html')
    itemz = build_item_dict(sort_item_list, data, trade_chain)
    outf.write(template.render(itemz=itemz))


def build_item_dict(item_list, data, trade_chain):
    itemz = []
    for item_id in item_list:
        item_rec = data[item_id]
        item_entry = build_basic_item_dict(item_id, item_rec, data, trade_chain)
        itemz.append(item_entry)
    return itemz


def player_report(data, outdir):
    player_list = []
    for unit in data:
        if u.is_player(data, unit):
            player_list.append(unit)
    sort_player_list =  sorted(player_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_player_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_player_report.html')
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
        if u.is_item(data, unit) and data[unit].get('IM', {}).get('uk', [''])[0] == '2':
            healing_potion_list.append(unit)
    # healing_potion_list.sort()
    # for unit in healing_potion_list:
    sort_healing_potion_list = sorted(healing_potion_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_healing_potion_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_healing_potion_report.html')
    healing_potion = build_item_dict(sort_healing_potion_list, data, None)
    outf.write(template.render(healing_potion=healing_potion))


def orb_report(data, outdir):
    orb_list = []
    for unit in data:
        if u.is_item(data, unit):
            item_rec = data[unit]
            if u.is_orb(item_rec):
                orb_list.append(unit)
    # orb_list.sort()
    # for unit in orb_list:
    sort_orb_list = sorted(orb_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_orb_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_orb_report.html')
    orb = build_item_dict(sort_orb_list, data, None)
    outf.write(template.render(orb=orb))


def projected_cast_potion_report(data, outdir):
    projected_cast_list = []
    for unit in data:
        if u.is_item(data, unit):
            item_rec = data[unit]
            if u.is_projected_cast(item_rec):
                projected_cast_list.append(unit)
    # projected_cast_list.sort()
    # for unit in projected_cast_list:
    sort_projected_cast_list = sorted(projected_cast_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_projected_cast_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_projected_cast_report.html')
    projected_cast = build_item_dict(sort_projected_cast_list, data, None)
    outf.write(template.render(projected_cast=projected_cast))


def location_report(data, outdir):
    location_list = []
    for unit in data:
        if u.is_loc(data, unit):
            location_list.append(unit)
    # location_list.sort()
    # for unit in location_list:
    sort_location_list = sorted(location_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_location_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_location_report.html')
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
    outf = open(pathlib.Path(outdir).joinpath('master_skill_xref_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Skill Xref Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Skill Xref Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Skill</th><th>Location</th><th>Region</th></tr>\n')
    skill_list = sorted(list(teaches_chain))
    for unit in skill_list:
        city_list = teaches_chain[unit]
        if len(city_list) > 0 and unit is not None:
            skill_rec = data[unit]
            for city in city_list:
                loc = data[city]
                where_rec = data[loc['LI']['wh'][0]]
                outf.write('<tr>')
                outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                              skill_rec['na'][0],
                                                                              anchor(to_oid(unit))))
                outf.write('<td sorttable_customkey="{}">'
                           '{} [{}], {} [{}]</td>'.format(city,
                                                          loc['na'][0],
                                                          anchor(to_oid(city)),
                                                          where_rec['na'][0],
                                                          anchor(to_oid(loc['LI']['wh'][0]))))
                region = u.region(city, data)
                region_rec = data[region]
                outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(region,
                                                                              region_rec['na'][0],
                                                                              anchor(to_oid(region))))
                outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def trade_report(data, trade_chain, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_trade_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Trade Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Trade Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Item</th><th>Seller</th><th>Buyer</th><th>Sell Region</th><th>Buy Region</th></tr>\n')
    trade_list = sorted(list(trade_chain))
    for unit in trade_list:
        city_list = trade_chain[unit]
        if len(city_list) > 0 and unit is not None:
            item_rec = data[unit]
            buy_literal = ''
            buy_id = ''
            sell_literal = ''
            sell_id = ''
            buy_reg_literal = ''
            buy_reg_id = ''
            sell_reg_literal = ''
            sell_reg_id = ''
            for city in city_list:
                loc = data[city[0]]
                if city[1] == '1':
                    if len(buy_literal) > 0:
                        buy_literal = buy_literal + '<br>'
                        buy_reg_literal = buy_reg_literal + '<br>'
                    buy_literal = buy_literal + loc['na'][0] + ' [' + anchor(to_oid(city[0])) + ']'
                    reg_rec = data[u.region(city[0], data)]
                    buy_reg_literal = buy_reg_literal + reg_rec['na'][0]
                    buy_reg_literal = buy_reg_literal + ' [' + anchor(to_oid(u.region(city[0], data))) + ']'
                    if buy_id == '':
                        buy_id = city[0]
                        buy_reg_id = u.region(city[0], data)
                else:
                    if len(sell_literal) > 0:
                        sell_literal = sell_literal + '<br>'
                        sell_reg_literal = sell_reg_literal + '<br>'
                    sell_literal = sell_literal + loc['na'][0] + ' [' + anchor(to_oid(city[0])) + ']'
                    reg_rec = data[u.region(city[0], data)]
                    sell_reg_literal = sell_reg_literal + reg_rec['na'][0] + ' ['
                    sell_reg_literal = sell_reg_literal + anchor(to_oid(u.region(city[0], data))) + ']'
                    if sell_id == '':
                        sell_id = city[0]
                        sell_reg_id = u.region(city[0], data)
            outf.write('<tr>')
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                          item_rec['na'][0],
                                                                          anchor(to_oid(unit))))
            outf.write('<td sorttable_customkey="{}">{}</td>'.format(sell_id,
                                                                     sell_literal))
            outf.write('<td sorttable_customkey="{}">{}</td>'.format(buy_id,
                                                                     buy_literal))
            outf.write('<td sorttable_customkey="{}">{}</td>'.format(sell_reg_id,
                                                                     sell_reg_literal))
            outf.write('<td sorttable_customkey="{}">{}</td>'.format(buy_reg_id,
                                                                     buy_reg_literal))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


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
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_road_report.html')
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
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_gate_report.html')
    loc = build_road_dict(sort_gate_list, data)
    outf.write(template.render(loc=loc))


def character_report(data, outdir):
    character_list = []
    for unit in data:
        if u.is_char(data, unit):
            character_list.append(unit)
    # character_list.sort()
    # for unit in character_list:
    sort_character_list =  sorted(character_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_character_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_character_report.html')
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
    outf = open(pathlib.Path(outdir).joinpath('master_graveyard_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Graveyard Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Graveyard Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Graveyard</th><th>Province</th><th>Region</th><th>Target</th></tr>\n')
    graveyard_list = []
    for unit in data:
        if u.is_graveyard(data, unit):
            graveyard_list.append(unit)
    # graveyard_list.sort()
    # for unit in graveyard_list:
    for unit in sorted(graveyard_list, key=lambda x: int(x)):
        graveyard = data[unit]
        if 'na' in graveyard:
            name = graveyard['na'][0]
        else:
            name = u.return_type(graveyard).capitalize()
        outf.write('<tr>')
        outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                      name,
                                                                      anchor(to_oid(unit))))
        loc_rec = data[graveyard['LI']['wh'][0]]
        if 'na' in loc_rec:
            name_loc = loc_rec['na'][0]
        else:
            name_loc = u.return_type(loc_rec).capitalize()
        outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(u.return_unitid(loc_rec),
                                                                      name_loc,
                                                                      anchor(to_oid(u.return_unitid(loc_rec)))))
        region = u.region(str(unit), data)
        region_rec = data[region]
        outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(region,
                                                                      region_rec['na'][0],
                                                                      anchor(to_oid(region))))
        # SL/lt
        if 'SL' in graveyard and 'lt' in graveyard['SL']:
            target = data[graveyard['SL']['lt'][0]]
            if 'na' in loc_rec:
                name_target = target['na'][0]
            else:
                name_target = u.return_type(target).capitalize()
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(u.return_unitid(target),
                                                                          name_target,
                                                                          anchor(to_oid(u.return_unitid(target)))))
        else:
            outf.write('<td>&nbsp;</td>')
        outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def faeryhill_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_faeryhill_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Faery Hill Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Faery Hill Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Faery Hill</th><th>Province</th><th>Region</th><th>Target</th><th>Target Region</th></tr>\n')
    faeryhill_list = []
    for unit in data:
        if u.is_faeryhill(data, unit):
            faeryhill_list.append(unit)
    # faeryhill_list.sort()
    # for unit in faeryhill_list:
    for unit in sorted(faeryhill_list, key=lambda x: int(x)):
        faeryhill = data[unit]
        if 'na' in faeryhill:
            name = faeryhill['na'][0]
        else:
            name = u.return_type(faeryhill).capitalize()
        outf.write('<tr>')
        outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                      name,
                                                                      anchor(to_oid(unit))))
        loc_rec = data[faeryhill['LI']['wh'][0]]
        if 'na' in loc_rec:
            name_loc = loc_rec['na'][0]
        else:
            name_loc = u.return_type(loc_rec).capitalize()
        outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(u.return_unitid(loc_rec),
                                                                      name_loc,
                                                                      anchor(to_oid(u.return_unitid(loc_rec)))))
        region = u.region(str(unit), data)
        region_rec = data[region]
        outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(region,
                                                                      region_rec['na'][0],
                                                                      anchor(to_oid(region))))
        # SL/lt
        if 'SL' in faeryhill and 'lt' in faeryhill['SL']:
            target = data[faeryhill['SL']['lt'][0]]
            if 'na' in loc_rec:
                name_target = target['na'][0]
            else:
                name_target = u.return_type(target).capitalize()
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(u.return_unitid(target),
                                                                          name_target,
                                                                          anchor(to_oid(u.return_unitid(target)))))
            target_region = u.region(str(faeryhill['SL']['lt'][0]), data)
            target_region_rec = data[target_region]
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(target_region,
                                                                          target_region_rec['na'][0],
                                                                          anchor(to_oid(target_region))))
        else:
            outf.write('<td>&nbsp;</td><td>&nbsp;</td>')
        outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()
    

def castle_report(data, outdir, garrisons_chain):
    castle_list = []
    for unit in data:
        if u.is_castle(data, unit):
            castle_list.append(unit)
    # castle_list.sort()
    # for unit in castle_list:
    sort_castle_list = sorted(castle_list, key=lambda x: int(x))
    # nbrmen, _, _ = maps.count_stuff(castle, data)
    outf = open(pathlib.Path(outdir).joinpath('master_castle_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_castle_report.html')
    loc = build_loc_dict(sort_castle_list, data, True, garrisons_chain)
    outf.write(template.render(loc=loc))


def city_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_city_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master City Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master City Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>City</th><th>Province</th><th>Region</th><th>Port City</th><th># Men</th></tr>\n')
    city_list = []
    for unit in data:
        if u.is_city(data, unit):
            city_list.append(unit)
    # city_list.sort()
    # for unit in city_list:
    sort_city_list = sorted(city_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_city_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_city_report.html')
    loc = build_loc_dict(sort_city_list, data, True, None, True)
    outf.write(template.render(loc=loc))


def region_report(data, outdir):
    region_list = []
    for unit in data:
        if u.is_region(data, unit):
            region_list.append(unit)
    # region_list.sort()
    # for unit in region_list:
    sort_region_list = sorted(region_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_region_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_region_report.html')
    loc = build_loc_dict(sort_region_list, data, False, None, False, True)
    outf.write(template.render(loc=loc))


def mage_report(data, outdir):
    mage_list = []
    for unit in data:
        if u.is_magician(data[unit]):
            mage_list.append(unit)
    # mage_list.sort()
    # for unit in mage_list:
    sort_mage_list = sorted(mage_list, key=lambda x: int(x))
    outf = open(pathlib.Path(outdir).joinpath('master_mage_report.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('master_mage_report.html')
    char = build_char_dict(sort_mage_list, data)
    outf.write(template.render(char=char))


def priest_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_priest_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Priest Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Priest Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Priest</th><th>Priest Name</th><th>Can Visison</th><th>Can Resurrect</th>'
               '<th># Visions</th><th>Visons Received</th></tr>\n')
    priest_list = []
    for unit in data:
        if u.is_priest(data[unit]):
            priest_list.append(unit)
    # priest_list.sort()
    # for unit in priest_list:
    for unit in sorted(priest_list, key=lambda x: int(x)):
        priest_rec = data[unit]
        outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                      priest_rec['na'][0],
                                                                      anchor(to_oid(unit))))
        outf.write('<td>{}</td>'.format(priest_rec['na'][0]))
        if 'CH' in priest_rec and 'sl' in priest_rec['CH']:
            skills_list = priest_rec['CH']['sl']
            skills_iteration = int(len(skills_list) / 5)
            skill_753 = 'No'
            skill_755 = 'No'
            if skills_iteration > 0:
                for skill in range(0, skills_iteration):
                    if skills_list[(skill * 5)] == '753' and skills_list[(skill * 5) + 1] == '2':
                        skill_753 = 'Yes'
                    if skills_list[(skill * 5)] == '755' and skills_list[(skill * 5) + 1] == '2':
                        skill_755 = 'Yes'
                outf.write('<td>{}</td>'.format(skill_753))
                outf.write('<td>{}</td>'.format(skill_755))
        else:
            outf.write('<td>No</td>')
            outf.write('<td>No</td>')
        if 'CM' in priest_rec and 'vi' in priest_rec['CM']:
            vision_list = priest_rec['CM']['vi']
            outf.write('<td>{}</td>'.format(len(vision_list)))
            outf.write('<td>')
            outf.write('<table>')
            second = False
            for vision in vision_list:
                if not second:
                    outf.write('<tr>')
                outf.write('<td>')
                try:
                    visioned = data[vision]
                except KeyError:
                    vision_name = 'missing'
                else:
                    vision_name = visioned.get('na', [u.return_kind(visioned)])[0]
                outf.write('{} [{}]'.format(vision_name,
                                            anchor(to_oid(vision))))
                outf.write('</td>')
                if second:
                    outf.write('</tr>\n')
                    second = False
                else:
                    second = True
            outf.write('</table>')
            outf.write('</td>')
        else:
            outf.write('<td>0</td>')
            outf.write('<td>&nbsp;</td>')
        outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def gold_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_gold_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Gold (> 10k) Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Gold (> 10k) Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Character</th><th>Character Name</th><th>Location</th><th>Gold</th></tr>\n')
    character_list = []
    for unit in data:
        if u.is_char(data, unit):
            character_list.append(unit)
    # character_list.sort()
    # for unit in character_list:
    for unit in sorted(character_list, key=lambda x: int(x)):
        character_rec = data[unit]
        if 'il' in character_rec:
            item_list = character_rec['il']
            if len(item_list) > 0:
                for itm in range(0, len(item_list), 2):
                    item_id = item_list[itm]
                    if item_id == '1':
                        item_qty = int(item_list[itm + 1])
                        if item_qty > 10000:
                            if 'na' in character_rec:
                                name = character_rec['na'][0]
                            else:
                                name = u.return_type(character_rec).capitalize()
                            if name == 'Ni':
                                name = data[character_rec['CH']['ni'][0]]['na'][0].capitalize()
                            outf.write('<tr>')
                            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                                          name,
                                                                                          anchor(to_oid(unit))))
                            outf.write('<td>{}</td>'.format(name))
                            loc_rec = data[character_rec['LI']['wh'][0]]
                            if 'na' in loc_rec:
                                name_loc = loc_rec['na'][0]
                            else:
                                name_loc = u.return_type(loc_rec).capitalize()
                            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(u.return_unitid(loc_rec),
                                                                                          name_loc,
                                                                                          anchor(to_oid(
                                                                                              u.return_unitid(
                                                                                                  loc_rec)))))
                            outf.write(f'<td>{item_qty:,d}</td>')
                            outf.write('</tr>\n')
                        break
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()
