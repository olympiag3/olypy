#!/usr/bin/python

from collections import defaultdict
from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor, get_oid, get_name, get_type
import pathlib
from jinja2 import Environment, PackageLoader, select_autoescape


def write_storm_page_header(v, k, outf):
    if 'na' in v:
        name = v['na'][0]
    else:
        name = u.return_type(v).capitalize()
    outf.write('<H3>{} [{}]</H3>\n'.format(name, to_oid(k)))


def write_storm_basic_info(v, k, data, outf, storm_chain):
    outf.write('<table>\n')
    write_type(outf, v)
    write_where(data, outf, v)
    write_strength(outf, v)
    write_bound_ship(data, k, outf, storm_chain)
    outf.write('</table>\n')


def write_bound_ship(data, k, outf, storm_chain):
    ship_list = storm_chain[k]
    if len(ship_list) > 0:
        for ship in ship_list:
            ship_rec = data[ship]
            outf.write('<tr><td>Bound Ship: </td><td>{} [{}]</td></tr>\n'.format(ship_rec['na'][0],
                                                                                 anchor(to_oid(ship))))


def write_strength(outf, v):
    outf.write('<tr><td>Strength: </td><td>{}</td></tr>\n'.format(v['MI']['ss'][0]))


def write_where(data, outf, v):
    where_rec = data[v['LI']['wh'][0]]
    outf.write('<tr><td>Where: </td><td>{} [{}]</td></tr>\n'.format(where_rec['na'][0],
                                                                    anchor(to_oid(v['LI']['wh'][0]))))


def write_type(outf, v):
    outf.write('<tr><td>Type: </td><td>{}</td></tr>\n'.format(u.return_type(v)))


def write_storm_html(v, k, data, storm_chain, outdir):
    # generate storm page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    if 'na' in v:
        name = v['na'][0]
    else:
        name = u.return_type(v).capitalize()
    outf.write('<TITLE>{} [{}]'.format(name,
               to_oid(k)))
    outf.write('</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    write_storm_page_header(v, k, outf)
    write_storm_basic_info(v, k, data, outf, storm_chain)
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '_z.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('storm.html')
    storm = build_complete_storm_dict(k, v, data, storm_chain)
    outf.write(template.render(storm=storm))


def get_strength(v):
    return v.get('MI', {}).get('ss', [0])[0]


def build_complete_storm_dict(k, v, data, storm_chain):
    storm_dict = {'oid': get_oid(k),
                  'name': get_name(v, data),
                  'type': get_type(v, data),
                  'kind': 'storm',
                  'strength': get_strength(v),
                  'loc': build_loc_dict(v, data),
                  'ship': build_ship_dict(k, data, storm_chain)}
    return storm_dict


def build_basic_storm_dict(k, v, data):
    storm_dict = {'oid': get_oid(k),
                  'name': get_name(v, data),
                  'type': get_type(v, data),
                  'kind': 'storm',
                  'strength': get_strength(v)}
    return storm_dict


def build_loc_dict(v, data):
    loc_id = v['LI']['wh'][0]
    loc_rec = data[loc_id]
    loc_dict = {'oid': get_oid(loc_id),
                'name': get_name(loc_rec, data),
                'type': get_type(loc_rec, data)}
    return loc_dict


def get_bound_ship(k, storm_chain):
    ship_list = storm_chain[k]
    if len(ship_list) > 0:
        return ship_list[0]
    else:
        return None


def build_ship_dict(k, data, storm_chain):
    ship_id = get_bound_ship(k, storm_chain)
    if ship_id is not None:
        ship_rec = data[ship_id]
        ship_dict = {'id': ship_id,
                     'oid': get_oid(ship_id),
                     'name': get_name(ship_rec, data)}
    else:
        ship_dict = None
    return ship_dict