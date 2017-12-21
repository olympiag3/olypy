#!/usr/bin/python
import math

from olypy.oid import to_oid
from olypy.oid import to_int
import olymap.utilities as u
from olymap.utilities import anchor
import olymap.maps as maps
import pathlib


def ship_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_ship_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Ship Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Ship Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Id</th><th>Type</th><th>Captain</th><th>Location</th><th>Damage</th>'
               '<th>Load</th><th>Storm (Strength)</th></tr>\n')
    ship_list = []
    for unit in data:
        if u.is_ship(data, unit):
            ship_list.append(int(to_int(unit)))
    ship_list.sort()
    if ship_list != '':
        for unit in ship_list:
            ship_rec = data[str(unit)]
            outf.write('<tr>')
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(to_oid(unit),
                                                                          ship_rec['na'][0],
                                                                          anchor(to_oid(unit))))
            outf.write('<td>{}</td>'.format(u.return_type(ship_rec)))
            captain = '&nbsp;'
            captainid = ''
            if 'LI' in ship_rec and 'hl' in ship_rec['LI']:
                here_list = ship_rec['LI']['hl']
                for here in here_list:
                    if u.is_char(data, here):
                        here_rec = data[here]
                        captain = here_rec['na'][0] + ' [' + anchor(to_oid(here)) + ']'
                        captainid = to_oid(here)
                        break
            outf.write('<td sorttable_customkey="{}">{}</td>'.format(captainid,
                                                                     captain))
            location = '&nbsp;'
            locid = ''
            if 'LI' in ship_rec and 'wh' in ship_rec['LI']:
                where_rec = data[ship_rec['LI']['wh'][0]]
                location = where_rec['na'][0] + ' [' + anchor(to_oid(u.return_unitid(where_rec))) + ']'
                locid = to_oid(u.return_unitid(where_rec))
            outf.write('<td sorttable_customkey="{}">{}</td>'.format(locid,
                                                                     location))
            if 'SL' in ship_rec and 'da' in ship_rec['SL']:
                outf.write('<td>{}%</td>'.format(ship_rec['SL']['da'][0]))
                damaged = int(ship_rec['SL']['da'][0])
            else:
                outf.write('<td>0%</td>')
                damaged = 0
            total_weight = 0
            seen_here_list = []
            level = 0
            seen_here_list = u.chase_structure(unit, data, level, seen_here_list)
            list_length = len(seen_here_list)
            if list_length > 1:
                for un in seen_here_list[1:]:
                    char = data[un[0]]
                    if u.return_kind(char) == 'char':
                        unit_type = '10'
                        if 'CH' in char:
                            if 'ni' in char['CH']:
                                unit_type = char['CH']['ni'][0]
                        base_unit = data[unit_type]
                        if 'IT' in base_unit and 'wt' in base_unit['IT']:
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
            stormid = ''
            if 'SL' in ship_rec:
                if 'bs' in ship_rec['SL']:
                    storm_rec = data[ship_rec['SL']['bs'][0]]
                    storm = u.return_type(storm_rec) + ' [' \
                            + anchor(to_oid(u.return_unitid(storm_rec))) \
                            + '] (' + storm_rec['MI']['ss'][0] + ')'
                    stormid = u.return_unitid(storm_rec)
            outf.write('<td sorttable_customkey="{}">{}</td>'.format(stormid,
                                                                     storm))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def item_report(data, trade_chain, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_item_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Item Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Item Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Item</th><th>Type</th><th>Weight</th><th>Man Item</th>'
               '<th>Prominent</th><th>Animal</th><th>Land Cap</th><th>Ride Cap</th>'
               '<th>Flying Cap</th><th>Who Has</th><th>Notes</th></tr>\n')
    item_list = []
    for unit in data:
        if u.is_item(data, unit):
            item_list.append(int(to_int(unit)))
    item_list.sort()
    if item_list != '':
        for unit in item_list:
            item_rec = data[str(unit)]
            outf.write('<tr>')
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                          item_rec['na'][0],
                                                                          anchor(to_oid(unit))))
            outf.write('<td>{}</td>'.format(u.return_type(item_rec)))
            if 'IT' in item_rec:
                weight = ''
                if 'wt' in item_rec['IT']:
                    weight = item_rec['IT']['wt'][0]
                outf.write('<td>{}</td>'.format(weight))
                man_item = ''
                if 'mu' in item_rec['IT']:
                    man_item = item_rec['IT']['mu'][0]
                outf.write('<td>{}</td>'.format(man_item))
                prominent = ''
                if 'pr' in item_rec['IT']:
                    prominent = item_rec['IT']['pr'][0]
                outf.write('<td>{}</td>'.format(prominent))
                animal = ''
                if 'an' in item_rec['IT']:
                    animal = item_rec['IT']['an'][0]
                outf.write('<td>{}</td>'.format(animal))
                land_cap = ''
                if 'lc' in item_rec['IT']:
                    land_cap = item_rec['IT']['lc'][0]
                outf.write('<td>{}</td>'.format(land_cap))
                ride_cap = ''
                if 'rc' in item_rec['IT']:
                    ride_cap = item_rec['IT']['rc'][0]
                outf.write('<td>{}</td>'.format(ride_cap))
                fly_cap = ''
                if 'fc' in item_rec['IT']:
                    fly_cap = item_rec['IT']['fc'][0]
                outf.write('<td>{}</td>'.format(fly_cap))
                if 'un' in item_rec['IT']:
                    who_has = item_rec['IT']['un'][0]
                    who_rec = data[who_has]
                    if 'na' in who_rec:
                        name = who_rec['na'][0]
                    else:
                        name = u.return_type(who_rec).capitalize()
                        if name == 'Ni':
                            name = data[who_rec['CH']['ni'][0]]['na'][0].capitalize()
                    who_literal = name + ' [' + anchor(to_oid(who_has)) + ']'
                    outf.write('<td sorttable_customkey="{}">{}</td>'.format(who_has,
                                                                             who_literal))
                else:
                    outf.write('<td>&nbsp;</td>')
            else:
                outf.write('<td>&nbsp;</td>'*8)
            outf.write('<td>{}</td>'.format(u.determine_item_use(item_rec, data, trade_chain)))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def player_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_player_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Player Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Player Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Player</th><th>Name</th><th>Type</th><th># Units</th></tr>\n')
    player_list = []
    for unit in data:
        if u.is_player(data, unit):
            player_list.append(int(to_int(unit)))
    player_list.sort()
    if player_list != '':
        for unit in player_list:
            player_rec = data[str(unit)]
            outf.write('<tr>')
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                          player_rec['na'][0],
                                                                          anchor(to_oid(unit))))
            outf.write('<td>{}</td>'.format(player_rec['na'][0]))
            outf.write('<td>{}</td>'.format(u.return_type(player_rec)))
            count = '0'
            if 'PL' in player_rec and 'un' in player_rec['PL']:
                count = len(player_rec['PL']['un'])
            outf.write('<td>{}</td>'.format(count))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def healing_potion_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_healing_potion_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Healing Potion Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Healing Potion Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Item</th><th>Who Has</th><th>Location</th></tr>\n')
    healing_potion_list = []
    for unit in data:
        if u.is_item(data, unit):
            healing_potion_list.append(int(to_int(unit)))
    healing_potion_list.sort()
    if healing_potion_list != '':
        for unit in healing_potion_list:
            itemz = data[str(unit)]
            if 'IM' in itemz and 'uk' in itemz['IM']:
                if itemz['IM']['uk'][0] == '2':
                    outf.write('<tr>')
                    outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                                  itemz['na'][0],
                                                                                  anchor(to_oid(unit))))
                    if 'IT' in itemz and 'un' in itemz['IT']:
                        unit = data[itemz['IT']['un'][0]]
                        if u.return_kind(unit) == 'char':
                            charac = data[itemz['IT']['un'][0]]
                            outf.write('<td sorttable_customkey="">{} [{}]</td>'
                                       '<td sorttable_customkey="">'
                                       '&nbsp;</td>'.format(itemz['IT']['un'][0],
                                                            charac['na'][0],
                                                            anchor(to_oid(itemz['IT']['un'][0]))))
                        elif u.return_kind(unit) == 'loc':
                            loc = data[itemz['IT']['un'][0]]
                            outf.write('<td sorttable_customkey="">&nbsp;</td>'
                                       '<td sorttable_customkey="{}">'
                                       '{} [{}]</td>'.format(itemz['IT']['un'][0],
                                                             loc['na'][0],
                                                             anchor(to_oid(itemz['IT']['un'][0]))))
                        else:
                            outf.write('<td sorttable_customkey="">unknown</td><td sorttable_customkey="">unknown</td>')
                    else:
                        outf.write('<td sorttable_customkey="">unknown</td><td sorttable_customkey="">unknown</td>')
                    outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def orb_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_orb_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Orb Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Orb Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Item</th><th>Who Has</th></tr>\n')
    orb_list = []
    for unit in data:
        if u.is_item(data, unit):
            orb_list.append(int(to_int(unit)))
        orb_list.sort()
    if orb_list != '':
        for unit in orb_list:
            itemz = data[str(unit)]
            if 'IM' in itemz and 'uk' in itemz['IM']:
                if itemz['IM']['uk'][0] == '9':
                    outf.write('<tr>')
                    outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                                  itemz['na'][0],
                                                                                  anchor(to_oid(unit))))
                    if 'IT' in itemz:
                        if 'un' in itemz['IT']:
                            charac = data[itemz['IT']['un'][0]]
                            outf.write('<td sorttable_customkey="{}">'
                                       '{} [{}]</td>'.format(itemz['IT']['un'][0],
                                                             charac['na'][0],
                                                             anchor(to_oid(itemz['IT']['un'][0]))))
                        else:
                            outf.write('<td sorttable_customkey="">unknown</td>')
                    else:
                        outf.write('<td sorttable_customkey="">unknown</td><')
                    outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def projected_cast_potion_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_projected_cast_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Projected Cast Potion Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Projected Cast Potion Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Item</th><th>Who Has</th><th>Target</th><th>Target Region</th></tr>\n')
    projected_cast_list = []
    for unit in data:
        if u.is_item(data, unit):
            projected_cast_list.append(int(to_int(unit)))
    projected_cast_list.sort()
    if projected_cast_list != '':
        for unit in projected_cast_list:
            itemz = data[str(unit)]
            if 'IM' in itemz and 'uk' in itemz['IM']:
                if itemz['IM']['uk'][0] == '5':
                    outf.write('<tr>')
                    outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                                  itemz['na'][0],
                                                                                  anchor(to_oid(unit))))
                    if 'IT' in itemz and 'un' in itemz['IT']:
                        charac = data[itemz['IT']['un'][0]]
                        outf.write('<td sorttable_customkey="{}">'
                                   '{} [{}]</td>'.format(itemz['IT']['un'][0],
                                                         charac['na'][0],
                                                         anchor(to_oid(itemz['IT']['un'][0]))))
                    else:
                        outf.write('<td sorttable_customkey="{}">unknown</td><')
                    if 'IM' in itemz and 'pc' in itemz['IM']:
                        try:
                            loc = data[itemz['IM']['pc'][0]]
                            outf.write('<td sorttable_customkey="{}">'
                                       '{} {} [{}]</td>'.format(itemz['IM']['pc'],
                                                                u.return_kind(loc),
                                                                loc['na'][0],
                                                                anchor(to_oid(itemz['IM']['pc'][0]))))
                            try:
                                region = u.region(str(itemz['IM']['pc'][0]), data)
                                region_rec = data[region]
                                outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(region,
                                                                                              region_rec['na'][0],
                                                                                              anchor(to_oid(region))))
                            except KeyError:
                                outf.write('<td>&nbsp;</td>')
                        except KeyError:
                            outf.write('<td sorttable_customkey="">unknown {}</td><td>&nbsp;</td>'.format(itemz['IM']['pc'][0]))
                    else:
                        outf.write('<td sorttable_customkey="">unknown</td><td>&nbsp;</td>')
                    outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def location_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_location_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Location Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Location Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Location</th><th>Type</th><th>Region</th><th># Men</th></tr>\n')
    location_list = []
    for unit in data:
        if u.is_loc(data, unit):
            location_list.append(int(to_int(unit)))
    location_list.sort()
    if location_list != '':
        for unit in location_list:
            loc = data[str(unit)]
            if 'na' in loc:
                name = loc['na'][0]
            else:
                name = u.return_type(loc).capitalize()
            outf.write('<tr>')
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                          name,
                                                                          anchor(to_oid(unit))))
            outf.write('<td>{}</td>'.format(u.return_type(loc)))
            region = u.region(str(unit), data)
            region_rec = data[region]
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(region,
                                                                          region_rec['na'][0],
                                                                          anchor(to_oid(region))))
            nbrmen, _, _ = maps.count_stuff(loc, data)
            outf.write('<td>{}</td>'.format(nbrmen))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


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
    outf = open(pathlib.Path(outdir).joinpath('master_road_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Road Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Road Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Type</th><th>Name</th><th>Start</th><th>Destination</th></tr>\n')
    road_list = []
    for unit in data:
        if u.is_road_or_gate(data[unit]):
            road_list.append(int(to_int(unit)))
    road_list.sort()
    if road_list != '':
        for road in road_list:
            road_rec = data[str(road)]
            try:
                if road_rec['GA']['rh'][0] == '1':
                    outf.write('<tr>')
                    outf.write('<td>{}</td>'.format(u.return_kind(road_rec)))
                    outf.write('<td>{}</td>'.format(road_rec['na'][0]))
                    start = road_rec['LI']['wh'][0]
                    start_rec = data[start]
                    outf.write('<td>{} [{}]</td>'.format(start_rec['na'][0],
                                                         anchor(to_oid(u.return_unitid(start_rec)))))
                    dest = road_rec['GA']['tl'][0]
                    dest_rec = data[dest]
                    outf.write('<td>{} [{}]</td>'.format(dest_rec['na'][0],
                                                         anchor(to_oid(u.return_unitid(dest_rec)))))
                    outf.write('</tr>\n')
            except KeyError:
                pass
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def gate_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_gate_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Gate Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Gate Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Type</th><th>Start</th><th>Destination</th></tr>\n')
    road_list = []
    for unit in data:
        if u.is_road_or_gate(data[unit]):
            road_list.append(int(to_int(unit)))
    road_list.sort()
    if road_list != '':
        for road in road_list:
            road_rec = data[str(road)]
            try:
                if road_rec['GA']['rh'][0] == '1':
                    pass
            except KeyError:
                outf.write('<tr>')
                outf.write('<td>{}</td>'.format(u.return_kind(road_rec)))
                start = road_rec['LI']['wh'][0]
                start_rec = data[start]
                outf.write('<td>{} [{}]</td>'.format(start_rec['na'][0],
                                                     anchor(to_oid(u.return_unitid(start_rec)))))
                dest = road_rec['GA']['tl'][0]
                dest_rec = data[dest]
                outf.write('<td>{} [{}]</td>'.format(dest_rec['na'][0],
                                                     anchor(to_oid(u.return_unitid(dest_rec)))))
                outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def character_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_character_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Character Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Character Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Character</th><th>Name</th><th>Faction</th><th>Loyalty</th>'
               '<th>Health</th><th>Mage</th><th>Priest</th><th># Men</th></tr>\n')
    character_list = []
    for unit in data:
        if u.is_char(data, unit):
            character_list.append(int(to_int(unit)))
    character_list.sort()
    if character_list != '':
        for unit in character_list:
            character = data[str(unit)]
            if 'na' in character:
                name = character['na'][0]
            else:
                name = u.return_type(character).capitalize()
            if name == 'Ni':
                name = data[character['CH']['ni'][0]]['na'][0].capitalize()
            outf.write('<tr>')
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                          name,
                                                                          anchor(to_oid(unit))))
            outf.write('<td>{}</td>'.format(name))
            if 'CH' in character and 'lo' in character['CH']:
                player = data[character['CH']['lo'][0]]
                outf.write('<td sorttable_customkey="{}">{} [{}]</td>\n'.format(u.return_unitid(player),
                                                                                     player['na'][0],
                                                                                     anchor(to_oid(u.return_unitid(player)))))
            else:
                outf.write('<td>&nbsp;</td>')
            outf.write('<td>{}</td>'.format(u.xlate_loyalty(character)))
            if 'CH' in character and 'he' in character['CH']:
                if int(character['CH']['he'][0]) < 0:
                    health = 'n/a'
                else:
                    health = character['CH']['he'][0]
                outf.write('<td>{}</td>'.format(health))
            else:
                outf.write('<td>&nbsp;</td>')
            if u.is_magician(character):
                outf.write('<td>Yes</td>')
            else:
                outf.write('<td>No</td>')
            if u.is_priest(character):
                outf.write('<td>Yes</td>')
            else:
                outf.write('<td>No</td>')
            nbrmen, _, _ = maps.count_stuff(character, data)
            outf.write('<td>{}</td>'.format(nbrmen))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


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
            graveyard_list.append(int(to_int(unit)))
        graveyard_list.sort()
    if graveyard_list != '':
        for unit in graveyard_list:
            graveyard = data[str(unit)]
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
            faeryhill_list.append(int(to_int(unit)))
        faeryhill_list.sort()
    if faeryhill_list != '':
        for unit in faeryhill_list:
            faeryhill = data[str(unit)]
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
    outf = open(pathlib.Path(outdir).joinpath('master_castle_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Castle Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Castle Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Castle</th><th>Province</th><th>Region</th><th># Garr</th><th># Men</th></tr>\n')
    castle_list = []
    for unit in data:
        if u.is_castle(data, unit):
            castle_list.append(int(to_int(unit)))
        castle_list.sort()
    if castle_list != '':
        for unit in castle_list:
            castle = data[str(unit)]
            if 'na' in castle:
                name = castle['na'][0]
            else:
                name = u.return_type(castle).capitalize()
            outf.write('<tr>')
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                          name,
                                                                          anchor(to_oid(unit))))
            loc_rec = data[castle['LI']['wh'][0]]
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
            garrison_list = garrisons_chain[str(unit)]
            outf.write('<td>{}</td>'.format(len(garrison_list)))
            nbrmen, _, _ = maps.count_stuff(castle, data)
            outf.write('<td>{}</td>'.format(nbrmen))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


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
            city_list.append(int(to_int(unit)))
        city_list.sort()
    if city_list != '':
        for unit in city_list:
            city = data[str(unit)]
            if 'na' in city:
                name = city['na'][0]
            else:
                name = u.return_type(city).capitalize()
            outf.write('<tr>')
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                          name,
                                                                          anchor(to_oid(unit))))
            loc_rec = data[city['LI']['wh'][0]]
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
            outf.write('<td>{}</td>'.format(u.is_port_city(city, data)))
            nbrmen, _, _ = maps.count_stuff(city, data)
            outf.write('<td>{}</td>'.format(nbrmen))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def region_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_region_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Region Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Region Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Region</th><th>Provinces</th></tr>\n')
    region_list = []
    for unit in data:
        if u.is_region(data, unit):
            region_list.append(int(to_int(unit)))
        region_list.sort()
    if region_list != '':
        for unit in region_list:
            region_rec = data[str(unit)]
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                          region_rec['na'][0],
                                                                          anchor(to_oid(unit))))
            nbr_provinces = 0
            if 'LI' in region_rec:
                if 'hl' in region_rec['LI']:
                    nbr_provinces = len(region_rec['LI']['hl'])
            outf.write('<td>{}</td>'.format(nbr_provinces))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def mage_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_mage_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Mage Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master Mage Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Mage</th><th>Mage Name</th><th>Rank</th>'
               '<th>Curr Aura</th><th>Max Aura</th><th>Auraculum Aura</th><th>Total Aura</th>'
               '<th>Auraculum</th><th>Player</th></tr>\n')
    mage_list = []
    for unit in data:
        if u.is_magician(data[unit]):
            mage_list.append(int(to_int(unit)))
        mage_list.sort()
    if mage_list != '':
        for unit in mage_list:
            mage_rec = data[str(unit)]
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                          mage_rec['na'][0],
                                                                          anchor(to_oid(unit))))
            outf.write('<td>{}</td>'.format(mage_rec['na'][0]))
            outf.write('<td>{}</td>'.format(u.xlate_magetype(mage_rec, data)))
            current_aura = 0
            max_aura = 0
            auraculum_aura = 0
            total_aura = 0
            auraculum_id = ''
            auraculum_name = ''
            if 'CM' in mage_rec:
                if 'ca' in mage_rec['CM']:
                    current_aura = int(mage_rec['CM']['ca'][0])
                if 'ma' in mage_rec['CM']:
                    max_aura = int(mage_rec['CM']['ma'][0])
                if 'ar' in mage_rec['CM']:
                    auraculum = data[mage_rec['CM']['ar'][0]]
                    auraculum_id = mage_rec['CM']['ar'][0]
                    if 'IM' in auraculum and 'au' in auraculum['IM']:
                        auraculum_aura = int(auraculum['IM']['au'][0])
                        auraculum_name = auraculum['na'][0]
                total_aura = max_aura + auraculum_aura
            outf.write('<td>{}</td>'.format(current_aura))
            outf.write('<td>{}</td>'.format(max_aura))
            outf.write('<td>{}</td>'.format(auraculum_aura))
            outf.write('<td>{}</td>'.format(total_aura))
            if len(auraculum_id) > 0:
                outf.write('<td>{} [{}]</td>'.format(auraculum_name,
                                                     anchor(to_oid(auraculum_id))))
            else:
                outf.write('<td>&nbsp;</td>')
            if 'CH' in mage_rec and 'lo' in mage_rec['CH']:
                player = data[mage_rec['CH']['lo'][0]]
                outf.write('<td sorttable_customkey="{}">{} [{}]</td>\n'.format(u.return_unitid(player),
                                                                                player['na'][0],
                                                                                anchor(to_oid(u.return_unitid(player)))))
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()


def priest_report(data, outdir):
    outf = open(pathlib.Path(outdir).joinpath('master_priest_report.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<script src="sorttable.js"></script>')
    outf.write('<TITLE>Olympia Master Priest Report</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<H3>Olympia Master priest Report</H3>\n')
    outf.write('<h5>(Click on table headers to sort)</h5>')
    outf.write('<table border="1" style="border-collapse: collapse" class="sortable">\n')
    outf.write('<tr><th>Priest</th><th>Priest Name</th><th>Visons Received</th></tr>\n')
    priest_list = []
    for unit in data:
        if u.is_priest(data[unit]):
            priest_list.append(int(to_int(unit)))
        priest_list.sort()
    if priest_list != '':
        for unit in priest_list:
            priest_rec = data[str(unit)]
            outf.write('<td sorttable_customkey="{}">{} [{}]</td>'.format(unit,
                                                                          priest_rec['na'][0],
                                                                          anchor(to_oid(unit))))
            outf.write('<td>{}</td>'.format(priest_rec['na'][0]))
            if 'CM' in priest_rec and 'vi' in priest_rec['CM']:
                vision_list = priest_rec['CM']['vi']
                outf.write('<td>')
                outf.write('<table>')
                second = False
                for vision in vision_list:
                    if not second:
                        outf.write('<tr>')
                    outf.write('<td>')
                    try:
                        visioned = data[vision]
                        vision_name = visioned['na'][0]
                    except KeyError:
                        vision_name = 'missing'
                    outf.write('{} [{}]'.format(vision_name,
                                                anchor(to_oid(vision))))
                    outf.write('</td>')
                    if second:
                        outf.write('</tr>')
                        second = False
                    else:
                        second = True
                outf.write('</table>')
                outf.write('</td>')
            outf.write('</tr>\n')
    outf.write('</table>\n')
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()
