#!/usr/bin/python
import math

import olymap.utilities as u
from olymap.utilities import anchor, get_oid, get_name, get_type, to_oid, loop_here2
import pathlib
from olypy.db import loop_here
import olymap.loc as loc
from olymap.utilities import calc_ship_pct_loaded
from jinja2 import Environment, PackageLoader, select_autoescape
import olymap.storm as storm
from olymap.char import get_char_detail


def write_ship_page_header(v, k, outf):
    outf.write('<H3>{} [{}], {}</H3>\n'.format(v['na'][0], to_oid(k), u.return_type(v)))


def write_ship_location(v, data, outf):
    outf.write('<tr>')
    here_rec = data[v['LI']['wh'][0]]
    outf.write('<td>Location:</td>')
    outf.write('<td>{} [{}]</td></tr>\n'.format(here_rec['na'][0],
                                                anchor(to_oid(v['LI']['wh'][0]))))


def write_ship_pct_complete(v, outf):
    if 'in-progress' in u.return_type(v):
        outf.write('<tr>')
        outf.write('<td>Percent Complete:</td>')
        outf.write('<td>{}%</td></tr>\n'.format((int(v['SL']['eg'][0]) / int(v['SL']['er'][0]))*100))


def write_ship_pct_loaded(v, k, data, outf):
    pct_loaded = calc_ship_pct_loaded(data, k, v)
    outf.write('<tr>')
    outf.write('<td>Percent Loaded:</td>')
    outf.write('<td>{}%</td></tr>\n'.format(pct_loaded))


def write_ship_defense(v, outf):
    if 'SL' in v and 'de' in v['SL']:
        defense = v['SL']['de'][0]
    else:
        defense = '0'
    outf.write('<tr>')
    outf.write('<td>Defense:</td>')
    outf.write('<td>{}</td></tr>\n'.format(defense))


def write_ship_damaged(v, outf):
    if 'SL' in v and 'da' in v['SL']:
        damaged = v['SL']['da'][0]
    else:
        damaged = '0'
    outf.write('<tr>')
    outf.write('<td>Damaged:</td>')
    outf.write('<td>{}%</td></tr>\n'.format(damaged))


def write_ship_owner(v, data, outf):
    if 'LI' in v and 'hl' in v['LI']:
        units = v['LI']['hl']
    else:
        units = '???'
    if units != '???':
        char = data[units[0]]
        outf.write('<tr>')
        outf.write('<td>Owner:</td>')
        outf.write('<td>{} [{}]</td></tr>\n'.format(char['na'][0],
                                                    anchor(to_oid(u.return_unitid(char)))))
    else:
        outf.write('<tr>')
        outf.write('<td>Owner:</td>')
        outf.write('<td>unoccupied</td></tr>\n')


def write_ship_seen_here(v, k, data, outf):
    label1 = 'Seen Here:'
    # seen_here_list = loop_here(data, k, False, True)
    # list_length = len(seen_here_list)
    # if list_length > 1:
    #     for un in seen_here_list:
    #         char = data[un]
    #         outf.write('<tr>')
    #         outf.write('<td>{}</td>'.format(label1))
    #         outf.write('<td>{} [{}]</td></tr>\n'.format(char['na'][0],
    #                                                        anchor(to_oid(u.return_unitid(char)))))
    #         label1 = '&nbsp;'
    if 'LI' in v and 'hl' in v['LI']:
        sub_here_list = v['LI']['hl']
        if len(sub_here_list) > 0:
            outf.write('<p>Seen Here:</p>\n')
            outf.write('<ul>\n')
            for sub_hl in sub_here_list:
                sub_sub_here = data[sub_hl]
                if u.return_kind(sub_sub_here) == 'char':
                    loc.write_characters(sub_sub_here,
                                         u.return_unitid(sub_sub_here),
                                         data, outf)
            outf.write('</ul>\n')


def write_ship_bound_storm(v, data, outf):
    if 'SL' in v and 'bs' in v['SL']:
        bound_storm = v['SL']['bs'][0]
    else:
        bound_storm = '???'
    if bound_storm != '???':
        bound_storm_rec = data[bound_storm]
        if 'na' in bound_storm_rec:
            name = bound_storm_rec['na'][0]
        else:
            name = u.return_type(bound_storm_rec).capitalize()
        outf.write('<tr>')
        outf.write('<td>Bound Storm:</td>')
        outf.write('<td>{} [{}] (Strength: {})</td></tr>\n'.format(name,
                                                                   anchor(to_oid(bound_storm)),
                                                                   bound_storm_rec['MI']['ss'][0]))


def write_ship_non_prominent(v, k, data, outf):
    seen_here_list = loop_here(data, k, False, True)
    list_length = len(seen_here_list)
    if list_length > 1:
        first_time = True
        printed_items = False
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
                            if first_time and total_weight > 0:
                                outf.write('<p>Non-Prominent Items Onboard:</p>\n')
                                outf.write('<table border="1" cellpadding="5">\n')
                                outf.write('<tr><th>Possessor</th><th>Item</th><th>Qty</th><th>Weight</th></tr>')
                                first_time = False
                            if total_weight > 0:
                                printed_items = True
                                outf.write('<tr>')
                                outf.write('<td>{} [{}]</td>'.format(unit_rec['na'][0],
                                                                     anchor(to_oid(un))))
                                outf.write('<td>{} [{}]</td>'.format(item_rec['na'][0],
                                                                     anchor(to_oid(item_list[items]))))
                                outf.write(f'<td style="text-align:right">{qty:,d}</td>')
                                outf.write(f'<td style="text-align:right">{total_weight:,d}</td>')
                                outf.write('</tr>\n')
        if printed_items:
            outf.write('</table>\n')


def write_ship_basic_info(v, k, data, outf):
    outf.write('<table>\n')
    write_ship_location(v, data, outf)
    write_ship_pct_complete(v, outf)
    write_ship_pct_loaded(v, k, data, outf)
    write_ship_defense(v, outf)
    write_ship_damaged(v, outf)
    write_ship_owner(v, data, outf)
    write_ship_bound_storm(v, data, outf)
    outf.write('</table>\n')
    write_ship_seen_here(v, k, data, outf)
    write_ship_non_prominent(v, k, data, outf)


def write_ship_html(v, k, data, outdir):
    # generate ship page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>{} [{}], {}'.format(v['na'][0],
               to_oid(k), u.return_type(v)))
    outf.write('</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    write_ship_page_header(v, k, outf)
    write_ship_basic_info(v, k, data, outf)
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '_z.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('ship.html')
    ship = build_ship_dict(k, v, data)
    loc_id = v['LI']['wh'][0]
    loc_rec = data[loc_id]
    loc = build_loc_dict(loc_id, loc_rec, data)
    owner = build_owner_dict(k, v, data)
    storm = build_storm_dict(k, v, data)
    seen_here = build_seenhere_dict(k, v, data)
    non_prominent_items = build_non_prominent_items_dict(k, v, data)
    outf.write(template.render(ship=ship, loc=loc, owner=owner, storm=storm,
                               seen_here=seen_here,
                               non_prominent_items = non_prominent_items))


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


def get_damage(v):
    return v.get('SL', {}).get('da', [0])


def build_ship_dict(k, v, data):
    ship_dict = {'oid' : get_oid(k),
                 'name' : get_name(v, data),
                 'type' : get_type(v),
                 'complete' : get_complete(v),
                 'load' : get_load(k, v, data),
                 'defense' : get_defense(v)[0],
                 'damage' : get_damage(v)[0]}
    return ship_dict


def build_loc_dict(k, v, data):
    loc_dict = {'oid' : get_oid(k),
                'name' : get_name(v, data),
                'type' : get_type(v)}
    return loc_dict


def get_owner(v):
    owner_id = v.get('LI', {}).get('hl', [None])[0]
    if owner_id is not None:
        return owner_id
    return None


def build_owner_dict(k, v, data):
    if get_owner(v) is not None:
        owner_id = get_owner(v)
        owner_rec = data[owner_id]
        owner_dict = {'oid' : get_oid(owner_id),
                      'name' : get_name(owner_rec, data)}
    else:
        owner_dict = None
    return owner_dict


def get_bound_storm(v):
    return v.get('SL', {}).get('bs', [None])[0]


def build_storm_dict(k, v, data):
    if get_bound_storm(v) is not None:
        storm_id = get_bound_storm(v)
        storm_rec = data[storm_id]
        storm_dict = {'oid' : get_oid(storm_id),
                      'name' : get_name(storm_rec, data),
                      'strength' : storm.get_strength(storm_rec)}
    else:
        storm_dict = None
    return storm_dict


def build_seenhere_dict(k, v, data):
    stack_list = []
    stack_list = loop_here2(data, k)
    # print (stack_list)
    seen_here = []
    # here_list =  v.get('LI', {}).get('hl', [None])
    if len(stack_list) > 0:
        for characters in stack_list:
            char_rec = data[characters[0]]
            seen_entry = {'oid' : get_oid(characters[0]),
                          'name' : get_name(char_rec, data),
                          'detail' : get_char_detail(characters[0], char_rec, data),
                          'level' : characters[1]}
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
                                npi_entry = {'possessor_oid' : to_oid(un),
                                             'possessor_name' : unit_rec['na'][0],
                                             'item_oid' : to_oid(item_list[items]),
                                             'item_name' : item_rec['na'][0],
                                             'qty' : qty,
                                             'weight' : total_weight}
                                npi_list.append(npi_entry)
    return npi_list