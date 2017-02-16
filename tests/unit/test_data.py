import pytest

from olypy.oid import to_int
from olypy.data import is_char, can_move, loop_here
from olypy.data import set_where, unset_where
from olypy.data import add_structure, add_scroll, add_potion


def check_where(data, unit, loc):
    '''
    Used by other tests to verify that unit is in loc and vice-versa.
    Does not work for unique items.
    '''
    unitint = to_int(str(unit))
    locint = to_int(str(loc))
    assert ' item ' not in data[unitint].get('firstline', '')
    assert data[unitint]['LI']['wh'] == [locint]

    # this will throw ValueError if it fails
    assert data[locint]['LI']['hl'].index(unitint) >= 0


def test_set_where():
    data = {'1001': {'LI': {'wh': ['9999']}},
            '1002': {}}
    set_where(data, '1001', '1002')
    assert data['1002']['LI']['hl'] == ['1001']
    assert data['1001']['LI']['wh'] == ['1002']
    set_where(data, '1001', '1002')  # should do nothing
    assert data['1002']['LI']['hl'] == ['1001']
    assert data['1001']['LI']['wh'] == ['1002']

    data = {'1001': {'LI': {'hl': ['1002']}},
            '1002': {'LI': {'wh': ['1001']}}}
    set_where(data, '1001', '9999', keep_children=True)
    assert data['1002']['LI']['wh'] == ['1001']
    assert data['1001']['LI']['hl'] == ['1002']
    set_where(data, '1001', '9999')
    assert data['1002']['LI']['wh'] == ['9999']
    assert data['1001']['LI']['hl'] == []


def test_unset_where():
    data = {'1001': {'LI': {'wh': ['9999']}},
            '1002': {}}
    unset_where(data, '1001')
    assert 'wh' not in data['1001']['LI']
    set_where(data, '1001', '1002')
    assert data['1002']['LI']['hl'] == ['1001']
    assert data['1001']['LI']['wh'] == ['1002']
    unset_where(data, '1001')
    assert 'wh' not in data['1001']['LI']
    assert data['1002']['LI']['hl'] == []
    set_where(data, '1001', '1002')
    data['1002']['LI']['hl'] = []  # so I'm not on the list to be removed
    unset_where(data, '1001')
    assert 'wh' not in data['1001']['LI']
    assert data['1002']['LI']['hl'] == []

    data = {'1001': {'LI': {'wh': ['9999'], 'hl': ['1002']}},
            '1002': {'LI': {'wh': ['1002'], 'hl': ['1002']}},
            '9999': {'LI': {'hl': ['1001']}}}
    unset_where(data, '1001', promote_children=True)
    assert data['1002']['LI']['wh'] == ['9999']
    assert data['9999']['LI']['hl'] == ['1002']


def test_is_char_and_can_move():
    data = {'1001': {'firstline': ['1001 char 0']}}
    assert is_char(data, '1001')
    assert can_move(data, '1001')
    data = {'1001': {'firstline': ['1001 loc tower']}}
    assert not is_char(data, '1001')
    assert not can_move(data, '1001')


def test_loop_here():
    data = {'1001': {'firstline': ['1001 loc forest'], 'LI': {'hl': ['1002', '1003', '1006']}},
            '1002': {'firstline': ['1002 char 0'], 'LI': {'hl': ['1004']}},
            '1003': {'firstline': ['1003 loc tower'], 'LI': {'hl': ['1005']}},
            '1004': {'firstline': ['1004 char 0']},
            '1005': {'firstline': ['1005 char 0']},
            '1006': {'firstline': ['1006 loc city'], 'LI': {'hl': ['1007']}},
            '1007': {'firstline': ['1007 char 0']}}
    assert loop_here(data, '1001') == {'1002', '1003', '1004', '1005', '1006'}
    assert loop_here(data, '1001', fog=True) == {'1003', '1005', '1006'}
    assert loop_here(data, '1003') == {'1005'}

    if loop_here(data, '1003', fog=True) == {'1005'}:
        pytest.xfail('have not implemented non-province fog yet')


def test_upsert_box():
    return


def test_destroy_box():
    return


def test_upsert_location():
    return


def test_upsert_char():
    return


def test_data_newbox():
    # Eh, tested by the various add_* below
    pass


def test_adds():
    data = {'1002': {}, '1004': {}}  # we insist that the target location exists
    set_where(data, 1001, 1002)
    check_where(data, '1001', '1002')
    set_where(data, '1003', '1004')
    check_where(data, 1003, 1004)
    set_where(data, '1003', '1004')  # second time shouldn't change anything
    check_where(data, 1003, 1004)

    data = {'1006': {}}
    add_structure(data, 'tower', '1006', 'Foo', oid='1005')
    result = {'1005': {'firstline': ['1005 loc tower'],
                       'na': ['Foo'],
                       'LI': {'wh': ['1006']},
                       'SL': {'de': ['40']}},
              '1006': {'LI': {'hl': ['1005']}}}
    assert data == result

    data = {'1007': {}}
    add_scroll(data, 600, 1007, oid=1008)
    result = {'1007': {'il': ['1008', '1']},
              '1008': {'IM': {'ms': ['600']},
                       'IT': {'un': ['1007'], 'wt': [1]},
                       'firstline': ['1008 item scroll'],
                       'na': ['Scroll of 600']}}
    assert data == result

    data = {'1009': {}}
    add_potion(data, 'heal', {'uk': ['2']}, 1009, oid=1010)
    result = {'1010': {'IM': {'uk': ['2']},
                       'IT': {'un': ['1009'], 'wt': [1]},
                       'firstline': ['1010 item 0'],
                       'na': ['Potion of heal']},
              '1009': {'il': ['1010', '1']}}
    assert data == result
