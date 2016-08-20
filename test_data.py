import pytest

from oid import to_int, to_oid
from data import place_new_unit, add_structure, add_scroll, add_potion

def check_where(data, unit, loc):
    unitint = to_int(str(unit))
    locint = to_int(str(loc))
    assert data[unitint]['LI']['wh'] == [ locint ]
    assert data[locint]['LI']['hl'].index(unitint) >= 0

def test_data():
    data = {}
    place_new_unit(data, 1001, 1002)
    check_where(data, '1001', '1002')
    place_new_unit(data, '1003', '1004')
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
