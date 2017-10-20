#!/usr/bin/python
#
# Given a game lib, generate HTML map for all components
#

import os

import olypy.oio as oio
import olymap.utilities as u
import olymap.ship as ship
import olymap.char as char
import olymap.loc as loc
import olymap.item as itm
import olymap.storm as storm
import olymap.player as player
import olymap.skill as skill
import olymap.reports as reports
import olymap.maps as maps


def make_map(inlib):
    if os.path.isdir(inlib):
        data = oio.read_lib(inlib)
    else:
        raise ValueError('Must specify the name of the lib directory')

    print('Loading common stuff')
    pledge_chain = u.resolve_all_pledges(data)
    prisoner_chain = u.resolve_all_prisoners(data)
    hidden_chain = u.resolve_hidden_locs(data)
    storm_chain = u.resolve_bound_storms(data)
    teaches_chain = u.resolve_teaches(data)
    child_skills_chain = u.resolve_child_skills(data)
    skills_known_chain = u.resolve_skills_known(data)
    garrisons_chain = u.resolve_garrisons(data)
    trade_chain = u.resolve_trades(data)
    castle_chain = u.resolve_castles(data)
    print('Writing box pages')
    for k, v in data.items():
        # if int(k) < 300:
        #     continue
        fl = v['firstline'][0]
        if u.return_kind(fl) == "loc":
            # generate location page
            loc.write_loc_html(v, k, data, hidden_chain, garrisons_chain, trade_chain)
        elif u.return_kind(fl) == "char":
            # generate char page
            char.write_char_html(v, k, data, pledge_chain, prisoner_chain)
        elif u.return_kind(fl) == "player":
            # generate player page
            player.write_player_html(v, k, data)
        elif u.return_kind(fl) == "item":
            # generate item page
            itm.write_item_html(v, k, data, trade_chain)
        elif u.return_kind(fl) == "ship":
            # generate ship page
            ship.write_ship_html(v, k, data)
        elif u.return_kind(fl) == "skill":
            # generate skill page
            # print('Skill {} {} {}'.format(fl, k, to_oid(k)))
            skill.write_skill_html(v, k, data, teaches_chain, child_skills_chain, skills_known_chain)
            pass
        elif u.return_kind(fl) == "storm":
            # generate storm page
            storm.write_storm_html(v, k, data, storm_chain)
    #
    # write reports
    #
    print('Writing reports')
    reports.ship_report(data)
    reports.player_report(data)
    reports.item_report(data, trade_chain)
    reports.healing_potion_report(data)
    reports.orb_report(data)
    reports.projected_cast_potion_report(data)
    reports.location_report(data)
    reports.skill_xref_report(data, teaches_chain)
    reports.trade_report(data, trade_chain)
    print('Writing Maps')
    maps.write_index()
    maps.write_main_map()
    maps.write_main_map_leaves(data, castle_chain)
