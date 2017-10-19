#!/usr/bin/python
import os
import sys
import math

from olypy.oid import to_oid
import olypy.oio as oio
import OlyMapperPy.OlyMapperUtilities as u
import olypy.details as details
from OlyMapperPy.OlyMapperUtilities import anchor


def write_skill_page_header(v,k,outf):
    outf.write('<H3>{} [{}]</H3>\n'.format(v['na'][0], to_oid((k))))


def write_skill_basic_info(v,k,data,outf, teaches_chain, child_skills_chain, skills_known_chain):
     outf.write('<table>\n')
     if 'SK' in v:
         if 'rs' in v['SK']:
              skill = data[v['SK']['rs'][0]]
              outf.write('<tr><td>Skill Required:</td><td>{} [{}]</td></tr>\n'\
                        .format(skill['na'][0],
                                anchor(u.return_unitid(skill['firstline'][0]))))
         if 'tl' in v['SK']:
             outf.write('<tr><td>Time to Learn:</td><td>{}</td></tr>\n'.format(v['SK']['tl'][0]))
     char_list = skills_known_chain[k]
     if len(char_list) > 0:
         outf.write('<tr><td valign="top">Known By:</td><td>')
         outf.write('<table>\n')
         columns = int(math.ceil(len(char_list) / 3))
         for charac in range(0,columns):
             outf.write('<tr>')
             if (columns*0) + charac < len(char_list):
                 char_rec = data[char_list[(columns*0) + charac]]
                 outf.write('<td>{} [{}]</td>' \
                            .format(char_rec['na'][0],
                                    anchor(to_oid(u.return_unitid(char_rec['firstline'][0])))))
             else:
                 outf.write('<td></td><td></td>')
             if (columns*1) + charac < len(char_list):
                 char_rec = data[char_list[(columns*1) + charac]]
                 outf.write('<td>{} [{}]</td>' \
                            .format(char_rec['na'][0],
                                    anchor(to_oid(u.return_unitid(char_rec['firstline'][0])))))
             else:
                 outf.write('<td></td><td></td>')
             if (columns*2) + charac < len(char_list):
                 char_rec = data[char_list[(columns*2) + charac]]
                 outf.write('<td>{} [{}]</td>' \
                            .format(char_rec['na'][0],
                                    anchor(to_oid(u.return_unitid(char_rec['firstline'][0])))))
             else:
                 outf.write('<td></td><td></td>')
             outf.write('</tr>\n')
         outf.write('</table>\n')
         outf.write('</td></tr>')
     child_list = child_skills_chain[k]
     if len(child_list) > 0:
         outf.write('<tr><td valign="top">Child Skills:</td><td>')
         outf.write('<table>\n')
         columns = int(math.ceil(len(child_list) / 3))
         for skill in range(0,columns):
             outf.write('<tr>')
             if (columns*0) + skill < len(child_list):
                 skill_rec = data[child_list[(columns*0) + skill]]
                 outf.write('<td>{} [{}]</td>' \
                            .format(skill_rec['na'][0],
                                    anchor(to_oid(u.return_unitid(skill_rec['firstline'][0])))))
             else:
                 outf.write('<td></td><')
             if (columns*1) + skill < len(child_list):
                 skill_rec = data[child_list[(columns*1) + skill]]
                 outf.write('<td>{} [{}]</td>' \
                            .format(skill_rec['na'][0],
                                    anchor(to_oid(u.return_unitid(skill_rec['firstline'][0])))))
             else:
                 outf.write('<td></td>')
             if (columns*2) + skill < len(child_list):
                 skill_rec = data[child_list[(columns*2) + skill]]
                 outf.write('<td>{} [{}]</td>' \
                            .format(skill_rec['na'][0],
                                    anchor(to_oid(u.return_unitid(skill_rec['firstline'][0])))))
             else:
                 outf.write('<td></td>')
             outf.write('</tr>\n')
         outf.write('</table>\n')
         outf.write('</td></tr>')
     skill_list = teaches_chain[k]
     if len(skill_list) > 0:
         skill_literal = 'Taught in:'
         for loc in skill_list:
            loc_rec = data[loc]
            where_rec = data[loc_rec['LI']['wh'][0]]
            region = data[u.region(u.return_unitid(where_rec['firstline'][0]),data)]
            outf.write('<tr><td>{}</td><td>{} [{}], {} [{}], in {}</td></tr>\n'\
                       .format(skill_literal,
                               loc_rec['na'][0],
                               anchor(to_oid(u.return_unitid(loc_rec['firstline'][0]))),
                               where_rec['na'][0],
                               anchor(to_oid(u.return_unitid(where_rec['firstline'][0]))),
                               region['na'][0]))
            skill_literal = ''
     outf.write('</table>\n')


def write_skill_html(v, k, data, teaches_chain, child_skills_chain, skills_known_chain):
    # generate skill page
    fl = v['firstline'][0]
    #print('skill {} {} {}'.format(fl, k, to_oid(k)))
    outf = open(to_oid(k)+'.html', 'w')
    outf.write('<HTML>\n')
    outf.write('<HEAD>\n')
    name = v['na'][0]
    outf.write('<TITLE>{} [{}]'.format(name, \
               to_oid(k)))
    outf.write('</TITLE>\n')
    outf.write('</HEAD>\n')
    outf.write('<BODY>\n')
    write_skill_page_header(v,k,outf)
    write_skill_basic_info(v,k,data,outf, teaches_chain, child_skills_chain, skills_known_chain)
    outf.write('</BODY>\n')
    outf.write('</HTML>\n')
    outf.close()