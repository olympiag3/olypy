#!/usr/bin/python
import math
from collections import defaultdict

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor
import pathlib


def write_char_page_header(v, k, outf):
    if u.return_type(v) == 'garrison':
        name = 'Garrison'
    else:
        name = v['na'][0]
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


def write_char_break_point(v, outf):
    # CH/bp
    break_point = '1'
    if 'CH' in v and 'bp' in v['CH']:
        break_point = v['CH']['bp'][0]
    if break_point == '0':
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
        if len(pledge_list) > 0:
            pledged_text = 'Pledged To Us:'
            for pledgee in pledge_list:
                pledgee_rec = data[pledgee]
                outf.write('<tr>')
                outf.write('<td>{}</td>'.format(pledged_text))
                pledged_text = '&nbsp;'
                outf.write('<td>{} [{}]</td></tr>\n'.format(pledgee_rec['na'][0],
                                                            anchor(to_oid(pledgee))))
    finally:
        pass


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
    if 'CM' in v and 'im' in v['CM']:
        if v['CM']['im'][0] == '1':
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
    finally:
        pass


def write_char_skills_known(v, data, outf):
    # CH/sl
    if 'CH' in v and 'sl' in v['CH']:
        skills_list = v['CH']['sl']
        skills_iteration = int(len(skills_list) / 5)
        skills_dict = defaultdict(list)
        if skills_iteration > 0:
            for skill in range(0, skills_iteration):
                skills_dict[skills_list[skill * 5]].append(skills_list[(skill * 5) + 1])
                skills_dict[skills_list[skill * 5]].append(skills_list[(skill * 5) + 2])
                skills_dict[skills_list[skill * 5]].append(skills_list[(skill * 5) + 3])
                skills_dict[skills_list[skill * 5]].append(skills_list[(skill * 5) + 4])
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
                skills_rec= skills_dict[skill_id]
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


def write_char_inventory(v, data, outf):
    total_weight = int(0)
    if 'il' in v:
        item_list = v['il']
        iterations = int(len(item_list) / 2)
        if iterations > 0:
            outf.write('<p>Inventory:</p>\n')
            outf.write('<table>\n')
            outf.write('<tr><td style="text-align:right">qty</td><td style="text-align:left">name</td><td '
                       'style="text-align:right">weight</td><td style="text-align:left">&nbsp;</td></tr>\n')
            outf.write('<tr><td style="text-align:right">---</td><td style="text-align:left">----</td><td '
                       'style="text-align:right">------</td><td style="text-align:left">&nbsp;</td></tr>\n')
            for itm in range(0, iterations):
                item_id = item_list[itm*2]
                item_qty = int(item_list[(itm*2)+1])
                outf.write('<tr>')
                outf.write('<td style="text-align:right">{}</td>'.format(item_qty))
                itemz = data[item_id]
                itemz_name = itemz['na'][0] if item_qty == 1 else itemz['IT']['pl'][0]
                outf.write('<td style="text-align:left">{} [{}]</td>'.format(itemz_name, anchor(to_oid(item_id))))
                if 'wt' in itemz['IT']:
                    item_weight = int(itemz['IT']['wt'][0])
                else:
                    item_weight = int(0)
                outf.write('<td style="text-align:right">{}</td>'.format(item_weight * item_qty))
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
                        outf.write('fly {}'.format(fly_capacity * item_qty))
                    elif ride_capacity > 0:
                        outf.write('ride {}'.format(ride_capacity * item_qty))
                    elif land_capacity > 0:
                        outf.write('cap {}'.format(land_capacity * item_qty))
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
                        if 'mi' in itemz['IT']:
                            missile_bonus = int(itemz['IM']['mb'][0])
                    if attack_bonus > 0:
                        outf.write('+ {} attack'.format(attack_bonus))
                    if defense_bonus > 0:
                        outf.write('+ {} defense'.format(defense_bonus))
                    if missile_bonus > 0:
                        outf.write('+ {} missile'.format(missile_bonus))
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
                outf.write('<tr><td></td><td></td><td style="text-align:right">{}</td>'
                           '<td>&nbsp;</td></tr>\n'.format(total_weight))
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
        if 'lc' in base_unit['IT']:
            land_cap = land_cap + int(base_unit['IT']['lc'][0])
        else:
            land_weight = land_weight + item_weight
        if 'fc' in base_unit['IT']:
            fly_cap = fly_cap + int(base_unit['IT']['fc'][0])
        else:
            fly_weight = fly_weight + item_weight
        if 'rc' in base_unit['IT']:
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
        iterations = int(len(item_list) / 2)
        for itm in range(0, iterations):
            item_id = item_list[itm * 2]
            item_qty = int(item_list[(itm * 2) + 1])
            try:
                base_unit = data[item_id]
                item_weight = 0
                if 'IT' in base_unit and 'wt' in base_unit['IT']:
                    item_weight = int(base_unit['IT']['wt'][0]) * item_qty
                if 'IT' in base_unit:
                    if 'lc' in base_unit['IT']:
                        land_cap = land_cap + int(base_unit['IT']['lc'][0]) * item_qty
                    else:
                        land_weight = land_weight + item_weight
                    if 'fc' in base_unit['IT']:
                        fly_cap = fly_cap + int(base_unit['IT']['fc'][0]) * item_qty
                    else:
                        fly_weight = fly_weight + item_weight
                    if 'rc' in base_unit['IT']:
                        ride_cap = ride_cap + int(base_unit['IT']['rc'][0]) * item_qty
                    else:
                        ride_weight = ride_weight + item_weight
                else:
                    land_weight = land_weight + item_weight
                    fly_weight = fly_weight + item_weight
                    ride_weight = ride_weight + item_weight
                total_weight = total_weight + item_weight
            except KeyError:
                pass
    outf.write('<p>Capacity: ')
    if land_cap > 0:
        pct = math.floor((land_weight * 100) / land_cap)
        outf.write('{}/{} land ({}%) '.format(land_weight, land_cap, pct))
    if ride_cap > 0:
        pct = math.floor((ride_weight * 100) / ride_cap)
        outf.write('{}/{} ride ({}%) '.format(ride_weight, ride_cap, pct))
    if fly_cap > 0:
        pct = math.floor((fly_weight * 100) / fly_cap)
        outf.write('{}/{} fly ({}%)'.format(fly_weight, fly_cap, pct))
    outf.write('</p>')


def write_char_pending_trades(v, data, outf):
    if 'tl' in v:
        trade_list = v['tl']
        iterations = int(len(trade_list) / 8)
        if iterations > 0:
            outf.write('<p>Pending Trades:</p>\n')
            outf.write('<table>\n')
            outf.write('<tr><td style="text-align:right">trades</td><td style="text-align:right">price</td>'
                       '<td style="text-align:right">qty</td><td style="text-align:left">item</td>\n')
            outf.write('<tr><td style="text-align:right">---</td><td style="text-align:right">-----</td>'
                       '<td style="text-align:right">---</td><td style="text-align:left">----</td>\n')
            for trades in range(0, iterations):
                try:
                    itemz = data[trade_list[(trades*8)+1]]
                    itemz_plural = itemz['IT']['pl'][0]
                    itemz_name = itemz['na'][0]
                    outf.write('<tr>')
                    direction = 'buy' if trade_list[(trades*8)+0] == '1' else 'sell'
                    outf.write('<td style="text-align:right">{}</td>'.format(direction))
                    outf.write('<td style="text-align:right">{}</td>'.format(trade_list[(trades*8)+3]))
                    outf.write('<td style="text-align:right">{}</td>'.format(trade_list[(trades*8)+2]))
                    name = itemz_name if int(trade_list[(trades*8)+2]) == 1 else itemz_plural
                    anch = anchor(to_oid(trade_list[(trades*8)+1]))
                    outf.write('<td style="text-align:left">{} [{}]</td>'.format(name, anch))
                    outf.write('</tr>\n')
                except KeyError:
                    pass
            outf.write('</table>\n')


def write_char_visions_received(v, data, outf):
    if 'CM' in v and 'vi' in v['CM']:
        vision_list = v['CM']['vi']
        # iterations = len(vision_list)
        outf.write('<p>Visions Received:</p>\n')
        outf.write('<table>\n')
        for vision in vision_list:
            try:
                visioned = data[vision]
                vision_name = visioned['na'][0]
            except KeyError:
                vision_name = 'missing'
            outf.write('<tr><td>{} [{}]</td></tr>\n'.format(vision_name,
                                                            anchor(to_oid(vision))))
        outf.write('</table>\n')


def write_char_magic_stuff(v, data, outf):
    if 'il' in v:
        item_list = v['il']
        iterations = int(len(item_list) / 2)
        for items in range(0, iterations):
            try:
                itemz = data[item_list[items*2]]
                item_type = u.return_type(itemz)
                if item_type == '0':
                    if 'IM' in itemz and 'uk' in itemz['IM']:
                        use_key = itemz['IM']['uk'][0]
                        if use_key == '2':
                            outf.write('<p>Healing Potion [{}]</p>\n'.format(anchor(to_oid(item_list[items*2]))))
                        elif use_key == '5':
                            loc_kind = ''
                            loc_name = ''
                            loc_id = ''
                            if 'IM' in itemz and 'pc' in itemz['IM']:
                                try:
                                    location = data[itemz['IM']['pc'][0]]
                                    if u.return_kind(location) != 'loc':
                                        loc_kind = u.return_kind(location)
                                    else:
                                        loc_kind = 'location'
                                    loc_name = location['na'][0]
                                    loc_id = anchor(to_oid(u.return_unitid(location)))
                                except KeyError:
                                    loc_kind = 'unknown'
                                    loc_name = 'unknown'
                                    loc_id = anchor(to_oid(itemz['IM']['pc'][0]))
                            anch = anchor(to_oid(item_list[items*2]))
                            outf.write('<p>Projected Cast [{}] to {} {} [{}]</p>\n'.format(anch,
                                                                                           loc_kind,
                                                                                           loc_name,
                                                                                           loc_id))
                elif item_type == 'scroll':
                    if 'IM' in itemz and 'ms' in itemz['IM']:
                        skill_id = anchor(to_oid(itemz['IM']['ms'][0]))
                        scroll_id = anchor(to_oid(item_list[items*2]))
                        required_study = ''
                        try:
                            skill = data[itemz['IM']['ms'][0]]
                            skill_name = skill['na'][0]
                            if 'SK' in skill:
                                if 'rs' in skill['SK']:
                                    try:
                                        skill2 = data[skill['SK']['rs'][0]]
                                        skill2_name = skill2['na'][0]
                                    except KeyError:
                                        skill2_name = 'unknown'
                                    anch = anchor(to_oid(skill['SK']['rs'][0]))
                                    required_study = '(requires {} [{}])'.format(skill2_name, anch)
                        except KeyError:
                            skill_name = 'unknown'
                        outf.write('<p>Scroll [{}] permits the study of the following skills:<br>&nbsp;&nbsp;&nbsp;'
                                   '{} [{}] {}</p>\n'.format(scroll_id,
                                                             skill_name,
                                                             skill_id,
                                                             required_study))
            except KeyError:
                pass


def write_char_basic_info(v, k, data, outf, pledge_chain, prisoner_chain):
    if u.return_type(v) != 'garrison':
        outf.write('<table>\n')
        write_char_rank(v, k, outf)
        write_char_faction(v, data, outf)
        write_char_location(data, outf, v)
        write_char_loyalty(v, outf)
        write_char_stacked_under(v, data, outf)
        write_char_stacked_over(v, data, outf)
        write_char_health(v, outf)
        write_char_combat(v, outf)
        write_char_break_point(v, outf)
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


def write_char_html(v, k, data, pledge_chain, prisoner_chain, outdir):
    # generate char page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k)+'.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    if u.return_type(v) == 'garrison':
        name = 'Garrison'
    else:
        name = v['na'][0]
    outf.write('<TITLE>{} [{}]'.format(name, to_oid(k)))
    outf.write('</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    write_char_page_header(v, k, outf)
    write_char_basic_info(v, k, data, outf, pledge_chain, prisoner_chain)
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()
