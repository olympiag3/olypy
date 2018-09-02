#!/usr/bin/python
import math

from olypy.oid import to_oid
import olymap.utilities as u
from olymap.utilities import get_name
import pathlib


# unit tested
def get_required_skill(v, data):
    required_skill = v.get('SK', {}).get('rs', [None])
    if required_skill[0] is not None:
        skill_id = required_skill[0]
        skill_rec = data[skill_id]
        required_skill_dict = {'id': skill_id,
                               'oid': to_oid(skill_id),
                               'name': get_name(skill_rec)}
        return required_skill_dict
    return None


# unit tested
def get_learn_time(v):
    learn_time = v.get('SK', {}).get('tl', [None])
    return learn_time[0]


def get_known_by(k, v, data, skills_known_chain):
    known_by_list = []
    char_list = skills_known_chain[k]
    if len(char_list) > 0:
        for char in char_list:
            char_rec = data[char]
            char_dict = {'id': char,
                         'oid': to_oid(char),
                         'name': get_name(char_rec)}
            known_by_list.append(char_dict)
    return known_by_list


def get_child_skills(k, v, data, child_skills_chain):
    child_skills_list = []
    child_list = child_skills_chain[k]
    if len(child_list) > 0:
        for skill in child_list:
            skill_rec = data[skill]
            skill_dict = {'id': skill,
                         'oid': to_oid(skill),
                         'name': get_name(skill_rec)}
            child_skills_list.append(skill_dict)
    return child_skills_list


def get_taught_in(k, v, data, teaches_chain):
    taught_in_list = []
    skill_list = teaches_chain[k]
    if len(skill_list) > 0:
        for loc in skill_list:
            loc_rec = data[loc]
            where_id = loc_rec['LI']['wh'][0]
            where_rec = data[where_id]
            region_id = u.region(u.return_unitid(where_rec), data)
            region_rec = data[region_id]
            loc_dict = {'id': loc,
                        'oid': to_oid(loc),
                        'name': get_name(loc_rec),
                        'where_id': where_id,
                        'where_oid': to_oid(where_id),
                        'where_name': get_name(where_rec),
                        'region_id': region_id,
                        'region_oid': to_oid(region_id),
                        'region_name': get_name(region_rec)}
            taught_in_list.append(loc_dict)
    return taught_in_list


def build_complete_skill_dict(k, v, data, teaches_chain, child_skills_chain, skills_known_chain):
    skills_dict = {'id': k,
                   'oid': to_oid(k),
                   'name': get_name(v),
                   'required_skill': get_required_skill(v, data),
                   'learn_time': get_learn_time(v),
                   'known_by': get_known_by(k, v, data, skills_known_chain),
                   'child_skills': get_child_skills(k, v, data, child_skills_chain),
                   'taught_in': get_taught_in(k, v, data, teaches_chain)}
    return skills_dict


def build_basic_skill_dict(k, v, data, teaches_chain, child_skills_chain, skills_known_chain):
    skills_dict = {'id': k,
                   'oid': to_oid(k),
                   'name': get_name(v),
                   'required_skill': get_required_skill(v, data),
                   'learn_time': get_learn_time(v)}
    return skills_dict
