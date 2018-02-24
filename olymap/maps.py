#!/usr/bin/python

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import anchor
from olymap.utilities import anchor2
import olypy.details as details
import pathlib
from pngcanvas import *
import math
from olypy.db import loop_here
from jinja2 import Environment, PackageLoader, select_autoescape


def write_index(outdir, instance, inst_dict):
    dimensions = inst_dict[instance]
    dimensions_list = []
    for world in dimensions:
        dimensions_dict = {'world': world,
                           'title': world.title()}
        dimensions_list.append(dimensions_dict)
    try:
        index_file = open('olymap/{}_index.txt'.format(instance), 'r')
    except:
        print('No index file')
        index_text = None
    else:
        index_text = index_file.read()
    index_dict = {'instance': instance,
                  'instance_title': instance.title(),
                  'file': index_text,
                  'dimensions_list': dimensions_list}
    outf = open(pathlib.Path(outdir).joinpath('index.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('index.html')
    outf.write(template.render(index=index_dict))


def write_top_map(outdir, upperleft, height, width, prefix):
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
    coords_list = []
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
                    coords_entry = {'left': lt,
                                    'top': tp,
                                    'right': rt,
                                    'bottom': bt,
                                    'oid': to_oid(currentpoint)}
                    coords_list.append(coords_entry)
    map_dict = {'prefix': prefix,
                'prefix_title': prefix.title(),
                'height': iheight,
                'width': iwidth,
                'coords_list': coords_list}
    outf = open(pathlib.Path(outdir).joinpath(prefix + '_map.html'), 'w')
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('top_map.html')
    outf.write(template.render(map=map_dict))


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
                    printpoint = currentpoint
                    # print('leaf {} ({})'.format(u.to_oid(printpoint),
                    #                             prefix))
                    outf = open(pathlib.Path(outdir).joinpath(prefix +
                                                              '_map_leaf_'
                                                              + u.to_oid(printpoint) +
                                                              '.html'), 'w')
                    write_leaf_header(printpoint, outdir, prefix, outf)
                    outf.write('<TABLE>\n')
                    topnav = False
                    botnav = False
                    leftnav = False
                    rightnav = False
                    upperleftnav = False
                    upperrightnav = False
                    lowerleftnav = False
                    lowerrightnav = False
                    if currentpoint > upperleft + 99 and height > 20:
                        topnav = True
                    if rem_height > 0:
                        if currentpoint < upperleft + ((y_max - 2) * 1000) and height > 20:
                            botnav = True
                    else:
                        if currentpoint < upperleft + ((y_max - 2) * 1000) and height > 20:
                            botnav = True
                    y1 = (currentpoint - upperleft) % 100
                    if ((y1 % 10) > 1 or (y1 / 10) > 0) and width > 20:
                        leftnav = True
                        if topnav:
                            upperleftnav = True
                        if botnav:
                            lowerleftnav = True
                    if rem_width > 0 and width > 20:
                        if (y1 % 10) > 1 or (y1 / 10) < (x_max - 2):
                            rightnav = True
                    else:
                        if ((y1 % 10) > 1 or (y1 / 10) < (x_max - 2)) and width > 20:
                            rightnav = True
                    if rightnav:
                        if topnav:
                            upperrightnav = True
                        if botnav:
                            lowerrightnav = True
                    if topnav:
                        generate_topnav(currentpoint, outf, prefix,
                                        upperleftnav, upperrightnav)
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
                        generate_botnav(currentpoint, lowerleftnav,
                                        lowerrightnav, outf, prefix)
                    outf.write('</TABLE>\n')
                    outf.write('<a href="{}_map.html">Return to {} Map</a>'.format(prefix,
                                                                                   prefix.capitalize()))
                    outf.write('</BODY>\n')
                    outf.write('</HTML>')
                    outf.close()


def write_cell(castle_chain, currentpoint, data, leftnav, outf, prefix, rightnav, x, y, rem_width, rem_height, instance):
    if x == 0 and y == 0:
        if leftnav:
            printpoint = currentpoint - 10
            outf.write('<td rowspan="20" class="left">')
            outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                               to_oid(printpoint)))
            outf.write('<img src="grey.gif" width="20" height="840">')
            outf.write('</a></td>\n')
    cell = currentpoint + (x + (y * 100))
    printpoint = cell
    try:
        loc_rec = data[str(printpoint)]
    except:
        outf.write('<td id ="{}" class="{}">'.format(to_oid(printpoint),
                                                     'undefined'))
        outf.write('{}'.format(to_oid(printpoint)))
        outf.write('<br>{}'.format('&nbsp;' * 8))
        outf.write('<br>{}'.format('&nbsp;' * 8))
        outf.write('</td>\n')
    else:
        outf.write('<td id ="{}" class="{}"'.format(to_oid(printpoint),
                                                    u.return_type(loc_rec)))
        generate_border(data, loc_rec, outf, instance)
        outf.write('>')
        generate_cell_contents(castle_chain, printpoint, data, loc_rec, outf)
        outf.write('</td>\n')
    # except KeyError:
    #    outf.write('<td id="{}" class="x-sea">{}</td>\n'.format(to_oid(printpoint), to_oid(printpoint)))
    if x == 19 and y == 0:
        if rightnav:
            printpoint = currentpoint + 10
            outf.write('<td rowspan="20" class="right">')
            outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                               to_oid(printpoint)))
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
        printpoint = currentpoint + 990
        outf.write('<td class="corner">')
        outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                           to_oid(printpoint)))
        outf.write('<img src="grey.gif" width="20" height="20">')
        outf.write('</a></td>\n')
    printpoint = currentpoint + 1000
    outf.write('<td colspan="20" class="bottom">')
    outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                       to_oid(printpoint)))
    outf.write('<img src="grey.gif" width="840" height="20">')
    outf.write('</a></td>\n')
    if lowerrightnav:
        printpoint = currentpoint + 1010
        outf.write('<td class="corner">')
        outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                           to_oid(printpoint)))
        outf.write('<img src="grey.gif" width="20" height="20">')
        outf.write('</a></td>\n')
    outf.write('</tr>\n')


def generate_topnav(currentpoint, outf, prefix, upperleftnav, upperrightnav):
    outf.write('<tr>\n')
    if upperleftnav:
        outf.write('<td class="corner">')
        printpoint = currentpoint - 1010
        outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                           to_oid(printpoint)))
        outf.write('<img src="grey.gif" width="20" height="20">')
        outf.write('</a></td>\n')
    outf.write('<td colspan="20" class="top">')
    printpoint = currentpoint - 1000
    outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                       to_oid(printpoint)))
    outf.write('<img src="grey.gif" width="840" height="20">')
    outf.write('</a></td>\n')
    if upperrightnav:
        outf.write('<td class="corner">')
        printpoint = currentpoint - 990
        outf.write('<a href="{}_map_leaf_{}.html">'.format(prefix,
                                                           to_oid(printpoint)))
        outf.write('<img src="grey.gif" width="20" height="20">')
        outf.write('</a></td>\n')
    outf.write('</tr>\n')


def generate_cell_contents(castle_chain, cell, data, loc_rec, outf):
    if 'LO' in loc_rec and 'lc' in loc_rec['LO']:
        if loc_rec['LO']['lc'][0] != '0':
            outf.write('<b>')
    a = to_oid(cell)
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
    count = int(0)
    if 'LI' in loc_rec and 'hl' in loc_rec['LI']:
        if len(loc_rec['LI']['hl']) > 0:
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
            count = count + 1
            if loc1 == '':
                loc1 = here_rec
            elif loc2 == '':
                loc2 = here_rec
        if 'lf' in loc_rec['SL']:
            here_rec = data[loc_rec['SL']['lf'][0]]
            count = count + 1
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
    seen_here_list = loop_here(data, k, False, True)
    list_length = len(seen_here_list)
    if list_length >= 1:
        for un in seen_here_list:
            unit = data[un]
            if 'char' in u.return_kind(unit):
                if'il' in unit:
                    item_list = unit['il']
                    if len(item_list) > 0:
                        for itemz in range(0, len(item_list), 2):
                            itemz_rec = data[item_list[itemz]]
                            if 'IT' in itemz_rec and 'pr' in itemz_rec['IT']:
                                if itemz_rec['IT']['pr'][0] == '1':
                                    if 'an' in itemz_rec['IT']:
                                        if itemz_rec['IT']['an'][0] != '1':
                                            nbr_men = nbr_men + int(item_list[itemz + 1])
                                    else:
                                        nbr_men = nbr_men + int(item_list[itemz + 1])
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
                # print('missing box record for: {} {}'.format(curr_loc,
                #                                              to_oid(curr_loc)))
                pass
    outf.write(map.dump())
    outf.close()
