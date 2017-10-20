#!/usr/bin/python

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor
from olymap.utilities import anchor2


def write_index():
    outf = open('index.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>Olympia Mapper Tool</TITLE>\n')
    outf.write('<link href="map.css" rel="stylesheet" type="text/css">\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<h3>Olympia Mapper Tool</h3>\n')
    outf.write('<table>')
    outf.write('<tr>')
    outf.write('<th>')
    outf.write('<ul>Maps<br>')
    outf.write('<li><a href="main_map.html">Main</a></li>')
    outf.write('<li>Hades</li>')
    outf.write('<li>Faery</li>')
    outf.write('</ul>')
    outf.write('</th>')
    outf.write('<th>')
    outf.write('<ul>Reports<br>')
    outf.write('<li><a href="master_item_report.html">Items</a></li>')
    outf.write('<li><a href="master_healing_potion_report.html">Healing Potions</a></li>')
    outf.write('<li><a href="master_orb_report.html">Orbs</a></li>')
    outf.write('<li><a href="master_projected_cast_report.html">Projected Casts</a></li>')
    outf.write('<li><a href="master_player_report.html">Players</a></li>')
    outf.write('<li><a href="master_skill_xref_report.html">Skills Xref</a></li>')
    outf.write('<li><a href="master_trade_report.html">Trades</a></li>')
    outf.write('<li><a href="master_ship_report.html">Ships</a></li>')
    outf.write('<li><a href="master_location_report.html">Locations</a></li>')
    outf.write('</ul>')
    outf.write('</th>')
    outf.write('<th>')
    outf.write('<ul>Links<br>')
    outf.write('<li><a href="http://shadowlandgames.com/olympia/rules.html">Rules</a></li>')
    outf.write('<li><a href="http://shadowlandgames.com/olympia/orders.html">Orders</a></li>')
    outf.write('<li><a href="http://shadowlandgames.com/olympia/skills.html">Skills</a></li>')
    outf.write('</ul>')
    outf.write('</th>')
    outf.write('</tr>')
    outf.write('</table>\n')
    outf.write('<h2>Intro</h2>\n')
    outf.write('This is the map of Olympia, including S.O.C.R.A.T.E.S. and Lords of the Crown data, as of the end of turn 192.<p>')
    outf.write('Mobile things (characters, ships) are present in the map only if they were seen in turn 192.\n')
    outf.write('<h2>Features</h2>\n')
    outf.write('<ul>\n')
    outf.write('<li>Concentrations of men indicated by red border (here is a <a href="main_map_leaf_an40.html">combat zone</a>)\n')
    outf.write('<li>Ships indicated by yellow border if troop count is low\n')
    outf.write('<li>Barriers indicated by brown border (e.g. ar54, aq52)\n')
    outf.write('<li>Garrison/castle allegiance is indicated by the @ after the province ID (<a href="main_map_leaf_ba10.html">Grinter</a> is a good example)\n')
    outf.write('<li>Keep clicking down, there is a lot of info about nobles, <a href="2160.html">garrisons</a>, etc.\n')
    outf.write('</ul>\n')
    outf.write('<h2>Limitations / Bugs</h2>\n')
    outf.write('<ul>\n')
    outf.write('<li>Vision / Scry information is not included\n')
    outf.write('Hades and Faery entrances are not represented correctly (Undercity is OK)\n')
    outf.write('Faery map is broken\n')
    outf.write('There is no indication of how old info is (e.g. "this market report is from turn 184")\n')
    outf.write('Mobile things (characters, ships) only included if seen in the last turn\n')
    outf.write('</ul>\n')
    outf.write('</BODY>\n')
    outf.write('</html>\n')
    outf.close()


def write_main_map():
    outf = open('main_map.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>Main Map</TITLE>\n')
    outf.write('<link href="map.css" rel="stylesheet" type="text/css">\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<h3>Olympia Main Map</h3>\n')
    outf.write('<img height="320" width="320" src="main_thumbnail.gif" usemap="#oly"/>\n')
    outf.write('<map name="oly" id="oly">\n')
    outf.write('<area shape="rect" coords="0, 0, 60, 60" href="main_map_leaf_aa00.html"/>\n')
    outf.write('<area shape="rect" coords="60,0,100,60" href="main_map_leaf_aa10.html"/>\n')
    outf.write('<area shape="rect" coords="100,0,140,60" href="main_map_leaf_aa20.html"/>\n')
    outf.write('<area shape="rect" coords="140,0,180,60" href="main_map_leaf_aa30.html"/>\n')
    outf.write('<area shape="rect" coords="180,0,220,60" href="main_map_leaf_aa40.html"/>\n')
    outf.write('<area shape="rect" coords="220,0,260,60" href="main_map_leaf_aa50.html"/>\n')
    outf.write('<area shape="rect" coords="260,0,320,60" href="main_map_leaf_aa60.html"/>\n')
    outf.write('<area shape="rect" coords="0,60,60,100" href="main_map_leaf_an00.html"/>\n')
    outf.write('<area shape="rect" coords="60,60,100,100" href="main_map_leaf_an10.html"/>\n')
    outf.write('<area shape="rect" coords="100,60,140,100" href="main_map_leaf_an20.html"/>\n')
    outf.write('<area shape="rect" coords="140,60,180,100" href="main_map_leaf_an30.html"/>\n')
    outf.write('<area shape="rect" coords="180,60,220,100" href="main_map_leaf_an40.html"/>\n')
    outf.write('<area shape="rect" coords="220,60,260,100" href="main_map_leaf_an50.html"/>\n')
    outf.write('<area shape="rect" coords="260,60,320,100" href="main_map_leaf_an60.html"/>\n')
    outf.write('<area shape="rect" coords="0,100,60,140" href="main_map_leaf_ba00.html"/>\n')
    outf.write('<area shape="rect" coords="60,100,100,140" href="main_map_leaf_ba10.html"/>\n')
    outf.write('<area shape="rect" coords="100,100,140,140" href="main_map_leaf_ba20.html"/>\n')
    outf.write('<area shape="rect" coords="140,100,180,140" href="main_map_leaf_ba30.html"/>\n')
    outf.write('<area shape="rect" coords="180,100,220,140" href="main_map_leaf_ba40.html"/>\n')
    outf.write('<area shape="rect" coords="220,100,260,140" href="main_map_leaf_ba50.html"/>\n')
    outf.write('<area shape="rect" coords="260,100,320,140" href="main_map_leaf_ba60.html"/>\n')
    outf.write('<area shape="rect" coords="0,140,60,180" href="main_map_leaf_bn00.html"/>\n')
    outf.write('<area shape="rect" coords="60,140,100,180" href="main_map_leaf_bn10.html"/>\n')
    outf.write('<area shape="rect" coords="100,140,140,180" href="main_map_leaf_bn20.html"/>\n')
    outf.write('<area shape="rect" coords="140,140,180,180" href="main_map_leaf_bn30.html"/>\n')
    outf.write('<area shape="rect" coords="180,140,220,180" href="main_map_leaf_bn40.html"/>\n')
    outf.write('<area shape="rect" coords="220,140,260,180" href="main_map_leaf_bn50.html"/>\n')
    outf.write('<area shape="rect" coords="260,140,320,180" href="main_map_leaf_bn60.html"/>\n')
    outf.write('<area shape="rect" coords="0,180,60,220" href="main_map_leaf_ca00.html"/>\n')
    outf.write('<area shape="rect" coords="60,180,100,220" href="main_map_leaf_ca10.html"/>\n')
    outf.write('<area shape="rect" coords="100,180,140,220" href="main_map_leaf_ca20.html"/>\n')
    outf.write('<area shape="rect" coords="140,180,180,22" href="main_map_leaf_ca30.html"/>\n')
    outf.write('<area shape="rect" coords="180,180,220,220" href="main_map_leaf_ca40.html"/>\n')
    outf.write('<area shape="rect" coords="220,180,260,220" href="main_map_leaf_ca50.html"/>\n')
    outf.write('<area shape="rect" coords="260,180,320,220" href="main_map_leaf_ca60.html"/>\n')
    outf.write('<area shape="rect" coords="0,220,60,260" href="main_map_leaf_cn00.html"/>\n')
    outf.write('<area shape="rect" coords="60,220,100,260" href="main_map_leaf_cn10.html"/>\n')
    outf.write('<area shape="rect" coords="100,220,140,260" href="main_map_leaf_cn20.html"/>\n')
    outf.write('<area shape="rect" coords="140,220,180,260" href="main_map_leaf_cn30.html"/>\n')
    outf.write('<area shape="rect" coords="180,220,220,260" href="main_map_leaf_cn40.html"/>\n')
    outf.write('<area shape="rect" coords="220,220,260,260" href="main_map_leaf_cn50.html"/>\n')
    outf.write('<area shape="rect" coords="260,220,320,260" href="main_map_leaf_cn60.html"/>\n')
    outf.write('<area shape="rect" coords="0,260,60,320" href="main_map_leaf_da00.html"/>\n')
    outf.write('<area shape="rect" coords="60,260,100,320" href="main_map_leaf_da10.html"/>\n')
    outf.write('<area shape="rect" coords="100,260,140,320" href="main_map_leaf_da20.html"/>\n')
    outf.write('<area shape="rect" coords="140,260,180,320" href="main_map_leaf_da30.html"/>\n')
    outf.write('<area shape="rect" coords="180,260,220,320" href="main_map_leaf_da40.html"/>\n')
    outf.write('<area shape="rect" coords="220,260,260,320" href="main_map_leaf_da50.html"/>\n')
    outf.write('<area shape="rect" coords="260,260,320,320" href="main_map_leaf_da60.html"/>\n')
    outf.write('</map>\n')
    outf.write('</BODY>\n')
    outf.write('</html>\n')
    outf.close()


def write_main_map_leaves(data, castle_chain):
    for outery in range (0, 7):
        startingpoint = 10000 + (outery * 1000)
        for outerx in range (0, 7):
            currentpoint = startingpoint + (outerx * 10)
            outf = open('main_map_leaf_' + u.to_oid(currentpoint) + '.html', 'w')
            outf.write('<HTML>\n')
            outf.write('<HEAD>\n')
            outf.write('<TITLE>Main Map Leaf {}</TITLE>\n'.format(to_oid(currentpoint)))
            outf.write('<link href="map.css" rel="stylesheet" type="text/css">\n')
            outf.write('</HEAD>\n')
            outf.write('<BODY>\n')
            outf.write('<a href="main_map.html">Return to Main Map</a>')
            outf.write('<TABLE>\n')
            topnav = False
            botnav = False
            leftnav = False
            rightnav = False
            upperleftnav = False
            upperrightnav = False
            lowerleftnav = False
            lowerrightnav = False
            if currentpoint > 10099:
                topnav = True
            if currentpoint < 16000:
                botnav = True
            y1 = (currentpoint - 10000) % 100
            if (y1 % 10) > 1 or (y1 / 10) > 0:
                leftnav = True
                if topnav:
                    upperleftnav = True
                if botnav:
                    lowerleftnav = True
            if (y1 % 10) > 1 or (y1 / 10) < 6:
                rightnav = True
                if topnav:
                    upperrightnav = True
                if botnav:
                    lowerrightnav = True
            if topnav:
                outf.write('<tr>\n')
                if upperleftnav:
                    outf.write('<td class="corner">')
                    outf.write('<a href="main_map_leaf_{}.html">'.format(to_oid(currentpoint - 1010)))
                    outf.write('<img src="grey.gif" width="20" height="20">')
                    outf.write('</a></td>\n')
                outf.write('<td colspan="20" class="top">')
                outf.write('<a href="main_map_leaf_{}.html">'.format(to_oid(currentpoint-1000)))
                outf.write('<img src="grey.gif" width="840" height="20">')
                outf.write('</a></td>\n')
                if upperrightnav:
                    outf.write('<td class="corner">')
                    outf.write('<a href="main_map_leaf_{}.html">'.format(to_oid(currentpoint - 990)))
                    outf.write('<img src="grey.gif" width="20" height="20">')
                    outf.write('</a></td>\n')
                outf.write('</tr>\n')
            for x in range(0, 20):
                outf.write('<tr>\n')
                for y in range(0, 20):
                    if x == 0 and y == 0:
                        if leftnav:
                            outf.write('<td rowspan="20" class="left">')
                            outf.write('<a href="main_map_leaf_{}.html">'.format(to_oid(currentpoint - 10)))
                            outf.write('<img src="grey.gif" width="20" height="840">')
                            outf.write('</a></td>\n')
                    cell = str(currentpoint + (x * 100) + y)
                    try:
                        loc_rec = data[cell]
                        outf.write('<td id ="{}" class="{}"'.format(to_oid(cell),
                                                                     u.return_type(loc_rec['firstline'][0])))

                        if barrier(loc_rec):
                            outf.write(' style="border: 2px solid purple" ')
                        else:
                            nbr_men, enemy_found, ships_found = count_stuff(loc_rec, data)
                            if nbr_men > 50:
                                outf.write(' style="border: 2px solid red" ')
                            elif ships_found:
                                outf.write(' style="border: 2px solid yellow" ')
                            elif enemy_found:
                                outf.write(' style="outline: 2px solid orange" ')
                        outf.write('>')
                        if 'LO' in loc_rec:
                            if 'lc' in loc_rec['LO']:
                                if int(loc_rec['LO']['lc'][0]) > 0:
                                    outf.write('<b>')
                        outf.write('{}'.format(anchor(to_oid(cell))))
                        if 'LO' in loc_rec:
                            if 'lc' in loc_rec['LO']:
                                if int(loc_rec['LO']['lc'][0]) > 0:
                                    outf.write('</b>')
                        if 'LI' in loc_rec:
                            if 'hl' in loc_rec['LI']:
                                here_list = loc_rec['LI']['hl']
                                for garr in here_list:
                                    garr_rec = data[garr]
                                    if u.return_type(garr_rec['firstline'][0]) == 'garrison':
                                        if 'MI' in garr_rec:
                                            if 'gc' in garr_rec['MI']:
                                                castle_id = garr_rec['MI']['gc'][0]
                                                outf.write('{}'.format(castle_chain[castle_id][0]))
                        if 'LI' in loc_rec:
                            if 'hl' in loc_rec['LI']:
                                if len(loc_rec['LI']['hl']) > 0:
                                    loc1 = ''
                                    loc2 = ''
                                    city = ''
                                    graveyard = ''
                                    count = int(0)
                                    here_list = loc_rec['LI']['hl']
                                    for here in here_list:
                                        if int(here) >= 56760 and int(here) <= 78999:
                                            count = count + 1
                                            here_rec = data[here]
                                            if u.return_type(here_rec['firstline'][0]) != 'city':
                                                city = here_rec
                                            elif u.return_type(here_rec['firstline'][0]) == 'graveyard':
                                                graveyard = here_rec
                                            elif loc1 == '' and u.return_kind(here_rec['firstline'][0]) == 'loc':
                                                loc1 = here_rec
                                            elif loc2 == '' and u.return_kind(here_rec['firstline'][0]) == 'loc':
                                                loc2 = here_rec
                                    if city != '':
                                        if loc2 == '':
                                            loc2 = loc1
                                        loc1 = city
                                    if graveyard != '':
                                        if loc1 == '':
                                            if loc2 == '':
                                                loc2 = loc1
                                            loc1 = graveyard
                                        else:
                                            if loc2 == '':
                                                loc2 = graveyard
                                    if count > 2:
                                        outf.write('<br />many')
                                    else:
                                        if loc2 != '':
                                            if u.return_type(loc2['firstline'][0]) == 'city' or u.return_type(loc2['firstline'][0]) == 'graveyard':
                                                outf.write('<br />')
                                                outf.write('{}'.format(anchor2(to_oid(u.return_unitid(loc2['firstline'][0])),
                                                                               u.return_short_type(loc2['firstline'][0]))))
                                            else:
                                                outf.write('<br />')
                                                if 'LO' in loc2:
                                                    if 'hi' in loc2['LO']:
                                                        if loc2['LO']['hi'][0] == '1':
                                                            outf.write('<i>')
                                                outf.write(u.return_short_type(loc2['firstline'][0]))
                                                if 'LO' in loc2:
                                                    if 'hi' in loc2['LO']:
                                                        if loc2['LO']['hi'][0] == '1':
                                                            outf.write('</i>')
                                        else:
                                            outf.write('<br />&nbsp;')
                                    if loc1 != '':
                                        if u.return_type(loc1['firstline'][0]) == 'city' or u.return_type(loc1['firstline'][0]) == 'graveyard':
                                            outf.write('<br />')
                                            outf.write('{}'.format(anchor2(to_oid(u.return_unitid(loc1['firstline'][0])),
                                                                           u.return_short_type(loc1['firstline'][0]))))
                                        else:
                                            outf.write('<br />')
                                            if 'LO' in loc1:
                                                if 'hi' in loc1['LO']:
                                                    if loc1['LO']['hi'][0] == '1':
                                                        outf.write('<i>')
                                            outf.write(u.return_short_type(loc1['firstline'][0]))
                                            if 'LO' in loc1:
                                                if 'hi' in loc1['LO']:
                                                    if loc1['LO']['hi'][0] == '1':
                                                        outf.write('</i>')
                                    else:
                                        outf.write('<br />&nbsp;')
                        outf.write('</td>\n')
                    except KeyError:
                        outf.write('<td id="{}" class="x-sea">{}</td>\n'.format(to_oid(cell), to_oid(cell)))
                    if x == 0 and y == 19:
                        if rightnav:
                            outf.write('<td rowspan="20" class="right">')
                            outf.write('<a href="main_map_leaf_{}.html">'.format(to_oid(currentpoint + 10)))
                            outf.write('<img src="grey.gif" width="20" height="840">')
                            outf.write('</a></td>\n')
                outf.write('</tr>\n')
            if botnav:
                outf.write('<tr>\n')
                if lowerleftnav:
                    outf.write('<td class="corner">')
                    outf.write('<a href="main_map_leaf_{}.html">'.format(to_oid(currentpoint + 990)))
                    outf.write('<img src="grey.gif" width="20" height="20">')
                    outf.write('</a></td>\n')
                outf.write('<td colspan="20" class="bottom">')
                outf.write('<a href="main_map_leaf_{}.html">'.format(to_oid(currentpoint + 1000)))
                outf.write('<img src="grey.gif" width="840" height="20">')
                outf.write('</a></td>\n')
                if lowerrightnav:
                    outf.write('<td class="corner">')
                    outf.write('<a href="main_map_leaf_{}.html">'.format(to_oid(currentpoint + 1010)))
                    outf.write('<img src="grey.gif" width="20" height="20">')
                    outf.write('</a></td>\n')
                outf.write('</tr>\n')
            outf.write('</TABLE>\n')
            outf.write('<a href="main_map.html">Return to Main Map</a>')
            outf.write('</BODY>\n')
            outf.write('</HTML>')
            outf.close()


def barrier(v):
    ret = False
    if 'LO' in v:
        if 'ba' in v['LO']:
            if v['LO']['ba'][0] == '1':
                ret = True
    return ret


def count_stuff(v, data):
    nbr_men = int(0)
    enemy_found = False
    ships_found = False
    seen_here_list = []
    level = 0
    k = u.return_unitid(v['firstline'][0])
    seen_here_list = u.chase_structure(k, data, level, seen_here_list)
    list_length = len(seen_here_list)
    if list_length > 1:
        for un in seen_here_list[1:]:
            unit = data[un[0]]
            if 'char' in u.return_kind(unit['firstline'][0]):
                if'il' in unit:
                    item_list = unit['il']
                    iterations = int(len(item_list) / 2)
                    for itemz in range(0, iterations):
                        itemz_rec = data[item_list[itemz*2]]
                        if 'IT' in itemz_rec:
                            if 'pr' in itemz_rec['IT']:
                                if itemz_rec['IT']['pr'][0] == '1':
                                    nbr_men = nbr_men + int(item_list[(itemz*2) + 1])
                if 'CH' in unit:
                    if 'lo' in unit['CH']:
                        if unit['CH']['lo'][0] == '100':
                            enemy_found = True
            elif u.return_kind(unit['firstline'][0]) == 'ship':
                ships_found = True
    return nbr_men, enemy_found, ships_found
