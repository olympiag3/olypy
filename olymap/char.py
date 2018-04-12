#!/usr/bin/python
import math
from collections import defaultdict

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import get_oid, get_name, get_subkind, to_oid, get_item_weight, get_pledged_to, return_char_skill
from olymap.item import get_magic_item, get_item_attack, get_attack_bonus, get_aura_bonus, get_item_defense
from olymap.item import get_defense_bonus, get_item_missile, get_missile_bonus
import olypy.details as details


def build_basic_char_dict(k, v, data, prominent_only=False):
    if not u.is_garrison(v):
        char_dict = {'id': k,
                     'oid': get_oid(k),
                     'name': get_name(v),
                     'subkind': get_subkind(v, data),
                     'kind': 'char',
                     'rank': get_rank(v),
                     'faction': get_faction(v, data),
                     'health_dict': get_health(v),
                     'nbr_men': get_nbr_men(v, data),
                     'absorb_blast': u.is_absorb_aura_blast(v),
                     'prisoner': u.is_prisoner(v),
                     'stacked_over_list': get_stacked_over(v, data),
                     'priest': u.is_priest(v),
                     'magetype': u.xlate_magetype(v, data),
                     'on_guard': u.is_on_guard(v),
                     'concealed': u.is_concealed(v),
                     'wearable': get_wearable_wielding(v, data),
                     'loyalty': get_loyalty(v),
                     'skills_known_list': get_skills_known(v, data),
                     'inventory_dict': get_inventory(v, data, prominent_only),
                     'aura_dict': get_aura(v, data),
                     'priest_dict': get_priest_skills(v, data)}
        return char_dict
    else:
        char_dict = {'id': k,
                     'oid': get_oid(k),
                     'name': get_name(v),
                     'subkind': get_subkind(v, data),
                     'kind': 'char',
                     'faction': get_faction(v, data),
                     'health_dict': get_health(v),
                     'nbr_men': get_nbr_men(v, data),
                     'on_guard': u.is_on_guard(v),
                     'loyalty': get_loyalty(v),
                     'inventory_dict': get_inventory(v, data, prominent_only)}
        return char_dict


def get_wearable_wielding(v, data):
    wearable_dict = {}
    attack_max = 0
    missile_max = 0
    defense_max = 0
    attack_unit_id = ''
    missile_unit_id = ''
    defense_unit_id = ''
    if 'il' in v:
        item_list = v['il']
        if len(item_list) > 0:
            for items in range(0, len(item_list), 2):
                itemz = data[item_list[items]]
                if 'IM' in itemz:
                    # find item(s) with best attack, defense and missile ratings
                    if get_attack_bonus(itemz) > attack_max:
                        attack_max = get_attack_bonus(itemz)
                        attack_unit_id = u.return_unitid(itemz)
                    if get_defense_bonus(itemz) > defense_max:
                        defense_max = get_defense_bonus(itemz)
                        defense_unit_id = u.return_unitid(itemz)
                    if get_missile_bonus(itemz) > missile_max:
                        missile_max = get_missile_bonus(itemz)
                        missile_unit_id = u.return_unitid(itemz)
        # found something
        if attack_unit_id != '' or missile_unit_id != '' or defense_unit_id != '':
            if attack_unit_id == missile_unit_id:
                missile_unit_id = ''
        if attack_unit_id == defense_unit_id:
            defense_unit_id = ''
        if attack_unit_id != '' or missile_unit_id != '':
            if attack_unit_id == '':
                missile_rec = data[missile_unit_id]
                missile_dict = {'id': missile_unit_id,
                                'oid': to_oid(missile_unit_id),
                                'name': get_name(missile_rec)}
                attack_dict = {}
            elif missile_unit_id == '':
                attack_rec = data[attack_unit_id]
                attack_dict = {'id': attack_unit_id,
                               'oid': to_oid(attack_unit_id),
                               'name': get_name(attack_rec)}
                missile_dict = {}
            else:
                missile_rec = data[missile_unit_id]
                missile_dict = {'id': missile_unit_id,
                                'oid': to_oid(missile_unit_id),
                                'name': get_name(missile_rec)}
                attack_rec = data[attack_unit_id]
                attack_dict = {'id': attack_unit_id,
                               'oid': to_oid(attack_unit_id),
                               'name': get_name(attack_rec)}
        else:
            attack_dict = {}
            missile_dict = {}
        if defense_unit_id != '':
            defense_rec = data[defense_unit_id]
            defense_dict = {'id': defense_unit_id,
                            'oid': to_oid(defense_unit_id),
                            'name': get_name(defense_rec)}
        else:
            defense_dict = {}
        wearable_dict = {'attack': attack_dict,
                         'defense': defense_dict,
                         'missile': missile_dict}
    return wearable_dict


# unit tested
def get_rank(box):
    rank = u.xlate_rank(box)
    return rank


# unit tested
def get_faction(box, data):
    faction_id = box.get('CH', {}).get('lo', [None])[0]
    if faction_id is not None:
        try:
            player_box = data[faction_id]
        except:
            return None
        faction_dict = {'id': faction_id,
                        'oid' : to_oid(faction_id),
                        'name' : get_name(player_box)}
        return faction_dict
    return None


# unit tested
def get_loc(box, data):
    loc_id = box.get('LI', {}).get('wh', [None])[0]
    if loc_id is not None:
        try:
            loc_box = data[loc_id]
        except:
            return None
        # could be location or stacked under something
        loc_dict = {'id': loc_id,
                    'oid' : to_oid(loc_id),
                    'name' : get_name(loc_box),
                    'kind' : u.return_kind(loc_box),
                    'subkind': u.return_subkind(loc_box)}
        return loc_dict
    return None


# unit tested
def get_loyalty(box):
    loyalty = u.xlate_loyalty(box)
    return loyalty


# unit tested 
def get_stacked_over(box, data):
    here_list = box.get('LI', {}).get('hl', [None])
    stacked_over_list = []
    if here_list[0] is not None:
        for char in here_list:
            char_box = data[char]
            if u.is_char(char_box):
                stacked_over_dict = {'id': char,
                                     'oid' : to_oid(char),
                                     'name' : get_name(char_box)}
                stacked_over_list.append(stacked_over_dict)
        return stacked_over_list
    return None


# unit tested
def get_health(box):
    health = box.get('CH', {}).get('he', [None])[0]
    status = None
    if health is not None:
        if -1 < int(health) < 100:
            sick = box.get('CH', {}).get('si', [None])[0]
            if sick is not None:
                if sick == '1':
                    status = '(getting worse)'
                else:
                    status = '(getting better)'
            else:
                status = '(getting better)'
        elif int(health) < 0:
            health = 'n/a'
        health_dict = {'health': health,
                       'status': status}
        return health_dict
    return 'n/a'


# unit tested
def get_combat(box):
    if get_char_behind(box) != '0':
        behind_text = '(stay behind in combat)'
    else:
        behind_text = '(front line in combat)'
    combat_dict = {'attack' : get_char_attack(box),
                   'defense' : get_char_defense(box),
                   'missile' : get_char_missile(box),
                   'behind' : get_char_behind(box),
                   'behind_text' : behind_text}
    return combat_dict


# unit tested
def get_break_point(box):
    break_point = box.get('CH', {}).get('bp', ['0'])[0]
    if break_point != '50':
        break_point_text = ('{}% (fight to the death)'.format(break_point))
    else:
        break_point_text = ('{}%'.format(break_point))
    return break_point_text


# unit tested
def get_vision_protection(v):
    vision_protection = v.get('CM', {}).get('vp', [None])[0]
    return vision_protection


# unit tested
def get_pledged_to_us(unit_id, data, pledge_list):
    pledged_to_us_list = []
    try:
        pledgee_list = pledge_list[unit_id]
    except:
        return None
    for pledgee_id in pledgee_list:
        pledgee_box = data[pledgee_id]
        pledgee_dict = {'id': pledgee_id,
                        'oid': to_oid(pledgee_id),
                        'name': get_name(pledgee_box)}
        pledged_to_us_list.append(pledgee_dict)
    return pledged_to_us_list


def get_aura(box, data):
    if u.is_magician(box):
        rank = u.xlate_magetype(box, data)
        current_aura = get_current_aura(box)
        max_aura = u.get_max_aura(box)
        auraculum_aura = 0
        if u.get_auraculum_id(box) is not None:
            auraculum_id = u.get_auraculum_id(box)
            auraculum_box = data[auraculum_id]
            auraculum_aura = u.get_auraculum_aura(auraculum_box)
            auraculum_dict = {'id': auraculum_id,
                              'oid': to_oid(auraculum_id),
                              'name': get_name(auraculum_box),
                              'aura': auraculum_aura}
        else:
            auraculum_dict = None
        aura_dict = {'rank': rank,
                     'current_aura': current_aura,
                     'max_aura': max_aura,
                     'total_aura': max_aura + auraculum_aura,
                     'auraculum_dict': auraculum_dict}
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
        prisoner_dict = {'oid': to_oid(prisoner),
                         'name': get_name(prisoner_rec),
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
            skill_dict = {'oid': to_oid(skill_id),
                          'name': get_name(skillz),
                          'req_skill': req_skill,
                          'known': 'Yes',
                          'days_studied': None,
                          'to_lear': None}
            skill_list.append(skill_dict)
        if know == '1':
            if not printunknown:
                printunknown = True
            skillz = data[skill_id]
            skill_dict = {'oid': to_oid(skill_id),
                          'name': get_name(skillz),
                          'req_skill': None,
                          'known': 'No',
                          'days_studied': days_studied,
                          'to_learn': skillz['SK']['tl'][0]}
            skill_list.append(skill_dict)
    return skill_list


def get_inventory(v, data, prominent_only):
    inventory_dict = {}
    total_items_weight = 0
    total_char_weight = 0
    land_cap = 0
    land_weight = 0
    ride_cap = 0
    ride_weight = 0
    fly_cap = 0
    fly_weight = 0
    items_list = []
    unit_subkind = '10'
    if 'CH' in v and 'ni' in v['CH']:
        unit_subkind = v['CH']['ni'][0]
    base_unit = data[unit_subkind]
    item_weight = get_item_weight(base_unit)
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
                if (prominent_only and u.is_prominent(itemz)) or prominent_only == False or prominent_only is None:
                    pass
                else:
                    continue
                itemz_name = u.get_item_name(itemz) if item_qty == 1 else u.get_item_plural(itemz)
                item_weight = get_item_weight(itemz)
                item_ext = int(item_weight * item_qty)
                total_items_weight = total_items_weight + item_ext
                fly_ext = None
                land_ext = None
                ride_ext = None
                if not u.is_garrison(v):
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
                items_dict = {'id': item_id,
                              'oid': to_oid(item_id),
                              'name': itemz_name,
                              'qty': item_qty,
                              'weight': item_weight,
                              'item_ext': item_ext,
                              'fly_ext': fly_ext,
                              'land_ext': land_ext,
                              'ride_ext': ride_ext,
                              'attack': get_item_attack(itemz),
                              'defense': get_item_defense(itemz),
                              'missile': get_item_missile(itemz),
                              'attack_bonus': get_attack_bonus(itemz),
                              'defense_bonus': get_defense_bonus(itemz),
                              'missile_bonus': get_missile_bonus(itemz),
                              'aura_bonus': get_aura_bonus(itemz),
                              'auraculum_aura': u.get_auraculum_aura(itemz)}
                items_list.append(items_dict)
    else:
        items_list = None
    land_pct = 0
    ride_pct = 0
    fly_pct = 0
    if not u.is_garrison(v):
        print_capacity = 'Yes'
        if land_cap > 0:
            land_pct = math.floor((land_weight * 100) / land_cap)
        if ride_cap > 0:
            ride_pct = math.floor((ride_weight * 100) / ride_cap)
        if fly_cap > 0:
            fly_pct = math.floor((fly_weight * 100) / fly_cap)
    else:
        print_capacity = None
    inventory_dict = {'total_items_weight': total_items_weight,
                      'total_char_weight': total_char_weight,
                      'land_weight': land_weight,
                      'ride_weight': ride_weight,
                      'fly_weight': fly_weight,
                      'land_cap': land_cap,
                      'ride_cap': ride_cap,
                      'fly_cap': fly_cap,
                      'land_pct': land_pct,
                      'ride_pct': ride_pct,
                      'fly_pct': fly_pct,
                      'print_capacity': print_capacity,
                      'items_list': items_list}
    return inventory_dict


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
                    trade_dict = {'direction': direction,
                                  'price': price,
                                  'qty': qty,
                                  'oid': oid,
                                  'name': name}
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
            vision_dict = {'oid': to_oid(vision),
                           'name': vision_name}
            visions_list.append(vision_dict)
    return visions_list


def get_magic_stuff(v, data):
    magic_list = []
    if 'il' in v:
        item_list = v['il']
        for items in range(0, len(item_list), 2):
            item_id = item_list[items]
            try:
                item_rec = data[item_id]
            except KeyError:
                pass
            else:
                magic_subkind = None
                magic_item_dict = get_magic_item(data, item_id, item_rec)
                if magic_item_dict is not None:
                    magic_list.append(magic_item_dict)
    return magic_list


def get_nbr_men(v, data):
    nbr_men = 0
    item_list = get_items_list(v, data, False)
    for item in item_list:
        item_dict = item
        id = item_dict['id']
        item_rec = data[id]
        if u.is_man_item(item_rec):
            nbr_men = nbr_men + item_dict['qty']
    return nbr_men


def get_items_list(v, data, prominent, item_select=None):
    items_list = []
    if 'il' in v:
        item_list = v['il']
        for item in range(0, len(item_list), 2):
            id = item_list[item]
            item_rec = data[id]
            if (prominent and u.is_prominent(item_rec)) or \
                (prominent == False and item_select is None or id == item_select):
                oid = to_oid(id)
                item_qty = int(item_list[item + 1])
                item_dict = {'id': id,
                             'oid': oid,
                             'name': get_name(item_rec, item_qty),
                             'qty': item_qty}
                items_list.append(item_dict)
    return items_list


def build_complete_char_dict(k, v, data, instance, pledge_chain, prisoner_chain, prominent_only):
    if not u.is_garrison(v):
        char_dict = {'id': k,
                     'oid': get_oid(k),
                     'name': get_name(v),
                     'subkind': get_subkind(v, data),
                     'kind': 'char',
                     'rank': get_rank(v),
                     'faction': get_faction(v, data),
                     'prisoner': u.is_prisoner(v),
                     'priest': u.is_priest(v),
                     'magetype': u.xlate_magetype(v, data),
                     'on_guard': u.is_on_guard(v),
                     'concealed': u.is_concealed(v),
                     'wearable': get_wearable_wielding(v, data),
                     'loc': get_loc(v, data),
                     'where': get_where(v, data),
                     'loyalty': get_loyalty(v),
                     # 'stacked_under': get_stacked_under(v, data),
                     'stacked_over_list': get_stacked_over(v, data),
                     'health_dict': get_health(v),
                     'break_point': get_break_point(v),
                     'vision_protection': get_vision_protection(v),
                     'pledged_to': get_pledged_to(v, data),
                     'pledged_to_us_list': get_pledged_to_us(k, data, pledge_chain),
                     'combat_dict': get_combat(v),
                     'aura_dict': get_aura(v, data),
                     'prisoner_list': get_prisoners(k, data, prisoner_chain),
                     'skills_known_list': get_skills_known(v, data),
                     'inventory_dict': get_inventory(v, data, prominent_only),
                     'trades_list': get_pending_trades(v, data),
                     'visions_list': get_visions_received(v, data),
                     'magic_list': get_magic_stuff(v, data),
                     'priest_dict': get_priest_skills(v, data)}
    else:
        char_dict = {'id': k,
                     'oid': get_oid(k),
                     'name': get_name(v),
                     'subkind': None,
                     'kind': 'char',
                     'rank': None,
                     'faction': get_faction(v, data),
                     'nbr_men': get_nbr_men(v, data),
                     'prisoner': None,
                     'priest': None,
                     'magetype': None,
                     'on_guard': None,
                     'wearable': None,
                     'loc': get_loc(v, data),
                     'loyalty': None,
                     # 'stacked_under': None,
                     'stacked_over_list': None,
                     'health_dict': None,
                     'break_point': None,
                     'vision_protection': None,
                     'pledged_to': None,
                     'pledged_to_us_list': None,
                     'combat_dict': None,
                     'concealed': None,
                     'aura_dict': None,
                     'prisoner_list': None,
                     'skills_known_list': None,
                     'inventory_dict': get_inventory(v, data, prominent_only),
                     'trades_list': None,
                     'visions_list': None,
                     'magic_list': get_magic_stuff(v, data)}
    return char_dict


def get_priest_skills(v, data):
    visions_list = []
    skill_751 = None
    skill_753 = None
    if return_char_skill(v, '751') is not None:
        skill_751 = True if return_char_skill(v, '751')[0]['known'] == True else False
    if return_char_skill(v, '753') is not None:
        skill_753 = True if return_char_skill(v, '753')[0]['known'] == True else False
    if 'CM' in v and 'vi' in v['CM']:
        vision_list = v['CM']['vi']
        for vision in vision_list:
            try:
                visioned = data[vision]
            except KeyError:
                vision_name = 'missing'
                vision_id = None
                vision_oid = None
            else:
                vision_name = visioned.get('na', [u.return_kind(visioned)])[0]
                vision_id = vision
                vision_oid = to_oid(vision)
            vision_dict = {'id': vision_id,
                           'oid': vision_oid,
                           'name': vision_name}
            visions_list.append(vision_dict)
    priest_dict = {'skill751': skill_751,
                   'skill753': skill_753,
                   'visions': visions_list}
    return priest_dict


# unit tested
def get_where(box, data):
    if get_loc(box, data) is not None:
        if get_loc(box, data)['kind'] != 'loc' or get_loc(box, data)['subkind'] not in details.province_kinds:
            where_id = u.province(u.return_unitid(box), data)
            where_box = data[where_id]
            where_dict = {'id': where_id,
                          'oid': to_oid(where_id),
                          'name': get_name(where_box)}
            return where_dict
    return None


# unit tested
def get_current_aura(box):
    return int(box.get('CM', {}).get('ca', [0])[0])


# unit tested
def get_char_attack(box):
    return int(box.get('CH', {}).get('at', ['0'])[0])


# unit tested
def get_char_behind(box):
    return box.get('CH', {}).get('bh', ['0'])[0]


# unit tested
def get_char_defense(box):
    return int(box.get('CH', {}).get('df', ['0'])[0])


# unit tested
def get_char_missile(box):
    return int(box.get('CH', {}).get('mi', ['0'])[0])

