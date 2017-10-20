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

    chains = resolve_chains(data)
    write_box_pages(data, chains)
    write_reports(data, chains)
    write_maps(data, chains)


def resolve_chains(data):
    print('Making chains')
    chains = {}
    chains['pledges'] = u.resolve_all_pledges(data)
    chains['prisoners'] = u.resolve_all_prisoners(data)
    chains['hidden'] = u.resolve_hidden_locs(data)
    chains['storms'] = u.resolve_bound_storms(data)
    chains['teaches'] = u.resolve_teaches(data)
    chains['child_skills'] = u.resolve_child_skills(data)
    chains['skills_knowns'] = u.resolve_skills_known(data)
    chains['garrisons'] = u.resolve_garrisons(data)
    chains['trades'] = u.resolve_trades(data)
    chains['castles'] = u.resolve_castles(data)
    return chains


def write_box_pages(data, chains):
    print('Writing box pages')
    for k, v in data.items():
        fl = v['firstline'][0]
        if u.return_kind(fl) == "loc":
            loc.write_loc_html(v, k, data, chains['hidden'], chains['garrisons'], chains['trades'])
        elif u.return_kind(fl) == "char":
            char.write_char_html(v, k, data, chains['pledges'], chains['prisoners'])
        elif u.return_kind(fl) == "player":
            player.write_player_html(v, k, data)
        elif u.return_kind(fl) == "item":
            itm.write_item_html(v, k, data, chains['trades'])
        elif u.return_kind(fl) == "ship":
            ship.write_ship_html(v, k, data)
        elif u.return_kind(fl) == "skill":
            skill.write_skill_html(v, k, data, chains['teaches'], chains['child_skills'], chains['skills_knowns'])
            pass
        elif u.return_kind(fl) == "storm":
            storm.write_storm_html(v, k, data, chains['storms'])


def write_reports(data, chains):
    print('Writing reports')
    reports.ship_report(data)
    reports.player_report(data)
    reports.item_report(data, chains['trades'])
    reports.healing_potion_report(data)
    reports.orb_report(data)
    reports.projected_cast_potion_report(data)
    reports.location_report(data)
    reports.skill_xref_report(data, chains['teaches'])
    reports.trade_report(data, chains['trades'])


def write_maps(data, chains):
    print('Writing Maps')
    maps.write_index()
    maps.write_main_map()
    maps.write_main_map_leaves(data, chains['castles'])
