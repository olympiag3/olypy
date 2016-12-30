import dbck


def test_check_where_here():

    data = {'1001': {'LI': {'wh': ['1003']}},
            '1002': {'LI': {'wh': ['1003']}},
            '1003': {'LI': {'hl': ['1001', '1002']}}}

    assert dbck.check_where_here(data) == 0

    del data['1002']

    assert dbck.check_where_here(data) == 1

    del data['1003']

    assert dbck.check_where_here(data) == 1


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
