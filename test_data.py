import pytest

from oid import to_int, to_oid
from data import uniq_f11
from data import data_append, data_remove, data_append2, data_remove2
from data import is_char, can_move, loop_here
from data import upsert_box, upsert_location
from data import dead_char_body, upsert_char
from data import destroy_box
from data import set_where, unset_where
from data import data_newbox
from data import add_structure, add_scroll, add_potion

def check_where(data, unit, loc):
    unitint = to_int(str(unit))
    locint = to_int(str(loc))
    assert data[unitint]['LI']['wh'] == [ locint ]

    # this will throw ValueError if it fails
    assert data[locint]['LI']['hl'].index(unitint) >= 0

def test_uniq_f11():
    seq = [1, 2, 3, 2]
    assert uniq_f11(seq) == [1, 2, 3]

def test_append_remove():
    data = {}
    data_append(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['foo']}}
    data_append(data, 1001, 'il', ['60000', 1], dedup=False)
    data_append(data, 1001, 'il', ['60001', 1], dedup=False)
    assert data == {'1001': {'na': ['foo'], 'il': ['60000', '1', '60001', '1']}}

    data = {}
    data_append(data, '1001', 'na', 'foo')
    assert data == {'1001': {'na': ['foo']}}
    data_append(data, '1001', 'na', 'bar')
    assert data == {'1001': {'na': ['foo', 'bar']}}
    del data['1001']['na']
    data_append(data, '1001', 'na', ['foo', 'bar'])
    assert data == {'1001': {'na': ['foo', 'bar']}}

    data = {}
    data_append(data, 1001, 'na', 'foo')
    data_remove(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': []}}
    data_remove(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': []}}
    data_remove(data, 1001, 'na', 'bar')
    assert data == {'1001': {'na': []}}
    data_append(data, 1001, 'na', ['foo', 'bar'])
    data_remove(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['bar']}}
    data_append(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['bar', 'foo']}}
    data_remove(data, 1001, 'na', 'bar')
    assert data == {'1001': {'na': ['foo']}}

    data = {}
    data_append(data, 1001, 'na', 'foo')
    data_append(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['foo']}}
    data_append(data, 1001, 'na', 'bar')
    data_append(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['foo', 'bar']}}
    data_append(data, 1001, 'na', 'bar')
    assert data == {'1001': {'na': ['foo', 'bar']}}
    data_remove(data, 1001, 'na', 'foo')
    data_append(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['bar', 'foo']}}
    return

def test_append2_remove2():
    '''
    These tests are a copy of test_append_remove with an extra level
    '''
    data = {}
    data_append2(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['foo']}}}

    data = {}
    data_append2(data, '1001', 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['foo']}}}
    data_append2(data, '1001', 'LI', 'hl', 'bar')
    assert data == {'1001': {'LI': {'hl': ['foo', 'bar']}}}
    del data['1001']['LI']['hl']
    data_append2(data, '1001', 'LI', 'hl', ['foo', 'bar'])
    assert data == {'1001': {'LI': {'hl': ['foo', 'bar']}}}

    data = {}
    data_append2(data, 1001, 'LI', 'hl', 'foo')
    data_remove2(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': []}}}
    data_remove2(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': []}}}
    data_remove2(data, 1001, 'LI', 'hl', 'bar')
    assert data == {'1001': {'LI': {'hl': []}}}
    data_append2(data, 1001, 'LI', 'hl', ['foo', 'bar'])
    data_remove2(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['bar']}}}
    data_append2(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['bar', 'foo']}}}
    data_remove2(data, 1001, 'LI', 'hl', 'bar')
    assert data == {'1001': {'LI': {'hl': ['foo']}}}

    data = {}
    data_append2(data, 1001, 'LI', 'hl', 'foo')
    data_append2(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['foo']}}}
    data_append2(data, 1001, 'LI', 'hl', 'bar')
    data_append2(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['foo', 'bar']}}}
    data_append2(data, 1001, 'LI', 'hl', 'bar')
    assert data == {'1001': {'LI': {'hl': ['foo', 'bar']}}}
    data_remove2(data, 1001, 'LI', 'hl', 'foo')
    data_append2(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['bar', 'foo']}}}
    return

def test_is_char_and_can_move():
    data = {'1001': {'firstline': ['1001 char 0']}}
    assert is_char(data, '1001') 
    assert can_move(data, '1001') 
    data = {'1001': {'firstline': ['1001 loc tower']}}
    assert not is_char(data, '1001') 
    assert not can_move(data, '1001') 
    return

def test_loop_here():
    data = {'1001': {'firstline': ['1001 loc tower'], 'LI': {'hl': ['1002']}},
            '1002': {'firstline': ['1002 char 0'], 'LI': {'hl': ['1003']}},
            '1003': {'firstline': ['1003 loc tower']},} # yeah, nonsensical
    assert loop_here(data, '1001') == {'1002', '1003'}
    assert loop_here(data, '1001', fogonly=True) == {'1002', '1003'}
    assert loop_here(data, '1002') == {'1003'}
    assert loop_here(data, '1002', fogonly=True) == set()
    return

def test_upsert_box():
    return

def test_upsert_location():
    return

def test_upsert_char():
    return

def test_destroy_box():
    return

def test_set_where():
    data = {'1001': {'LI': {'wh': ['9999']}},
            '1002': {},}
    set_where(data, '1001', '1002')
    assert data['1002']['LI']['hl'] == ['1001']
    assert data['1001']['LI']['wh'] == ['1002']
    set_where(data, '1001', '1002') # should do nothing
    assert data['1002']['LI']['hl'] == ['1001']
    assert data['1001']['LI']['wh'] == ['1002']
    return

def test_unset_where():
    data = {'1001': {'LI': {'wh': ['9999']}},
            '1002': {},}
    unset_where(data, '1001')
    assert data['1001']['LI']['wh'] == []
    set_where(data, '1001', '1002')
    assert data['1002']['LI']['hl'] == ['1001']
    assert data['1001']['LI']['wh'] == ['1002']
    unset_where(data, '1001')
    assert data['1001']['LI']['wh'] == []
    assert data['1002']['LI']['hl'] == []
    set_where(data, '1001', '1002')
    data['1002']['LI']['hl'] = [] # so I'm not on the list to be removed
    unset_where(data, '1001')
    assert data['1001']['LI']['wh'] == []
    assert data['1002']['LI']['hl'] == []

    data = {'1001': {'LI': {'wh': ['9999'], 'hl': ['1002']}},
            '1002': {'LI': {'wh': ['1002'], 'hl': ['1002']}},
            '9999': {'LI': {'hl': ['1001']}},}
    unset_where(data, '1001', promote_children=True)
    assert data['1002']['LI']['wh'] == ['9999']
    assert data['9999']['LI']['hl'] == ['1002']
    return

def test_data_newbox():
    '''
    Eh, tested by the various add_* below
    '''
    return

def test_adds():
    data = {'1002': {}, '1004': {}} # we insist that the target location exists
    set_where(data, 1001, 1002)
    check_where(data, '1001', '1002')
    set_where(data, '1003', '1004')
    check_where(data, 1003, 1004)
    set_where(data, '1003', '1004') # second time shouldn't change anything
    check_where(data, 1003, 1004)

    data = {'1006': {}}
    add_structure(data, 'tower', '1006', 'Foo', who='1005')
    result = {'1005': {'firstline': ['1005 loc tower'],
                       'na': ['Foo'],
                       'LI': {'wh': ['1006']},
                       'SL': {'de': ['40']}},
              '1006': {'LI': {'hl': ['1005']}}
    }
    assert data == result

    data = {'1007': {}}
    add_scroll(data, 600, 1007, who=1008)
    result = {'1007': {'il': ['1008', '1']},
              '1008': {'IM': {'ms': ['600']},
                       'IT': {'un': ['1007'], 'wt': [1]},
                       'firstline': ['1008 item scroll'],
                       'na': ['Scroll of 600']}
    }
    assert data == result

    data = {'1009': {}}
    add_potion(data, 'heal', {'uk': ['2']}, 1009, who=1010)
    result = {'1010': {'IM': {'uk': ['2']},
                       'IT': {'un': ['1009'], 'wt': [1]},
                       'firstline': ['1010 item 0'],
                       'na': ['Potion of heal']},
              '1009': {'il': ['1010', '1']}
    }
    assert data == result

