#!/usr/bin/python

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor


def write_item_page_header(v, k, outf):
    outf.write('<H3>{} [{}]</H3>\n'.format(v['na'][0], to_oid(k)))


def write_item_basic_info(v, k, data, outf, trade_chain):
    outf.write('<table>\n')
    outf.write('<tr><td></td><td></td></tr>\n')
    if u.return_type(v) != '0':
        outf.write('<tr><td>Type:</td><td>{}</td></tr>\n'.format(u.return_type(v)))
    if 'IM' in v:
        if 'ab' in v['IM']:
            outf.write('<tr><td>Attack Bonus:</td><td>{}</td></tr>\n'.format(v['IM']['ab'][0]))
        if 'au' in v['IM']:
            outf.write('<tr><td>Aura:</td><td>{}</td></tr>\n'.format(v['IM']['au'][0]))
        if 'ba' in v['IM']:
            outf.write('<tr><td>Aura Bonus:</td><td>{}</td></tr>\n'.format(v['IM']['ba'][0]))
        if 'db' in v['IM']:
            outf.write('<tr><td>Defense Bonus:</td><td>{}</td></tr>\n'.format(v['IM']['db'][0]))
        if 'ms' in v['IM']:
            skill = data[v['IM']['ms'][0]]
            outf.write('<tr><td>May Study:</td><td>{} [{}]</td></tr>\n'
                       .format(skill['na'][0],
                               anchor(to_oid(v['IM']['ms'][0]))))
        if 'mb' in v['IM']:
            outf.write('<tr><td>Missile Bonus:</td><td>{}</td></tr>\n'.format(v['IM']['mb'][0]))
        if 'uk' in v['IM']:
            outf.write('<tr><td>Use Key:</td><td>{}</td></tr>\n'.format(u.xlate_use_key(v['IM']['uk'][0])))
        if 'lo' in v['IM']:
            outf.write('<tr><td>Lore:</td><td>{}</td></tr>\n'.format(v['IM']['lo'][0]))
        if 'pc' in v['IM']:
            outf.write('<tr><td>Project Cast:</td><td>{}</td></tr>\n'.format(v['IM']['pc'][0]))
    if 'IT' in v:
        if 'an' in v['IT']:
            outf.write('<tr><td>Animal:</td><td>{}</td></tr>\n'.format(v['IT']['an'][0]))
        if 'at' in v['IT']:
            outf.write('<tr><td>Attack:</td><td>{}</td></tr>\n'.format(v['IT']['at'][0]))
        if 'de' in v['IT']:
            outf.write('<tr><td>Defense:</td><td>{}</td></tr>\n'.format(v['IT']['de'][0]))
        if 'fc' in v['IT']:
            outf.write('<tr><td>Fly Capacity:</td><td>{}</td></tr>\n'.format(v['IT']['fc'][0]))
        if 'lc' in v['IT']:
            outf.write('<tr><td>Land Capacity:</td><td>{}</td></tr>\n'.format(v['IT']['lc'][0]))
        if 'mi' in v['IT']:
            outf.write('<tr><td>Missile:</td><td>{}</td></tr>\n'.format(v['IT']['mi'][0]))
        if 'pl' in v['IT']:
            outf.write('<tr><td>Plural Name:</td><td>{}</td></tr>\n'.format(v['IT']['pl'][0]))
        if 'pr' in v['IT']:
            outf.write('<tr><td>Prominent:</td><td>{}</td></tr>\n'.format(v['IT']['pr'][0]))
        if 'mu' in v['IT']:
            outf.write('<tr><td>Man Item:</td><td>{}</td></tr>\n'.format(v['IT']['mu'][0]))
        if 'rc' in v['IT']:
            outf.write('<tr><td>Ride Capacity:</td><td>{}</td></tr>\n'.format(v['IT']['rc'][0]))
        if 'wt' in v['IT']:
            outf.write('<tr><td>Weight:</td><td>{}</td></tr>\n'.format(v['IT']['wt'][0]))
        if 'un' in v['IT']:
            charac = data[v['IT']['un'][0]]
            outf.write('<tr><td>Who Has:</td><td>{} [{}]</td></tr>\n'.format(charac['na'][0],
                                                                             anchor(to_oid(v['IT']['un'][0]))))
    if 'PL' in v:
        if 'un' in v['PL']:
            charac = data[v['PL']['un'][0]]
            outf.write('<tr><td>Dead Body Of:</td><td>{} [{}]</td></tr>\n'.format(charac['na'][0],
                                                                                  v['PL']['un'][0]))
    if u.return_type(v) == 'tradegood':
        trade_list = trade_chain[k]
        if len(trade_list) > 0:
            outf.write('<tr><td valign="top">Traded in:</td><td>')
            first = True
            ret = ''
            for loc in trade_list:
                loc_rec = data[loc[0]]
                if not first:
                    ret = ret + '<br>'
                first = False
                if loc[1] == '1':
                    ret = ret + 'buy: '
                else:
                    ret = ret + 'sell: '
                ret = ret + loc_rec['na'][0] + ' [' + anchor(to_oid(loc[0])) + ']'
            outf.write('{}</td></tr>\n'.format(ret))
    outf.write('<tr><td></td><td></td></tr>\n')
    outf.write('</table>\n')


def write_item_html(v, k, data, trade_chain):
    # generate item page
    outf = open(to_oid(k)+'.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    name = v['na'][0]
    outf.write('<TITLE>{} [{}]'.format(name,
               to_oid(k)))
    outf.write('</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    write_item_page_header(v, k, outf)
    write_item_basic_info(v, k, data, outf, trade_chain)
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()
