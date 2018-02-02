#!/usr/bin/python
import math
from collections import defaultdict

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor, get_oid, get_name, get_type, to_oid, loop_here2, get_who_has
import pathlib
from jinja2 import Environment, PackageLoader, select_autoescape


def write_char_page_header(v, k, outf, data):
    if u.return_type(v) == 'garrison':
        name = 'Garrison'
    else:
        name = v['na'][0]
        if name == 'Ni':
            name = data[v['CH']['ni'][0]]['na'][0].capitalize()
    outf.write('<H3>{} [{}]</H3>\n'.format(name, to_oid(k)))


def write_char_faction(v, data, outf):
    # CH/lo
    if 'CH' in v and 'lo' in v['CH']:
        player = data[v['CH']['lo'][0]]
        outf.write('<tr>')
        outf.write('<td>Faction:</td>')
        outf.write('<td>{} [{}]</td></tr>\n'.format(player['na'][0],
                                                    anchor(to_oid(u.return_unitid(player)))))


def write_char_rank(v, k, outf):
    # CH/ra
    if 'CH' in v and 'ra' in v['CH']:
        outf.write('<tr>')
        outf.write('<td>Rank:</td>')
        outf.write('<td>{}</td></tr>\n'.format(u.xlate_rank(k)))


def write_char_loyalty(v, outf):
    # CH/lk
    if 'CH' in v and 'lk' in v['CH']:
        outf.write('<tr>')
        outf.write('<td>Loyalty:</td>')
        outf.write('<td>{}</td></tr>\n'.format(u.xlate_loyalty(v)))


def write_char_stacked_under(v, data, outf):
    # LI/wh
    if 'LI' in v and 'wh' in v['LI']:
        charu = data[v['LI']['wh'][0]]
        # if it's not a 'char' type, then it's a location/ship
        # and I handle that in location row
        if u.return_kind(charu) == 'char':
            outf.write('<tr>')
            outf.write('<td>Stacked Under:</td>')
            outf.write('<td>{} [{}]</td></tr>\n'.format(charu['na'][0],
                                                        anchor(to_oid(u.return_unitid(charu)))))


def write_char_stacked_over(v, data, outf):
    # LI/hl
    if 'LI' in v and 'hl' in v['LI']:
        over_list = v['LI']['hl']
        stacked_over = 'Stacked Over:'
        for ov in over_list:
            charo = data[ov]
            outf.write('<tr>')
            outf.write('<td>{}</td>'.format(stacked_over))
            outf.write(
                '<td>{} [{}]</td></tr>\n'.format(charo['na'][0],
                                                 anchor(to_oid(u.return_unitid(charo)))))
            stacked_over = ''


def write_char_health(v, outf):
    # CH/he and CH/si
    if 'CH' in v and 'he' in v['CH']:
        outf.write('<tr>')
        outf.write('<td>Health:</td>')
        if int(v['CH']['he'][0]) < 100:
            status = ''
            if 'si' in v['CH']:
                if v['CH']['si'][0] == '1':
                    status = '(getting worse)'
                else:
                    status = '(getting better)'
            if int(v['CH']['he'][0]) < 0:
                outf.write('<td>{} {}</td></tr>\n'.format('n/a', status))
            else:
                outf.write('<td>{}% {}</td></tr>\n'.format(v['CH']['he'][0], status))
        else:
            outf.write('<td>{}%</td></tr>\n'.format(v['CH']['he'][0]))


def write_char_combat(v, outf):
    # CH/at, CH/df, CH/mi
    attack = 0
    defense = 0
    missile = 0
    if 'CH' in v:
        if 'at' in v['CH']:
            attack = v['CH']['at'][0]
        if 'df' in v['CH']:
            defense = v['CH']['df'][0]
        if 'mi' in v['CH']:
            missile = v['CH']['mi'][0]
    outf.write('<tr>')
    outf.write('<td>Combat:</td>')
    outf.write('<td>attack {}, defense {}, missile {}</td></tr>\n'.format(attack,
                                                                          defense,
                                                                          missile))
    behind = '0'
    if 'CH' in v and 'bh' in v['CH']:
        behind = v['CH']['bh'][0]
    if behind != '0':
        behind_text = '(stay behind in combat)'
    else:
        behind_text = '(front line in combat)'
    outf.write('<tr>')
    outf.write('<td>&nbsp;</td>')
    outf.write('<td>behind {} {}</td></tr>\n'.format(behind, behind_text))


def write_char_break_point(v, outf, instance):
    # CH/bp
    # workaround for differences between g2 and g4
    if instance.lower() in {'g2','qa'}:
        break_point = '0'
    else:
        break_point = '50'
    if 'CH' in v and 'bp' in v['CH']:
        break_point = v['CH']['bp'][0]
    if break_point != '50':
        break_point_text = '(fight to the death)'
    else:
        break_point_text = ''
    outf.write('<tr>')
    outf.write('<td>Break Point:</td>')
    outf.write('<td>{}% {}</td></tr>\n'.format(break_point, break_point_text))


def write_char_vision_protection(v, outf):
    # CM/vp
    if 'CM' in v and 'vp' in v['CM']:
        outf.write('<tr>')
        outf.write('<td>Receive Vision :</td>')
        outf.write('<td>{} protection</td></tr>\n'.format(v['CM']['vp'][0]))


def write_char_pledged_to(v, data, outf):
    # CM/pl
    if 'CM' in v and 'pl' in v['CM']:
        pledged_to = data[v['CM']['pl'][0]]
        outf.write('<tr>')
        outf.write('<td>Pledged To:</td>')
        outf.write('<td>{} [{}]</td></tr>\n'.format(pledged_to['na'][0],
                                                    anchor(to_oid(u.return_unitid(pledged_to)))))


def write_char_pledged_to_us(k, data, outf, pledge_chain):
    # CM/pl
    try:
        pledge_list = pledge_chain[k]
    except:
        pass
    else:
        if len(pledge_list) > 0:
            pledged_text = 'Pledged To Us:'
            for pledgee in pledge_list:
                pledgee_rec = data[pledgee]
                outf.write('<tr>')
                outf.write('<td>{}</td>'.format(pledged_text))
                pledged_text = '&nbsp;'
                outf.write('<td>{} [{}]</td></tr>\n'.format(pledgee_rec['na'][0],
                                                            anchor(to_oid(pledgee))))


def write_char_concealed(v, outf):
    # CM/hs
    # need to check if alone - lib doesn't currently show
    if 'CM' in v and 'hs' in v['CM']:
        if v['CM']['hs'][0] == '1':
            outf.write('<tr>')
            outf.write('<td>Concealed:</td>')
            outf.write('<td>Yes</td></tr>\n')


def write_char_aura(v, data, outf):
    # CM/im, CM/ca, CM/ma, CN/ar
    # need to check if alone - lib doesn't currently show
    if u.is_magician(v):
        if u.xlate_magetype(v, data) not in {'', 'undefined'}:
            outf.write('<tr>')
            outf.write('<td>Mage Rank:</td>')
            outf.write('<td>{}</td></tr>\n'.format(u.xlate_magetype(v, data).capitalize()))
        if 'ca' in v['CM']:
            outf.write('<tr>')
            outf.write('<td>Current Aura:</td>')
            outf.write('<td>{}</td></tr>\n'.format(v['CM']['ca'][0]))
        max_aura = '0'
        if 'ma' in v['CM']:
            max_aura = v['CM']['ma'][0]
        if 'ar' in v['CM']:
            auraculum = data[v['CM']['ar'][0]]
            auraculum_amt = '0'
            if 'IM' in auraculum:
                if 'au' in auraculum['IM']:
                    auraculum_amt = auraculum['IM']['au'][0]
            outf.write('<tr>')
            outf.write('<td>Max Aura:</td>')
            outf.write('<td>{} ({}+{})</td></tr>\n'.format((int(max_aura) + int(auraculum_amt)),
                                                           max_aura, auraculum_amt))
        else:
            outf.write('<tr>')
            outf.write('<td>Max Aura:</td>')
            outf.write('<td>{}</td></tr>\n'.format(max_aura))


def write_char_prisoners(k, data, outf, prisoner_chain):
    # CH/pr
    try:
        prisoner_list = prisoner_chain[k]
    except:
        pass
    else:
        if len(prisoner_list) > 0:
            prisoner_text = 'Prisoners:'
            for prisoner in prisoner_list:
                prisoner_rec = data[prisoner]
                outf.write('<tr>')
                outf.write('<td>{}</td>'.format(prisoner_text))
                prisoner_text = '&nbsp;'
                prisoner_health_text = ''
                if 'CH' in prisoner_rec:
                    if 'he' in prisoner_rec['CH']:
                        prisoner_health_text = ' (health {})'.format(prisoner_rec['CH']['he'][0])
                outf.write('<td>{} [{}]{}</td></tr>\n'.format(prisoner_rec['na'][0],
                                                              anchor(to_oid(prisoner)),
                                                              prisoner_health_text))


def write_char_skills_known(v, data, outf):
    # CH/sl
    if 'CH' in v and 'sl' in v['CH']:
        skills_list = v['CH']['sl']
        skills_dict = defaultdict(list)
        if len(skills_list) > 0:
            for skill in range(0, len(skills_list), 5):
                skills_dict[skills_list[skill]].append(skills_list[skill + 1])
                skills_dict[skills_list[skill]].append(skills_list[skill + 2])
                skills_dict[skills_list[skill]].append(skills_list[skill + 3])
                skills_dict[skills_list[skill]].append(skills_list[skill + 4])
        sort_list = []
        for skill in skills_dict:
            skill_id = skill
            skills_rec = skills_dict[skill]
            know = skills_rec[0]
            sort_list.append([int(know) * -1, skill_id])
        sort_list.sort()
        if len(sort_list) > 0:
            printknown = False
            printunknown = False
            for skill in sort_list:
                skill_id = skill[1]
                skills_rec = skills_dict[skill_id]
                know = skills_rec[0]
                days_studied = skills_rec[1]
                if know == '2':
                    if not printknown:
                        if printunknown:
                            outf.write('</ul>\n')
                        outf.write('<p>Skills known:</p>\n')
                        outf.write('<ul style="list-style-type:none">\n')
                        printknown = True
                    skillz = data[skill_id]
                    outf.write('<li>')
                    if 'rs' in skillz['SK']:
                        req_skill = skillz['SK']['rs'][0]
                    else:
                        req_skill = '0'
                    if req_skill != '0':
                        outf.write('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                    outf.write('{} [{}]'.format(skillz['na'][0],
                                                anchor(to_oid(skill_id))))
                    outf.write('</li>\n')
                if know == '1':
                    if not printunknown:
                        if printknown:
                            outf.write('</ul>\n')
                        outf.write('<p>Partially known skills:</p>\n')
                        outf.write('<ul style="list-style-type:none">\n')
                        printunknown = True
                    skillz = data[skill_id]
                    outf.write('<li>')
                    outf.write('{} [{}], {}/{}'.format(skillz['na'][0],
                                                       anchor(to_oid(skill_id)),
                                                       days_studied,
                                                       skillz['SK']['tl'][0]))
                    outf.write('</li>\n')
            if printknown or printunknown:
                outf.write('</ul>\n')
    else:
        outf.write('<p>Skills known:</p>\n')
        outf.write('<ul style="list-style-type:none">\n')
        outf.write('<li>none</li></ul>\n')


def write_char_inventory(v, data, outf):
    total_weight = int(0)
    if 'il' in v:
        item_list = v['il']
        if len(item_list) > 0:
            outf.write('<p>Inventory:</p>\n')
            outf.write('<table>\n')
            outf.write('<tr><td style="text-align:right">qty</td><td style="text-align:left">name</td><td '
                       'style="text-align:right">weight</td><td style="text-align:left">&nbsp;</td></tr>\n')
            outf.write('<tr><td style="text-align:right">---</td><td style="text-align:left">----</td><td '
                       'style="text-align:right">------</td><td style="text-align:left">&nbsp;</td></tr>\n')
            for itm in range(0, len(item_list), 2):
                item_id = item_list[itm]
                item_qty = int(item_list[itm + 1])
                outf.write('<tr>')
                outf.write(f'<td style="text-align:right">{item_qty:,d}</td>')
                itemz = data[item_id]
                itemz_name = u.get_item_name(itemz) if item_qty == 1 else u.get_item_plural(itemz)
                outf.write('<td style="text-align:left">{} [{}]</td>'.format(itemz_name, anchor(to_oid(item_id))))
                if 'wt' in itemz['IT']:
                    item_weight = int(itemz['IT']['wt'][0])
                else:
                    item_weight = int(0)
                item_ext = int(item_weight * item_qty)
                outf.write(f'<td style="text-align:right">{item_ext:,d}</td>')
                total_weight = total_weight + (item_weight * item_qty)
                if u.return_type(v) != "garrison":
                    outf.write('<td>')
                    fly_capacity = int(0)
                    if 'fc' in itemz['IT']:
                        fly_capacity = int(itemz['IT']['fc'][0])
                    land_capacity = int(0)
                    if 'lc' in itemz['IT']:
                        land_capacity = int(itemz['IT']['lc'][0])
                    ride_capacity = int(0)
                    if 'rc' in itemz['IT']:
                        ride_capacity = int(itemz['IT']['rc'][0])
                    if fly_capacity > 0:
                        outf.write(f'fly {(fly_capacity * item_qty):,d}')
                    elif ride_capacity > 0:
                        outf.write(f'ride {(ride_capacity * item_qty):,d}')
                    elif land_capacity > 0:
                        outf.write(f'cap {(land_capacity * item_qty):,d}')
                    if u.is_fighter(itemz, item_id):
                        attack = int(0)
                        defense = int(0)
                        missile = int(0)
                        if 'at' in itemz['IT']:
                            attack = int(itemz['IT']['at'][0])
                        if 'df' in itemz['IT']:
                            defense = int(itemz['IT']['df'][0])
                        if 'mi' in itemz['IT']:
                            missile = int(itemz['IT']['mi'][0])
                        outf.write(' ({},{},{})'.format(attack, defense, missile))
                    attack_bonus = int(0)
                    defense_bonus = int(0)
                    missile_bonus = int(0)
                    if 'IM' in itemz:
                        if 'ab' in itemz['IM']:
                            attack_bonus = int(itemz['IM']['ab'][0])
                        if 'db' in itemz['IM']:
                            defense_bonus = int(itemz['IM']['db'][0])
                        if 'mb' in itemz['IM']:
                            missile_bonus = int(itemz['IM']['mb'][0])
                    if attack_bonus > 0:
                        outf.write(f'+ {attack_bonus:,d} attack')
                    if defense_bonus > 0:
                        outf.write(f'+ {defense_bonus:,d} defense')
                    if missile_bonus > 0:
                        outf.write(f'+ {missile_bonus:,d} missile')
                    if u.is_magician(v):
                        aura_bonus = 0
                        if 'IM' in itemz and 'ba' in itemz['IM']:
                            aura_bonus = int(itemz['IM']['ba'][0])
                        if aura_bonus > 0:
                            outf.write('+{} aura'.format(aura_bonus))
                    outf.write('&nbsp;</td>')
                else:
                    outf.write('<td>&nbsp;</td>')
                outf.write('</tr>\n')
            if u.return_type(v) != 'garrison':
                outf.write('<tr><td></td><td></td><td style="text-align:right">====='
                           '</td><td>&nbsp;</td></tr>\n')
                outf.write('<tr><td></td><td></td>'
                           f'<td style="text-align:right">{total_weight:,d}</td>'
                           '<td>&nbsp;</td></tr>\n')
            outf.write('</table>\n')


def write_char_capacity(v, data, outf):
    # animals = int(0)
    total_weight = int(0)
    land_cap = int(0)
    land_weight = int(0)
    ride_cap = int(0)
    ride_weight = int(0)
    fly_cap = int(0)
    fly_weight = int(0)
    unit_type = '10'
    if 'CH' in v and 'ni' in v['CH']:
        unit_type = v['CH']['ni'][0]
    base_unit = data[unit_type]
    item_weight = 0
    if 'IT' in base_unit and 'wt' in base_unit['IT']:
        item_weight = int(base_unit['IT']['wt'][0]) * 1
    if 'IT' in base_unit:
        if 'lc' in base_unit['IT'] and base_unit['IT']['lc'][0] != '0':
            land_cap = land_cap + int(base_unit['IT']['lc'][0])
        else:
            land_weight = land_weight + item_weight
        if 'fc' in base_unit['IT'] and base_unit['IT']['fc'][0] != '0':
            fly_cap = fly_cap + int(base_unit['IT']['fc'][0])
        else:
            fly_weight = fly_weight + item_weight
        if 'rc' in base_unit['IT'] and base_unit['IT']['rc'][0] != '0':
            ride_cap = ride_cap + int(base_unit['IT']['rc'][0])
        else:
            ride_weight = ride_weight + item_weight
    else:
        land_weight = land_weight + item_weight
        fly_weight = fly_weight + item_weight
        ride_weight = ride_weight + item_weight
    total_weight = total_weight + item_weight
    if 'il' in v:
        # not used for now
        # if 'IT' in base_unit:
        #    if 'an' in base_unit['IT']:
        #        animals = animals + 1
        item_list = v['il']
        for itm in range(0, len(item_list), 2):
            item_id = item_list[itm]
            item_qty = int(item_list[itm + 1])
            try:
                base_unit = data[item_id]
            except KeyError:
                pass
            else:
                item_weight = 0
                if 'IT' in base_unit and 'wt' in base_unit['IT']:
                    item_weight = int(base_unit['IT']['wt'][0]) * item_qty
                if 'IT' in base_unit:
                    if 'lc' in base_unit['IT'] and base_unit['IT']['lc'][0] != '0':
                        land_cap = land_cap + int(base_unit['IT']['lc'][0]) * item_qty
                    else:
                        land_weight = land_weight + item_weight
                    if 'fc' in base_unit['IT'] and base_unit['IT']['fc'][0] != '0':
                        fly_cap = fly_cap + int(base_unit['IT']['fc'][0]) * item_qty
                    else:
                        fly_weight = fly_weight + item_weight
                    if 'rc' in base_unit['IT'] and base_unit['IT']['rc'][0] != '0':
                        ride_cap = ride_cap + int(base_unit['IT']['rc'][0]) * item_qty
                    else:
                        ride_weight = ride_weight + item_weight
                else:
                    land_weight = land_weight + item_weight
                    fly_weight = fly_weight + item_weight
                    ride_weight = ride_weight + item_weight
                total_weight = total_weight + item_weight
    outf.write('<p>Capacity: ')
    if land_cap > 0:
        pct = math.floor((land_weight * 100) / land_cap)
        outf.write(f'{land_weight:,d}/{land_cap:,d} land ({pct:,d}%)')
    if ride_cap > 0:
        pct = math.floor((ride_weight * 100) / ride_cap)
        outf.write(f' {ride_weight:,d}/{ride_cap:,d} ride ({pct:,d}%)')
    if fly_cap > 0:
        pct = math.floor((fly_weight * 100) / fly_cap)
        outf.write(f' {fly_weight:,d}/{fly_cap:,} fly ({pct:,d}%)')
    outf.write('</p>\n')


def write_char_pending_trades(v, data, outf):
    if 'tl' in v:
        trade_list = v['tl']
        if len(trade_list) > 0:
            outf.write('<p>Pending Trades:</p>\n')
            outf.write('<table>\n')
            outf.write('<tr><td style="text-align:right">trades</td><td style="text-align:right">price</td>'
                       '<td style="text-align:right">qty</td><td style="text-align:left">item</td>\n')
            outf.write('<tr><td style="text-align:right">---</td><td style="text-align:right">-----</td>'
                       '<td style="text-align:right">---</td><td style="text-align:left">----</td>\n')
            for trades in range(0, len(trade_list), 8):
                try:
                    itemz = data[trade_list[trades + 1]]
                except KeyError:
                    pass
                else:
                    outf.write('<tr>')
                    direction = 'buy' if trade_list[trades] == '1' else 'sell'
                    outf.write('<td style="text-align:right">{}</td>'.format(direction))
                    outf.write('<td style="text-align:right">{}</td>'.format(trade_list[trades + 3]))
                    outf.write('<td style="text-align:right">{}</td>'.format(trade_list[trades + 2]))
                    name = u.get_item_name (itemz) if int(trade_list[trades + 2]) == 1 else u.get_item_plural(itemz)
                    anch = anchor(to_oid(trade_list[trades + 1]))
                    outf.write('<td style="text-align:left">{} [{}]</td>'.format(name, anch))
                    outf.write('</tr>\n')
            outf.write('</table>\n')


def write_char_visions_received(v, data, outf):
    if 'CM' in v and 'vi' in v['CM']:
        vision_list = v['CM']['vi']
        outf.write('<p>Visions Received:</p>\n')
        outf.write('<table>\n')
        for vision in vision_list:
            try:
                visioned = data[vision]
            except KeyError:
                vision_name = 'missing'
            else:
                vision_name = visioned.get('na', ['missing'])[0]
            outf.write('<tr><td>{} [{}]</td></tr>\n'.format(vision_name,
                                                            anchor(to_oid(vision))))
        outf.write('</table>\n')


def write_char_magic_stuff(v, data, outf):
    if 'il' in v:
        item_list = v['il']
        for items in range(0, len(item_list), 2):
            try:
                itemz = data[item_list[items]]
            except KeyError:
                pass
            else:
                item_type = u.return_type(itemz)
                if item_type == '0':
                    if 'IM' in itemz and 'uk' in itemz['IM']:
                        use_key = itemz['IM']['uk'][0]
                        if use_key == '2':
                            outf.write('<p>Healing Potion [{}]</p>\n'.format(anchor(to_oid(item_list[items]))))
                        elif use_key == '5':
                            loc_kind = 'unknown'
                            loc_name = 'unknown'
                            loc_id = ''
                            if 'IM' in itemz and 'pc' in itemz['IM']:
                                try:
                                    location = data[itemz['IM']['pc'][0]]
                                except KeyError:
                                    loc_kind = 'unknown'
                                    loc_name = 'unknown'
                                    loc_id = to_oid(itemz['IM']['pc'][0])
                                else:
                                    loc_id = anchor(to_oid(itemz['IM']['pc'][0]))
                                    if u.return_kind(location) != 'loc':
                                        loc_kind = u.return_kind(location)
                                    else:
                                        loc_kind = 'location'
                                    loc_name = location.get('na', ['unknown'])[0]
                                    loc_id = anchor(to_oid(u.return_unitid(location)))
                            else:
                                loc_id = '(no id)'
                            anch = anchor(to_oid(item_list[items]))
                            outf.write('<p>Projected Cast [{}] to {} {}'.format(anch,
                                                                                loc_kind,
                                                                                loc_name))
                            if loc_id != '':
                                outf.write(' [{}]'.format(loc_id))
                            outf.write('</p>\n')
                elif item_type == 'scroll':
                    if 'IM' in itemz and 'ms' in itemz['IM']:
                        skill_id = anchor(to_oid(itemz['IM']['ms'][0]))
                        scroll_id = anchor(to_oid(item_list[items]))
                        required_study = ''
                        try:
                            skill = data[itemz['IM']['ms'][0]]
                        except KeyError:
                            skill_name = 'unknown'
                        else:
                            skill_name = skill['na'][0]
                            if 'SK' in skill:
                                if 'rs' in skill['SK']:
                                    try:
                                        skill2 = data[skill['SK']['rs'][0]]
                                    except KeyError:
                                        skill2_name = 'unknown'
                                    else:
                                        skill2_name = skill2.get('na', ['unknown'])[0]
                                    anch = anchor(to_oid(skill['SK']['rs'][0]))
                                    required_study = '(requires {} [{}])'.format(skill2_name, anch)
                        outf.write('<p>Scroll [{}] permits the study of the following skills:<br>&nbsp;&nbsp;&nbsp;'
                                   '{} [{}] {}</p>\n'.format(scroll_id,
                                                             skill_name,
                                                             skill_id,
                                                             required_study))


def write_char_type(v, k, data, outf):
    if u.return_type(v) == 'ni':
        outf.write('<tr>')
        outf.write('<td>Type:</td>')
        outf.write('<td>{} [{}]</td></tr>\n'.format(data[v['CH']['ni'][0]]['na'][0],
                                                    anchor(to_oid(v['CH']['ni'][0]))))


def write_char_basic_info(v, k, data, outf, pledge_chain, prisoner_chain, instance):
    if u.return_type(v) != 'garrison':
        outf.write('<table>\n')
        write_char_type(v, k, data, outf)
        write_char_rank(v, k, outf)
        write_char_faction(v, data, outf)
        write_char_location(data, outf, v)
        write_char_loyalty(v, outf)
        write_char_stacked_under(v, data, outf)
        write_char_stacked_over(v, data, outf)
        write_char_health(v, outf)
        write_char_combat(v, outf)
        write_char_break_point(v, outf, instance)
        write_char_vision_protection(v, outf)
        write_char_pledged_to(v, data, outf)
        write_char_pledged_to_us(k, data, outf, pledge_chain)
        write_char_concealed(v, outf)
        write_char_aura(v, data, outf)
        # appear common not in lib yet
        # write_char_appear_common(v, k, data, outf)
        write_char_prisoners(k, data, outf, prisoner_chain)
        outf.write('</table>\n')
    if u.return_type(v) != 'garrison':
        write_char_skills_known(v, data, outf)
    write_char_inventory(v, data, outf)
    if u.return_type(v) != 'garrison':
        write_char_capacity(v, data, outf)
        write_char_pending_trades(v, data, outf)
        write_char_visions_received(v, data, outf)
    write_char_magic_stuff(v, data, outf)


def write_char_location(data, outf, v):
    if 'LI' in v and 'wh' in v['LI']:
        loc = data[v['LI']['wh'][0]]
        anch = anchor(to_oid(v['LI']['wh'][0]))
        outf.write('<tr>')
        outf.write('<td>Where:</td><td>{} [{}]</td>'.format(loc['na'][0], anch))
        outf.write('</tr>\n')


def write_char_html(v, k, data, pledge_chain, prisoner_chain, outdir, instance):
    # generate char page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k)+'.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    if u.return_type(v) == 'garrison':
        name = 'Garrison'
    else:
        name = v['na'][0]
        if name == 'Ni':
            name = data[v['CH']['ni'][0]]['na'][0].capitalize()
    outf.write('<TITLE>{} [{}]'.format(name, to_oid(k)))
    outf.write('</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    write_char_page_header(v, k, outf, data)
    write_char_basic_info(v, k, data, outf, pledge_chain, prisoner_chain, instance)
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '_z.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('char.html')
    char = build_char_dict(k, v, data, instance, pledge_chain, prisoner_chain)
    outf.write(template.render(char=char))


def build_char_dict(k, v, data, instance, pledge_chain, prisoner_chain):
    items_total_dict, items_list =  get_inventory(v, data)
    if u.return_type(v) != "garrison":
        char_dict = {'oid' : get_oid(k),
                     'name' : get_name(v, data),
                     'type' : get_type(v),
                     'rank' : get_rank(v),
                     'faction' : get_faction(v, data),
                     'loc' : get_loc(v, data),
                     'loyalty' : get_loyalty(v),
                     'stacked_under' : get_stacked_under(v, data),
                     'stacked_over_list' : get_stacked_over(v, data),
                     'health' : get_health(v),
                     'break_point' : get_break_point(v, instance),
                     'vision_protection' : get_vision_protection(v),
                     'pledged_to' : get_pledged_to(v, data),
                     'pledged_to_us_list' : get_pledged_to_us(k, data, pledge_chain),
                     'combat_dict' : get_combat(v),
                     'concealed' : get_concealed(v),
                     'aura_dict' : get_aura(v, data),
                     'prisoner_list' : get_prisoners(k, data, prisoner_chain),
                     'skills_known_list' : get_skills_known(v, data),
                     'items_total_dict' : items_total_dict,
                     'inventory_list' : items_list,
                     'trades_list' : get_pending_trades(v, data),
                     'visions_list' : get_visions_received(v, data),
                     'magic_list' : get_magic_stuff(v, data)}
    else:
        char_dict = {'oid': get_oid(k),
                     'name': get_name(v, data),
                     'type': None,
                     'rank': None,
                     'faction': None,
                     'loc': None,
                     'loyalty': None,
                     'stacked_under': None,
                     'stacked_over_list': None,
                     'health': None,
                     'break_point': None,
                     'vision_protection': None,
                     'pledged_to': None,
                     'pledged_to_us_list': None,
                     'combat_dict': None,
                     'concealed': None,
                     'aura_dict': None,
                     'prisoner_list': None,
                     'skills_known_list': None,
                     'items_total_dict': items_total_dict,
                     'inventory_list': items_list,
                     'trades_list': None,
                     'visions_list': None,
                     'magic_list': get_magic_stuff(v, data)}
    return char_dict


def get_char_detail(k, v, data):
    char_detail = ''
    if u.xlate_loyalty(v) not in {'Undefined'}:
        char_detail = char_detail + ' (' + u.xlate_loyalty(v)
        if u.is_absorb_aura_blast(v, data):
            char_detail = char_detail + ':AB'
        char_detail = char_detail + ')'
    else:
        if u.is_absorb_aura_blast(v, data):
            char_detail = char_detail + '(AB)'
    if u.return_type(v) != '0':
        if u.return_type(v) == 'ni':
            # char_type = v['na'][0].lower()
            char_type = data[v['CH']['ni'][0]]['na'][0]
        else:
            char_type = u.return_type(v)
        char_detail = char_detail + ', ' + char_type
    if u.is_prisoner(v):
        char_detail = char_detail + ', prisoner'
    if u.is_priest(v):
        char_detail = char_detail = ', priest'
    if u.is_on_guard(v):
        char_detail = char_detail + ', on guard'
    if u.is_concealed(v):
        char_detail = char_detail + ', concealed'
    char_detail = char_detail + get_char_wearable_wielding(v, data)
    char_detail = char_detail + get_char_prominent_items(v, data)
    char_detail = char_detail + get_char_accomp_by(v, data)
    return char_detail


def get_char_wearable_wielding(v, data):
    ww_str = ''
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
                ww_str = ww_str + ', wielding {} [{}]'.format(missile_rec['na'][0],
                                     anchor(to_oid(u.return_unitid(missile_rec))))
            elif missile == '':
                attack_rec = data[attack]
                ww_str = ww_str + ', wielding {} [{}]'.format(attack_rec['na'][0],
                                     anchor(to_oid(u.return_unitid(attack_rec))))
            else:
                missile_rec = data[missile]
                attack_rec = data[attack]
                ww_str = ww_str + ', wielding {} [{}] and {} [{}]'.format(attack_rec['na'][0],
                                     anchor(to_oid(u.return_unitid(attack_rec))),
                                     missile_rec['na'][0],
                                     anchor(to_oid(u.return_unitid(missile_rec))))
        if defense != '':
            defense_rec = data[defense]
            ww_str = ww_str + ', wearing {} [{}]'.format(defense_rec['na'][0],
                                 anchor(to_oid(u.return_unitid(defense_rec))))
    return ww_str


def get_char_prominent_items(v, data):
    pi_str = ''
    if 'il' in v:
        item_list = v['il']
        if len(item_list) > 0:
            for items in range(0, len(item_list), 2):
                itemz = data[item_list[items]]
                if 'IT' in itemz:
                    if 'pr' in itemz['IT']:
                        if itemz['IT']['pr'][0] == '1':
                            item_name = u.get_item_name(itemz) if int(item_list[items + 1]) == 1 else u.get_item_plural(itemz)
                            pi_str = pi_str + ', {} {}'.format(item_list[items + 1], item_name)
    return pi_str


def get_char_accomp_by(v, data):
    ab_str = ''
    if 'LI' in v and 'hl' in v['LI']:
        ab_str = ab_str + ', accompanied by: '
    # add nsted list
    return ab_str


def get_rank(v):
    rank = u.xlate_rank(v)
    return rank


def get_faction(v, data):
    faction_oid = v.get('CH', {}).get('lo', [None])
    if faction_oid[0] is not None:
        player_rec = data[faction_oid[0]]
        faction_name = get_name(player_rec, data)
        faction_dict = {'oid' : to_oid(faction_oid[0]),
                        'name' : faction_name}
        return faction_dict
    return None


def get_loc(v, data):
    loc_oid = v.get('LI', {}).get('wh', [None])
    if loc_oid[0] is not None:
        loc_rec = data[loc_oid[0]]
        loc_name = get_name(loc_rec, data)
        loc_dict = {'oid' : to_oid(loc_oid[0]),
                    'name' : loc_name}
        return loc_dict
    return None


def get_loyalty(v):
    loyalty = u.xlate_loyalty(v)
    return loyalty


def get_stacked_under(v, data):
    stacked_under_oid = v.get('LI', {}).get('wh', [None])
    if stacked_under_oid[0] is not None:
        char_rec = data[stacked_under_oid[0]]
        if u.return_kind(char_rec) == 'char':
            char_name = get_name(char_rec, data)
            stacked_under_dict = {'oid' : to_oid(stacked_under_oid[0]),
                                  'name' : char_name}
            return stacked_under_dict
    return None


def get_stacked_over(v, data):
    here_list = v.get('LI', {}).get('hl', [None])
    stacked_over_list = []
    if here_list[0] is not None:
        for char in here_list:
            char_rec = data[char]
            if u.return_kind(char_rec) == 'char':
                stacked_over_dict = {'oid' : to_oid(char),
                                     'name' : get_name(char_rec, data)}
                stacked_over_list.append(stacked_over_dict)
        return stacked_over_list
    return None


def get_health(v):
    health = v.get('CH', {}).get('he', [None])
    if health[0] is not None:
        if int(health[0]) < 100:
            status = ''
            if 'si' in v['CH']:
                if v['CH']['si'][0] == '1':
                    status = '(getting worse)'
                else:
                    status = '(getting better)'
            if int(health[0]) < 0:
                health_str = ('n/a {}'.format(status))
            else:
                health_str = ('{}% {}'.format(health[0], status))
        else:
            health_str = ('{}%'.format(health[0]))
        return health_str
    return None


def get_combat(v):
    attack = v.get('CH', {}).get('at', ['0'])
    defense = v.get('CH', {}).get('df', ['0'])
    missile = v.get('CH', {}).get('mi', ['0'])
    behind = v.get('CH', {}).get('bh', ['0'])
    if behind[0] != '0':
        behind_text = '(stay behind in combat)'
    else:
        behind_text = '(front line in combat)'
    combat_dict = {'attack' : attack[0],
                   'defense' : defense[0],
                   'missile' : missile[0],
                   'behind' : behind[0],
                   'behind_text' : behind_text}
    return combat_dict


def get_break_point(v, instance):
    if instance.lower() in {'g2','qa'}:
        break_point = '0'
    else:
        break_point = '50'
    if 'CH' in v and 'bp' in v['CH']:
        break_point = v['CH']['bp'][0]
    if break_point != '50':
        break_point_text = ('{}% (fight to the death)'.format(break_point))
    else:
        break_point_text = ('{}%'.format(break_point))
    return break_point_text


def get_vision_protection(v):
    vision_protection = v.get('CM', {}).get('vp', [None])
    return vision_protection[0]


def get_pledged_to(v, data):
    pledged_to = v.get('CM', {}).get('pl', [None])
    if pledged_to[0] is not None:
        char_rec = data[pledged_to[0]]
        if u.return_kind(char_rec) == 'char':
            char_name = get_name(char_rec, data)
            pledged_to_dict = {'oid' : to_oid(pledged_to[0]),
                               'name' : char_name}
            return pledged_to_dict
    return None


def get_pledged_to_us(k, data, pledge_list):
    pledged_to_us_list = []
    try:
        pledgee_list = pledge_list[k]
    except:
        return None
    for pledgee in pledgee_list:
        pledgee_rec = data[pledgee]
        pledgee_dict = {'oid' : to_oid(pledgee),
                        'name' : get_name(pledgee_rec, data)}
        pledged_to_us_list.append(pledgee_dict)
    return pledged_to_us_list


def get_concealed(v):
    concealed = v.get('CM', {}).get('hs', [None])
    if concealed[0] == '1':
        return 'Yes'
    return None


def get_aura(v, data):
    if u.is_magician(v):
        rank = None
        if u.xlate_magetype(v, data) not in {'', 'undefined'}:
            rank = u.xlate_magetype(v, data).capitalize()
        current_aura = v.get('CM', {}).get('ca', ['0'])
        max_aura = v.get('CM', {}).get('ma', ['0'])
        max_aura_str = ''
        if 'ar' in v['CM']:
            auraculum = data[v['CM']['ar'][0]]
            auraculum_amt = '0'
            if 'IM' in auraculum:
                if 'au' in auraculum['IM']:
                    auraculum_amt = auraculum['IM']['au'][0]
                    max_aura_str = ('{} ({}+{})'.format((int(max_aura[0]) + int(auraculum_amt)),
                                                          max_aura[0], auraculum_amt))
        else:
            max_aura_str = max_aura[0]
        aura_dict = {'rank' : rank,
                     'current_aura' : current_aura[0],
                     'max_aura_str' : max_aura_str}
        return aura_dict
    return None


def get_prisoners(k, data, prisoner_chain):
    try:
        char_list = prisoner_chain[k]
    except:
        return None
    prisoner_list = []
    for prisoner in char_list:
        prisoner_rec = data[prisoner]
        prisoner_health_text = ''
        if 'CH' in prisoner_rec:
            if 'he' in prisoner_rec['CH']:
                prisoner_health_text = ' (health {})'.format(prisoner_rec['CH']['he'][0])
        prisoner_dict = {'oid' : to_oid(prisoner),
                         'name' : get_name(prisoner_rec, data),
                         'health_text': prisoner_health_text}
        prisoner_list.append(prisoner_dict)
    return prisoner_list


def get_skills_known(v, data):
    skills_list = v.get('CH', {}).get('sl', [None])
    if skills_list[0] is None:
        return None
    skills_dict = defaultdict(list)
    if len(skills_list) > 0:
        for skill in range(0, len(skills_list), 5):
            skills_dict[skills_list[skill]].append(skills_list[skill + 1])
            skills_dict[skills_list[skill]].append(skills_list[skill + 2])
            skills_dict[skills_list[skill]].append(skills_list[skill + 3])
            skills_dict[skills_list[skill]].append(skills_list[skill + 4])
    sort_list = []
    for skill in skills_dict:
        skill_id = skill
        skills_rec = skills_dict[skill]
        know = skills_rec[0]
        sort_list.append([int(know) * -1, skill_id])
    sort_list.sort()
    printknown = False
    printunknown = False
    skill_list = []
    for skill in sort_list:
        skill_id = skill[1]
        skills_rec = skills_dict[skill_id]
        know = skills_rec[0]
        days_studied = skills_rec[1]
        if know == '2':
            if not printknown:
                printknown = True
            skillz = data[skill_id]
            if 'SK' in skillz and 'rs' in skillz['SK']:
                req_skill = skillz['SK']['rs'][0]
            else:
                req_skill = '0'
            skill_dict = {'oid' : to_oid(skill_id),
                          'name' : get_name(skillz, data),
                          'req_skill' : req_skill,
                          'known' : 'Yes',
                          'days_studied' : None,
                          'to_lear' : None}
            skill_list.append(skill_dict)
        if know == '1':
            if not printunknown:
                printunknown = True
            skillz = data[skill_id]
            skill_dict = {'oid' : to_oid(skill_id),
                          'name' : get_name(skillz, data),
                          'req_skill' : None,
                          'known' : 'No',
                          'days_studied' : days_studied,
                          'to_learn' : skillz['SK']['tl'][0]}
            skill_list.append(skill_dict)
    return skill_list


def get_inventory(v, data):
    total_items_weight = int(0)
    total_char_weight = int(0)
    land_cap = int(0)
    land_weight = int(0)
    ride_cap = int(0)
    ride_weight = int(0)
    fly_cap = int(0)
    fly_weight = int(0)
    items_list = []
    unit_type = '10'
    if 'CH' in v and 'ni' in v['CH']:
        unit_type = v['CH']['ni'][0]
    base_unit = data[unit_type]
    item_weight = 0
    if 'IT' in base_unit and 'wt' in base_unit['IT']:
        item_weight = int(base_unit['IT']['wt'][0]) * 1
    if 'IT' in base_unit:
        if 'lc' in base_unit['IT'] and base_unit['IT']['lc'][0] != '0':
            land_cap = land_cap + int(base_unit['IT']['lc'][0])
        else:
            land_weight = land_weight + item_weight
        if 'fc' in base_unit['IT'] and base_unit['IT']['fc'][0] != '0':
            fly_cap = fly_cap + int(base_unit['IT']['fc'][0])
        else:
            fly_weight = fly_weight + item_weight
        if 'rc' in base_unit['IT'] and base_unit['IT']['rc'][0] != '0':
            ride_cap = ride_cap + int(base_unit['IT']['rc'][0])
        else:
            ride_weight = ride_weight + item_weight
    else:
        land_weight = land_weight + item_weight
        fly_weight = fly_weight + item_weight
        ride_weight = ride_weight + item_weight
    total_char_weight = total_char_weight + item_weight
    if 'il' in v:
        item_list = v['il']
        if len(item_list) > 0:
            for itm in range(0, len(item_list), 2):
                item_id = item_list[itm]
                item_qty = int(item_list[itm + 1])
                itemz = data[item_id]
                itemz_name = u.get_item_name(itemz) if item_qty == 1 else u.get_item_plural(itemz)
                if 'wt' in itemz['IT']:
                    item_weight = int(itemz['IT']['wt'][0])
                else:
                    item_weight = int(0)
                item_ext = int(item_weight * item_qty)
                total_items_weight = total_items_weight + item_ext
                fly_ext = None
                land_ext = None
                ride_ext = None
                attack = None
                defense = None
                missile = None
                attack_bonus = None
                defense_bonus = None
                missile_bonus = None
                aura_bonus = None
                if u.return_type(v) != "garrison":
                    if 'fc' in itemz['IT']:
                        fly_capacity = int(itemz['IT']['fc'][0])
                        if fly_capacity > 0:
                            fly_ext = fly_capacity * item_qty
                        if fly_capacity != 0:
                            fly_cap = fly_cap + (fly_capacity * item_qty)
                        else:
                            fly_weight = fly_weight + item_ext
                    else:
                        fly_weight = fly_weight + item_ext
                    if 'rc' in itemz['IT']:
                        ride_capacity = int(itemz['IT']['rc'][0])
                        if ride_capacity > 0:
                            ride_ext = ride_capacity * item_qty
                        if ride_capacity != 0:
                            ride_cap = ride_cap + (ride_capacity * item_qty)
                        else:
                            ride_weight = ride_weight + item_ext
                    else:
                        ride_weight = ride_weight + item_ext
                    if 'lc' in itemz['IT']:
                        land_capacity = int(itemz['IT']['lc'][0])
                        if land_capacity > 0:
                            land_ext = land_capacity * item_qty
                        if land_capacity != 0:
                            land_cap = land_cap + (land_capacity * item_qty)
                        else:
                            land_weight = land_weight + item_ext
                    else:
                        land_weight = land_weight + item_ext
                    if 'IT' not in itemz:
                        land_weight = land_weight + item_ext
                        fly_weight = fly_weight + item_ext
                        ride_weight = ride_weight + item_ext
                    total_char_weight = total_char_weight + item_ext
                    if u.is_fighter(itemz, item_id):
                        attack = 0
                        defense = 0
                        missile = 0
                        if 'at' in itemz['IT']:
                            attack = int(itemz['IT']['at'][0])
                        if 'df' in itemz['IT']:
                            defense = int(itemz['IT']['df'][0])
                        if 'mi' in itemz['IT']:
                            missile = int(itemz['IT']['mi'][0])
                    if 'IM' in itemz:
                        if 'ab' in itemz['IM']:
                            attack_bonus = int(itemz['IM']['ab'][0])
                        if 'db' in itemz['IM']:
                            defense_bonus = int(itemz['IM']['db'][0])
                        if 'mb' in itemz['IM']:
                            missile_bonus = int(itemz['IM']['mb'][0])
                    if u.is_magician(v):
                        if 'IM' in itemz and 'ba' in itemz['IM']:
                            if int(itemz['IM']['ba'][0]) > 0:
                                aura_bonus = int(itemz['IM']['ba'][0])
                items_dict = {'item' : to_oid(item_id),
                              'item_name' : itemz_name,
                              'item_qty' : item_qty,
                              'item_weight' : item_weight,
                              'item_ext' : item_ext,
                              'fly_ext' : fly_ext,
                              'land_ext' : land_ext,
                              'ride_ext' : ride_ext,
                              'attack' : attack,
                              'defense' : defense,
                              'missile' : missile,
                              'attack_bonus' : attack_bonus,
                              'defense_bonus' : defense_bonus,
                              'missile_bonus' : missile_bonus,
                              'aura_bonus' : aura_bonus}
                items_list.append(items_dict)
    else:
        items_list = None
    land_pct = 0
    ride_pct = 0
    fly_pct = 0
    if u.return_type(v) != "garrison":
        print_capacity = 'Yes'
        if land_cap > 0:
            land_pct = math.floor((land_weight * 100) / land_cap)
        if ride_cap > 0:
            ride_pct = math.floor((ride_weight * 100) / ride_cap)
        if fly_cap > 0:
            fly_pct = math.floor((fly_weight * 100) / fly_cap)
    else:
        print_capacity = None
    items_total_dict = {'total_items_weight' : total_items_weight,
                        'total_char_weight' : total_char_weight,
                        'land_weight' : land_weight,
                        'ride_weight' : ride_weight,
                        'fly_weight' : fly_weight,
                        'land_cap': land_cap,
                        'ride_cap': ride_cap,
                        'fly_cap': fly_cap,
                        'land_pct' : land_pct,
                        'ride_pct' : ride_pct,
                        'fly_pct' : fly_pct,
                        'print_capacity' : print_capacity}
    return items_total_dict, items_list


def get_pending_trades(v, data):
    trades_list = []
    if 'tl' in v:
        trade_list = v['tl']
        if len(trade_list) > 0:
            for trades in range(0, len(trade_list), 8):
                try:
                    itemz = data[trade_list[trades + 1]]
                except KeyError:
                    pass
                else:
                    direction = 'buy' if trade_list[trades] == '1' else 'sell'
                    price = int(trade_list[trades + 3])
                    qty = int(trade_list[trades + 2])
                    name = u.get_item_name (itemz) if int(trade_list[trades + 2]) == 1 else u.get_item_plural(itemz)
                    oid = to_oid(trade_list[trades + 1])
                    trade_dict = {'direction' : direction,
                                  'price' : price,
                                  'qty' : qty,
                                  'oid' : oid,
                                  'name' : name}
                    trades_list.append(trade_dict)
    return trades_list


def get_visions_received(v, data):
    visions_list = []
    if 'CM' in v and 'vi' in v['CM']:
        vision_list = v['CM']['vi']
        for vision in vision_list:
            try:
                visioned = data[vision]
            except KeyError:
                vision_name = 'missing'
            else:
                vision_name = visioned.get('na', ['missing'])[0]
            vision_dict = {'oid' : to_oid(vision),
                           'name' : vision_name}
            visions_list.append(vision_dict)
    return visions_list


def get_magic_stuff(v, data):
    magic_list = []
    if 'il' in v:
        item_list = v['il']
        for items in range(0, len(item_list), 2):
            try:
                itemz = data[item_list[items]]
            except KeyError:
                pass
            else:
                magic_type = None
                item_type = u.return_type(itemz)
                if item_type == '0':
                    if 'IM' in itemz and 'uk' in itemz['IM']:
                        use_key = itemz['IM']['uk'][0]
                        if use_key == '2':
                            magic_type = 'Healing Potion'
                            magic_dict = {'oid': to_oid(item_list[items]),
                                          'name': None,
                                          'skill_id': None,
                                          'required_study': None,
                                          'required_name': None,
                                          'loc_kind': None,
                                          'loc_id' : None,
                                          'magic_type': magic_type}
                            magic_list.append(magic_dict)
                        elif use_key == '5':
                            loc_kind = 'unknown'
                            loc_name = 'unknown'
                            loc_id = ''
                            if 'IM' in itemz and 'pc' in itemz['IM']:
                                try:
                                    location = data[itemz['IM']['pc'][0]]
                                except KeyError:
                                    loc_kind = 'unknown'
                                    loc_name = 'unknown'
                                    loc_id = to_oid(itemz['IM']['pc'][0])
                                else:
                                    loc_id = to_oid(itemz['IM']['pc'][0])
                                    if u.return_kind(location) != 'loc':
                                        loc_kind = u.return_kind(location)
                                    else:
                                        loc_kind = 'location'
                                    loc_name = location.get('na', ['unknown'])[0]
                                    loc_id = to_oid(u.return_unitid(location))
                            else:
                                loc_id = '(no id)'
                            magic_type = 'Projected Cast'
                            magic_dict = {'oid': to_oid(item_list[items]),
                                          'name': loc_name,
                                          'skill_id': None,
                                          'required_study': None,
                                          'required_name': None,
                                          'loc_kind' : loc_kind,
                                          'loc_id' : loc_id,
                                          'magic_type': magic_type}
                            magic_list.append(magic_dict)
                elif item_type == 'scroll':
                    if 'IM' in itemz and 'ms' in itemz['IM']:
                        skill_id = to_oid(itemz['IM']['ms'][0])
                        scroll_id = to_oid(item_list[items])
                        required_study = ''
                        try:
                            skill = data[itemz['IM']['ms'][0]]
                        except KeyError:
                            skill_name = 'unknown'
                        else:
                            skill_name = skill['na'][0]
                            if 'SK' in skill:
                                if 'rs' in skill['SK']:
                                    try:
                                        skill2 = data[skill['SK']['rs'][0]]
                                    except KeyError:
                                        required_name = 'unknown'
                                    else:
                                        required_name = skill2.get('na', ['unknown'])[0]
                                        required_study = to_oid(skill['SK']['rs'][0])
                                        magic_type = 'Scroll'
                                        magic_dict = {'oid' : scroll_id,
                                                      'name' : skill_name,
                                                      'skill_id' : skill_id,
                                                      'required_study' : required_study,
                                                      'required_name' : required_name,
                                                      'loc_kind' : None,
                                                      'loc_id' : None,
                                                      'magic_type' : magic_type}
                                        magic_list.append(magic_dict)
    return magic_list