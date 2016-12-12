from box import uniq_f11
from box import data_append, data_remove, data_overwrite
from box import data_append2, data_remove2, data_overwrite2


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

def test_overwrite():
    data = {}
    data_overwrite(data, 1, 2, ['3'])
    assert data == {'1': {'2': ['3']}}

    data = {'1001': {'na': ['Oleg the Loudmouth']}}
    data_overwrite(data, 1001, 'na', ['Phydeaux, RIP'])
    assert data == {'1001': {'na': ['Phydeaux, RIP']}}

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

def test_overwrite2():
    data = {}
    data_overwrite2(data, 1, 2, 3, ['3'])
    assert data == {'1': {'2': {'3': ['3']}}}

    data = {'1001': {'LI': {'wh': ['10000']}}}
    data_overwrite2(data, 1001, 'LI', 'wh', ['10001'])
    assert data == {'1001': {'LI': {'wh': ['10001']}}}

