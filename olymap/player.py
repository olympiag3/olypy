#!/usr/bin/python

import math

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor, get_oid, get_name, get_type
import pathlib


def get_email(v):
    return v.get('PL', {}).get('em', [None])[0]


def get_fast_study(v):
    return v.get('PL', {}).get('fs', [None])[0]


def get_first_turn(v):
    return v.get('PL', {}).get('ft', [None])[0]


def get_full_name(v):
    full_name = None
    if 'PL' in v and 'fn' in v['PL']:
        full_name = v['PL']['fn'][0]
        name_list = v['PL']['fn']
        if len(name_list) > 1:
            for name in name_list[1:]:
                full_name = full_name + ' ' + name
    return full_name


def get_last_turn(v):
    return v.get('PL', {}).get('lt', [None])[0]


def get_noble_points(v):
    return v.get('PL', {}).get('np', [None])[0]


def get_unit_list(v, data):
    units_list = []
    if 'PL' in v and 'un' in v['PL']:
        unit_list = v['PL']['un']
        unit_list.sort()
        for unit in unit_list:
            unit_rec = data[unit]
            unit_dict={'id': unit,
                       'oid': to_oid(unit),
                       'name': get_name(unit_rec, data)}
            units_list.append(unit_dict)
    return units_list


def write_unit_list(data, outf, v):
    if 'PL' in v and 'un' in v['PL']:
        unit_list = v['PL']['un']
        unit_list.sort()
        outf.write('<tr><td valign="top">Unit List:</td><td>')
        outf.write('<table>\n')
        columns = int(math.ceil(len(unit_list) / 3))
        for unit in range(0, columns):
            outf.write('<tr>')
            if (columns * 0) + unit < len(unit_list):
                char = data[unit_list[(columns * 0) + unit]]
                if 'na' in char:
                    name = char['na'][0]
                else:
                    name = u.return_type(char).capitalize()
                if name == 'Ni':
                    name = data[char['CH']['ni'][0]]['na'][0].capitalize()
                outf.write('<td>{} [{}]</td>'.format(name,
                                                     anchor(to_oid(u.return_unitid(char)))))
            else:
                outf.write('<td></td>')
            if (columns * 1) + unit < len(unit_list):
                char = data[unit_list[(columns * 1) + unit]]
                if 'na' in char:
                    name = char['na'][0]
                else:
                    name = u.return_type(char).capitalize()
                if name == 'Ni':
                    name = data[char['CH']['ni'][0]]['na'][0].capitalize()
                outf.write('<td>{} [{}]</td>'.format(name,
                                                     anchor(to_oid(u.return_unitid(char)))))
            else:
                outf.write('<td></td><td></td>')
            if (columns * 2) + unit < len(unit_list):
                char = data[unit_list[(columns * 2) + unit]]
                if 'na' in char:
                    name = char['na'][0]
                else:
                    name = u.return_type(char).capitalize()
                if name == 'Ni':
                    name = data[char['CH']['ni'][0]]['na'][0].capitalize()
                outf.write('<td>{} [{}]</td>'.format(name,
                                                     anchor(to_oid(u.return_unitid(char)))))
            else:
                outf.write('<td></td><td></td>')
            outf.write('</tr>\n')
        outf.write('</table>\n')
        outf.write('</td></tr>')


def build_complete_player_dict(k, v, data):
    storm_dict = {'oid': get_oid(k),
                  'name': get_name(v, data),
                  'type': get_type(v, data),
                  'kind': 'player',
                  'email': get_email(v),
                  'fast_study': get_fast_study(v),
                  'first_turn': get_first_turn(v),
                  'full_name': get_full_name(v),
                  'last_turn': get_last_turn(v),
                  'noble_points': get_noble_points(v),
                  'unit_list': get_unit_list(v, data)}
    return storm_dict