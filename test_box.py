from box import uniq_f11
from box import box_append, box_remove, box_overwrite
from box import subbox_append, subbox_remove, subbox_overwrite


def test_uniq_f11():
    seq = [1, 2, 3, 2]
    assert uniq_f11(seq) == [1, 2, 3]

def test_append_remove():
    data = {}
    box_append(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['foo']}}
    box_append(data, 1001, 'il', ['60000', 1], dedup=False)
    box_append(data, 1001, 'il', ['60001', 1], dedup=False)
    assert data == {'1001': {'na': ['foo'], 'il': ['60000', '1', '60001', '1']}}

    data = {}
    box_append(data, '1001', 'na', 'foo')
    assert data == {'1001': {'na': ['foo']}}
    box_append(data, '1001', 'na', 'bar')
    assert data == {'1001': {'na': ['foo', 'bar']}}
    del data['1001']['na']
    box_append(data, '1001', 'na', ['foo', 'bar'])
    assert data == {'1001': {'na': ['foo', 'bar']}}

    data = {}
    box_append(data, 1001, 'na', 'foo')
    box_remove(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': []}}
    box_remove(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': []}}
    box_remove(data, 1001, 'na', 'bar')
    assert data == {'1001': {'na': []}}
    box_append(data, 1001, 'na', ['foo', 'bar'])
    box_remove(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['bar']}}
    box_append(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['bar', 'foo']}}
    box_remove(data, 1001, 'na', 'bar')
    assert data == {'1001': {'na': ['foo']}}

    data = {}
    box_append(data, 1001, 'na', 'foo')
    box_append(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['foo']}}
    box_append(data, 1001, 'na', 'bar')
    box_append(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['foo', 'bar']}}
    box_append(data, 1001, 'na', 'bar')
    assert data == {'1001': {'na': ['foo', 'bar']}}
    box_remove(data, 1001, 'na', 'foo')
    box_append(data, 1001, 'na', 'foo')
    assert data == {'1001': {'na': ['bar', 'foo']}}

def test_overwrite():
    data = {}
    box_overwrite(data, 1, 2, ['3'])
    assert data == {'1': {'2': ['3']}}

    data = {'1001': {'na': ['Oleg the Loudmouth']}}
    box_overwrite(data, 1001, 'na', ['Phydeaux, RIP'])
    assert data == {'1001': {'na': ['Phydeaux, RIP']}}

def test_append2_remove2():
    '''
    These tests are a copy of test_append_remove with an extra level
    '''
    data = {}
    subbox_append(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['foo']}}}

    data = {}
    subbox_append(data, '1001', 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['foo']}}}
    subbox_append(data, '1001', 'LI', 'hl', 'bar')
    assert data == {'1001': {'LI': {'hl': ['foo', 'bar']}}}
    del data['1001']['LI']['hl']
    subbox_append(data, '1001', 'LI', 'hl', ['foo', 'bar'])
    assert data == {'1001': {'LI': {'hl': ['foo', 'bar']}}}

    data = {}
    subbox_append(data, 1001, 'LI', 'hl', 'foo')
    subbox_remove(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': []}}}
    subbox_remove(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': []}}}
    subbox_remove(data, 1001, 'LI', 'hl', 'bar')
    assert data == {'1001': {'LI': {'hl': []}}}
    subbox_append(data, 1001, 'LI', 'hl', ['foo', 'bar'])
    subbox_remove(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['bar']}}}
    subbox_append(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['bar', 'foo']}}}
    subbox_remove(data, 1001, 'LI', 'hl', 'bar')
    assert data == {'1001': {'LI': {'hl': ['foo']}}}

    data = {}
    subbox_append(data, 1001, 'LI', 'hl', 'foo')
    subbox_append(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['foo']}}}
    subbox_append(data, 1001, 'LI', 'hl', 'bar')
    subbox_append(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['foo', 'bar']}}}
    subbox_append(data, 1001, 'LI', 'hl', 'bar')
    assert data == {'1001': {'LI': {'hl': ['foo', 'bar']}}}
    subbox_remove(data, 1001, 'LI', 'hl', 'foo')
    subbox_append(data, 1001, 'LI', 'hl', 'foo')
    assert data == {'1001': {'LI': {'hl': ['bar', 'foo']}}}

def test_overwrite2():
    data = {}
    subbox_overwrite(data, 1, 2, 3, ['3'])
    assert data == {'1': {'2': {'3': ['3']}}}

    data = {'1001': {'LI': {'wh': ['10000']}}}
    subbox_overwrite(data, 1001, 'LI', 'wh', ['10001'])
    assert data == {'1001': {'LI': {'wh': ['10001']}}}

