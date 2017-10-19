#!/usr/bin/python
import os
import sys
import math

from olypy.oid import to_oid
import olypy.oio as oio
import OlyMapperPy.OlyMapperUtilities as u
import olypy.details as details
from OlyMapperPy.OlyMapperUtilities import anchor


def write_player_page_header(v,k,outf):
    outf.write('<H3>{} [{}]</H3>\n'.format(v['na'][0], to_oid((k))))


def write_player_basic_info(v,k,data,outf):
    outf.write('<table>\n')
    outf.write('<tr><td>Type</td><td>{}</td></tr>\n'.format(u.return_type(v['firstline'][0])))
    if 'PL' in v:
        if 'em' in v['PL']:
            outf.write('<tr><td>Email Address:</td><td>{}</td></tr>\n'.format(v['PL']['em'][0]))
        if 'fs' in v['PL']:
            outf.write('<tr><td>Fast Study Points:</td><td>{}</td></tr>\n'.format(v['PL']['fs'][0]))
        if 'ft' in v['PL']:
            outf.write('<tr><td>First Turn:</td><td>{}</td></tr>\n'.format(v['PL']['ft'][0]))
    write_full_name(outf, v)
    # outf.write('<tr><td>Known:</td><td></td></tr>\n')
    if 'PL' in v:
        if 'lt' in v['PL']:
            outf.write('<tr><td>Last Turn:</td><td>{}</td></tr>\n'.format(v['PL']['lt'][0]))
        if 'np' in v['PL']:
            outf.write('<tr><td>Noble Points</td><td>{}</td></tr>\n'.format(v['PL']['np'][0]))
    write_unit_list(data, outf, v)
    outf.write('</table>\n')


def write_unit_list(data, outf, v):
    if 'PL' in v:
        if 'un' in v['PL']:
            unit_list = v['PL']['un']
            unit_list.sort()
            outf.write('<tr><td valign="top">Unit List:</td><td>')
            outf.write('<table>\n')
            columns = int(math.ceil(len(unit_list) / 3))
            for unit in range(0, columns):
                outf.write('<tr>')
                if (columns * 0) + unit < len(unit_list):
                    charac = data[unit_list[(columns * 0) + unit]]
                    name = ''
                    if 'na' in charac:
                        name = charac['na'][0]
                    else:
                        name = u.return_type(charac['firstline'][0]).capitalize()
                    outf.write('<td>{} [{}]</td>'.format(name,
                                                         anchor(to_oid(u.return_unitid(
                                                         charac['firstline'][0])))))
                else:
                    outf.write('<td></td>')
                if (columns * 1) + unit < len(unit_list):
                    charac = data[unit_list[(columns * 1) + unit]]
                    name = ''
                    if 'na' in charac:
                        name = charac['na'][0]
                    else:
                        name = u.return_type(charac['firstline'][0]).capitalize()
                    outf.write('<td>{} [{}]</td>'.format(name,
                                                         anchor(to_oid(u.return_unitid(
                                                         charac['firstline'][0])))))
                else:
                    outf.write('<td></td><td></td>')
                if (columns * 2) + unit < len(unit_list):
                    charac = data[unit_list[(columns * 2) + unit]]
                    name = ''
                    if 'na' in charac:
                        name = charac['na'][0]
                    else:
                        name = u.return_type(charac['firstline'][0]).capitalize()
                    outf.write('<td>{} [{}]</td>'.format(name,
                                                         anchor(to_oid(u.return_unitid(
                                                         charac['firstline'][0])))))
                else:
                    outf.write('<td></td><td></td>')
                outf.write('</tr>\n')
            outf.write('</table>\n')
            outf.write('</td></tr>')


def write_full_name(outf, v):
    if 'PL' in v:
        if 'fn' in v['PL']:
            full_name = v['PL']['fn'][0]
            name_list = v['PL']['fn']
            if len(name_list) > 1:
                for name in name_list[1:]:
                    full_name = full_name + ' ' + name
            outf.write('<tr><td>Full Name:</td><td>{}</td></tr>\n'.format(full_name))


def write_player_html(v, k, data):
    # generate player page
    fl = v['firstline'][0]
    #print('player {} {} {}'.format(fl, k, to_oid(k)))
    outf = open(to_oid(k)+'.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    name = v['na'][0]
    outf.write('<TITLE>{} [{}]'.format(name, \
               to_oid(k)))
    outf.write('</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    write_player_page_header(v,k,outf)
    write_player_basic_info(v,k,data,outf)
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()