#!/usr/bin/python
import os
import operator
import string
import olypy.details as details
from collections import defaultdict
from olypy.oid import to_int
from olypy.oid import to_oid


def return_type(firstline):
    # return 3rd argument of firstlist
    _, _, type = firstline.split(' ', maxsplit=2)
    return type


def return_short_type(firstline):
    # return 3rd argument of firstlist
    _, _, type = firstline.split(' ', maxsplit=2)
    if 'poppy ' in type:
        short_type = type.replace('poppy ', 'p.')
    elif 'sacred grove' in type:
        short_type = type.replace('sacred grove', 's.grov')
    elif 'rocky ' in type:
        short_type = type.replace('rocky ', 'r.')
    elif 'battlefield' in type:
        short_type = type.replace('battlefield', 'btfd.')
    elif 'graveyard' in type:
        short_type = type.replace('graveyard', 'gvyd.')
    elif 'port ' in type:
        short_type = type.replace('port ', 'p.')
    elif 'yew grove' in type:
        short_type = type.replace('yew grove', 'yew')
    elif 'pasture' in type:
        short_type = type.replace('pasture', 'past.')
    elif 'circle of ' in type:
        short_type = type.replace('circle of ', 'c.')
    elif 'ring of ' in type:
        short_type = type.replace('ring of ', 'r.')
    elif 'sand ' in type:
        short_type = type.replace('sand ', 's.')
    elif 'mallorn grove' in type:
        short_type = type.replace('mallorn grove', 'm.grov')
    elif 'faery ' in type:
        short_type = type.replace('faery ', 'f.')
    elif 'enchanted forest' in type:
        short_type = type.replace('enchanted forest', 'e.forst')
    elif 'collapsed ' in type:
        short_type = type.replace('collapsed ', '')
    elif '-in-progress' in type:
        short_type = type.replace('-in-progress', '')
    else:
        short_type = type
    return short_type


def return_kind(firstline):
    # return 2nd argument of firstlist
    _, kind, _ = firstline.split(' ', maxsplit=2)
    return kind


def return_unitid(firstline):
    # return 1st argument of firstlist
    unitid, _, _ = firstline.split(' ', maxsplit=2)
    return unitid


def return_firstline(v):
    # return firstlist from lib entry
    # firstline
    firstline = v['firstline'][0]
    return firstline


def chase_structure(k, data, level, seen_here_list):
    try:
        z = data[k]
        seen_here_list.append((return_unitid(z['firstline'][0]), level))
        if 'LI' in z:
            if 'hl' in z['LI']:
                level = level + 1
                for here in z['LI']['hl']:
                   seen_here_list = chase_structure(here,data,level, seen_here_list)
    except KeyError:
        return seen_here_list
    return seen_here_list


def xlate_rank(k):
    rank = 'Undefined'
    if 'CH' in k:
        if 'ra' in k['CH']:
            # could be a dict, but doing this for now because
            # rank can be a range??
            if k['CH']['ra'][0] == '10':
                rank = 'lord'
            elif k['CH']['ra'][0] == '20':
                    rank = 'knight'
            elif k['CH']['ra'][0] == '30':
                    rank = 'baron'
            elif k['CH']['ra'][0] == '40':
                    rank = 'count'
            elif k['CH']['ra'][0] == '50':
                    rank = 'earl'
            elif k['CH']['ra'][0] == '60':
                    rank = 'marquess'
            elif k['CH']['ra'][0] == '70':
                    rank = 'duke'
            elif k['CH']['ra'][0] == '80':
                    rank = 'king'
    return rank


def xlate_loyalty(v):
    # translate loyalty
    loyalty = 'Undefined'
    if 'CH' in v:
        if 'lk' in v['CH']:
            if v['CH']['lk'][0] == '0':
                loyalty = 'Unsworn'
            elif v['CH']['lk'][0] == '1' and 'lr' in v['CH']:
                loyalty = 'Contract-' + v['CH']['lr'][0]
            elif v['CH']['lk'][0] == '2' and 'lr' in v['CH']:
                loyalty = 'Oath-' + v['CH']['lr'][0]
            elif v['CH']['lk'][0] == '3' and 'lr' in v['CH']:
                loyalty = 'Fear-' + v['CH']['lr'][0]
            elif v['CH']['lk'][0] == '4':
                loyalty = 'Npc'
            elif v['CH']['lk'][0] == '5':
                loyalty = 'Summon'
            else:
                loyalty = 'Undefined'
    return loyalty


def is_fighter(item_record, item_id):
    attack = int(0)
    defense = int(0)
    missile = int(0)
    if 'at' in item_record['IT']:
        attack = int(item_record['IT']['at'][0])
    if 'df' in item_record['IT']:
        defense = int(item_record['IT']['df'][0])
    if 'mi' in item_record['IT']:
        missile = int(item_record['IT']['mi'][0])
    if attack > 0 or defense > 0 or missile > 0 or item_id == '18':
        return True
    return False


def is_magician(char_record):
    if 'CM' in char_record:
        if 'im' in char_record['CM']:
            if char_record['CM']['im'][0] == '1':
                return True
    return False


def is_char(data, id):
    if ' char ' in data[id]['firstline'][0]:
        return True
    return False


def is_loc(data, id):
    if ' loc ' in data[id]['firstline'][0]:
        return True
    return False


def is_item(data, id):
    if ' item ' in data[id]['firstline'][0]:
        return True
    return False


def is_ship(data, id):
    if ' ship ' in data[id]['firstline'][0]:
        return True
    return False


def is_player(data, id):
    if ' player ' in data[id]['firstline'][0]:
        return True
    return False


def is_city(data, id):
    if 'city' in data[id]['firstline'][0]:
        return True
    return False


def is_skill(data, id):
    if ' skill ' in data[id]['firstline'][0]:
        return True
    return False


def is_garrison(data, id):
    if 'garrison' in data[id]['firstline'][0]:
        return True
    return False


def is_castle(data, id):
    v = data[id]
    if return_type(v['firstline'][0]) == 'castle':
        return True
    return False


def resolve_all_pledges(data):
    ret = defaultdict(list)
    for id in data:
        if is_char(data, id):
            pl = data[id].get('CM', {}).get('pl', [None])[0]
            if pl:
                ret[pl].append(id)
    return ret


def resolve_castles(data):
    castle_ind = ['!','@','#','%','^','*','-','+','a','b','c','d','e','f','g','h']
    ret2 = defaultdict(list)
    for id in data:
        if is_castle(data, id):
            pl = data[id]
            if pl:
                ret2[region(id, data)].append(id)
    ret = defaultdict(list)
    for reg in ret2:
        castle_list = ret2[reg]
        i = 0
        for castle in castle_list:
            ret[castle].append(castle_ind[i])
            i = i + 1
    return ret


def resolve_bound_storms(data):
    ret = defaultdict(list)
    for id in data:
        if is_ship(data, id):
            pl = data[id].get('SL', {}).get('bs', [None])[0]
            if pl:
                ret[pl].append(id)
    return ret


def resolve_all_prisoners(data):
    ret = defaultdict(list)
    for id in data:
        if is_char(data, id):
            pl = data[id].get('CH', {}).get('pr', [None])[0]
            if pl:
                ret[data[id].get('LI', {}).get('wh', [None])[0]].append(id)
    return ret


def resolve_hidden_locs(data):
    ret = defaultdict(list)
    for id in data:
        if is_player(data, id):
            rec = data[id]
            pl = data[id].get('PL', {}).get('kn', [None])
            if pl:
                for loc in pl:
                    try:
                        loc_rec = data[loc]
                        if return_kind(loc_rec['firstline'][0]) == 'loc':
                            ret[loc].append(id)
                    except KeyError:
                        pass
    return ret


def resolve_teaches(data):
    ret = defaultdict(list)
    for id in data:
        if is_city(data, id):
            rec = data[id]
            pl=data[id].get('SL', {}).get('te', [None])
            if pl:
                for skill in pl:
                    if skill is not None:
                        ret[skill].append(id)
    return ret


def resolve_child_skills(data):
    ret = defaultdict(list)
    for id in data:
        if is_skill(data, id):
            rec = data[id]
            pl=data[id].get('SK', {}).get('rs', [None])
            if pl:
                for skill in pl:
                    ret[skill].append(id)
    return ret


def resolve_garrisons(data):
    ret = defaultdict(list)
    for id in data:
        if is_garrison(data, id):
            rec = data[id]
            pl=data[id].get('MI', {}).get('gc', [None])
            if pl:
                for skill in pl:
                    ret[skill].append(id)
    return ret


def resolve_skills_known(data):
    ret = defaultdict(list)
    for id in data:
        if is_char(data, id):
            rec = data[id]
            pl=data[id].get('CH', {}).get('sl', [None])
            if pl:
                iterations = int(len(pl) / 5)
                for skill in range(0, iterations - 1):
                    ret[pl[skill*5]].append(id)
    for row in ret:
        ret[row].sort()
    return ret


def resolve_trades(data):
    ret = defaultdict(list)
    for id in data:
        if is_city(data, id):
            rec = data[id]
            pl = data[id].get('tl', [None])
            iterations = int(len(pl) / 8)
            for goods in range(0, iterations - 1):
                if int(pl[(goods*8) + 1]) >= 300:
                    if int(pl[(goods * 8) + 0]) in {1,2}:
                        if pl[(goods*8) + 1] is not None:
                            ret[pl[(goods*8) + 1]].append([id, pl[(goods * 8) + 0]])
    return ret


def loc_depth(loc_type):
    if loc_type == "region":
        return 1
    elif loc_type in details.province_kinds:
        return 2
    elif loc_type in details.subloc_kinds:
        return 3
    # details.structure_type does not include 'in-progress' or could use it
    elif loc_type in ['temple', 'galley', 'roundship', 'castle', 'galley-in-progress', \
                      'roundship-in-progress', 'ghost ship', 'temple-in-progress', 'inn' \
                      'inn-in-progress', 'castle-in-progress', 'mine', 'mine-in-progress' \
                      'collapsed mine', 'tower', 'tower-in-progress', 'sewer']:
        return 4
    return 0


def region(who, data):
    v = data[who]
    while (int(who) > 0 and \
            (return_kind(v['firstline'][0]) != 'loc' or loc_depth(return_type(v['firstline'][0])) != 1)):
        v = data[v['LI']['wh'][0]]
        who = return_unitid(v['firstline'][0])
    return who


def top_ruler(k, data):
    cont = True
    while cont == True:
        top_dog = k
        try:
            v = data[k]
        except KeyError:
            return top_dog
        if 'CM' in v:
            if 'pl' in v['CM']:
                k = v['CM']['pl'][0]
            else:
                cont = False
        else:
            cont = False
    return top_dog


def calc_exit_distance(loc1, loc2):
    if return_type(loc1['firstline'][0]) == 'pit' or return_type(loc2['firstline'][0]) == 'pit':
        return 28
    if loc_depth(return_type(loc1['firstline'][0])) > loc_depth(return_type(loc2['firstline'][0])):
        tmp = loc1
        loc1 = loc2
        loc2 = tmp
    w_d = loc_depth(return_type(loc1['firstline'][0]))
    d_d = loc_depth(return_type(loc2['firstline'][0]))
    if d_d == 4:
        return 0
    if d_d == 3:
        return 1
    if return_type(loc1['firstline'][0]) == 'ocean' and \
        return_type(loc2['firstline'][0]) != 'ocean':
        return 2
    if return_type(loc1['firstline'][0]) != 'ocean' and \
        return_type(loc2['firstline'][0]) == 'ocean':
        return 2
    #
    # skipping province logic for now
    #
    if return_type(loc2['firstline'][0]) == 'ocean':
        return 3
    elif return_type(loc2['firstline'][0]) == 'mountain':
        return 10
    elif return_type(loc2['firstline'][0]) == 'forest':
        return 8
    elif return_type(loc2['firstline'][0]) == 'swamp':
        return 14
    elif return_type(loc2['firstline'][0]) == 'desert':
        return 8
    elif return_type(loc2['firstline'][0]) == 'plain':
        return 7
    elif return_type(loc2['firstline'][0]) == 'underground':
        return 7
    elif return_type(loc2['firstline'][0]) == 'cloud':
        return 7
    elif return_type(loc2['firstline'][0]) == 'tunnel':
        return 5
    elif return_type(loc2['firstline'][0]) == 'chamber':
        return 5
    return 0


def is_port_city(loc, data):
    if 'city' not in return_type(loc['firstline'][0]):
        return False
    province = data[loc['LI']['wh'][0]]
    if return_type(province['firstline'][0]) == 'mountain':
        return False
    province_list = province['LO']['pd']
    for pd in province_list:
        if int(pd) > 0:
            dest_loc = data[pd]
            if return_type(dest_loc['firstline'][0]) == 'ocean':
                return True
    return False


def province_has_port_city(loc, data):
    if 'LI' in loc:
        if 'hl' in loc['LI']:
            here_list = loc['LI']['hl']
            for here in here_list:
                try:
                    here_loc = data[here]
                    if is_port_city(here_loc,data):
                        return here
                except KeyError:
                    pass
    return '0'


def is_priest(v):
    if 'CH' in v:
        if 'sl' in v['CH']:
            skills_list = v['CH']['sl']
            if int(len(skills_list)) > 0:
                iterations = int(len(skills_list) / 5)
                for skill in range(0, iterations - 1):
                    if skills_list[skill * 5] == '750':
                        if skills_list[(skill * 5) + 1] == '2':
                            return True
    return False


def xlate_magetype(v):
    if 'CM' in v:
        if 'ma' in v['CM']:
            if int(v['CM']['ma'][0]) <= 5:
                return ''
            elif int(v['CM']['ma'][0]) <= 10:
                return 'conjurer'
            elif int(v['CM']['ma'][0]) <= 15:
                return 'mage'
            elif int(v['CM']['ma'][0]) <= 20:
                return 'wizard'
            elif int(v['CM']['ma'][0]) <= 30:
                return 'sorcerer'
            elif int(v['CM']['ma'][0]) <= 40:
                return '6th black circle'
            elif int(v['CM']['ma'][0]) <= 50:
                return '5th black circle'
            elif int(v['CM']['ma'][0]) <= 60:
                return '4th black circle'
            elif int(v['CM']['ma'][0]) <= 70:
                return '3rd black circle'
            elif int(v['CM']['ma'][0]) <= 80:
                return '2nd black circle'
            else:
                return 'master of the black arts'
    return ''


def anchor(k):
    # if int(to_int(k)) >= 300:
    return '<a href="{}.html">{}</a>'.format(k, k)
    # return k


def anchor2(k, text):
    # if int(to_int(k)) >= 300:
    return '<a href="{}.html">{}</a>'.format(k, text)
    # return k


def xlate_use_key(k):
    ret = 'undefined'
    if k == '1':
        ret = 'Death Potion'
    elif k == '2':
        ret = 'Healing Potion'
    elif k == '3':
        ret = 'Slave Potion'
    elif k == '4':
        ret = 'Palantir'
    elif k == '5':
        ret = 'Projected Cast'
    elif k == '6':
        ret = 'Quick Cast Potion'
    elif k == '7':
        ret = 'Drum'
    elif k == '8':
        ret = 'Elf Stone'
    elif k == '9':
        ret = 'Orb'
    return ret


def determine_item_use(v, data, trade_chain):
    ret = ''
    if return_type(v['firstline'][0]) == '0':
        if 'IM' in v:
            if 'uk' in v['IM']:
                use_key = v['IM']['uk'][0]
                if use_key == '1':
                    ret = 'death potion'
                elif use_key == '2':
                    ret = 'healing potion'
                elif use_key == '3':
                    ret = 'slave potion'
                elif use_key == '4':
                    ret = 'palantir'
                elif use_key == '5':
                    ret = "projected cast: "
                    if 'IM' in v:
                        if 'pc' in v['IM']:
                            try:
                                itemz = v['IM']['pc'][0]
                                itemz_rec = data[itemz]
                                name = ''
                                if 'na' in v:
                                    name = v['na'][0]
                                else:
                                    name = return_type(itemz_rec['firstline'][0]).capitalize()
                                ret = ret + return_kind(itemz_rec['firstline'][0]) +\
                                      ' ' + name + ' [' +\
                                    anchor(to_oid(itemz)) + ']'
                            except KeyError:
                                ret = ret + 'unknown target'
                        else:
                            ret = ret + 'unknown target'
                    else:
                        ret = ret + 'unknown target'
                elif use_key == '6':
                    ret = 'quick cast potion'
                elif use_key == '7':
                    ret = 'drum'
                elif use_key == '8':
                    ret = 'elf stone'
                elif use_key == '9':
                    ret = 'orb'
    elif return_type(v['firstline'][0]) == 'artifact':
        if 'IM' in v:
            ret = ''
            first = True
            if 'ab' in v['IM']:
                if first == False:
                    ret = ret + ', '
                ret = ret + 'attack +' + v['IM']['ab'][0]
                first = False
            if 'db' in v['IM']:
                if first == False:
                    ret = ret + ', '
                ret = ret + 'defense +' + v['IM']['db'][0]
                first = False
            if 'mb' in v['IM']:
                if first == False:
                    ret = ret + ', '
                ret = ret + 'missile +' + v['IM']['mb'][0]
                first = False
            if 'ba' in v['IM']:
                if first == False:
                    ret = ret + ', '
                ret = ret + 'aura +' + v['IM']['ba'][0]
                first = False
        else:
            ret = 'unknown'
    elif return_type(v['firstline'][0]) == 'dead body':
        if 'PL' in v:
            if 'un' in v['PL']:
                charac = v['PL']['un'][0]
                charac_rec = data[charac]
                ret = charac_rec['na'][0] + ' [' + anchor(to_oid(charac)) + ']'
            else:
                ret = 'unknown dead guy'
        else:
            ret = 'unknown dead guy'
    elif return_type(v['firstline'][0]) == 'npc_token':
        ret = 'controls: '
        if 'PL' in v:
            if 'un' in v['PL']:
                charac = v['PL']['un'][0]
                charac_rec = data[charac]
                ret = ret + charac_rec['na'][0] + ' [' + anchor(to_oid(charac)) + ']'
            else:
                ret = ret + 'unknown'
        else:
            ret = ret + 'unknown'
    elif return_type(v['firstline'][0]) == 'auraculum':
        ret = 'aura: '
        if 'IM' in v:
            if 'au' in v['IM']:
                ret = ret + v['IM']['au'][0]
            else:
                ret = ret + 'unknown'
        else:
            ret = ret + 'unknown'
    elif return_type(v['firstline'][0]) == 'scroll':
        ret = 'study: '
        if 'IM' in v:
            if 'ms' in v['IM']:
                skill = v['IM']['ms'][0]
                skill_rec = data[skill]
                ret = ret + skill_rec['na'][0] + ' [' + anchor(to_oid(skill)) + ']'
            else:
                ret = ret + 'unknown'
        else:
            ret = ret + 'unknown'
    elif return_type(v['firstline'][0]) == 'tradegood':
        trade_list = trade_chain[return_unitid(v['firstline'][0])]
        first = True
        if len(trade_list) > 0:
            for trade in trade_list:
                loc_rec = data[trade[0]]
                if first != True:
                    ret = ret + '<br>'
                else:
                    first = False
                if trade[1] == '1':
                    ret = ret + 'buy: ' + loc_rec['na'][0] + ' [' + anchor(to_oid(trade[0])) + ']'
                if trade[1] == '2':
                    ret = ret + 'sell: ' + loc_rec['na'][0] + ' [' + anchor(to_oid(trade[0])) + ']'
        else:
            ret = 'inactive tradegood'
    return ret