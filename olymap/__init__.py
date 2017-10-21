#!/usr/bin/python
#
# Given a game lib, generate HTML map for all components
#

import os
import pathlib

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


def make_map(inlib, outdir):
    if os.path.isdir(inlib):
        data = oio.read_lib(inlib)
    else:
        raise ValueError('Must specify the name of the lib directory')

    if outdir == '':
        # non specified sp will go in current directory
        print('No outdir specified')
    else:
        if os.path.isdir(outdir):
            # path specified and exists
            print('Outdir exists: {}'.format(outdir))
        else:
            # path specified but doesn't exist - will create
            pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
            print('Outdir does not exists and created: {}'.format(outdir))

    chains = resolve_chains(data)
    write_box_pages(data, chains, outdir)
    write_reports(data, chains, outdir)
    write_maps(data, chains, outdir)


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


def write_box_pages(data, chains, outdir):
    print('Writing box pages')
    for k, v in data.items():
        if u.return_kind(v) == 'loc':
            loc.write_loc_html(v, k, data, chains['hidden'], chains['garrisons'], chains['trades'], outdir)
        elif u.return_kind(v) == 'char':
            char.write_char_html(v, k, data, chains['pledges'], chains['prisoners'], outdir)
        elif u.return_kind(v) == 'player':
            player.write_player_html(v, k, data, outdir)
        elif u.return_kind(v) == 'item':
            itm.write_item_html(v, k, data, chains['trades'], outdir)
        elif u.return_kind(v) == 'ship':
            ship.write_ship_html(v, k, data, outdir)
        elif u.return_kind(v) == 'skill':
            skill.write_skill_html(v, k, data, chains['teaches'], chains['child_skills'], chains['skills_knowns'], outdir)
        elif u.return_kind(v) == 'storm':
            storm.write_storm_html(v, k, data, chains['storms'], outdir)


def write_reports(data, chains, outdir):
    print('Writing reports')
    reports.ship_report(data, outdir)
    reports.player_report(data, outdir)
    reports.item_report(data, chains['trades'], outdir)
    reports.healing_potion_report(data, outdir)
    reports.orb_report(data, outdir)
    reports.projected_cast_potion_report(data, outdir)
    reports.location_report(data, outdir)
    reports.skill_xref_report(data, chains['teaches'], outdir)
    reports.trade_report(data, chains['trades'], outdir)


def write_maps(data, chains, outdir):
    print('Writing Maps')
    maps.write_index(outdir)
    maps.write_main_map(outdir)
    maps.write_main_map_leaves(data, chains['castles'], outdir)
