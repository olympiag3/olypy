'''
Code that manipulates the in-memory version of the Olympia
database, which is composed of boxes.
'''

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


def box_append(data, box, subbox, value, dedup=False):
    '''
    append value to list data[box][subbox], doing what's needed to initialize things
    '''
    box = str(box)
    subbox = str(subbox)
    if not isinstance(value, list):
        value = [value]

    data[box] = data.get(box, {})

    l = data[box].get(subbox, [])
    [l.append(str(v)) for v in value]
    if dedup:
        l = uniq_f11(l)  # XXXv0 replace with if value not in l ...
    data[box][subbox] = l


def box_remove(data, box, subbox, value):
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


def box_overwrite(data, box, subbox, value):
    '''
    overwrite list with a new one
    '''
    box = str(box)
    subbox = str(subbox)
    if not isinstance(value, list):
        value = [value]
    value = [str(v) for v in value]

    data[box] = data.get(box, {})

    data[box][subbox] = value


def subbox_append(data, box, subbox, key, value, dedup=False):
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
    [l.append(str(v)) for v in value]
    if dedup:
        l = uniq_f11(l)  # XXXv0 replace with if value not in l ...
    data[box][subbox][key] = l


def subbox_remove(data, box, subbox, key, value):
    '''
    remove value from list data[box][subbox][key]
    '''
    box = str(box)
    subbox = str(subbox)
    key = str(key)

    data[box] = data.get(box, {})
    data[box][subbox] = data[box].get(subbox, {})

    l = data[box][subbox].get(key, [])
    try:
        l.remove(value)
        data[box][subbox][key] = l
    except ValueError:
        pass

def subbox_overwrite(data, box, subbox, key, value):
    '''
    overwrite list with a new one
    '''
    box = str(box)
    subbox = str(subbox)
    key = str(key)

    if not isinstance(value, list):
        value = [value]
    value = [str(v) for v in value]

    data[box] = data.get(box, {})
    data[box][subbox] = data[box].get(subbox, {})

    data[box][subbox][key] = value
