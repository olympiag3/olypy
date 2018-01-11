#!/usr/bin/python
import math

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor
import pathlib
from olypy.db import loop_here
from olymap.loc import write_characters
from olymap.utilities import calc_ship_pct_loaded


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
                    write_characters(sub_sub_here,
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
