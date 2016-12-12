'''
Code that manipulates the in-memory Olympia database
'''

from oid import to_oid, to_int, allocate_oid

# uniq a list, order preserving
# see: https://www.peterbe.com/plog/uniqifiers-benchmark

def uniq_f11(seq):
    return list(_uniq_f11(seq))

def _uniq_f11(seq):
    seen = set()
    for x in seq:
        if x in seen:
            continue
        seen.add(x)
        yield x

def data_append(data, box, subbox, value, dedup=True):
    '''
    append value to list data[box][subbox], doing what's needed to initialize things
    '''
    box = str(box)
    subbox = str(subbox)
    if not isinstance(value, list):
        value = [value]

    data[box] = data.get(box, {})
    l = data[box].get(subbox, [])
    [ l.append(str(v)) for v in value ]
    if dedup:
        l = uniq_f11(l) # XXXv0 replace with if value not in l ...
    data[box][subbox] = l

def data_remove(data, box, subbox, value):
    '''
    remove value from list data[box][subbox]
    '''
    box = str(box)
    subbox = str(subbox)
    data[box] = data.get(box, {})
    l = data[box].get(subbox, [])
    try:
        l.remove(value)
        data[box][subbox] = l
    except ValueError:
        pass

def data_overwrite(data, box, subbox, value):
    '''
    overwrite list with a new one
    '''
    box = str(box)
    data[box] = data.get(box, {})
    subbox = str(subbox)
    data[box][subbox] = value

def data_append2(data, box, subbox, key, value, dedup=True):
    '''
    append value to list data[box][subbox][key], doing what's needed to initialize things
    '''
    box = str(box)
    subbox = str(subbox)
    key = str(key)
    if not isinstance(value, list):
        value = [value]

    data[box] = data.get(box, {})
    data[box][subbox] = data[box].get(subbox, {})
    l = data[box][subbox].get(key, [])
    [ l.append(str(v)) for v in value ]
    if dedup:
        l = uniq_f11(l) # XXXv0 replace with if value not in l ...
    data[box][subbox][key] = l

def data_remove2(data, box, subbox, key, value):
    '''
    remove value from list data[box][subbox][key]
    '''
    box = str(box)
    subbox = str(subbox)
    key = str(key)
    l = data[box].get(subbox,{}).get(key, [])
    try:
        l.remove(value)
        data[box][subbox][key] = l
    except ValueError:
        pass

def data_overwrite2(data, box, subbox, key, value):
    '''
    overwrite list with a new one
    '''
    box = str(box)
    data[box] = data.get(box, {})
    subbox = str(subbox)
    data[box][subbox] = data[box].get(subbox, {})
    key = str(key)
    data[box][subbox][key] = value

def is_char(data, who):
    if ' char ' in data[who]['firstline'][0]:
        return True

def can_move(data, who):
    '''
    Used for situations such as deciding to destroy or unlink a no-longer-present box
    '''
    if ' loc ' not in data[who]['firstline'][0]:
        return True

def loop_here(data, who, fogonly=False):
    '''
    Make a list of everything here: chars, structures, sublocs
    If fogonly, make a list of only the invisible things (chars)
    (Name similar to C code)
    '''
    hls = set()
    if 'LI' in data[who]:
        if 'hl' in data[who]['LI']:
            for w in data[who]['LI']['hl']:
                if fogonly and not is_char(data, w):
                    continue
                hls.add(w)
                [hls.add(x) for x in loop_here(data,w)] # don't propagate fogonly, it only applies to top
    return hls

def upsert_box(data, newdata, who):
    '''
    '''

def upsert_location(data, newdata, top, promote_children=True):
    '''
    As we parse turns going forward in time, players observe locations.
    These might have been seen before, or may have changed. They may
    contain numerous structures, nobles, etc.
    '''

    # if not the same type, destroy the previous thing
    old_firstline = data.get(top, {}).get('firstline','99999 nothing nothing')
    _, old_kind, old_subkind = old_firstline.split(' ', maxsplit=2)
    new_firstline = newdata[top]['firstline']
    _, new_kind, new_subkind = new_firstline.split(' ', maxsplit=2)
    # XXXv0 what about foo-in-progress to foo? lot of churn for castle with towers
    if old_kind != new_kind:
        if top in data: # likely it is not
            raise ValueError('hey check this out')
            destroy_box(data, top, promote_children=promote_children)
        else:
            data[top] = {}

    data[top]['firstline'] = newdata[top]['firstline']
    data[top]['na'] = newdata[top]['na']

    oldhl = loop_here(data[top])
    newhl = loop_here(newdata[top])
    gone_or_new = oldhl.symmetric_difference(newhl)
    gone = gone_or_new.intersect(oldhl)
    new = gone_or_new.intersect(newhl)
    invisible_friends = set()
    if newdata[top].get('foggy'):
        invisible_friends = loop_here(data[top], fogonly=True)
        for i in list(invisible_friends):
            try:
                gone.remove(i)
            except KeyError:
                # this char is visible in newdata. remove from invisible.
                invisible_friends.remove(i)
    for g in list(gone):
        if data[g].get('LO',{}).get('hi'):
            # hidden sublocs never actually go away
            gone.remove(g)
    for g in gone:
        if can_move(data, g):
            unset_where(data, g)
        else:
            destroy_box(data, g)
    for n in new:
        upsert_box(data, newdata, n)

    # get current things to the right places - can just overwrite wh hl
    # thanks to the above processing of gone+new
    for lh in loop_here(newdata, top):
        hl = newdata[lh].get('LI', {}).get('hl', [])
        data_overwrite2(data, lh, 'LI', 'hl', hl)
        for hll in hl:
            data_overwrite(data, hll, 'LI', 'wh', lh)
    for f in invisible_friends:
        # put these on the end, that's OK
        data_append2(data, lh, 'LI', 'hl', f)

    for lh in loop_here(newdata, top):
        tl = newdata[lh].get('tl')
        if tl is not None:
            data_overwrite(data, lh, 'tl', tl)
    # mid-turn trade info
    #  XXXv1 don't trust any city *counts* but end-of-turn; city *prices* do not change
    #  XXXv1 do figure out if tradegoods have expired: 2 visible mid-turn means others have expired

def dead_char_body(data, who):
    '''
    Characters die mid-turn and become dead bodies. The previous
    turn end-state isn't quite right to freeze, but we'll do that for v0 XXXv1
    Location is province, or nowhere if at sea (province will be wrong if the char moved and died)
    '''

    # XXXv1 melters, npcs don't get a body
    # XXXv0 set a location

    data_overwrite(data, who, 'firstline', str(who) + ' item dead body')
    data_overwrite2(data, who, 'MI', 'sn', data[who]['na'])
    data_overwrite(data, who, 'na', 'dead body')
    pl = data[who]['CH']['lo']
    data_overwrite2(data, who, 'MI', 'ol', pl)
    data_overwrite2(data, who, 'IT', 'wt', 100)
    data_overwrite2(data, who, 'IT', 'pl', 'dead bodies')

    # changing the firstline kind from char has consequences for the player thing
    # XXXv0 is this complete?
    # XXXv0 should I just let this get taken care of another way?
    data_remove2(data, who, 'PL', 'un', who)
    data_remove2(data, who, 'PL', 'kn', who)

def upsert_char(data, newdata, who):
    pass

def destroy_box(data, who, promote_children=True):
    '''
    Destroy a box that's become something different.
    '''
    unset_where(data, who, promote_children=promote_children)
    # XXXv0 other links:
    # pledge chain - CM,pl is one-way so it needs a end-of-run fixup XXXv0
    # lord: CH,lo and previous lord CH,pl -- needs end-of-run fixup XXXv0
    # unique items - need to look at firstline - IT,un is where it is
    # creater of things like storms, artifacts - IM,ct
    # owner of storm - MI,sb {summoned by}
    # storm bound to a ship - ship has SL,bs ... and the storm has MI,bs=itself (?)

def set_where(data, who, where):
    who = to_int(who)
    unset_where(data, who)
    where = to_int(where)
    data_append2(data, who, 'LI', 'wh', where)
    existing_hl = data[where].get('LI', {}).get('hl', [])
    if who not in existing_hl:
        data_append2(data, where, 'LI', 'hl', who)

def unset_where(data, who, promote_children=True):
    '''
    If I'm somewhere, remove me from that somewhere.
    If promote_children & anyone is inside me, move them up.
    I may well end up nowhere... that will get cleaned up in the end.
    (Things that move can be nowhere... things that can't move should be destroyed XXXv0)
    '''
    if data.get(who) is None:
        return
    wh = data[who].get('LI', {}).get('wh', [])
    hl = data[who].get('LI', {}).get('hl')

    if len(wh):
        data[who]['LI']['wh'] = [] # XXXv0 data_overwrite2(...)
        other_hl = data.get(wh[0], {}).get('LI', {}).get('hl')
        if other_hl is not None:
            try:
                other_hl.remove(who)
                data[wh[0]]['LI']['hl'] = other_hl
            except ValueError:
                pass

    if promote_children and hl is not None:
        for child in hl:
            data_append2(data, wh[0], 'LI', 'hl', child)
            data[child]['LI']['wh'] = wh

# XXXv0 can't have an endless loop of unlink->destroy->unlink 
#    if not can_move(data, who):
#        destroy_box(data, who)

def data_newbox(data, oid_kind, firstline, who=None, overwrite=False):
    '''
    Create a new box. Intended for generating QA libs, not for parsing turns.
    '''
    if who:
        who = to_int(who) # roundtrips if already an int
    else:
        who = allocate_oid(data, oid_kind) # e.g. NNNN
    if who in data:
        if not overwrite:
            raise ValueError( who + ' is already in data')
        # if I am not the same thing, destory the old thing
        if data[who]['firstline'] != firstline:
            destroy_box(data, who)
    data[who] = {}
    data[who]['firstline'] = [str(who) + ' ' + firstline]
    return who

structures = {
    # in-progress: bm, er, eg ... bm runs 0..4
    'roundship': {'type': 'ship', 'de': 10, 'er': 50000, 'ca': 25000,},
    'galley': {'type': 'ship', 'de': 20, 'er': 25000, 'ca': 5000,},
    'inn': {'de': 10, 'er': 30000,},
    'mine': {'de': 10, 'er': 50000, 'sd': 3, }, # depth is sd//3
    'temple': {'de': 10, 'er': 100000, 'te': 750},
    'tower': {'de': 40, 'er': 200000,},
    'castle': {'de': 50, 'er': 1000000,},
    'castle1': {'kind': 'castle', 'de': 55, 'er': 1000000, 'cl': 1,},
    'castle2': {'kind': 'castle', 'de': 60, 'er': 1000000, 'cl': 2,},
    'castle3': {'kind': 'castle', 'de': 65, 'er': 1000000, 'cl': 3,},
    'castle4': {'kind': 'castle', 'de': 70, 'er': 1000000, 'cl': 4,},
    'castle5': {'kind': 'castle', 'de': 75, 'er': 1000000, 'cl': 5,},
    'castle6': {'kind': 'castle', 'de': 80, 'er': 1000000, 'cl': 6,},
}

def add_structure(data, kind, where, name, progress=None, damage=None, defense=None, who=None):
    if kind not in structures:
        raise ValueError
    where = to_int(where)
    if where not in data:
        raise ValueError('where ' + where + ' is not in data')

    who = data_newbox(data, 'NNNN', structures[kind].get('type', 'loc') + ' ' + structures[kind].get('kind', kind), who=who)
    set_where(data, who, where)
    data[who]['na'] = [ name ]

    # fully-finished structure
    if 'ca' in structures[kind]:
        data_append2(data, who, 'SL', 'ca', structures[kind]['ca'])
    if 'cl' in structures[kind]:
        data_append2(data, who, 'SL', 'cl', structures[kind]['cl'])
    if 'sd' in structures[kind]:
        data_append2(data, who, 'SL', 'sd', structures[kind]['sd'])
    data_append2(data, who, 'SL', 'de', defense or structures[kind]['de'])
    if damage:
        data_append2(data, who, 'SL', 'da', damage)

    # XXX if under construction
    # remove ca if present
    # remove de
    #data_append2(data, who, 'SL', 'er', structures[kind]['er'])
    # compute eg
    # compute bm 0-4
    if progress:
        raise ValueError

def add_scroll(data, skill, loc, who=None):
    who = data_newbox(data, 'CNNN', 'item scroll', who=who)
    loc = to_int(loc)
    skill = str(skill)

    data[who]['na'] = ['Scroll of '+skill]
    data[who]['IT'] = {}
    data[who]['IT']['wt'] = [1]
    data[who]['IT']['un'] = [loc]
    data[who]['IM'] = {}
    data[who]['IM']['ms'] = [skill]

    data_append(data, loc, 'il', [who, 1], dedup=False)

def add_potion(data, kind, im, loc, who=None):
    who = data_newbox(data, 'CNNN', 'item 0', who=who)
    loc = to_int(loc)

    data[who]['na'] = ['Potion of '+kind]
    data[who]['IT'] = {}
    data[who]['IT']['wt'] = [1]
    data[who]['IT']['un'] = [loc]
    data[who]['IM'] = im

    data_append(data, loc, 'il', [who, 1], dedup=False)
