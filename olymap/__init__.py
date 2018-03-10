#!/usr/bin/python
#
# Given a game lib, generate HTML map for all components
#

import olypy.oio as oio
from olypy.oid import to_oid
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


env = None


def make_map(inlib, outdir, instance):
    global env
    env = Environment(
        loader=PackageLoader('olymap', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    inst_dict = {'g2': {'main': [10000, 100, 100], 'hades': [24251, 76, 76, 'Y'], 'faery': [20013, 7, 938, 'Y'],
                        'cloudlands': [23184, 5, 5, 'Y'], 'subworld': [39167, 11, 11, 'Y']},
                 'g4': {'main': [10000, 80, 80], 'hades': [24000, 50, 50], 'faery': [18000, 46, 46],
                        'cloudlands': [30000, 5, 5], 'subworld': [32005, 6, 6]},
                 'qa': {'main': [10000, 10, 10], 'hades': [14000, 7, 7], 'faery': [12000, 10, 10]}}
    data = oio.read_lib(inlib)
    dbck.check_db(data, fix=True, checknames=True)
    print('Creating custom maps (if any)')
    dimensions = inst_dict[instance]
    map_matrices = {}
    for world in dimensions:
        world_rec = dimensions[world]
        if len(world_rec) > 3:
            if world_rec[3] == 'Y':
                map_matrices[world] = create_map_matrix(data, inst_dict[instance][world][0])
    chains = resolve_chains(data)
    write_box_pages(data, chains, outdir, instance, inst_dict, map_matrices)
    write_reports(data, chains, outdir)
    write_maps(data, chains, outdir, instance, inst_dict, map_matrices)


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


def write_box_pages(data, chains, outdir, instance, inst_dict, map_matrices):
    print('Writing box pages')
    for k, v in data.items():
        if u.is_loc(v):
            write_loc_html(v, k, data, chains['hidden'], chains['garrisons'],
                               chains['trades'], outdir, instance, inst_dict, map_matrices)
        elif u.is_char(v):
            write_char_html(v, k, data, chains['pledges'],
                                 chains['prisoners'], outdir, instance)
        elif u.is_player(v) :
            write_player_html(v, k, data, outdir)
        elif u.is_item(v):
            write_item_html(v, k, data, chains['trades'], outdir)
        elif u.is_ship(v):
            write_ship_html(v, k, data, outdir, instance, chains['pledges'], chains['prisoners'])
        elif u.is_skill(v):
            write_skill_html(v, k, data, outdir, chains['teaches'],
                                   chains['child_skills'], chains['skills_knowns'])
        elif u.return_kind(v) == 'storm':
            write_storm_html(v, k, data, chains['storms'], outdir)


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
    reports.road_report(data, outdir)
    reports.gate_report(data, outdir)
    reports.character_report(data, outdir)
    reports.graveyard_report(data, outdir)
    reports.faeryhill_report(data, outdir)
    reports.castle_report(data, outdir, chains['garrisons'])
    reports.city_report(data, outdir)
    reports.region_report(data, outdir)
    reports.mage_report(data, outdir)
    reports.priest_report(data, outdir)
    reports.gold_report(data, outdir)


def write_maps(data, chains, outdir, instance, inst_dict, map_matrices):
    print('Writing Maps')
    # inst_dict = {'g2': {'main': [10000, 100, 100]},
    #              'g4': {'main': [10000, 80, 80], 'hades': [24000, 50, 50], 'faery': [18000, 46, 46], 'cloudlands': [30000, 5, 5]},
    #              'qa': {'main': [10000, 10, 10], 'hades': [14000, 7, 7], 'faery': [12000, 10, 10]}}
    dimensions = inst_dict[instance]
    write_index(outdir, instance, inst_dict)
    for world in dimensions:
        world_rec = dimensions[world]
        if len(world_rec) > 3 and world_rec[3] == 'Y':
            write_legacy_bitmap(outdir,
                                data,
                                world_rec[0],
                                world_rec[1],
                                world_rec[2],
                                world,
                                map_matrices[world])
            write_legacy_top_map(outdir,
                                 world_rec[0],
                                 world_rec[1],
                                 world_rec[2],
                                 world,
                                 map_matrices[world])
            write_legacy_map_leaves(data,
                                    chains['castles'],
                                    outdir,
                                    world_rec[0],
                                    world_rec[1],
                                    world_rec[2],
                                    world,
                                    instance,
                                    map_matrices[world])
        else:
            write_bitmap(outdir,
                             data,
                             world_rec[0],
                             world_rec[1],
                             world_rec[2],
                             world)
            write_top_map(outdir,
                               world_rec[0],
                               world_rec[1],
                               world_rec[2],
                               world)
            write_map_leaves(data,
                                  chains['castles'],
                                  outdir,
                                  world_rec[0],
                                  world_rec[1],
                                  world_rec[2],
                                  world,
                                  instance)


def write_loc_html(v, k, data, hidden_chain, garrisons_chain, trade_chain, outdir, instance, inst_dict, map_matrices):
    # generate loc page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '.html'), 'w')
    template = env.get_template('loc.html')
    loc = build_complete_loc_dict(k, v, data, garrisons_chain, hidden_chain, trade_chain, instance, inst_dict, map_matrices)
    outf.write(template.render(loc=loc))


def write_ship_html(v, k, data, outdir, instance, pledge_chain, prisoner_chain):
    # generate ship page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '.html'), 'w')
    template = env.get_template('ship.html')
    ship = build_complete_ship_dict(k, v, data, instance, pledge_chain, prisoner_chain)
    outf.write(template.render(ship=ship))


def write_char_html(v, k, data, pledge_chain, prisoner_chain, outdir, instance):
    # generate char page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '.html'), 'w')
    template = env.get_template('char.html')
    char = build_complete_char_dict(k, v, data, instance, pledge_chain, prisoner_chain, False)
    outf.write(template.render(char=char))


def write_item_html(v, k, data, trade_chain, outdir):
    # generate item page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '.html'), 'w')
    template = env.get_template('item.html')
    item = build_complete_item_dict(k, v, data, trade_chain)
    outf.write(template.render(item=item))


def write_skill_html(v, k, data, outdir, teaches_chain, child_skills_chain, skills_known_chain):
    # generate skill page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '.html'), 'w')
    template = env.get_template('skill.html')
    skill = build_complete_skill_dict(k, v, data, teaches_chain, child_skills_chain, skills_known_chain)
    outf.write(template.render(skill=skill))


def write_storm_html(v, k, data, storm_chain, outdir):
    # generate storm page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '.html'), 'w')
    template = env.get_template('storm.html')
    storm = build_complete_storm_dict(k, v, data, storm_chain)
    outf.write(template.render(storm=storm))


def write_player_html(v, k, data, outdir):
    # generate player page
    outf = open(pathlib.Path(outdir).joinpath(to_oid(k) + '.html'), 'w')
    template = env.get_template('player.html')
    player = build_complete_player_dict(k, v, data)
    outf.write(template.render(player=player))
