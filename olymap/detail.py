#!/usr/bin/python

long_subkind_to_display_subkind = {'poppy field': 'p.field',
                                   'sacred grove': 's.grov',
                                   'rocky hill': 'r.hill',
                                   'battlefield': 'btfd.',
                                   'graveyard': 'gvyd.',
                                   'port city': 'p.city',
                                   'yew grove': 'yew',
                                   'pasture': 'past.',
                                   'circle of trees': 'c.trees',
                                   'ring of stones': 'r.stones',
                                   'sand pit': 's.pit',
                                   'mallorn grove': 'm.grov',
                                   'faery hill': 'f.hill',
                                   'enchanted forest': 'e.forst',
                                   'collapsed mine': 'c.mine'}

long_kind_to_display_kind = {'Secret pass': 's.pass',
                             'Secret route': 's.rte',
                             'Old road': 'o.road',
                             'Narrow channel': 'n.chan',
                             'Rocky channel': 'r.chan',
                             'Secret sea route': 'sea.rte',
                             'Underground': 'ugrnd'}
rank_num_string = {'10': 'lord',
                   '20': 'knight',
                   '30': 'baron',
                   '40': 'count',
                   '50': 'earl',
                   '60': 'marquess',
                   '70': 'duke',
                   '80': 'king'}

castle_ind = ['!', '@', '#', '%', '^', '*', '-', '+', 'a',
              'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm',
              'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z',
              'A', 'B', 'C', 'D','G', 'H', 'J','K', 'M',
              'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Z']

structure_kinds = ['temple', 'galley', 'roundship', 'castle', 'galley-in-progress',
             'roundship-in-progress', 'ghost ship', 'temple-in-progress', 'inn',
             'inn-in-progress', 'castle-in-progress', 'mine', 'mine-in-progress',
             'collapsed mine', 'tower', 'tower-in-progress', 'sewer']

use_key = {'1': 'Death Potion', '2': 'Healing Potion', '3': 'Slave Potion',
           '4': 'Palantir', '5': 'Projected Cast', '6': 'Quick Cast Potion',
           '7': 'Drum', '8': 'Elf Stone', '9': 'Orb'}
