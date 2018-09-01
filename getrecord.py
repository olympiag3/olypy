#!/usr/bin/python
#
# retrieve specified record from lib
#

import sys
import olypy.oio as oio
from olypy.oid import to_oid, to_int
import olypy.dbck as dbck

import pathlib
from jinja2 import Environment, PackageLoader, select_autoescape
from olymap.loc import build_complete_loc_dict
from olymap.ship import build_complete_ship_dict
from olymap.char import build_complete_char_dict
from olymap.item import build_complete_item_dict
from olymap.skill import build_complete_skill_dict
from olymap.storm import build_complete_storm_dict
from olymap.player import build_complete_player_dict

import olymap.utilities as u
import olymap.reports as reports
from olymap.maps import write_index, write_map_leaves, write_top_map, write_bitmap
from olymap.legacy import create_map_matrix, write_legacy_bitmap, write_legacy_top_map, write_legacy_map_leaves


inlib = sys.argv[1]
data = oio.read_lib(inlib)
dbck.check_db(data, fix=True, checknames=True)
rec_id = ' '
rec_id = input('Enter record id ("0" to exit): ')
while rec_id != '0':
    try:
        rec_id_conv = to_int(rec_id)
        try:
            print(data[rec_id_conv])
        except:
            print('Invalid key')
    except:
        print('Invalid key')
    rec_id = input('Enter record id ("0" to exit): ')
