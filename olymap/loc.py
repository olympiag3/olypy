#!/usr/bin/python

import math

from olypy.oid import to_oid
import olymap.utilities as u
import olypy.details as details
import olymap.detail as detail
from operator import itemgetter
# import olymap.ship as ship
from olymap.utilities import anchor, anchor2, get_oid, get_name, get_type, to_oid, loop_here2, get_who_has
from olymap.utilities import calc_ship_pct_loaded, is_impassable
import pathlib
from jinja2 import Environment, PackageLoader, select_autoescape
from olymap.char import get_items_list
from olymap.item import get_weight

pd_directions = {0: 'North', 1: 'East', 2: 'South', 3: 'West', 4: 'Up', 5: 'Down'}


def write_loc_page_header(v, k, data, outf):
    outf.write('<H3>')
    loc_type = get_type(v, data)
    outf.write('{} [{}]'.format(v['na'][0], to_oid(k)))
    outf.write(', {}'.format(loc_type))
    if u.return_type(v) != 'region':
        outf.write(', in')
        if loc_type == 'city':
            outf.write(' province ')
        try:
            loc2 = data[v['LI']['wh'][0]]
        except KeyError:
            pass
        else:
            outf.write(' {} [{}]'.format(loc2['na'][0],
                                         anchor(to_oid(u.return_unitid(loc2)))))
    # if 'city' in loc_type:
    #    outf.write(' [{}]'.format(anchor(to_oid(v['LI']['wh'][0]))))
    if 'SL' in v and 'sh' in v['SL']:
        outf.write(', safe haven')
    if 'LO' in v and 'hi' in v['LO']:
        outf.write(', hidden')
    if loc_type != 'ocean' and u.loc_depth(u.return_type(v)) == 2 \
            and data[u.region(k, data)]['na'][0] != 'faery' and data[u.region(k, data)]['na'][0] != 'hades':
        civ_level = 'wilderness'
        if 'LO' in v and 'lc' in v['LO']:
            if v['LO']['lc'][0] == '0':
                civ_level = 'wilderness'
            else:
                civ_level = 'civ-' + v['LO']['lc'][0]
        outf.write(', {}'.format(civ_level))
    outf.write('</H3>\n')


def write_loc_shroud(v, k, outf):
    if 'LO' in v and 'sh' in v['LO']:
        if v['LO']['sh'][0] != '0':
            outf.write('<p>A magical shroud surrounds {} [{}].</p>\n'.format(v['na'][0],
                                                                              anchor(to_oid(k))))


def write_loc_barrier(v, k, outf):
    if 'LO' in v and 'ba' in v['LO']:
        if v['LO']['ba'][0] != '0':
            outf.write('<p>A magical barrier surrounds {} [{}].</p>\n'.format(v['na'][0],
                                                                             anchor(to_oid(k))))


def write_loc_controlled_by(v, data, outf):
    if 'LI' in v and 'hl' in v['LI']:
        here_list = v['LI']['hl']
        if len(here_list) > 0:
            for loc in here_list:
                try:
                    charac = data[loc]
                except KeyError:
                    pass
                else:
                    if 'MI' in charac and 'gc' in charac['MI']:
                        if charac['MI']['gc'][0] != '0':
                            dest_loc = data[charac['MI']['gc'][0]]
                            dest_loc2 = data[dest_loc['LI']['wh'][0]]
                            outf.write('<p>Province controlled by ')
                            dest_name = dest_loc['na'][0]
                            dest_id = anchor(to_oid(u.return_unitid(dest_loc)))
                            dest_type = u.return_type(dest_loc)
                            outf.write('{} [{}], {}'.format(dest_name, dest_id, dest_type))
                            dest_type2 = u.return_type(dest_loc2)
                            if dest_type2 != 'city':
                                dest_name2 = dest_loc2['na'][0]
                                dest_id2 = anchor(to_oid(u.return_unitid(dest_loc2)))
                                outf.write(', in {} [{}]'.format(dest_name2, dest_id2))
                            else:
                                dest_loc2 = data[dest_loc2['LI']['wh'][0]]
                                dest_name2 = dest_loc2['na'][0]
                                dest_id2 = anchor(to_oid(u.return_unitid(dest_loc2)))
                                outf.write(', in {} [{}]'.format(dest_name2, dest_id2))
                            try:
                                garrison = data[dest_loc2['LI']['hl'][0]]
                            except KeyError:
                                pass
                            else:
                                garr_type = u.return_type(garrison)
                                if garr_type == 'garrison':
                                    # calculate top of pledge chain
                                    if 'LI' in dest_loc and 'hl' in dest_loc['LI']:
                                        top_guy = u.top_ruler(dest_loc['LI']['hl'][0], data)
                                        try:
                                            top_dog = data[top_guy]
                                        except KeyError:
                                            pass
                                        else:
                                            a = top_dog['na'][0]
                                            b = anchor(to_oid(top_guy))
                                            outf.write('<br>Ruled by {} [{}]'.format(a, b))
                            outf.write('</p>\n')


def write_province_destination(loc, dest_loc, direction, data, outf):
    if (u.is_port_city(dest_loc, data) or u.province_has_port_city(dest_loc, data) is not None) \
            and u.return_type(loc) == 'ocean':
        if not u.is_port_city(dest_loc, data):
            dest_loc = data[u.province_has_port_city(dest_loc, data)]
        dest_loc_host = data[dest_loc['LI']['wh'][0]]
        outf.write('<li>{}, port city, to {} [{}]'
                   .format(direction,
                           dest_loc['na'][0],
                           anchor(to_oid(u.return_unitid(dest_loc)))))
        if u.region(u.return_unitid(loc), data) != u.region(u.return_unitid(dest_loc), data):
            region_key = u.return_unitid(dest_loc)
            region_rec = data[u.region(region_key, data)]
            outf.write(', {}'.format(region_rec['na'][0]))
        barrier = '0'
        if 'LO' in dest_loc and 'ba' in dest_loc['LO']:
            barrier = dest_loc['LO']['ba'][0]
        if barrier != '0':
            outf.write(', impassable<br>&nbsp;&nbsp;&nbsp;A magical barrier prevents entry.')
        else:
            out_distance = u.calc_exit_distance(loc, dest_loc)
            outf.write(', {} {}'.format(out_distance,
                                        'day' if out_distance == 1 else 'days'))
        outf.write('</li>\n')
        outf.write('<li> {}, to {} [{}]'.format(direction,
                                                dest_loc_host['na'][0],
                                                anchor(to_oid(u.return_unitid(dest_loc_host)))))
        if u.region(u.return_unitid(loc), data) != \
           u.region(u.return_unitid(dest_loc), data):
            region_key = u.return_unitid(dest_loc_host)
            region_rec = data[u.region(region_key, data)]
            outf.write(', {}'.format(region_rec['na'][0]))
        barrier = '0'
        if 'LO' in dest_loc_host and 'ba' in dest_loc_host['LO']:
            barrier = dest_loc_host['LO']['ba'][0]
        if barrier != '0':
            outf.write(', impassable<br>&nbsp;&nbsp;&nbsp;A magical barrier prevents entry.')
        else:
            outf.write(', impassable')
        outf.write('</li>\n')
    else:
        outf.write('<li>{}'.format(direction))
        if direction == 'Out':
            outf.write(', {}'.format(u.return_type(dest_loc)))
        outf.write(', to {} [{}]'.format(dest_loc['na'][0],
                                         anchor(to_oid(u.return_unitid(dest_loc)))))
        if u.region(u.return_unitid(loc), data) != \
                u.region(u.return_unitid(dest_loc), data):
            region_key = u.return_unitid(dest_loc)
            region_rec = data[u.region(region_key, data)]
            outf.write(', {}'.format(region_rec['na'][0]))
        barrier = '0'
        if 'LO' in dest_loc and 'ba' in dest_loc['LO']:
            barrier = dest_loc['LO']['ba'][0]
        if barrier != '0':
            outf.write(', impassable<br>&nbsp;&nbsp;&nbsp;A magical barrier prevents entry.')
        elif (u.return_type(loc) == 'ocean' and \
            u.return_type(dest_loc) == 'mountain') or \
            (u.return_type(loc) == 'mountain' and \
            u.return_type(dest_loc) == 'ocean') and \
            direction.lower() not in details.road_directions:
            outf.write(', impassable')
        else:
            out_distance = u.calc_exit_distance(loc, dest_loc)
            outf.write(', {} {}'.format(out_distance,
                                        'day' if out_distance == 1 else 'days'))
        if dest_loc['na'][0] == 'Hades' and loc['na'][0] != 'Hades':
            outf.write('<br>&nbsp;&nbsp;&nbsp;"Notice to all mortals, from the Gatekeeper '
                       'Spirit of Hades: 100 gold/head<br>&nbsp;&nbsp;&nbsp;&nbsp;'
                       'is removed from any stack taking this road"')
        outf.write('</li>\n')


def write_province_destinations(v, data, outf):
    print_header = False
    pd_list = ''
    if 'LO' in v:
        if 'pd' in v['LO']:
            pd_list = v['LO']['pd']
    if len(pd_list) > 0:
        i = int(0)
        for pd in pd_list:
            if pd != '0':
                if not print_header:
                    print_header = True
                    outf.write('<H4>Routes leaving {}:</H4>\n'.format(v['na'][0]))
                    outf.write('<ul>\n')
                write_province_destination(v,
                                           data[pd],
                                           pd_directions[i],
                                           data,
                                           outf)
            i = i + 1
    if u.return_type(v) not in details.province_kinds:
        if 'LI' in v:
            if 'wh' in v['LI']:
                if not print_header:
                    print_header = True
                    outf.write('<H4>Routes leaving {}:</H4>\n'.format(v['na'][0]))
                    outf.write('<ul>\n')
                out_rec = data[v['LI']['wh'][0]]
                write_province_destination(v,
                                           out_rec,
                                           'Out',
                                           data,
                                           outf)
    # see if road or gate
    if 'LI' in v and 'hl' in v['LI']:
        here_list = v['LI']['hl']
        for here in here_list:
            here_record = data[here]
            if u.is_road_or_gate(here_record):
                to_record = data[here_record['GA']['tl'][0]]
                if u.return_kind(here_record) == 'gate':
                    name = 'Gate'
                else:
                    name = here_record['na'][0]
                if not print_header:
                    print_header = True
                    outf.write('<H4>Routes leaving {}:</H4>\n'.format(v['na'][0]))
                    outf.write('<ul>\n')
                write_province_destination(v,
                                           to_record,
                                           name,
                                           data,
                                           outf)
    if 'SL' in v and 'lt' in v['SL']:
        link_to_record = data[v['SL']['lt'][0]]
        if not print_header:
            print_header = True
            outf.write('<H4>Routes leaving {}:</H4>\n'.format(v['na'][0]))
            outf.write('<ul>\n')
        write_province_destination(v,
                                   link_to_record,
                                   u.return_type(link_to_record).title(),
                                   data,
                                   outf)
    if print_header:
        outf.write('</ul>\n')


def write_loc_routes_out(v, data, outf):
    if u.return_type(v) != 'city':
        write_province_destinations(v, data, outf)
    else:
        header_printed = False
        host_prov = data[v['LI']['wh'][0]]
        # If city is in a mountain, can't move from city to ocean
        if u.return_type(host_prov) != 'mountain':
            dest_loc_list = host_prov['LO']['pd']
            i = int(0)
            for pd in dest_loc_list:
                try:
                    pd_loc = data[pd]
                except KeyError:
                    pass
                else:
                    if u.return_type(pd_loc) == 'ocean':
                        if not header_printed:
                            outf.write('<H4>Routes leaving {}:</H4>\n'.format(v['na'][0]))
                            outf.write('<ul>\n')
                            header_printed = True
                        pd_name = pd_loc['na'][0]
                        pd_loc_id = u.return_unitid(pd_loc)
                        out_distance = u.calc_exit_distance(v, pd_loc)
                        outf.write('<li>{}, to {} [{}], {}, {} {}</li>\n'
                                   .format(pd_directions[i],
                                           pd_name,
                                           anchor(to_oid(pd_loc_id)),
                                           data[u.region(pd_loc_id, data)]['na'][0],
                                           out_distance,
                                           'day' if out_distance == 1 else 'days'))
                i = i + 1
        if not header_printed:
            outf.write('<H4>Routes leaving {}:</H4\n'.format(v['na'][0]))
            outf.write('<ul>\n')
        out_distance = u.calc_exit_distance(v, host_prov)
        outf.write('<li>Out, to {} [{}], {} {}</li>\n'
                   .format(host_prov['na'][0],
                           anchor(to_oid(u.return_unitid(host_prov))),
                           out_distance,
                           'day' if out_distance == 1 else 'days'))
        if 'LI' in v:
            if 'hl' in v['LI']:
                here_list = v['LI']['hl']
                for here in here_list:
                    here_record = data[here]
                    if u.is_road_or_gate(here_record):
                        to_record = data[here_record['GA']['tl'][0]]
                        if u.return_kind(here_record) == 'gate':
                            name = 'Gate'
                        else:
                            name = here_record['na'][0]
                        if not header_printed:
                            outf.write('<H4>Routes leaving {}:</H4\n'.format(v['na'][0]))
                            outf.write('<ul>\n')
                        write_province_destination(v,
                                                   to_record,
                                                   name,
                                                   data,
                                                   outf)
        if header_printed:
            outf.write('</ul>\n')


def write_structure_basic_info(v, outf):
    try:
        defense = v['SL']['de'][0]
    except KeyError:
        defense = '0'
    try:
        damage = v['SL']['da'][0]
    except KeyError:
        damage = '0'
    try:
        effort_given = v['SL']['eg'][0]
    except KeyError:
        effort_given = '0'
    try:
        effort_required = v['SL']['er'][0]
    except KeyError:
        effort_required = '0'
    try:
        depth = v['SL']['sd'][0]
    except KeyError:
        depth = '0'
    try:
        level = v['SL']['cl'][0]
    except KeyError:
        level = '0'
    if defense != '0' or damage != '0' or int(effort_given) < int(effort_required):
        outf.write('<table>\n')
        if effort_given < effort_required:
            outf.write('<tr><td>Percent Complete:</td><td>{}%</td></tr>\n'
                       .format(int(int(effort_given) / int(effort_required)) * 100))
        if defense != '0':
            outf.write('<tr><td>Defense:</td><td>{}</td></tr>\n'
                       .format(defense))
        outf.write('<tr><td>Damage:</td><td>{}%</td></tr>\n'
                   .format(damage))
        if depth != '0':
            outf.write('<tr><td>Level:</td><td>{}</td></tr>\n'
                       .format(int(int(depth) / 3)))
        if u.return_type(v) == 'castle':
            outf.write('<tr><td>Level:</td><td>{}</td></tr>\n'
                       .format(level))
        outf.write('</table>\n')


def write_loc_skills_report(v, data, outf):
    if 'SL' in v and 'te' in v['SL']:
        skills_list = v['SL']['te']
        if len(skills_list) > 0:
            outf.write('<H4> Skills taught here:</H4>\n')
            outf.write('<ul>\n')
            for skill in skills_list:
                outf.write('<li>{} [{}]</li>\n'.format(data[skill]['na'][0],
                                                       anchor(to_oid(skill))))
            outf.write('</ul>\n')


def write_loc_market_report(v, k, data, outf, trade_chain):
    try:
        trade_list = v['tl']
    except KeyError:
        return
    # load city/character trades
    city_trade_list = []
    if len(trade_list) > 0:
        # city trades
        for trade in range(0, len(trade_list), 8):
            if trade_list[trade] in {'1', '2'}:
                city_trade_list.append([trade_list[trade],
                                        trade_list[trade + 1],
                                        k,
                                        trade_list[trade + 2],
                                        trade_list[trade + 3]])
        # character trades - needs to be recursive
        if 'LI' in v and 'hl' in v['LI']:
            seen_here_list = v['LI']['hl']
        else:
            seen_here_list = []
        list_length = len(seen_here_list)
        if list_length > 1:
            for un in seen_here_list[1:]:
                charac_rec = data[un]
                if u.return_kind(charac_rec) == 'char':
                    if 'tl' in charac_rec:
                        trade_list = charac_rec['tl']
                        if len(trade_list) > 0:
                            # character trades
                            for trade in range(0, len(trade_list), 8):
                                if trade_list[trade] in {'1', '2'}:
                                    city_trade_list.append([trade_list[trade],
                                                            trade_list[trade + 1],
                                                            un,
                                                            trade_list[trade + 2],
                                                            trade_list[trade + 3]])
    if len(city_trade_list) > 0:
        sorted_list = sorted(city_trade_list, key=itemgetter(0, 1, 2))
        outf.write('<H4>Market Report:</H4>\n')
        outf.write('<table border="1" cellpadding="5">\n')
        outf.write('<tr>')
        outf.write('<th>trade</th><th>who</th><th>price</th><th>qty</th><th>wt/ea</th><th>item</th>'
                   '<th>recip who</th><th>recip price</th><th>recip qty</th>\n')
        outf.write('</tr>\n')
        for trade in sorted_list:
            if trade[0] in {'1', '2'}:
                trade_kind = 'buy' if trade[0] == '1' else 'sell'
                item_rec = data[trade[1]]
                trade_item = anchor(to_oid(trade[1]))
                trade_qty = trade[3]
                trade_price = trade[4]
                trade_who = anchor(to_oid(trade[2]))
                trade_recip = trade_chain[trade[1]]
                recip_name = ''
                recip_loc = '0'
                recip_rec = ''
                if len(trade_recip) > 0:
                    for recip in trade_recip:
                        if recip[0] != k:
                            recip_type = recip[1]
                            if recip_type != trade[0]:
                                recip_loc = recip[0]
                                recip_rec = data[recip_loc]
                                recip_name = recip_rec['na'][0]
                outf.write('<tr>')
                outf.write('<td>{}</td>\n'.format(trade_kind))
                outf.write('<td>{}</td>\n'.format(trade_who))
                outf.write('<td>{}</td>\n'.format(trade_price))
                outf.write('<td>{}</td>\n'.format(trade_qty))
                outf.write('<td>{}</td>\n'.format(item_rec['IT']['wt'][0]))
                outf.write('<td>{} [{}]</td>\n'.format(item_rec['na'][0], trade_item))
                if recip_loc != '0':
                    outf.write('<td>{} [{}]</td>\n'.format(recip_name,
                                                           anchor(to_oid(recip_loc))))
                    recip_trade_list = recip_rec['tl']
                    for recip in range(0, len(recip_trade_list), 8):
                        if recip_trade_list[recip + 1] == trade[1]:
                            if recip_trade_list[recip] in {'1', '2'}:
                                recip_qty = recip_trade_list[recip + 2]
                                recip_price = recip_trade_list[recip + 3]
                                outf.write('<td>{}</td>\n'.format(recip_price))
                                outf.write('<td>{}</td>\n'.format(recip_qty))
                else:
                    outf.write('<td>&nbsp;</td>\n')
                    outf.write('<td>&nbsp;</td>\n')
                    outf.write('<td>&nbsp;</td>\n')
            outf.write('</tr>\n')
        outf.write('</table>\n')


def print_wearable_wielding(v, data, outf):
    attack_max = 0
    missile_max = 0
    defense_max = 0
    attack = ''
    missile = ''
    defense = ''
    if 'il' in v:
        item_list = v['il']
        if len(item_list) > 0:
            for items in range(0, len(item_list), 2):
                itemz = data[item_list[items]]
                if 'IM' in itemz:
                    if 'ab' in itemz['IM']:
                        if int(itemz['IM']['ab'][0]) > attack_max:
                            attack_max = int(itemz['IM']['ab'][0])
                            attack = u.return_unitid(itemz)
                    if 'mb' in itemz['IM']:
                        if int(itemz['IM']['mb'][0]) > missile_max:
                            missile_max = int(itemz['IM']['mb'][0])
                            missile = u.return_unitid(itemz)
                    if 'db' in itemz['IM']:
                        if int(itemz['IM']['db'][0]) > defense_max:
                            defense_max = int(itemz['IM']['db'][0])
                            defense = u.return_unitid(itemz)
        # found something
        if attack != '' or missile != '' or defense != '':
            if attack == missile:
                missile = ''
        if attack == defense:
            defense = ''
        if attack != '' or missile != '':
            if attack == '':
                missile_rec = data[missile]
                outf.write(', wielding {} [{}]'.format(missile_rec['na'][0],
                                                       anchor(to_oid(u.return_unitid(missile_rec)))))
            elif missile == '':
                attack_rec = data[attack]
                outf.write(', wielding {} [{}]'.format(attack_rec['na'][0],
                                                       anchor(to_oid(u.return_unitid(attack_rec)))))
            else:
                missile_rec = data[missile]
                attack_rec = data[attack]
                outf.write(', wielding {} [{}] and {} [{}]'.format(attack_rec['na'][0],
                                                                   anchor(to_oid(u.return_unitid(attack_rec))),
                                                                   missile_rec['na'][0],
                                                                   anchor(to_oid(u.return_unitid(missile_rec)))))
        if defense != '':
            defense_rec = data[defense]
            outf.write(', wearing {} [{}]'.format(defense_rec['na'][0],
                                                  anchor(to_oid(u.return_unitid(defense_rec)))))


def write_characters(v, k, data, outf, print_province = False):
    outf.write('<li>')
    if print_province:
        if 'LI' in v and 'wh' in v['LI']:
            province_rec = data[v['LI']['wh'][0]]
            outf.write('({}) '.format(anchor(to_oid(v['LI']['wh'][0]))))
    # code fix to bug in lib where garrison name is sometimes missing
    if u.return_type(v) == 'garrison':
        name = 'Garrison'
    else:
        name = v['na'][0]
        if name == 'Ni':
            name = data[v['CH']['ni'][0]]['na'][0].capitalize()
    outf.write('{} [{}]'.format(name,
                                anchor(to_oid(k))))
    if u.xlate_loyalty(v) not in {'Undefined'}:
        outf.write(' ({}'.format(u.xlate_loyalty(v)))
        if u.is_absorb_aura_blast(v, data):
            outf.write(':AB')
        outf.write(')')
    else:
        if u.is_absorb_aura_blast(v, data):
            outf.write('(AB)')
    if u.return_type(v) != '0':
        if u.return_type(v) == 'ni':
            # char_type = v['na'][0].lower()
            char_type = data[v['CH']['ni'][0]]['na'][0]
        else:
            char_type = u.return_type(v)
        outf.write(', {}'.format(char_type))
    if 'CH' in v:
        if 'pr' in v['CH'] and v['CH']['pr'][0] == '2':
            outf.write(', prisoner')
    if u.is_priest(v):
        outf.write(', priest')
    if u.is_magician(v):
        if u.xlate_magetype(v, data) not in {'', 'undefined'}:
            outf.write(', {}'.format(u.xlate_magetype(v, data)))
    if 'CH' in v:
        if 'gu' in v['CH'] and v['CH']['gu'][0] == '1':
            outf.write(', on guard')
        if 'hs' in v['CH'] and v['CH']['hs'][0] == '1':
            outf.write(' concealed')
    # print wearing/wielding
    print_wearable_wielding(v, data, outf)
    # print prominent items
    if 'il' in v:
        item_list = v['il']
        if len(item_list) > 0:
            for items in range(0, len(item_list), 2):
                itemz = data[item_list[items]]
                if 'IT' in itemz:
                    if 'pr' in itemz['IT']:
                        if itemz['IT']['pr'][0] == '1':
                            item_name = u.get_item_name(itemz) if int(item_list[items + 1]) == 1 else u.get_item_plural(itemz)
                            outf.write(', {} {}'.format(item_list[items + 1], item_name))
    if 'LI' in v:
        if 'hl' in v['LI']:
            outf.write(', accompanied by: ')
    outf.write('</li>\n')
    if 'LI' in v:
        if 'hl' in v['LI']:
            here_list = v['LI']['hl']
            if len(here_list) > 0:
                outf.write('<ul>\n')
                for here in here_list:
                    charac = data[here]
                    write_characters(charac, here, data, outf)
                outf.write('</ul>\n')


def write_sub_locs(loc, sub_loc, k, data, outf):
    outf.write('<li>')
    outf.write('{} [{}], {}'.format(sub_loc['na'][0],
                                    anchor(to_oid(k)),
                                    u.return_type(sub_loc)))
    if 'LO' in sub_loc and 'hi' in sub_loc['LO']:
        outf.write(', hidden')
    out_distance = u.calc_exit_distance(loc, sub_loc)
    if out_distance > 0:
        outf.write(', {} {}'.format(out_distance,
                                    'day' if out_distance == 1 else 'days'))
    if 'SL' in sub_loc and 'de' in sub_loc['SL']:
        outf.write(', defense {}'.format(sub_loc['SL']['de'][0]))
    if 'castle' in u.return_type(sub_loc):
        if 'SL' in sub_loc:
            if 'cl' in sub_loc['SL']:
                if sub_loc['SL']['cl'][0] != '0':
                    outf.write(', level {}'.format(sub_loc['SL']['cl'][0]))
    if 'mine' in u.return_type(sub_loc):
        if 'SL' in sub_loc and 'sd' in sub_loc['SL']:
            if sub_loc['SL']['sd'][0] != '0':
                outf.write(', level {}'.format(int(sub_loc['SL']['sd'][0]) / 3))
    if 'SL' in sub_loc:
        if 'eg' and 'er' in sub_loc['SL']:
            effort_given = int(sub_loc['SL']['eg'][0])
            effort_required = int(sub_loc['SL']['er'][0])
            pct_complete = int(float(effort_given / effort_required)*100)
            outf.write(', {}% completed'.format(pct_complete))
    if 'SL' in sub_loc and 'da' in sub_loc['SL']:
        outf.write(', {}% damaged'.format(sub_loc['SL']['da'][0]))
    if 'LI' in sub_loc and 'hl' in sub_loc['LI']:
        sub_here_list = sub_loc['LI']['hl']
        if len(sub_here_list) > 0:
            first_here = data[sub_here_list[0]]
            if u.return_kind(first_here) == 'char':
                outf.write(', owner:')
    outf.write('</li>\n')
    # see if stuff stacked under it
    if 'LI' in sub_loc and 'hl' in sub_loc['LI']:
        sub_here_list = sub_loc['LI']['hl']
        if len(sub_here_list) > 0:
            outf.write('<ul>\n')
            for sub_hl in sub_here_list:
                sub_sub_here = data[sub_hl]
                if u.return_kind(sub_sub_here) == 'loc':
                    write_sub_locs(sub_loc,
                                   sub_sub_here,
                                   sub_hl,
                                   data,
                                   outf)
                elif u.return_kind(sub_sub_here) == 'char':
                    write_characters(sub_sub_here,
                                     u.return_unitid(sub_sub_here),
                                     data, outf)
                elif u.return_kind(sub_sub_here) == 'ship':
                    write_ships(sub_sub_here,
                                u.return_unitid(sub_sub_here),
                                data,
                                outf)
            outf.write('</ul>\n')


def write_ships(v, k, data, outf):
    outf.write('<li>\n')
    outf.write('{} [{}], {}'.format(v['na'][0],
                                    anchor(to_oid(k)),
                                    u.return_type(v)))
    if 'SL' in v:
        if 'bs' in v['SL']:
            storm = data[v['SL']['bs'][0]]
            if 'na' in storm:
                name = storm['na'][0]
            else:
                name = u.return_type(storm)
            outf.write(', bound {}-storm {} [{}] (strength: {})'.format(u.return_type(storm),
                                                                        name,
                                                                        anchor(to_oid(v['SL']['bs'][0])),
                                                                        storm['MI']['ss'][0]))
    if 'SL' in v:
        if 'de' in v['SL']:
            outf.write(', defense {}'.format(v['SL']['de'][0]))
        if 'eg' and 'er' in v['SL']:
            effort_given = int(v['SL']['eg'][0])
            effort_required = int(v['SL']['er'][0])
            pct_complete = int(float(effort_given / effort_required)*100)
            outf.write(', {}% completed'.format(pct_complete))
        if 'da' in v['SL']:
            outf.write(', {}% damaged'.format(v['SL']['da'][0]))
    pct_load = calc_ship_pct_loaded(data, k, v)
    if pct_load > 0:
        outf.write(', {}% loaded'.format(pct_load))
    if 'LI' in v and 'hl' in v['LI']:
        sub_here_list = v['LI']['hl']
        if len(sub_here_list) > 0:
            first_here = data[sub_here_list[0]]
            if u.return_kind(first_here) == 'char':
                outf.write(', owner:')
    outf.write('</li>\n')
    # see if stuff stacked under it
    if 'LI' in v and 'hl' in v['LI']:
        sub_here_list = v['LI']['hl']
        if len(sub_here_list) > 0:
            outf.write('<ul>\n')
            for sub_hl in sub_here_list:
                sub_sub_here = data[sub_hl]
                if u.return_kind(sub_sub_here) == 'loc':
                    write_sub_locs(v, sub_sub_here, sub_hl, data, outf)
                elif u.return_kind(sub_sub_here) == 'char':
                    write_characters(sub_sub_here,
                                     u.return_unitid(sub_sub_here),
                                     data, outf)
            outf.write('</ul>\n')


def write_storms(v, k, outf):
    outf.write('<li>\n')
    if 'na' in v:
        name = v['na'][0]
    else:
        name = u.return_type(v).capitalize()
    outf.write('{} [{}], {}'.format(name,
                                    anchor(to_oid(k)),
                                    u.return_type(v)))
    if 'MI' in v and 'ss' in v['MI']:
        outf.write(' (strength: {})'.format(v['MI']['ss'][0]))
    outf.write('</li>\n')


def write_inner_locs(v, data, outf, here_list):
    outf.write('<ul>\n')
    if len(here_list) > 0:
        for here in here_list:
            here_rec = data[here]
            if u.return_kind(here_rec) == 'loc':
                write_sub_locs(v, here_rec, u.return_unitid(here_rec),
                               data, outf)
    if 'SL' in v:
        if 'lf' in v['SL']:
            link_from_record = data[v['SL']['lf'][0]]
            if u.return_kind(link_from_record) == 'loc':
                write_sub_locs(v, link_from_record, u.return_unitid(link_from_record),
                               data, outf)
    outf.write('</ul>\n')


def write_seen_here(data, outf, here_list):
    outf.write('<ul>\n')
    for here in here_list:
        here_rec = data[here]
        if u.return_kind(here_rec) == 'char':
            write_characters(here_rec, here, data, outf)
    outf.write('</ul>\n')


def write_ships_docked(data, outf, here_list):
    outf.write('<ul>\n')
    for here in here_list:
        here_rec = data[here]
        if u.return_kind(here_rec) == 'ship':
            write_ships(here_rec, here, data, outf)
    outf.write('</ul>\n')


def write_storms_here(data, outf, here_list):
    outf.write('<ul>\n')
    for here in here_list:
        here_rec = data[here]
        if u.return_kind(here_rec) == 'storm':
            write_storms(here_rec, here, outf)
    outf.write('</ul>\n')


def write_here_list(v, data, outf):
    print_inner = False
    seen_here = False
    ships_docked = False
    storms_here = False
    here_list = []
    try:
        here_list = v['LI']['hl']
    except KeyError:
        pass
    else:
        for here in here_list:
            here_rec = data[here]
            if u.return_kind(here_rec) == 'loc':
                print_inner = True
            elif u.return_kind(here_rec) == 'char':
                seen_here = True
            elif u.return_kind(here_rec) == 'ship':
                ships_docked = True
            elif u.return_kind(here_rec) == 'storm':
                storms_here = True
    try:
        inner_list = v['SL']['lf']
    except KeyError:
        pass
    else:
        if len(inner_list) > 0:
            print_inner = True
    if print_inner:
        outf.write('<H4>Inner Locations:</H4>\n')
        write_inner_locs(v, data, outf, here_list)
    if seen_here:
        outf.write('<H4>Seen Here:</H4>\n')
        write_seen_here(data, outf, here_list)
    if ships_docked:
        outf.write('<H4>{}:</H4>\n'.format('Ships docked' if u.return_type(v) != 'ocean' else 'Ships sighted'))
        write_ships_docked(data, outf, here_list)
    if storms_here:
        outf.write('<H4>Storms Here:</H4>\n')
        write_storms_here(data, outf, here_list)


def write_hidden_access(v, k, data, outf, hidden_chain):
    if 'LO' in v and 'hi' in v['LO']:
        if v['LO']['hi'][0] == '1' or u.region(k, data) in {'faery', 'hades'}:
            # PL/kn
            try:
                hidden_list = hidden_chain[k]
            except:
                pass
            else:
                if len(hidden_list) > 0:
                    outf.write('<H4>Hidden location known by:</H4>\n')
                    outf.write('<ul>\n')
                    for hidden in hidden_list:
                        hidden_rec = data[hidden]
                        outf.write('<li>{} [{}]</td></li>\n'.format(hidden_rec['na'][0],
                                                                    anchor(to_oid(hidden))))
                    outf.write('</ul>\n')


def write_garrisons(v, k, data, outf, garrisons_chain):
    if u.return_type(v) == 'castle':
        garrison_list = garrisons_chain[k]
        if len(garrison_list) > 0:
            province_list = []
            for garrison in garrison_list:
                province_rec = data[garrison]
                province_list.append([province_rec['LI']['wh'][0], garrison])
            province_list.sort()
            outf.write('<H4>Garrisons:</H4>\n')
            outf.write('<ul>\n')
            for province in province_list:
                garrison_rec = data[province[1]]
                write_characters(garrison_rec, province[1], data, outf, True)
            outf.write('</ul>\n')


def write_loc_map_anchor(v, k, data, outf, instance, inst_dict, map_matrices):
    if u.return_type(v) in ['tunnel', 'chamber']:
        return 0
    dimensions = inst_dict[instance]
    region = u.region(k, data)
    region_rec = data[region]
    province = u.province(k, data)
    if province == 0:
        return 0
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
    #                                u.return_type(v)))
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
        outf.write('<p>{}</p>\n'.format(anchor2(anchor_string, 'Return to map')))
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
        outf.write('<p>{}</p>\n'.format(anchor2(anchor_string, 'Return to map')))


def write_loc_basic_info(v, k, data, outf, hidden_chain, garrisons_chain, trade_chain, instance, inst_dict, map_matrices):
    write_loc_map_anchor(v, k, data, outf, instance, inst_dict, map_matrices)
    write_loc_barrier(v, k, outf)
    write_loc_shroud(v, k, outf)
    write_loc_controlled_by(v, data, outf)
    write_loc_routes_out(v, data, outf)
    # not doing nearby cities because lib doesn't support
    write_structure_basic_info(v, outf)
    write_loc_skills_report(v, data, outf)
    write_loc_market_report(v, k, data, outf, trade_chain)
    write_here_list(v, data, outf)
    write_hidden_access(v, k, data, outf, hidden_chain)
    write_garrisons(v, k, data, outf, garrisons_chain)
    write_loc_map_anchor(v, k, data, outf, instance, inst_dict, map_matrices)


def write_loc_html(v, k, data, hidden_chain, garrisons_chain, trade_chain, outdir, instance, inst_dict, map_matrices):
    # generate loc page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    name = v['na'][0]
    try:
        loc2 = data[v['LI']['wh'][0]]
    except KeyError:
        loc2_name = ''
    else:
        loc2_name = ', in ' + loc2['na'][0]
    outf.write('<TITLE>{} [{}], {}{}'.format(name,
               to_oid(k), u.return_type(v), loc2_name))
    outf.write('</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    write_loc_page_header(v, k, data, outf)
    write_loc_basic_info(v, k, data, outf, hidden_chain, garrisons_chain, trade_chain, instance, inst_dict, map_matrices)
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '_z.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('loc.html')
    loc = build_loc_dict(k, v, data, garrisons_chain, hidden_chain, trade_chain)
    outf.write(template.render(loc=loc))


def build_loc_dict(k, v, data, garrisons_chain, hidden_chain, trade_chain):
    where_oid, where_type, where_name = get_where_info(v, data)
    loc_dict = {'oid': to_oid(k),
                'name': get_name(v, data),
                'type': get_type(v, data),
                'where_oid': where_oid,
                'where_name': where_name,
                'safe_haven': get_safe_haven(v),
                'hidden': u.is_hidden(v),
                'civ_level': get_civ_level(k, v, data),
                'barrier': get_barrier(k, v, data),
                'shroud': get_shroud(k, v, data),
                'anchor': get_map_anchor(v, k),
                'controlled_by': get_controlled_by (v, data),
                'routes_out': get_routes_out(k, v, data),
                'structure': get_structure_info(v),
                'skills': get_skills_taught(v, data),
                'markets': get_markets(k, v, data, trade_chain),
                'seen_here': get_here_list(k, v, data),
                'hidden_access': get_hidden_access(k, v, data, hidden_chain),
                'garrisons': get_garrisons(k, v, data, garrisons_chain)}
    return loc_dict


def get_where_info(v, data):
    where_id = v.get('LI', {}).get('wh', None)
    if where_id is not None:
        try:
            where_rec = data[where_id[0]]
        except KeyError:
            where_oid = None
            where_name = None
            where_type = None
        else:
            where_oid = to_oid(where_id[0])
            where_name = get_name(where_rec, data)
            where_type = get_type(where_rec, data)
    else:
        where_oid = None
        where_name = None
        where_type = None
    return where_oid, where_type, where_name


def get_safe_haven(v):
    safe_haven = v.get('SL', {}).get('sh', [None])
    return safe_haven[0]


def get_civ_level(k, v, data):
    civ_level = None
    if u.return_type(v) != 'ocean' and u.loc_depth(u.return_type(v)) == 2 \
    and data[u.region(k, data)]['na'][0] != 'faery' and data[u.region(k, data)]['na'][0] != 'hades':
        civ_level = 'wilderness'
        if 'LO' in v and 'lc' in v['LO']:
            if v['LO']['lc'][0] == '0':
                civ_level = 'wilderness'
            else:
                civ_level = 'civ-' + v['LO']['lc'][0]
    return civ_level


def get_map_anchor(v, data):
    anchor_dict = {}
    return anchor_dict


def get_barrier(k, v, data):
    barrier = v.get('LO', {}).get('ba', [None])
    if barrier[0] is not None and barrier[0] != '0':
        barrier_dict = {'oid': to_oid(k),
                        'name': get_name(v, data)}
        return barrier_dict
    else:
        return None


def get_shroud(k, v, data):
    shroud = v.get('LO', {}).get('sh', [None])
    if shroud[0] is not None and shroud[0] != '0':
        shroud_dict = {'oid': to_oid(k),
                       'name': get_name(v, data)}
        return shroud_dict
    else:
        return None


def get_controlled_by(v, data):
    controlled_dict = {}
    here_list = v.get('LI', {}).get('hl', [None])
    if here_list[0] is not None and len(here_list) > 0:
        for loc in here_list:
            garrison_rec = data[loc] # looking for garrisons
            if get_type(garrison_rec, data) == 'garrison':
                castle = garrison_rec.get('MI', {}).get('gc', [None])
                if castle[0] is not None and castle[0] != '0':
                    castle_rec = data[castle[0]]
                    castle_name = castle_rec['na'][0]
                    castle_oid = to_oid(castle[0])
                    castle_type = u.return_type(castle_rec)
                    castle_loc_id = castle_rec['LI']['wh'][0]
                    castle_loc_rec = data[castle_loc_id]
                    castle_loc_type = get_type(castle_loc_rec, data)
                    if castle_loc_type == 'city':  # in a city
                        castle_loc_id = castle_loc_rec['LI']['wh'][0]
                        castle_loc_rec = data[castle_loc_id]
                    castle_loc_oid = to_oid(castle_loc_id)
                    castle_loc_name = castle_loc_rec['na'][0]
                    # calculate top of pledge chain
                    castle_here_list = castle_rec.get('LI', {}).get('hl', [None])
                    ruled_by_oid = None
                    ruled_by_name = None
                    if castle_here_list[0] is not None:
                        top_guy = u.top_ruler(castle_here_list[0], data)
                        try:
                            top_dog = data[top_guy]
                        except KeyError:
                            pass
                        else:
                            ruled_by_oid = to_oid(top_guy)
                            ruled_by_name = top_dog['na'][0]
                    controlled_dict = {'oid': castle_oid,
                                       'name': castle_name,
                                       'type': castle_type,
                                       'loc_oid': castle_loc_oid,
                                       'loc_name': castle_loc_name,
                                       'ruled_by_oid': ruled_by_oid,
                                       'ruled_by_name': ruled_by_name}
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
                to_dict = create_loc_dict_entry(data, direction, pd_rec, v, region_rec)
                dest_list.append(to_dict)
                # see if port city so show province also
                if u.is_port_city(pd_rec, data):
                    prov_rec = data[u.province(pd, data)]
                    to_dict = create_loc_dict_entry(data, direction, prov_rec, v, region_rec)
                    dest_list.append(to_dict)
                elif u.province_has_port_city(pd_rec, data) is not None:
                    city_rec = data[u.province_has_port_city(pd_rec, data)]
                    to_dict = create_loc_dict_entry(data, direction, city_rec, v, region_rec)
                    dest_list.append(to_dict)
            i = i + 1
    if u.return_type(v) not in details.province_kinds:
        if 'LI' in v and 'wh' in v['LI']:
            out_id = v['LI']['wh'][0]
            out_rec = data[out_id]
            region_id = u.region(out_id, data)
            region_rec = data[region_id]
            to_dict = create_loc_dict_entry(data, 'Out', out_rec, v, region_rec)
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
                    direction = get_name(here_record, data)
                to_dict = create_loc_dict_entry(data, direction, to_rec, here_record, region_rec)
                dest_list.append(to_dict)
    if 'SL' in v and 'lt' in v['SL']:
        link_id = v['SL']['lt'][0]
        link_rec = data[link_id]
        region_id = u.region(link_id, data)
        region_rec = data[region_id]
        to_dict = create_loc_dict_entry(data, get_type(link_id, data).title(), link_rec, v, region_rec)
        dest_list.append(to_dict)
    region_id = u.region(k, data)
    region_rec = data[region_id]
    dest_dict = {'id': k,
                 'oid': to_oid(k),
                 'name': get_name(v, data),
                 'type': get_type(v, data),
                 'region_oid': to_oid(region_id),
                 'region_name': get_name(region_rec, data),
                 'dest': dest_list}
    return dest_dict


def create_loc_dict_entry(data, direction, to_loc_rec, from_loc_rec, region_rec):
    to_dict = {'id': u.return_unitid(to_loc_rec),
               'oid': to_oid(u.return_unitid(to_loc_rec)),
               'name': get_name(to_loc_rec, data),
               'type': get_type(to_loc_rec, data),
               'is_port': u.is_port_city(to_loc_rec, data),
               'prov_port': u.province_has_port_city(to_loc_rec, data),
               'region_oid': to_oid(u.return_unitid(region_rec)),
               'region_name': get_name(region_rec, data),
               'direction': direction,
               'barrier': get_barrier(u.return_unitid(to_loc_rec), to_loc_rec, data),
               'distance': u.calc_exit_distance(from_loc_rec, to_loc_rec),
               'impassable': is_impassable(from_loc_rec, to_loc_rec, direction, data)}
    return to_dict


def get_routes_out(k, v, data):
    routes_out_list = []
    if get_type(v, data) != 'city':
        dest_dict = get_destinations(k, v, data)
    else:
        dest_list = []
        host_prov_id = v['LI']['wh'][0]
        host_prov_rec = data[host_prov_id]
        # If city is in a mountain, can't move from city to ocean
        if u.return_type(host_prov_rec) != 'mountain':
            dest_loc_list = host_prov_rec['LO']['pd']
            i = int(0)
            for pd in dest_loc_list:
                if pd != '0':
                    pd_loc = data[pd]
                    if u.return_type(pd_loc) == 'ocean':
                        pd_name = pd_loc['na'][0]
                        pd_loc_id = u.return_unitid(pd_loc)
                        pd_rec = data[pd_loc_id]
                        direction = pd_directions[i]
                        region_id = u.region(pd_loc_id, data)
                        region_rec = data[region_id]
                        to_dict = create_loc_dict_entry(data, direction, pd_rec, v, region_rec)
                        dest_list.append(to_dict)
                i = i + 1
        region_id = u.region(host_prov_id, data)
        region_rec = data[region_id]
        direction = 'Out'
        to_dict = create_loc_dict_entry(data, direction, host_prov_rec, v, region_rec)
        dest_list.append(to_dict)
        region_id = u.region(k, data)
        region_rec = data[region_id]
        dest_dict = {'id': k,
                     'oid': to_oid(k),
                     'name': get_name(v, data),
                     'type': get_type(v, data),
                     'region_oid': to_oid(region_id),
                     'region_name': get_name(region_rec, data),
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


def get_structure_info(v):
    structure_dict = {'defense': get_defense(v),
                      'damage': get_damage(v),
                      'effort_given': get_effort_given(v),
                      'effort_required': get_effort_required(v),
                      'depth': get_depth(v),
                      'level': get_level(v)}
    return structure_dict


def get_skills_taught(v, data):
    skills_taught_list = []
    if 'SL' in v and 'te' in v['SL']:
        skills_list = v['SL']['te']
        if len(skills_list) > 0:
            for skill in skills_list:
                skill_rec = data[skill]
                skills_dict = {'oid': to_oid(skill),
                               'name': get_name(skill_rec, data)}
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
                                recip_name = get_name(recip_rec, data)
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
                market_dict = {'type': trade_list[trade],
                               'item_id': trade_list[trade + 1],
                               'item_oid': to_oid(trade_list[trade + 1]),
                               'item_name': get_name(item_rec, data),
                               'item_weight': get_weight(item_rec)[0],
                               'who_id': k,
                               'who_oid': to_oid(k),
                               'who_name': get_name(v, data),
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
                                                    recip_name = get_name(recip_rec, data)
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
                                    market_dict = {'type': trade_list[trade],
                                                   'item_id': trade_list[trade + 1],
                                                   'item_oid': to_oid(trade_list[trade + 1]),
                                                   'item_name': get_name(item_rec, data),
                                                   'item_weight': get_weight(item_rec)[0],
                                                   'who_id': un[0],
                                                   'who_oid': to_oid(un[0]),
                                                   'who_name': get_name(charac_rec, data),
                                                   'who_qty': trade_list[trade + 2],
                                                   'who_price': trade_list[trade + 3],
                                                   'recip_list' : recip_list}
                                    markets_list.append(market_dict)
    sorted_list = sorted(markets_list, key=itemgetter('type', 'item_oid', 'who_oid'))
    return sorted_list


def get_here_list(k, v, data):
    inner_list = []
    seen_list = []
    ships_list = []
    storms_list = []
    if 'LI' in v and 'hl' in v['LI']:
        here_list = v['LI']['hl']
        for here in here_list:
            here_rec = data[here]
            if u.return_kind(here_rec) == 'loc':
                inner_dict = {'id': here,
                              'oid': to_oid(here)}
                inner_list.append(inner_dict)
            elif u.return_kind(here_rec) == 'char':
                seen_dict = {'id': here,
                              'oid': to_oid(here)}
                seen_list.append(seen_dict)
            elif u.return_kind(here_rec) == 'ship':
                ship_dict = {'id': here,
                              'oid': to_oid(here)}
                ships_list.append(ship_dict)
            elif u.return_kind(here_rec) == 'storm':
                storm_dict = {'id': here,
                              'oid': to_oid(here)}
                storms_list.append(storm_dict)
    if 'SL' in v and 'lf' in v['SL']:
        here_rec = data[v['SL']['lf']]
        if u.return_kind(here_rec) == 'loc':
            inner_dict = {'id': here,
                          'oid': to_oid(here)}
            inner_list.append(inner_dict)
    here_dict = {'id': k,
                 'oid': to_oid(k),
                 'inner': inner_list,
                 'seen': seen_list,
                 'ships': ships_list,
                 'storms': storms_list}
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
                                   'name': get_name(hidden_rec, data)}
                    hidden_access_list.append(hidden_dict)
    return hidden_access_list


def get_garrisons(k, v, data, garrisons_chain):
    garrisons_list = []
    if u.return_type(v) == 'castle':
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


def get_wearable_wielding(v, data):
    wearable_dict = {}
    attack_max = 0
    missile_max = 0
    defense_max = 0
    attack = ''
    missile = ''
    defense = ''
    if 'il' in v:
        item_list = v['il']
        if len(item_list) > 0:
            for items in range(0, len(item_list), 2):
                itemz = data[item_list[items]]
                if 'IM' in itemz:
                    if 'ab' in itemz['IM']:
                        if int(itemz['IM']['ab'][0]) > attack_max:
                            attack_max = int(itemz['IM']['ab'][0])
                            attack = u.return_unitid(itemz)
                    if 'mb' in itemz['IM']:
                        if int(itemz['IM']['mb'][0]) > missile_max:
                            missile_max = int(itemz['IM']['mb'][0])
                            missile = u.return_unitid(itemz)
                    if 'db' in itemz['IM']:
                        if int(itemz['IM']['db'][0]) > defense_max:
                            defense_max = int(itemz['IM']['db'][0])
                            defense = u.return_unitid(itemz)
        # found something
        if attack != '' or missile != '' or defense != '':
            if attack == missile:
                missile = ''
        if attack == defense:
            defense = ''
        if attack != '' or missile != '':
            if attack == '':
                missile_rec = data[missile]
                missile_dict = {'id': missile,
                                'oid': to_oid(missile),
                                'name': get_name(missile_rec, data)}
                attack_dict = {}
            elif missile == '':
                attack_rec = data[attack]
                attack_dict = {'id': attack,
                               'oid': to_oid(attack),
                               'name': get_name(attack_rec, data)}
                missile_dict = {}
            else:
                missile_rec = data[missile]
                missile_dict = {'id': missile,
                                'oid': to_oid(missile),
                                'name': get_name(missile_rec, data)}
                attack_rec = data[attack]
                attack_dict = {'id': attack,
                               'oid': to_oid(attack),
                               'name': get_name(attack_rec, data)}
        else:
            attack_dict = {}
            missile_dict = {}
        if defense != '':
            defense_rec = data[defense]
            defense_dict = {'id': defense,
                           'oid': to_oid(defense),
                           'name': get_name(defense_rec, data)}
        else:
            defense_dict = {}
        wearable_dict = {'attack': attack_dict,
                         'defense': defense_dict,
                         'missile': missile_dict}
    return wearable_dict


def get_character_info(k, v, data, print_province):
    char_dict = {}
    province_oid = None
    if print_province:
        if 'LI' in v and 'wh' in v['LI']:
            province_rec = data[v['LI']['wh'][0]]
            province_oid = to_oid(v['LI']['wh'][0])
    character_dict = {'oid': to_oid(k),
                     'name': get_name(v, data),
                     'type': get_type(v, data),
                     'province_oid': province_oid,
                     'absorb_blast': u.is_absorb_aura_blast(v, data),
                     'loyalty': u.xlate_loyalty(v),
                     'prisoner': u.is_prisoner(v),
                     'priest': u.is_priest(v),
                     'magetype': u.is_magician(v),
                     'on_guard': u.is_on_guard(v),
                     'concealed': u.is_concealed(v),
                     'wearable': get_wearable_wielding(v, data),
                     'items_list': get_items_list(v, data, True)}
    return character_dict
