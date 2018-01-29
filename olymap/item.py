#!/usr/bin/python

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor, get_oid, get_name, get_type, to_oid, loop_here2, get_who_has
import pathlib
from jinja2 import Environment, PackageLoader, select_autoescape


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
    if 'PL' in v and 'un' in v['PL']:
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


def write_item_html(v, k, data, trade_chain, outdir):
    # generate item page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '.html'), 'w')
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
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '_z.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('item.html')
    item = build_item_dict(k, v, data, trade_chain)
    outf.write(template.render(item=item))


def build_item_dict(k, v, data, trade_chain):
    who_has_id, who_has_name = get_who_has(v, data)
    dead_body_id, dead_body_name = get_dead_body(v, data)
    may_study_id, may_study_name = get_may_study(v, data)
    item_dict = {'oid' : get_oid(k),
                 'name' : get_name(v, data),
                 'type' : get_type(v),
                 'plural' : get_plural(v, data)[0],
                 'animal' : get_animal(v)[0],
                 'attack' : get_attack(v)[0],
                 'attack_bonus' : get_attack_bonus(v)[0],
                 'aura' : get_aura(v)[0],
                 'aura_bonus' : get_aura_bonus(v)[0],
                 'dead_body_oid' : dead_body_id,
                 'dead_body_name' : dead_body_name,
                 'defense' : get_defense(v)[0],
                 'defense_bonus' : get_defense_bonus(v)[0],
                 'fly_capacity' : get_fly_capacity(v)[0],
                 'land_capacity' : get_land_capacity(v)[0],
                 'lore' : get_lore(v)[0],
                 'may_study_oid' : may_study_id,
                 'may_study_name' : may_study_name,
                 'missile' : get_missile(v)[0],
                 'missile_bonus' : get_missile_bonus(v)[0],
                 'project_cast' : get_project_cast(v)[0],
                 'prominent' : get_prominent(v)[0],
                 'ride_capacity' : get_ride_capacity(v)[0],
                 'use_key' : get_use_key(v)[0],
                 'weight' : get_weight(v)[0],
                 'who_has_oid' : who_has_id,
                 'who_has_name' : who_has_name,
                 'trade_good' : get_trade_good(k, v, data, trade_chain)}
    return item_dict


def get_animal(v):
    return v.get('IT', {}).get('an', [None])


def get_attack(v):
    return v.get('IT', {}).get('at', [None])


def get_attack_bonus(v):
    return v.get('IM', {}).get('ab', [None])


def get_aura(v):
    return v.get('IM', {}).get('au', [None])


def get_aura_bonus(v):
    return v.get('IM', {}).get('ba', [None])


def get_capacities(v):
    return v.get('IT', {}).get('lc', [0]), v.get('IT', {}).get('rc', [0]), v.get('IT', {}).get('fc', [0])


def get_dead_body(v, data):
    oid =  v.get('PL', {}).get('un', [None])
    if oid[0] is not None:
        dead_body_rec = data[oid[0]]
        dead_body_name = get_name (dead_body_rec, data)
        return to_oid(oid[0]), dead_body_name
    return None, None


def get_defense(v):
    return v.get('IT', {}).get('de', [None])


def get_defense_bonus(v):
    return v.get('IM', {}).get('db', [None])


def get_fly_capacity(v):
    return v.get('IT', {}).get('fc', [None])


def get_land_capacity(v):
    return v.get('IT', {}).get('lc', [None])


def get_lore(v):
    return v.get('IM', {}).get('lo', [None])


def get_man_item(v):
    return v.get('IT', {}).get('mu', [None])


def get_may_study(v, data):
    oid = v.get('IM', {}).get('ms', [None])
    if oid[0] is not None:
        skill_rec = data[oid[0]]
        skill_name = get_name(skill_rec, data)
        return to_oid(oid[0]), skill_name
    return None, None


def get_missile(v):
    return v.get('IT', {}).get('mi', [None])


def get_missile_bonus(v):
    return v.get('IM', {}).get('mb', [None])


def get_plural(v, data):
    plural = v.get('IT', {}).get('pl', [None])
    if plural[0] is None:
        plural = [get_name(v, data)]
    return plural


def get_project_cast(v):
    return v.get('IM', {}).get('pc', [None])


def get_prominent(v):
    return v.get('IT', {}).get('pr', [None])


def get_ride_capacity(v):
    return v.get('IT', {}).get('rc', [None])


def get_use_key(v):
    return v.get('IM', {}).get('uk', [None])


def get_weight(v):
    return v.get('IT', {}).get('wt', [None])


def get_trade_good(k, v, data, trade_chain):
    if u.return_type(v) == 'tradegood':
        trade_list = trade_chain[k]
        if len(trade_list) > 0:
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
            return ret
    return None