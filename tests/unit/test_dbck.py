import copy

import olypy.dbck as dbck


def test_check_firstline(capsys):
    data = {'1001': {}}
    assert dbck.check_firstline(data, False) == 1
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'has no firstline' in err

    data = {'1001': {'asdf': 1}}
    assert dbck.check_firstline(data, False) == 1
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'has no firstline' in err

    data = {'1001': {'firstline': ['1001 loc forest']}}
    assert dbck.check_firstline(data, False, checknames=True) == 1
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'no name' in err

    assert dbck.check_firstline(data, True, checknames=True) == 0
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'no name' in err
    assert 'fixed' in err

    data = {'1001': {'firstline': ['1001 char ni'], 'CH': {'ni': ['33'], 'bp': ['0']}},
            '33': {'firstline': ['33 item 0'], 'na': ['skeleton']}}
    assert dbck.check_firstline(data, True, checknames=True) == 0
    assert data['1001']['na'][0] == 'Skeleton'
    assert 'bp' not in data['1001']['CH']
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'no name' in err
    assert 'fixed' in err


def test_check_boxes(capsys):
    data = {'1001': {'foo': 1}}
    assert dbck.check_boxes(data) == 1
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'unknown section' in err

    data = {'1001': {'na': ['list', 'of', 'stuff']}}
    assert dbck.check_boxes(data) == 1
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'should have 1 entry' in err

    data = {'1001': {'na': {'a': 'dict'}}}
    assert dbck.check_boxes(data) == 1
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'is a dict but should not be' in err

    data = {'1001': {'CH': {'foo': 1}}}
    assert dbck.check_boxes(data) == 1
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'unknown section' in err

    data = {'1001': {'CH': {'ni': ['list', 'of', 'stuff']}}}
    assert dbck.check_boxes(data) == 1
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'multi-item list' in err

    data = {'1001': {'CH': {'ni': 1}}}
    assert dbck.check_boxes(data) == 1
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'a bad value' in err

    data = {'1001': {'CH': 1}}
    assert dbck.check_boxes(data) == 1
    out, err = capsys.readouterr()
    assert '1001' in err
    assert 'has bad value' in err


def test_check_where_here(capsys):

    data = {'1001': {'firstline': ['1001 char 0'],
                     'LI': {'wh': ['1003']}},
            '1002': {'firstline': ['1002 loc tower'],
                     'LI': {'wh': ['1003']}},
            '1003': {'firstline': ['1003 loc castle-in-progress'],
                     'LI': {'hl': ['1001', '1002'], 'wh': ['56789']}},
            '56789': {'firstline': ['56789 loc region'],
                      'LI': {'hl': ['1003']}}}

    data2 = copy.deepcopy(data)

    assert dbck.check_where_here(data) == 0
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''

    del data['1002']

    assert dbck.check_where_here(data) == 1
    out, err = capsys.readouterr()
    assert out == ''
    assert '1002' in err
    assert '1003' in err

    assert dbck.check_where_here(data, fix=True) == 0
    out, err = capsys.readouterr()
    assert out == ''
    assert '1002' in err
    assert '1003' in err

    del data2['1002']
    del data2['1003']

    assert dbck.check_where_here(data2) == 2
    out, err = capsys.readouterr()
    assert out == ''
    assert '56789' in err
    assert '1003' in err
    assert '1001' in err

    data = {'1001': {'firstline': ['1001 loc forest']}}
    assert dbck.check_where_here(data) == 1
    out, err = capsys.readouterr()
    assert out == ''
    assert 'is not anywhere' in err
    assert '1001' in err


def test_check_faction_units():

    data = {'1001': {'firstline': ['1001 char 0'],
                     'CH': {'lo': ['52341']}},
            '6940': {'firstline': ['6940 char 0'],
                     'CH': {'lo': ['52341']}},
            '52341': {'firstline': ['foo player foo'],
                      'PL': {'un': ['1001', '6940']}}}

    assert dbck.check_faction_units(data) == 0

    del data['1001']

    assert dbck.check_faction_units(data) == 1

    del data['52341']

    assert dbck.check_faction_units(data) == 1


def test_check_unique_items():
    data = {'1001': {'firstline': ['1001 char 0'],
                     'il': ['10', '1', '400', '1']},
            '400': {'firstline': ['400 item 0'],
                    'IT': {'un': ['1001']}}}

    assert dbck.check_unique_items(data) == 0

    data['1001']['il'][3] = '2'

    assert dbck.check_unique_items(data) == 1

    data['1001']['il'][3] = '0'
    del data['400']['IT']['un']

    assert dbck.check_unique_items(data) == 2


def test_check_prisoners():
    data = {'1001': {'firstline': ['1001 char 0']},
            '1002': {'firstline': ['1002 loc tower']},
            '6940': {'firstline': ['6940 char 0'],
                     'CH': {'pr': ['1']},
                     'LI': {'wh': ['1001']}}}

    assert dbck.check_prisoners(data) == 0

    data['6940']['LI']['wh'] = ['1002']

    assert dbck.check_prisoners(data) == 1


def test_check_links(capsys):
    data = {'10010': {'firstline': ['10010 loc forest']}}
    assert dbck.check_links(data) == 1
    out, err = capsys.readouterr()
    assert 'lacks LO pd' in err

    data['10010']['LO'] = {}
    data['10010']['LO']['pd'] = ['1']

    assert dbck.check_links(data) == 1
    out, err = capsys.readouterr()
    assert 'which does not exist' in err

    assert dbck.check_links(data, fix=True) == 0
    out, err = capsys.readouterr()
    assert 'which does not exist' in err
    assert 'fixed' in err

    data = {'56799': {'firstline': ['56799 loc city'],
                      'LO': {'pd': ['10010']}}}
    assert dbck.check_links(data) == 1
    out, err = capsys.readouterr()
    assert 'has NESW link' in err

    data['10010'] = {'firstline': ['10010 loc forest'],
                     'LO': {'pd': ['56799']}}
    assert dbck.check_links(data) == 2
    out, err = capsys.readouterr()
    assert 'has a NESWUD link to city' in err
