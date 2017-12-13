#!/usr/bin/python

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor
from olymap.utilities import anchor2
import olypy.details as details
import pathlib
from pngcanvas import *
import math


def write_index(outdir, instance, inst_dict):
    outf = open(pathlib.Path(outdir).joinpath('index.html'), 'w')
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
    dimensions = inst_dict[instance]
    for world in dimensions:
        outf.write('<li><a href="{}_map.html">{}</a></li>'.format(world,
                                                                  world.title()))
    outf.write('</ul>')
    outf.write('</th>')
    outf.write('<th>')
    outf.write('<ul>Reports<br>')
    outf.write('<li><a href="master_castle_report.html">Castles</a></li>')
    outf.write('<li><a href="master_character_report.html">Characters</a></li>')
    outf.write('<li><a href="master_city_report.html">Citys</a></li>')
    outf.write('<li><a href="master_faeryhill_report.html">Faery Hills</a></li>')
    outf.write('<li><a href="master_gate_report.html">Gates</a></li>')
    outf.write('<li><a href="master_graveyard_report.html">Graveyards</a></li>')
    outf.write('<li><a href="master_healing_potion_report.html">Healing Potions</a></li>')
    outf.write('<li><a href="master_item_report.html">Items</a></li>')
    outf.write('<li><a href="master_location_report.html">Locations</a></li>')
    outf.write('<li><a href="master_orb_report.html">Orbs</a></li>')
    outf.write('<li><a href="master_player_report.html">Players</a></li>')
    outf.write('<li><a href="master_projected_cast_report.html">Projected Casts</a></li>')
    outf.write('<li><a href="master_road_report.html">Roads</a></li>')
    outf.write('<li><a href="master_ship_report.html">Ships</a></li>')
    outf.write('<li><a href="master_skill_xref_report.html">Skills Xref</a></li>')
    outf.write('<li><a href="master_trade_report.html">Trades</a></li>')
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
    if instance == "g4":
        outf.write('<h2>Intro</h2>\n')
        outf.write('This is the map of Olympia, including S.O.C.R.A.T.E.S. and Lords of the Crown data, '
                   'as of the end of turn 192.<p>')
        outf.write('Mobile things (characters, ships) are present in the map only if they were seen in '
                   'turn 192.\n')
        outf.write('<h2>Features</h2>\n')
        outf.write('<ul>\n')
        outf.write('<li>Concentrations of men indicated by red border (here is a <a href="main_map_leaf_an40.html">'
                   'combat zone</a>)\n')
        outf.write('<li>Ships indicated by yellow border if troop count is low\n')
        outf.write('<li>Barriers indicated by brown border (e.g. ar54, aq52)\n')
        outf.write('<li>Garrison/castle allegiance is indicated by the @ after the province ID '
                   '(<a href="main_map_leaf_ba10.html">Grinter</a> is a good example)\n')
        outf.write('<li>Keep clicking down, there is a lot of info about nobles, <a href="2160.html">garrisons</a>, '
                   'etc.\n')
        outf.write('</ul>\n')
        outf.write('<h2>Limitations / Bugs</h2>\n')
        outf.write('<ul>\n')
        outf.write('<li>Vision / Scry information is not included\n')
        outf.write('<li>Hades and Faery entrances are not represented correctly (Undercity is OK)\n')
        outf.write('<li>Faery map is broken\n')
        outf.write('<li>There is no indication of how old info is (e.g. "this market report is from turn 184")\n')
        outf.write('<li>Mobile things (characters, ships) only included if seen in the last turn\n')
        outf.write('</ul>\n')
    outf.write('</BODY>\n')
    outf.write('</html>\n')
    outf.close()


def write_top_map(outdir, upperleft, height, width, prefix):
    outf = open(pathlib.Path(outdir).joinpath(prefix + '_map.html'), 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>{} Map</TITLE>\n'.format(prefix.capitalize()))
    outf.write('<link href="map.css" rel="stylesheet" type="text/css">\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<h3>Olympia {} Map</h3>\n'.format(prefix.capitalize()))
    if height <= 50 and width <= 50:
        multiple = 12
    elif height <= 80 and width <= 80:
        multiple = 7
    else:
        multiple = 5
    rem_height = height % 10
    if rem_height > 0 and height >= 10:
        iheight = (multiple * (height - 10)) + (rem_height * multiple)
    else:
        iheight = (multiple * height)
    rem_width = width % 10
    if rem_width > 0 and width >= 10:
        iwidth = (multiple * (width - 10)) + (rem_width * multiple)
    else:
        iwidth = (multiple * width)
    outf.write('<img height="{}" width="{}" src="{}_thumbnail.png" usemap="#oly"/>\n'.format(iheight,
                                                                                             iwidth,
                                                                                             prefix))
    outf.write('<map name="oly" id="oly">\n')
    x_max = math.ceil(width / 10)
    y_max = math.ceil(height / 10)
    if x_max == 1:
        lwidth = width * multiple
    else:
        lwidth = int(iwidth / (x_max - 1))
    if y_max == 1:
        lheight = height * multiple
    else:
        lheight = int(iheight / (y_max - 1))
    tp = 0
    bt = lheight
    for outery in range(0, y_max):
        if outery < y_max - 1 or (outery == y_max - 1 and rem_height > 0) or y_max == 1:
            startingpoint = upperleft + (outery * 1000)
            lt = 0
            rt = lwidth
            if outery == 0:
                lt = 0
            elif outery == 1:
                tp = lheight
                bt = bt + lheight
            elif outery == y_max - 2:
                tp = tp + lheight
                bt = bt + lheight
            elif outery == y_max - 1:
                bt = bt + (rem_height * multiple)
            else:
                tp = tp + lheight
                bt = bt + lheight
            for outerx in range(0, x_max):
                if outerx < x_max - 1 or (outerx == x_max - 1 and rem_width > 0) or x_max == 1:
                    currentpoint = startingpoint + (outerx * 10)
                    if outerx == 0 and x_max != 1:
                        pass
                    elif outerx == 1:
                        lt = lwidth
                        rt = rt + lwidth
                    elif outerx == x_max - 2:
                        lt = lt + lwidth
                        rt = rt + lwidth
                    elif outerx == x_max - 1 or x_max == 1:
                        rt = rt + (rem_width * multiple)
                    else:
                        lt = lt + lwidth
                        rt = rt + lwidth
                    outf.write('<area shape="rect" '
                               'coords="{}, {}, {}, {}" href="{}_map_leaf_{}.html"/>\n'.format(lt,
                                                                                               tp,
                                                                                               rt,
                                                                                               bt,
                                                                                               prefix,
                                                                                               to_oid(currentpoint)))
    outf.write('</map>\n')
    outf.write('</BODY>\n')
    outf.write('</html>\n')
    outf.close()


def write_map_leaves(data, castle_chain, outdir, upperleft, height, width, prefix, instance):
    x_max = math.ceil(width / 10)
    y_max = math.ceil(height / 10)
    rem_height = height % 20
    rem_width = width % 20
    for outery in range(0, y_max):
        if outery < y_max - 1 or y_max == 1:
            startingpoint = upperleft + (outery * 1000)
            for outerx in range(0, x_max):
                if outerx < x_max - 1 or x_max == 1:
                    currentpoint = startingpoint + (outerx * 10)
                    outf = open(pathlib.Path(outdir).joinpath(prefix +
                                                              '_map_leaf_'
                                                              + u.to_oid(currentpoint) +
                                                              '.html'), 'w')
                    write_leaf_header(currentpoint, outdir, prefix, outf)
                    outf.write('<TABLE>\n')
                    topnav = False
                    botnav = False
                    leftnav = False
                    rightnav = False
                    upperleftnav = False
                    upperrightnav = False
                    lowerleftnav = False
                    lowerrightnav = False
                    if currentpoint > upperleft + 99:
                        topnav = True
                    if rem_height > 0:
                        if currentpoint < upperleft + ((x_max - 2) * 1000):
                            botnav = True
                    else:
                        if currentpoint < upperleft + ((x_max - 2) * 1000):
                            botnav = True
                    y1 = (currentpoint - upperleft) % 100
                    if (y1 % 10) > 1 or (y1 / 10) > 0:
                        leftnav = True
                        if topnav:
                            upperleftnav = True
                        if botnav:
                            lowerleftnav = True
                    if rem_width > 0:
                        if (y1 % 10) > 1 or (y1 / 10) < (y_max - 2):
                            rightnav = True
                    else:
                        if (y1 % 10) > 1 or (y1 / 10) < (y_max - 2):
                            rightnav = True
                    if rightnav:
                        if topnav:
                            upperrightnav = True
                        if botnav:
                            lowerrightnav = True
                    if topnav:
                        generate_topnav(currentpoint, outf, prefix, upperleftnav, upperrightnav)
                    for y in range(0, 20):
                        if (rem_height == 0 or outery <= y_max - 3) or \
                            (outery == y_max - 2 and y < rem_height + 10) or \
                            (y_max == 1 and y < rem_height):
                            outf.write('<tr>\n')
                            for x in range(0, 20):
                                if (rem_width == 0 or outerx <= x_max - 3) or \
                                    (outerx == x_max - 2 and x < rem_width + 10) or \
                                    (x_max == 1 and x < rem_width):
                                    write_cell(castle_chain,
                                               currentpoint,
                                               data,
                                               leftnav,
                                               outf,
                                               prefix,
                                               rightnav,
                                               x,
                                               y,
                                               rem_width,
                                               rem_height,
                                               instance)
                            outf.write('</tr>\n')
                    if botnav:
                        generate_botnav(currentpoint, lowerleftnav, lowerrightnav, outf, prefix)
                    outf.write('</TABLE>\n')
                    outf.write('<a href="{}_map.html">Return to {} Map</a>'.format(prefix,
                                                                                   prefix.capitalize()))
                    outf.write('</BODY>\n')
                    outf.write('</HTML>')
                    outf.close()


def write_cell(castle_chain, currentpoint, data, leftnav, outf, prefix, rightnav, x, y, rem_width, rem_height, instance):
    if x == 0 and y == 0:
        if leftnav:
            outf.write('<td rowspan="20" class="left">')
            outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                               to_oid(currentpoint - 10)))
            outf.write('<img src="grey.gif" width="20" height="840">')
            outf.write('</a></td>\n')
    cell = str(currentpoint + (x + (y * 100)))
    try:
        loc_rec = data[cell]
        outf.write('<td id ="{}" class="{}"'.format(to_oid(cell),
                                                    u.return_type(loc_rec)))

        generate_border(data, loc_rec, outf, instance)
        outf.write('>')
        generate_cell_contents(castle_chain, cell, data, loc_rec, outf)
        outf.write('</td>\n')
    except KeyError:
        outf.write('<td id="{}" class="x-sea">{}</td>\n'.format(to_oid(cell), to_oid(cell)))
    if x == 19 and y == 0:
        if rightnav:
            outf.write('<td rowspan="20" class="right">')
            outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                               to_oid(currentpoint + 10)))
            outf.write('<img src="grey.gif" width="20" height="840">')
            outf.write('</a></td>\n')


def write_leaf_header(currentpoint, outdir, prefix, outf):
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    outf.write('<TITLE>{} Map Leaf {}</TITLE>\n'.format(prefix.capitalize(),
                                                        to_oid(currentpoint)))
    outf.write('<link href="map.css" rel="stylesheet" type="text/css">\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    outf.write('<a href="{}_map.html">Return to {} Map</a>'.format(prefix,
                                                                   prefix.capitalize()))


def generate_botnav(currentpoint, lowerleftnav, lowerrightnav, outf, prefix):
    outf.write('<tr>\n')
    if lowerleftnav:
        outf.write('<td class="corner">')
        outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                           to_oid(currentpoint + 990)))
        outf.write('<img src="grey.gif" width="20" height="20">')
        outf.write('</a></td>\n')
    outf.write('<td colspan="20" class="bottom">')
    outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                       to_oid(currentpoint + 1000)))
    outf.write('<img src="grey.gif" width="840" height="20">')
    outf.write('</a></td>\n')
    if lowerrightnav:
        outf.write('<td class="corner">')
        outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                           to_oid(currentpoint + 1010)))
        outf.write('<img src="grey.gif" width="20" height="20">')
        outf.write('</a></td>\n')
    outf.write('</tr>\n')


def generate_topnav(currentpoint, outf, prefix, upperleftnav, upperrightnav):
    outf.write('<tr>\n')
    if upperleftnav:
        outf.write('<td class="corner">')
        outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                           to_oid(currentpoint - 1010)))
        outf.write('<img src="grey.gif" width="20" height="20">')
        outf.write('</a></td>\n')
    outf.write('<td colspan="20" class="top">')
    outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                       to_oid(currentpoint - 1000)))
    outf.write('<img src="grey.gif" width="840" height="20">')
    outf.write('</a></td>\n')
    if upperrightnav:
        outf.write('<td class="corner">')
        outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                           to_oid(currentpoint - 990)))
        outf.write('<img src="grey.gif" width="20" height="20">')
        outf.write('</a></td>\n')
    outf.write('</tr>\n')


def generate_cell_contents(castle_chain, cell, data, loc_rec, outf):
    if 'LO' in loc_rec and 'lc' in loc_rec['LO']:
        if loc_rec['LO']['lc'][0] != '0':
            outf.write('<b>')
    outf.write('{}'.format(anchor(to_oid(cell))))
    if 'LO' in loc_rec and 'lc' in loc_rec['LO']:
        if loc_rec['LO']['lc'][0] != '0':
            outf.write('</b>')
    if 'LI' in loc_rec and 'hl' in loc_rec['LI']:
        here_list = loc_rec['LI']['hl']
        for garr in here_list:
            garr_rec = data[garr]
            if u.return_type(garr_rec) == 'garrison':
                if 'MI' in garr_rec:
                    if 'gc' in garr_rec['MI']:
                        castle_id = garr_rec['MI']['gc'][0]
                        outf.write('{}'.format(castle_chain[castle_id][0]))
    loc1 = ''
    loc2 = ''
    city = ''
    graveyard = ''
    road_or_gate = ''
    if 'LI' in loc_rec and 'hl' in loc_rec['LI']:
        if len(loc_rec['LI']['hl']) > 0:
            count = int(0)
            here_list = loc_rec['LI']['hl']
            for here in here_list:
                # if 56760 <= int(here) <= 78999:
                here_rec = data[here]
                if u.return_type(here_rec) in details.subloc_kinds or u.is_road_or_gate(here_rec):
                    count = count + 1
                    if u.return_type(here_rec) == 'city':
                        city = here_rec
                    elif u.return_type(here_rec) == 'graveyard':
                        graveyard = here_rec
                    elif u.is_road_or_gate(here_rec):
                        road_or_gate = here_rec
                    elif loc1 == '' and u.return_kind(here_rec) == 'loc':
                        loc1 = here_rec
                    elif loc2 == '' and u.return_kind(here_rec) == 'loc':
                        loc2 = here_rec
    if 'SL' in loc_rec:
        if 'lt' in loc_rec['SL']:
            here_rec = data[loc_rec['SL']['lt'][0]]
            if loc1 == '':
                loc1 = here_rec
            elif loc2 == '':
                loc2 = here_rec
        if 'lf' in loc_rec['SL']:
            here_rec = data[loc_rec['SL']['lf'][0]]
            if loc1 == '':
                loc1 = here_rec
            elif loc2 == '':
                loc2 = here_rec
    if loc1 != '' or loc2 != '' or city != '' or graveyard != ''or road_or_gate != '':
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
        if road_or_gate != '':
            if loc1 == '':
                if loc2 == '':
                    loc2 = loc1
                loc1 = road_or_gate
            else:
                if loc2 == '':
                    loc2 = road_or_gate
        if count > 2:
            outf.write('<br />many')
        else:
            if loc2 != '':
                if u.return_type(loc2) == 'city' or u.return_type(loc2) == 'graveyard' or u.return_type(loc2) == 'faery hill':
                    outf.write('<br />')
                    outf.write('{}'.format(anchor2(to_oid(u.return_unitid(loc2)),
                                                   u.return_short_type(loc2))))
                else:
                    outf.write('<br />')
                    if 'LO' in loc2 and 'hi' in loc2['LO']:
                        if loc2['LO']['hi'][0] == '1':
                            outf.write('<i>')
                    outf.write(u.return_short_type(loc2))
                    if 'LO' in loc2:
                        if 'hi' in loc2['LO'] and loc2['LO']['hi'][0] == '1':
                            outf.write('</i>')
            else:
                outf.write('<br />&nbsp;')
        if loc1 != '':
            if u.return_type(loc1) == 'city' or u.return_type(loc1) == 'graveyard' or u.return_type(loc1) == 'faery hill':
                outf.write('<br />')
                outf.write('{}'.format(anchor2(to_oid(u.return_unitid(loc1)),
                                               u.return_short_type(loc1))))
            else:
                outf.write('<br />')
                if 'LO' in loc1 and 'hi' in loc1['LO']:
                    if loc1['LO']['hi'][0] == '1':
                        outf.write('<i>')
                outf.write(u.return_short_type(loc1))
                if 'LO' in loc1 and 'hi' in loc1['LO']:
                    if loc1['LO']['hi'][0] == '1':
                        outf.write('</i>')
        else:
            outf.write('<br />&nbsp;')


def generate_border(data, loc_rec, outf, instance):
    if barrier(loc_rec):
        outf.write(' style="border: 2px solid blue" ')
    else:
        nbr_men, enemy_found, ships_found = count_stuff(loc_rec, data)
        if nbr_men > 50:
            outf.write(' style="border: 2px solid red" ')
        elif ships_found:
            outf.write(' style="border: 2px solid yellow" ')
        elif enemy_found:
            if instance not in {'g2', 'qa'}:
                outf.write(' style="outline: 2px solid orange" ')


def barrier(v):
    ret = False
    if 'LO' in v:
        if 'ba' in v['LO'] and v['LO']['ba'][0] != '0':
            ret = True
    return ret


def count_stuff(v, data):
    nbr_men = int(0)
    enemy_found = False
    ships_found = False
    seen_here_list = []
    level = 0
    k = u.return_unitid(v)
    seen_here_list = u.chase_structure(k, data, level, seen_here_list)
    list_length = len(seen_here_list)
    if list_length > 1:
        for un in seen_here_list[1:]:
            unit = data[un[0]]
            if 'char' in u.return_kind(unit):
                if'il' in unit:
                    item_list = unit['il']
                    iterations = int(len(item_list) / 2)
                    for itemz in range(0, iterations):
                        itemz_rec = data[item_list[itemz*2]]
                        if 'IT' in itemz_rec and 'pr' in itemz_rec['IT']:
                            if itemz_rec['IT']['pr'][0] == '1':
                                nbr_men = nbr_men + int(item_list[(itemz*2) + 1])
                if 'CH' in unit:
                    if 'lo' in unit['CH'] and unit['CH']['lo'][0] == '100':
                        enemy_found = True
            elif u.return_kind(unit) == 'ship':
                ships_found = True
    return nbr_men, enemy_found, ships_found


def write_bitmap(outdir, data, upperleft, height, width, prefix):
    BUFSIZE = 8*1024
    color_pallette = {'ocean': (0x00, 0xff, 0xff, 0xff),
                      'plain': (0x90, 0xee, 0x90, 0xff),
                      'forest': (0x32, 0xcd, 0x32, 0xff),
                      'swamp': (0xff, 0x00, 0xff, 0xff),
                      'mountain': (0x80, 0x80, 0x80, 0xff),
                      'desert': (0xff, 0xff, 0x00, 0xff),
                      'underground': (0xff, 0xa5, 0x00, 0xff),
                      'cloud': (0xad, 0xd8, 0xe6, 0xff)}
    outf = open(pathlib.Path(outdir).joinpath(prefix + '_thumbnail.png'), 'wb')
    map = PNGCanvas(width, height, color=(0xff, 0, 0, 0xff))
    for x in range(0, width):
        for y in range(0, height):
            curr_loc = upperleft + (y * 100) + (x * 1)
            try:
                province_box = data[str(curr_loc)]
                try:
                    color = color_pallette[u.return_type(province_box)]
                    map.point(x, y, color)
                except KeyError:
                    print('missing color for: {}'.format(u.return_type(province_box)))
            except KeyError:
                # print('missing box record for: {}'.format(curr_loc))
                pass
    outf.write(map.dump())
    outf.close()
