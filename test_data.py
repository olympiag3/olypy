import pytest

from oid import to_int, to_oid
from data import data_append, data_remove, data_append2, data_remove2
from data import upsert_box, destroy_box
from data import link_box, add_structure, add_scroll, add_potion

def check_where(data, unit, loc):
    unitint = to_int(str(unit))
    locint = to_int(str(loc))
    assert data[unitint]['LI']['wh'] == [ locint ]

    # this will throw ValueError if it fails
    assert data[locint]['LI']['hl'].index(unitint) >= 0

def test_append_remove():
    data = {}
    data_append(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['foo']}}

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

def test_upsert_destroy_link_box():
    return

def test_adds():
    data = {}
    link_box(data, 1001, 1002)
    check_where(data, '1001', '1002')
    link_box(data, '1003', '1004')
    check_where(data, 1003, 1004)
    link_box(data, '1003', '1004') # second time shouldn't change anything
    check_where(data, 1003, 1004)

    data = {'1006': {}}
    add_structure(data, 'tower', '1006', 'Foo', oid='1005')
    result = {'1005': {'firstline': ['1005 loc tower'],
                       'na': ['Foo'],
                       'LI': {'wh': ['1006']},
                       'SL': {'de': ['40']}},
              '1006': {'LI': {'hl': ['1005']}}
    }
    assert data == result

    data = {'1007': {}}
    add_scroll(data, 600, 1007, oid=1008)
    result = {'1007': {'il': ['1008', '1']},
              '1008': {'IM': {'ms': ['600']},
                       'IT': {'un': ['1007'], 'wt': [1]},
                       'firstline': ['1008 item scroll'],
                       'na': ['Scroll of 600']}
    }
    assert data == result

    data = {'1009': {}}
    add_potion(data, 'heal', {'uk': ['2']}, 1009, oid=1010)
    result = {'1010': {'IM': {'uk': ['2']},
                       'IT': {'un': ['1009'], 'wt': [1]},
                       'firstline': ['1010 item 0'],
                       'na': ['Potion of heal']},
              '1009': {'il': ['1010', '1']}
    }
    assert data == result

