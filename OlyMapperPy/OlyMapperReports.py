#!/usr/bin/python
import os
import sys
import math

from olypy.oid import to_oid
import olypy.oio as oio
import OlyMapperPy.OlyMapperUtilities as u
import olypy.details as details
from OlyMapperPy.OlyMapperUtilities import anchor


def ship_report(data):
    outf = open('master_ship_report.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>Olympia Master Ship Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Ship Report</H3>\n')
    outf.write('<table border="1" style="border-collapse: collapse">\n')
    outf.write('<tr><th>Id</th><th>Type</th><th>Captain</th><th>Location</th><th>Damage</th><th>Load</th><th>Storm (Strength)</th></tr>\n')
    for id in data:
        if u.is_ship(data, id):
            ship_rec = data[id]
            outf.write('<tr>')
            outf.write('<td>{} [{}]</td>'.format(ship_rec['na'][0],
                                                 anchor(to_oid(id))))
            outf.write('<td>{}</td>'.format(u.return_type(ship_rec['firstline'][0])))
            captain = '&nbsp;'
            if 'LI' in ship_rec:
                if 'hl' in ship_rec['LI']:
                    here_list = ship_rec['LI']['hl']
                    for here in here_list:
                        if u.is_char(data, here):
                            here_rec = data[here]
                            captain = here_rec['na'][0] + ' [' + anchor(to_oid(here)) + ']'
            outf.write('<td>{}</td>'.format(captain))
            location = '&nbsp;'
            if 'LI' in ship_rec:
                if 'wh' in ship_rec['LI']:
                    where_rec = data[ship_rec['LI']['wh'][0]]
                    location = where_rec['na'][0] + ' [' + anchor(to_oid(u.return_unitid(where_rec['firstline'][0]))) + ']'
            outf.write('<td>{}</td>'.format(location))
            if 'SL' in ship_rec:
                if 'da' in ship_rec['SL']:
                    outf.write('<td>{}%</td>'.format(ship_rec['SL']['da'][0]))
                else:
                    outf.write('<td>0%</td>')
            else:
                outf.write('<td>0%</td>')
            total_weight = 0
            try:
                damaged = int(ship_rec['SL']['da'][0])
            except KeyError:
                damaged = 0
            seen_here_list = []
            level = 0
            seen_here_list = u.chase_structure(id, data, level, seen_here_list)
            list_length = len(seen_here_list)
            if list_length > 1:
                for un in seen_here_list[1:]:
                    char = data[un[0]]
                    if 'char' in u.return_kind(char['firstline'][0]):
                        unit_type = '10'
                        if 'CH' in char:
                            if 'ni' in char['CH']:
                                unit_type = char['CH']['ni'][0]
                        base_unit = data[unit_type]
                        if 'IT' in base_unit:
                            if 'wt' in base_unit['IT']:
                                item_weight = int(base_unit['IT']['wt'][0]) * 1
                                total_weight = total_weight + item_weight
                        if 'il' in char:
                            item_list = char['il']
                            iterations = int(len(item_list) / 2)
                            for itm in range(0, iterations - 1):
                                itemz = data[item_list[itm * 2]]
                                try:
                                    item_weight = int(itemz['IT']['wt'][0])
                                except KeyError:
                                    item_weight = int(0)
                                qty = int(item_list[(itm * 2) + 1])
                                total_weight = total_weight + int(qty * item_weight)
            ship_capacity = int(ship_rec['SL']['ca'][0])
            actual_capacity = int(ship_capacity - ((ship_capacity * damaged) / 100))
            pct_loaded = math.floor((total_weight * 100) / actual_capacity)
            outf.write('<td>{}%</td>'.format(pct_loaded))
            storm = ''
            if 'SL' in ship_rec:
                if 'bs' in ship_rec['SL']:
                    storm_rec = data[ship_rec['SL']['bs'][0]]
                    storm = u.return_type(storm_rec['firstline'][0]) + ' [' + anchor(to_oid(u.return_unitid(storm_rec['firstline'][0]))) + '] (' + storm_rec['MI']['ss'][0] + ')'
            outf.write('<td>{}</td>'.format(storm))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def item_report(data, trade_chain):
    outf = open('master_item_report.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>Olympia Master Item Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Item Report</H3>\n')
    outf.write('<table border="1" style="border-collapse: collapse">\n')
    outf.write('<tr><th>Item</th><th>Type</th><th>Weight</th><th>Man Item</th><th>Prominent</th><th>Animal</th><th>Land Cap</th><th>Ride Cap</th><th>Flying Cap</th><th>Who Has</th><th>Notes</th></tr>\n')
    for id in data:
        if u.is_item(data, id):
            item_rec = data[id]
            outf.write('<tr>')
            outf.write('<td>{} [{}]</td>'.format(item_rec['na'][0],
                                                 anchor(to_oid(id))))
            outf.write('<td>{}</td>'.format(u.return_type(item_rec['firstline'][0])))
            weight = ''
            if 'IT' in item_rec:
                if 'wt' in item_rec['IT']:
                    weight = item_rec['IT']['wt'][0]
            outf.write('<td>{}</td>'.format(weight))
            man_item = ''
            if 'IT' in item_rec:
                if 'mu' in item_rec['IT']:
                    man_item = item_rec['IT']['mu'][0]
            outf.write('<td>{}</td>'.format(man_item))
            prominent = ''
            if 'IT' in item_rec:
                if 'pr' in item_rec['IT']:
                    prominent = item_rec['IT']['pr'][0]
            outf.write('<td>{}</td>'.format(prominent))
            animal = ''
            if 'IT' in item_rec:
                if 'an' in item_rec['IT']:
                    animal = item_rec['IT']['an'][0]
            outf.write('<td>{}</td>'.format(animal))
            land_cap = ''
            if 'IT' in item_rec:
                if 'lc' in item_rec['IT']:
                    land_cap = item_rec['IT']['lc'][0]
            outf.write('<td>{}</td>'.format(land_cap))
            ride_cap = ''
            if 'IT' in item_rec:
                if 'rc' in item_rec['IT']:
                    ride_cap = item_rec['IT']['rc'][0]
            outf.write('<td>{}</td>'.format(ride_cap))
            fly_cap = ''
            if 'IT' in item_rec:
                if 'fc' in item_rec['IT']:
                    fly_cap = item_rec['IT']['fc'][0]
            outf.write('<td>{}</td>'.format(fly_cap))
            who_has = ''
            if 'IT' in item_rec:
                if 'un' in item_rec['IT']:
                    who_has = item_rec['IT']['un'][0]
                    who_rec = data[who_has]
                    name = ''
                    if 'na' in who_rec:
                        name = who_rec['na'][0]
                    else:
                        name = u.return_type(who_rec['firstline'][0]).capitalize()
                    who_has = name + ' [' + anchor(to_oid(who_has)) + ']'
            outf.write('<td>{}</td>'.format(who_has))
            outf.write('<td>{}</td>'.format(u.determine_item_use(item_rec, data, trade_chain)))
        outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def player_report(data):
    outf = open('master_player_report.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>Olympia Master Player Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Player Report</H3>\n')
    outf.write('<table border="1" style="border-collapse: collapse">\n')
    outf.write('<tr><th>Player</th><th>Name</th><th>Type</th><th># Units</th></tr>\n')
    for id in data:
        if u.is_player(data, id):
            player_rec = data[id]
            outf.write('<tr>')
            outf.write('<td>{} [{}]</td>'.format(player_rec['na'][0],
                                                 anchor(to_oid(id))))
            outf.write('<td>{}</td>'.format(player_rec['na'][0]))
            outf.write('<td>{}</td>'.format(u.return_type(player_rec['firstline'][0])))
            count = '0'
            if 'PL' in player_rec:
                if 'un' in player_rec['PL']:
                    count = len(player_rec['PL']['un'])
            outf.write('<td>{}</td>'.format(count))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def healing_potion_report(data):
    outf = open('master_healing_potion_report.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>Olympia Master Healing Potion Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Healing Potion Report</H3>\n')
    outf.write('<table border="1" style="border-collapse: collapse">\n')
    outf.write('<tr><th>Item</th><th>Who Has</th><th>Location</th></tr>\n')
    for id in data:
        if u.is_item(data, id):
            itemz = data[id]
            if 'IM' in itemz:
                if 'uk' in itemz['IM']:
                    if itemz['IM']['uk'][0] == '2':
                        outf.write('<tr>')
                        outf.write('<td>{} [{}]</td>'.format(itemz['na'][0], anchor(to_oid(id))))
                        if 'IT' in itemz:
                            if 'un' in itemz['IT']:
                                unit = data[itemz['IT']['un'][0]]
                                if u.return_kind(unit['firstline'][0]) == 'char':
                                    charac = data[itemz['IT']['un'][0]]
                                    outf.write('<td>{} [{}]</td><td>&nbsp;</td>'.format(charac['na'][0],
                                                                                        anchor(to_oid(itemz['IT']['un'][0]))))
                                elif u.return_kind(unit['firstline'][0]) == 'loc':
                                    loc = data[itemz['IT']['un'][0]]
                                    outf.write('<td>&nbsp;</td><td>{} [{}]</td>'.format(loc['na'][0],
                                                                                        anchor(to_oid(itemz['IT']['un'][0]))))
                                else:
                                    outf.write('<td>unknown</td><td>unknown</td>')
                            else:
                                outf.write('<td>unknown</td><td>unknown</td>')
                        else:
                            outf.write('<td>unknown</td><td>unknown</td>')
                        outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def orb_report(data):
    outf = open('master_orb_report.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>Olympia Master Orb Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Orb Report</H3>\n')
    outf.write('<table border="1" style="border-collapse: collapse">\n')
    outf.write('<tr><th>Item</th><th>Who Has</th></tr>\n')
    for id in data:
        if u.is_item(data, id):
            itemz = data[id]
            if 'IM' in itemz:
                if 'uk' in itemz['IM']:
                    if itemz['IM']['uk'][0] == '9':
                        outf.write('<tr>')
                        outf.write('<td>{} [{}]</td>'.format(itemz['na'][0], anchor(to_oid(id))))
                        if 'IT' in itemz:
                            if 'un' in itemz['IT']:
                                charac = data[itemz['IT']['un'][0]]
                                outf.write('<td>{} [{}]</td>'.format(charac['na'][0],
                                                                    anchor(to_oid(itemz['IT']['un'][0]))))
                            else:
                                outf.write('<td>unknown</td>')
                        else:
                            outf.write('<td>unknown</td><')
                        outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def projected_cast_potion_report(data):
    outf = open('master_projected_cast_report.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>Olympia Master Projected Cast Potion Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Projected Cast Potion Report</H3>\n')
    outf.write('<table border="1" style="border-collapse: collapse">\n')
    outf.write('<tr><th>Item</th><th>Who Has</th><th>Target</th></tr>\n')
    for id in data:
        if u.is_item(data, id):
            itemz = data[id]
            if 'IM' in itemz:
                if 'uk' in itemz['IM']:
                    if itemz['IM']['uk'][0] == '5':
                        outf.write('<tr>')
                        outf.write('<td>{} [{}]</td>'.format(itemz['na'][0], anchor(to_oid(id))))
                        if 'IT' in itemz:
                            if 'un' in itemz['IT']:
                                charac = data[itemz['IT']['un'][0]]
                                outf.write('<td>{} [{}]</td>'.format(charac['na'][0],
                                                                    anchor(to_oid(itemz['IT']['un'][0]))))
                            else:
                                outf.write('<td>unknown</td>')
                        else:
                            outf.write('<td>unknown</td><')
                        if 'IM' in itemz:
                            if 'pc' in itemz['IM']:
                                try:
                                    loc = data[itemz['IM']['pc'][0]]
                                    outf.write('<td>{} {} [{}]</td>'.format(u.return_kind(loc['firstline'][0]),
                                                                            loc['na'][0],
                                                                            anchor(to_oid(itemz['IM']['pc'][0]))))
                                except KeyError:
                                    outf.write('<td>unknown {}</td>'.format(itemz['IM']['pc'][0]))
                            else:
                                outf.write('<td>unknown</td>')
                        else:
                            outf.write('<td>unknown</td><')
                        outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def location_report(data):
    outf = open('master_location_report.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>Olympia Master Location Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Location Report</H3>\n')
    outf.write('<table border="1" style="border-collapse: collapse">\n')
    outf.write('<tr><th>Location</th><th>Type</th><th>Region</th></tr>\n')
    for id in data:
        if u.is_loc(data, id):
            loc = data[id]
            name = ''
            if 'na' in loc:
                name = loc['na'][0]
            else:
                name = u.return_type(loc['firstline'][0]).capitalize()
            outf.write('<tr>')
            outf.write('<td>{} [{}]</td>'.format(name,
                                                 anchor(to_oid(id))))
            outf.write('<td>{}</td>'.format(u.return_type(loc['firstline'][0])))
            region = u.region(id, data)
            region_rec = data[region]
            outf.write('<td>{} [{}]</td>'.format(region_rec['na'][0],
                                                 anchor(to_oid(region))))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def skill_xref_report(data, teaches_chain):
    outf = open('master_skill_xref_report.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>Olympia Master Skill Xref Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Skill Xref Report</H3>\n')
    outf.write('<table border="1" style="border-collapse: collapse">\n')
    outf.write('<tr><th>Skill</th><th>Location</th><th>Region</th></tr>\n')
    skill_list = sorted(list(teaches_chain))
    for id in skill_list:
        city_list = teaches_chain[id]
        if len(city_list) > 0 and id is not None:
            skill_rec = data[id]
            for city in city_list:
                loc = data[city]
                where_rec = data[loc['LI']['wh'][0]]
                outf.write('<tr>')
                outf.write('<td>{} [{}]</td>'.format(skill_rec['na'][0],
                                                     anchor(to_oid(id))))
                outf.write('<td>{} [{}], {} [{}]</td>'.format(loc['na'][0],
                                                              anchor(to_oid(city)),
                                                              where_rec['na'][0],
                                                              anchor(to_oid(loc['LI']['wh'][0]))))
                region = u.region(city, data)
                region_rec = data[region]
                outf.write('<td>{} [{}]</td>'.format(region_rec['na'][0],
                                                     anchor(to_oid(region))))
                outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def trade_report(data, trade_chain):
    outf = open('master_trade_report.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>Olympia Master Trade Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Trade Report</H3>\n')
    outf.write('<table border="1" style="border-collapse: collapse">\n')
    outf.write('<tr><th>Item</th><th>Seller</th><th>Buyer</th><th>Sell Region</th><th>Buy Region</th></tr>\n')
    trade_list = sorted(list(trade_chain))
    for id in trade_list:
        city_list = trade_chain[id]
        if len(city_list) > 0 and id is not None:
            item_rec = data[id]
            buy_literal = ''
            sell_literal = ''
            buy_reg_literal = ''
            sell_reg_literal = ''
            for city in city_list:
                loc = data[city[0]]
                if city[1] == '1':
                    if len(buy_literal) > 0:
                        buy_literal = buy_literal + '<br>'
                        buy_reg_literal = buy_reg_literal + '<br>'
                    buy_literal = buy_literal + loc['na'][0] + ' [' + anchor(to_oid(city[0])) + ']'
                    reg_rec = data[u.region(city[0], data)]
                    buy_reg_literal = buy_reg_literal + reg_rec['na'][0] + ' [' + anchor(to_oid(u.region(city[0], data))) + ']'
                else:
                    if len(sell_literal) > 0:
                        sell_literal = sell_literal + '<br>'
                        sell_reg_literal = sell_reg_literal + '<br>'
                    sell_literal = sell_literal + loc['na'][0] + ' [' + anchor(to_oid(city[0])) + ']'
                    reg_rec = data[u.region(city[0], data)]
                    sell_reg_literal = sell_reg_literal + reg_rec['na'][0] + ' [' + anchor(to_oid(u.region(city[0], data))) + ']'
            outf.write('<tr>')
            outf.write('<td>{} [{}]</td>'.format(item_rec['na'][0],
                                                 anchor(to_oid(id))))
            outf.write('<td>{}</td>'.format(sell_literal))
            outf.write('<td>{}</td>'.format(buy_literal))
            outf.write('<td>{}</td>'.format(sell_reg_literal))
            outf.write('<td>{}</td>'.format(buy_reg_literal))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()
