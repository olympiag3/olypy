import pytest
from collections import defaultdict

from oid import to_int
import turnparser


def test_parse_an_id():
    assert turnparser.parse_an_id('Foo [1024]') == '1024'
    with pytest.raises(ValueError):
        turnparser.parse_an_id('')
    with pytest.raises(ValueError):
        turnparser.parse_an_id('Foo [1234567]')


def test_split_into_sections():
    t = '''
Oleg's Olympians [ja1]
------------------------------------------------------------------------
asdf
Garrison log
------------------------------------------------------------------------
 1: 5027: Received nine pikes [75] from Babra [2233].
Oleg the Loudmouth [6940]
------------------------------------------------------------------------
 1: > press 0
'''
    ret = [
'''Oleg's Olympians [ja1]
------------------------------------------------------------------------

asdf
Garrison log
''',
'''Garrison log
------------------------------------------------------------------------

 1: 5027: Received nine pikes [75] from Babra [2233].
Oleg the Loudmouth [6940]
''',
'''Oleg the Loudmouth [6940]
------------------------------------------------------------------------

 1: > press 0
'''
        ]
    assert turnparser.split_into_sections(t) == ret


def test_parse_wait_args():
    vectors = [['wait top', [8]],
               ['wait time 7', [0, '7']],
               ['wait loc aa01', [6, '10001']],
               ['wait not day 7', [14, 1, '7']],
               ['wait item 1 100', [4, '1', '100']],  # 2 args
               ['wait item 1 100 day 7', [4, '1', '100', 1, '7']],
               ['wait flag blue 1001', [5, 'blue', '1001']],
               ['wait flag blue day 7', [5, 'blue', 1, '7']],
               ['wait flag blue 1001 day 7', [5, 'blue', '1001', 1, '7']]]

    for v in vectors:
        order, ar = v
        assert turnparser.parse_wait_args(order) == ar

    raising_vectors = [['wait time', IndexError],
                       ['wait item 1', IndexError],
                       ['wait item 1 day 3', ValueError],
                       ['wait flag blue blue day 7', ValueError],
                       ['wait loc blue', ValueError]]
    for v in raising_vectors:
        order, e = v
        with pytest.raises(e):
            turnparser.parse_wait_args(order)


def test_generate_move_args():
    tests = [[['29', '5', to_int('aa02'), to_int('aa01')], ['0', '0', '10002', '0', '0', '7', '10001', '0']]]
    for t in tests:
        print(len(t[0]))
        assert turnparser.generate_move_args(*t[0]) == t[1]


def test_split_order_args():
    tests = [['foo bar', ['foo', 'bar']],
             ['foo "bar baz"', ['foo', '"foo"']]]
    for t in tests:
        assert turnparser.split_order_args(t[0]) == t[1]


def test_canonicalize_order():
    tests = [['train something', 'make something'],
             ['sneak out', 'use 639 out'],
             ['go up', 'move up'],
             ['north', 'move n'],
             ['n', 'move n'],
             ['in', 'move in']]
    for t in tests:
        assert turnparser.canonicalize_order(t[0]) == t[1]


def test_fake_order():
    # fake_order(order, start_day, remaining, last_move_dest, unit, data)
    # uses data[unit]['LI']['wh'] for moves
    # XXXv0 todo CH mo set to days_since_epoch + remaining for moves

    tests = [[['move e', '10', '2', '10002', '1000'], {'ar': ['0', '0', '10002', '0', '0', '23', '10001', '0'],
                                                       'cs': ['2'],
                                                       'de': ['21'],
                                                       'li': ['move e'],
                                                       'pr': ['3'],
                                                       'st': ['1'],
                                                       'wa': ['2']}],
             [['sail e', '10', '2', '10002', '1000'], {'ar': ['0', '0', '10002', '0', '0', '23', '10001', '0'],
                                                       'cs': ['2'],
                                                       'de': ['21'],
                                                       'li': ['sail e'],
                                                       'pr': ['4'],
                                                       'st': ['1'],
                                                       'wa': ['2']}],
             [['collect 10 0 0', '29', '-1', 'x', 'x'], {'ar': ['10', '0', '0', '2', '0', '0', '0', '0'],
                                                         'cs': ['2'],
                                                         'de': ['2'],
                                                         'li': ['collect 10 0 0'],
                                                         'po': ['1'],
                                                         'pr': ['3'],
                                                         'st': ['1'],
                                                         'wa': ['-1']}],
             [['use 823 832', '29', '12', 'x', 'x'], {'ar': ['832', '0', '0', '0', '0', '0', '0', '823'],
                                                      'cs': ['2'],
                                                      'de': ['2'],
                                                      'li': ['use 823 832'],
                                                      'po': ['1'],
                                                      'pr': ['3'],
                                                      'st': ['1'],
                                                      'ue': ['1'],
                                                      'us': ['823'],
                                                      'wa': ['12']}]]


    data = {'1000': {'LI': {'wh': ['10001']}}}

    for t in tests:
        t[0].append(data)
        assert turnparser.fake_order(*t[0]) == t[1]


def test_parse_inventory():
    t = '''

      qty  name				     weight
      ---  ----				     ------
    3,929  gold [1]				  0  
	1  riding horse [52]		      1,000  ride 150
        1  Amulet of Halhere [b999]              10  +1 aura
        1  Dior [n999]                           10  +100 defense
        1  639 - Sneak in structure [b199]         1  

   639 - Sneak in structure [b199] permits study of the following skills:
      Sneak into structure [639] (requires Stealth)

    '''
    data = {}
    ret = ['1', 'gold', '0', '3929', 0, '',
           '52', 'riding horse', '1000', '1', 0, '',
           '60199', '639 - Sneak in structure', '1', '1', 0, '',
           '60999', 'Amulet of Halhere', '10', '1', '1', 'aura',
           '69999', 'Dior', '10', '1', '100', 'defense']
    inventory = turnparser.parse_inventory(t, '1000', data)
    assert inventory == ret

    il = ['1', '3929',
          '52', '1',
          '60199', '1',
          '60999', '1',
          '69999', '1']
    assert turnparser.reformat_inventory(inventory) == il

    unique_item_data = {'60199': {'IM': {'ms': ['639']},
                                  'IT': {'un': ['1000'], 'wt': ['1']},
                                  'firstline': ['60199 item scroll'],
                                  'na': ['639 - Sneak in structure']},
                        '60999': {'IM': {'ba': ['1']},
                                  'IT': {'un': ['1000'], 'wt': ['10']},
                                  'firstline': ['60999 item artifact'],
                                  'na': ['Amulet of Halhere']},
                        '69999': {'IM': {'db': ['100']},
                                  'IT': {'un': ['1000'], 'wt': ['10']},
                                  'firstline': ['69999 item artifact'],
                                  'na': ['Dior']}}
    assert data == unique_item_data


def test_parse_admit():
    t = '''

   admit 1933  zb1 1001
	       1002 2001 3001
   admit 8738  qm9  ez0

    '''
    ret = [['1933', to_int('zb1'), '1001', '1002', '2001', '3001'],
           ['8738', to_int('qm9'), to_int('ez0')]]
    assert turnparser.parse_admit(t) == ret


def test_parse_attitudes():
    t = '''

      defend   ad3  ez0  ig7  ja1  qm9
      Hostile  ad3
      neutral  ad3

    '''
    ret = {'defend': [to_int('ad3'), to_int('ez0'), to_int('ig7'), to_int('ja1'), to_int('qm9')],
           'hostile': [to_int('ad3')],
           'neutral': [to_int('ad3')]}
    assert turnparser.parse_attitudes(t) == ret

    t = '''

   defend   ad3  dk3  dq4  
            jq9

    '''
    ret = {'defend': [to_int('ad3'), to_int('dk3'), to_int('dq4'), to_int('jq9')]}
    assert turnparser.parse_attitudes(t) == ret


def test_parse_skills():
    t = '''
   Skills known:
      Combat [610]
	    Survive fatal wound [611]
      Stealth [630]
	    Conceal self [638], journeyman
    '''
    ret = ['610', '2', '21', '0', '0',
           '611', '2', '28', '0', '0',
           '630', '2', '28', '0', '0',
           '638', '2', '28', '5', '0']
    assert turnparser.parse_skills(t) == ret


def test_parse_partial_skills():
    t = '''
      Locate character [847], 7/21
      Raise undead [901], 0/21
    '''
    ret = ['847', '1', '7', '0', '0',
           '901', '0', '0', '0', '0']
    assert turnparser.parse_partial_skills(t) == ret


def test_parse_pending_trades():
    t = '''

      trade    price	qty   item
      -----    -----	---   ----
       sell	   7  9,849   clay pot [95]
       sell	   2  8,565   fish [87]
    '''
    ret = ['2', '95', '9849', '7', '0',  '0',  '0',  '0',
           '2', '87', '8565', '2', '0',  '0',  '0',  '0']
    assert turnparser.parse_pending_trades(t) == ret


def test_parse_location_top():
    t = 'Forest [ah08], forest, in Acaren, wilderness'
    ret = ['Forest', to_int('ah08'), 'forest', 0, 'Acaren', 0, 0, 0]
    assert turnparser.parse_location_top(t) == ret
    assert turnparser.regions_set == set(('Cloudlands', 'Great Sea', 'Hades', 'Undercity',
                                          'Acaren', 'Nowhere'))


def test_parse_a_structure():
    pass  # tested by test_parse_location


def test_parse_a_character():
    pass  # tested by test_parse_location


def test_parse_a_structure_or_character():
    pass  # tested by test_parse_location


def test_parse_routes_leaving():
    with pytest.raises(ValueError):
        turnparser.parse_routes_leaving('South, to Forest, Ishdol, 2 days')
    with pytest.raises(ValueError):
        turnparser.parse_routes_leaving('South, to Forest [badiddd], Ishdol, 2 days')
    with pytest.raises(ValueError):
        turnparser.parse_routes_leaving('South, to Invalid [bx39], Ishdol, 2 days')
    with pytest.raises(ValueError):
        turnparser.parse_routes_leaving('South, to Forest [bx39], Ishdol, X days')
    with pytest.raises(ValueError):
        turnparser.parse_routes_leaving('South, to Forest [bx39], Ishdol')

    # This test uses a grab-bag of stuff that would never appear together:
    t = '''
    West, swamp, to The Dark Lands [cv34], Teysel, 2 days
    West, to Swamp [cv34], Teysel, 2 days
    West, swamp, to The Dark Lands [cv34], 14 days
    West, to Swamp [cv34], 14 days
    South, city, to Hornmar [g02], Olbradim, 1 day
    South, to Swamp [ac21], Olbradim, impassable
    Out, to Forest [bg36], 1 day
    Underground, to Hades [hs70], Hades, hidden, 1 day
    Secret pass, to Forest [bw22], hidden, 8 days
    Rocky channel, to Mountain [bz63], hidden, 2 days
    Forest, to The Dark Lands [cn76], Gothin, 1 day
    To Osswid's Roundship [6014], 0 days
    '''
    r = [{'days': '2',
          'destination': '15634',
          'dir': 'west',
          'kind': 'swamp',
          'name': 'The Dark Lands',
          'region': 'Teysel'},
         {'days': '2',
          'destination': '15634',
          'dir': 'west',
          'kind': 'swamp',
          'name': 'Swamp',
          'region': 'Teysel'},
         {'days': '14',
          'destination': '15634',
          'dir': 'west',
          'kind': 'swamp',
          'name': 'The Dark Lands'},
         {'days': '14',
          'destination': '15634',
          'dir': 'west',
          'kind': 'swamp',
          'name': 'Swamp'},
         {'days': '1',
          'destination': '57262',
          'dir': 'south',
          'kind': 'city',
          'name': 'Hornmar',
          'region': 'Olbradim'},
         {'destination': '10221',
          'dir': 'south',
          'impassable': 1,
          'kind': 'swamp',
          'name': 'Swamp',
          'region': 'Olbradim'},
         {'days': '1',
          'destination': '12536',
          'dir': 'out',
          'kind': 'forest',
          'name': 'Forest'},
         {'days': '1',
          'destination': '23470',
          'dir': 'hades road',
          'hidden': 1,
          'kind': 'underground',
          'name': 'Hades',
          'region': 'Hades'},
         {'days': '8',
          'destination': '13722',
          'dir': 'road road',
          'hidden': 1,
          'kind': 'forest',
          'name': 'Forest'},
         {'days': '2',
          'destination': '13963',
          'dir': 'road road',
          'hidden': 1,
          'kind': 'mountain',
          'name': 'Mountain'},
         {'days': '1',
          'destination': '15076',
          'dir': 'faery road',
          'kind': 'forest',
          'name': 'The Dark Lands',
          'region': 'Gothin'},
         {'days': '0',
          'destination': '6014',
          'dir': 'faery road',
          'kind': 'ship',
          'name': "Osswid's Roundship"}]

    assert turnparser.parse_routes_leaving(t) == r

    expected = {'10221': {'LI': {'wh': ['Olbradim'], 'hl': ['57262']},
                          'LO': {'pd': ['10101', 0, 0, 0]},
                          'firstline': ['10221 loc swamp'],
                          'il': ['66', '1', '96', '50', '101', '1', '274', '1'],
                          'na': ['Swamp']},
                '12536': {'LI': {'wh': ['Camaris']},
                          'LO': {'pd': [0, 0, 0, 0]},
                          'firstline': ['12536 loc forest'],
                          'il': ['77', '30', '10', '10', '96', '50', '101', '1', '276', '1', '274', '1'],
                          'na': ['Forest']},
                '13722': {'LI': {'wh': ['Camaris']},
                          'LO': {'pd': [0, 0, 0, 0]},
                          'firstline': ['13722 loc forest'],
                          'il': ['77', '30', '10', '10', '96', '50', '101', '1', '276', '1', '274', '1'],
                          'na': ['Forest']},
                '13963': {'LI': {'wh': ['Camaris']},
                          'LO': {'pd': [0, 0, 0, 0]},
                          'firstline': ['13963 loc mountain'],
                          'il': ['78', '50', '10', '10', '96', '50', '101', '1', '275', '1'],
                          'na': ['Mountain']},
                '15076': {'LI': {'wh': ['Gothin']},
                          'LO': {'pd': [0, 0, 0, 0]},
                          'firstline': ['15076 loc forest'],
                          'il': ['77', '30', '10', '10', '96', '50', '101', '1', '276', '1', '274', '1'],
                          'na': ['The Dark Lands']},
                '15634': {'LI': {'wh': ['Teysel']},
                          'LO': {'pd': [0, '10101', 0, 0]},
                          'firstline': ['15634 loc swamp'],
                          'il': ['66', '1', '96', '50', '101', '1', '274', '1'],
                          'na': ['The Dark Lands']},
                '23470': {'LI': {'wh': ['Hades']},
                          'LO': {'pd': [0, 0, 0, 0]},
                          'firstline': ['23470 loc underground'],
                          'il': ['101', '1', '96', '50'],
                          'na': ['Hades']},
                '57262': {'LI': {'wh': ['10221']},
                          'firstline': ['57262 loc city'],
                          'il': ['10', '10', '294', '1', '277', '5', '96', '100', '101', '1'],
                          'na': ['Swamp']}}

    data = {}
    turnparser.make_locations_from_routes(r, '10101', 'Camaris', data)
    assert data == expected

    data['10101'] = {'LI': {'wh': ['Camaris']},
                     'LO': {'pd': [0, 0, 0, 0]},
                     'firstline': ['10101 loc forest'],
                     'il': ['77', '30', '10', '10', '96', '50', '101', '1', '276', '1', '274', '1'],
                     'na': ['Forest']}
    turnparser.make_direction_routes(r, '10101', 'forest', data)
    assert data['10101']['LO']['pd'] == [0, 0, '10221', '15634']


def test_parse_inner_locations():
    t = '''   Oleg the Loudmouth [6940], with 14 peasants, 11 workers
   Woodrow Call [1771], with 19 peasants, accompanied by:
      Pea Eye Parker [2480], with two peasants
   Eric [2370], "A hooded cloak pulled up shrouding his face", with
   15 peasants, five workers

   Tub 1 [3622], roundship-in-progress, 46% completed, 19% loaded, owner:
      Yoyo 2 [2259], with 20 workers, accompanied by:
\t Yoyo 5 [3984], with two peasants, six sailors
'''
    ret = {'1001': {'LI': {'hl': ['6940', '1771', '2370', '3622']}},
           '1771': {'LI': {'hl': ['2480'], 'wh': ['1001'], 'hl': ['2480']},
                    'firstline': ['1771 char 0'],
                    'il': ['10', '19'],
                    'na': ['Woodrow Call']},
           '2259': {'LI': {'hl': ['3984'], 'wh': ['3622'], 'hl': ['3984']},
                    'firstline': ['2259 char 0'],
                    'il': ['11', '20'],
                    'na': ['Yoyo 2']},
           '2370': {'LI': {'wh': ['1001']},
                    'firstline': ['2370 char 0'],
                    'il': ['10', '15', '11', '5'],
                    'na': ['Eric']},
           '2480': {'LI': {'wh': ['1771']},
                    'firstline': ['2480 char 0'],
                    'il': ['10', '2'],
                    'na': ['Pea Eye Parker']},
           '3622': {'LI': {'hl': ['2259'], 'wh': ['1001'], 'hl': ['2259']},
                    'SL': {'eg': ['230'], 'er': ['500']},
                    'firstline': ['3622 ship roundship-in-progress'],
                    'na': ['Tub 1']},
           '3984': {'LI': {'wh': ['2259']},
                    'firstline': ['3984 char 0'],
                    'il': ['10', '2', '19', '6'],
                    'na': ['Yoyo 5']},
           '6940': {'LI': {'wh': ['1001']},
                    'firstline': ['6940 char 0'],
                    'il': ['10', '14', '11', '11'],
                    'na': ['Oleg the Loudmouth']}}

    idint = '1001'
    things = {}

    turnparser.parse_inner_locations(idint, t.expandtabs(), things)
    assert things == ret

    t = '''   Tub 14 [5614], roundship, 83% loaded, defense 10, owner:
 *    Alice [1238], with three workers, six soldiers, 49 pikemen,
      eight sailors, 46 crossbowmen, accompanied by:
 *       Bob [8140], with 94 soldiers
   Tub 19 [2219], roundship, 83% loaded, defense 10, 5% damaged, owner:
 *    Carol [2437], with 100 soldiers, eight sailors, accompanied by:
 *       Dan [1229], wielding Big Fork [z999], wearing Rugged
         vest [d999], with 83 pikemen, four peasants
'''
    ret = {'1229': {'LI': {'wh': ['2437']},
                    'firstline': ['1229 char 0'],
                    'il': ['78999', '1', '62999', '1', '16', '83', '10', '4'],
                    'na': ['Dan']},
           '1238': {'LI': {'hl': ['8140'], 'wh': ['5614']},
                    'firstline': ['1238 char 0'],
                    'il': ['11', '3', '12', '6', '16', '49', '19', '8', '21', '46'],
                    'na': ['Alice']},
           '12399': {'LI': {'hl': ['5614', '2219']}},
           '2219': {'LI': {'hl': ['2437'], 'wh': ['12399']},
                    'SL': {'da': ['5d'], 'df': ['10']},
                    'firstline': ['2219 ship roundship'],
                    'na': ['Tub 19']},
           '2437': {'LI': {'hl': ['1229'], 'wh': ['2219']},
                    'firstline': ['2437 char 0'],
                    'il': ['12', '100', '19', '8'],
                    'na': ['Carol']},
           '5614': {'LI': {'hl': ['1238'], 'wh': ['12399']},
                    'SL': {'df': ['10']},
                    'firstline': ['5614 ship roundship'],
                    'na': ['Tub 14']},
           '8140': {'LI': {'wh': ['1238']},
                    'firstline': ['8140 char 0'],
                    'il': ['12', '94'],
                    'na': ['Bob']}}

    idint = '12399'
    things = {}

    turnparser.parse_inner_locations(idint, t.expandtabs(), things)
    assert things == ret


def test_parse_market_report():
    t = '''
  trade    who   price    qty   wt/ea   item      
  -----    ---   -----    ---   -----   ----    
    buy    m19       7     17       5   clay pots [95]    
    buy    m19      65      3   1,000   riding horses [52]    
    buy    m19      83     38      43   tea [t526]    
   sell    m19     100      5   2,000   oxen [76]    
   sell    2002     80      3   2,000   oxen [76]    
   sell    m19     130      3   1,000   riding horses [52]    
   sell    m19      82     41      80   fine cloaks [g950]    
   sell    m19      11     27     100   salt [r384]    
    '''
    r_all = ['1',           '95', '17',   '7', '0', '0', '0', '0',
             '4',           '95', '17',   '7', '0', '0', '0', '0',
             '1',           '52',  '3',  '65', '0', '0', '0', '0',
             '4',           '52',  '3',  '65', '0', '0', '0', '0',
             '1', to_int('t526'), '38',  '83', '0', '0', '0', '0',
             '4', to_int('t526'), '38',  '83', '0', '0', '0', '0',
             '2',           '76',  '5', '100', '0', '0', '0', '0',
             '3',           '76',  '5', '100', '0', '0', '0', '0',
             '2',           '76',  '3',  '80', '0', '0', '0', '0',
             '3',           '76',  '3',  '80', '0', '0', '0', '0',
             '2',           '52',  '3', '130', '0', '0', '0', '0',
             '3',           '52',  '3', '130', '0', '0', '0', '0',
             '2', to_int('g950'), '41',  '82', '0', '0', '0', '0',
             '3', to_int('g950'), '41',  '82', '0', '0', '0', '36',
             '2', to_int('r384'), '27',  '11', '0', '0', '0', '0',
             '3', to_int('r384'), '27',  '11', '0', '0', '0', '36',
             '1',           '93', '80',  '17', '0', '0', '0', '0',
             '4',           '93', '80',  '17', '0', '0', '0', '0']
    r_cty = ['1',           '95', '17',   '7', '0', '0', '0', '0',
             '4',           '95', '17',   '7', '0', '0', '0', '0',
             '1',           '52',  '3',  '65', '0', '0', '0', '0',
             '4',           '52',  '3',  '65', '0', '0', '0', '0',
             '1', to_int('t526'), '38',  '83', '0', '0', '0', '0',
             '4', to_int('t526'), '38',  '83', '0', '0', '0', '0',
             '2',           '76',  '5', '100', '0', '0', '0', '0',
             '3',           '76',  '5', '100', '0', '0', '0', '0',
             '2',           '52',  '3', '130', '0', '0', '0', '0',
             '3',           '52',  '3', '130', '0', '0', '0', '0',
             '2', to_int('g950'), '41',  '82', '0', '0', '0', '0',
             '3', to_int('g950'), '41',  '82', '0', '0', '0', '36',
             '2', to_int('r384'), '27',  '11', '0', '0', '0', '0',
             '3', to_int('r384'), '27',  '11', '0', '0', '0', '36',
             '1',           '93', '80',  '17', '0', '0', '0', '0',
             '4',           '93', '80',  '17', '0', '0', '0', '0']
    data = {}
    data_out = {'64950': {'IT': {'bp': ['82'], 'pl': ['fine cloaks'], 'wt': ['80']},
                          'firstline': ['64950 item tradegood'],
                          'na': ['fine cloaks']},
                '72384': {'IT': {'bp': ['11'], 'pl': ['salt'], 'wt': ['100']},
                          'firstline': ['72384 item tradegood'],
                          'na': ['salt']},
                '74526': {'IT': {'bp': ['83'], 'pl': ['tea'], 'wt': ['43']},
                          'firstline': ['74526 item tradegood'],
                          'na': ['tea']}}

    assert turnparser.parse_market_report(t, data) == r_all
    assert data == data_out

    data = {}
    data_out = {'64950': {'IT': {'bp': ['82'], 'pl': ['fine cloaks'], 'wt': ['80']},
                          'firstline': ['64950 item tradegood'],
                          'na': ['fine cloaks']},
                '72384': {'IT': {'bp': ['11'], 'pl': ['salt'], 'wt': ['100']},
                          'firstline': ['72384 item tradegood'],
                          'na': ['salt']},
                '74526': {'IT': {'bp': ['83'], 'pl': ['tea'], 'wt': ['43']},
                          'firstline': ['74526 item tradegood'],
                          'na': ['tea']}}

    assert turnparser.parse_market_report(t, data, include=to_int('m19')) == r_cty
    assert data == data_out


def test_parse_seen_here():
    pass  # same as test_parse_inner_locations


def test_parse_ships_sighted():
    pass  # same as test_parse_inner_locations


def test_analyze_regions():
    t = '''A
 B
C
D
 E
    '''
    ret = {'A': set(('C', 'D')), 'C': set(('D',))}
    region_after = defaultdict(set)
    turnparser.analyze_regions(t, region_after)
    assert region_after == ret


def test_match_line():
    t = '''
29: Meditate for six days.
   
   Location:	   Ship of Fools [9309], in province Plain [aq54], in Hilrun
   Loyalty:	   Oath-2
   Health:	   71% (getting better)
   Combat:	   attack 80, defense 81, missile 0
		   behind 0  (front line in combat)
   Break point:    50%
   use	638 1	   (concealing self)
   Pledged to:	   Tom [2527]
   Pledged to us:  Kelly [8412]
   
   Current aura:   36
   Maximum aura:   102 (4+98)

    '''
    health, = turnparser.match_line(t, 'Health:', capture=r'(\d+)')
    assert health == '71'

    attack, defense, missile = turnparser.match_line(t, 'attack', capture=r'(\d+), defense (\d+), missile (\d+)')
    assert attack == '80'
    assert defense == '81'
    assert missile == '0'

    ca, = turnparser.match_line(t, 'Current aura:')
    assert ca == '36'

    foo, = turnparser.match_line(t, 'Foo:')
    assert foo is None

    t = 'Province controlled by Castle [8103], castle, in Plain [ar16]'
    cc, = turnparser.match_line(t, 'Province controlled by', capture=r'.*?\[([0-9]{4})\]')
    assert cc == '8103'


def test_remove_visions():
    t = '''
26: Received 2 gold from Garrison [2346].
27: Osswid the Brave [7651] receives a vision of RC-2080 [2080]:
27:
27: Location:       Tomb in swamp [4082], in province Swamp [aq21], in
27: Received 2 gold from Garrison [1610].
27: > use Orb
28: foo
    '''
    r = '''
26: Received 2 gold from Garrison [2346].
28: foo
    '''
    v = '''27: Osswid the Brave [7651] receives a vision of RC-2080 [2080]:
27:
27: Location:       Tomb in swamp [4082], in province Swamp [aq21], in
27: Received 2 gold from Garrison [1610].
27: > use Orb
'''
    s, visions = turnparser.remove_visions(t)
    assert s == r
    assert len(visions) == 1
    assert visions[0] == v
    # XXXv2 note that currently multiple orbs fall into the same vision!


def test_remove_days():
    t = '''26: Received 2 gold from Garrison [2346].

27: foo

    
bar
    '''
    nondays, days = turnparser.remove_days(t)
    assert nondays == '\n\n    \nbar\n    \n'
    assert days == '26: Received 2 gold from Garrison [2346].\n27: foo\n'


def test_parse_turn_header():
    t = '''

Olympia G4 turn 2
Report for Oleg's Olympians [ja1].
Season "Snowmelt", month 2, in the year 1.


   
   Game totals:
      Players:		       80
      Controlled units:       305
      Other units:	      262
   
   Faction [ja1]			  rank	 
   -------------			  ----	 
   Characters:			       3  49th	 
   Men:				      25  21st	 
   Gold:			     284  49th	 
   Land controlled:		       0  1st	 
   Skills known:		    0/74  28th	 
   Spells known:		    0/79  10th	 
   Provinces visited:		0/14,914  45th	 
   
   
Noble points:  11     (0 gained, 7 spent)
The next NP will be received at the end of turn 8.

The next five nobles formed will be:  8012 6124 4547 5157 3518

200 fast study days are left.

Location			   Stack
--------			   -----
Grinter
  Forest [bf23]
    Wildefort [h63]
      HMS Pinafore [9651]	   Osswid the Destroyer [7271]
				     Candide the Captain [3175]

    '''
    ret = {'3518': {'firstline': ['3518 unform 0']},
           '4547': {'firstline': ['4547 unform 0']},
           '5157': {'firstline': ['5157 unform 0']},
           '52341': {'firstline': ['52341 player pl_regular'],
                     'na': ["Oleg's Olympians"],
                     'PL': {'em': ['example@example.com'],
                            'fn': ['Full Name'],
                            'fs': ['200'],
                            'ft': ['1'],
                            'kn': ['69'],
                            'lt': ['2'],
                            'np': ['11'],
                            'uf': ['8012', '6124', '4547', '5157', '3518'],
                            'un': []}},
           '6124': {'firstline': ['6124 unform 0']},
           '8012': {'firstline': ['8012 unform 0']}}

    assert turnparser.parse_turn_header({}, t, True) == ('52341', '2', ret)

    t = '''

Olympia G4 turn 1
Initial Position Report for Oleg's Olympians [ja1].
Season "Fierce winds", month 1, in the year 1.

Welcome to Olympia G4!

This is an initial position report for your new faction.
You are player ja1, "Oleg's Olympians".

The next turn will be turn 2.


Noble points:  18     (0 gained, 0 spent)
The next NP will be received at the end of turn 8.

The next five nobles formed will be:  7815 1933 8012 6124 4547

200 fast study days are left.

    '''
    ret = {'1933': {'firstline': ['1933 unform 0']},
           '4547': {'firstline': ['4547 unform 0']},
           '52341': {'PL': {'em': ['example@example.com'],
                            'fn': ['Full Name'],
                            'fs': ['200'],
                            'ft': ['1'],
                            'kn': ['69'],
                            'lt': ['1'],
                            'np': ['18'],
                            'uf': ['7815', '1933', '8012', '6124', '4547'],
                            'un': []},
                     'firstline': ['52341 player pl_regular'],
                     'na': ["Oleg's Olympians"]},
           '6124': {'firstline': ['6124 unform 0']},
           '7815': {'firstline': ['7815 unform 0']},
           '8012': {'firstline': ['8012 unform 0']}}

    assert turnparser.parse_turn_header({}, t, True) == ('52341', '1', ret)


def test_parse_faction():
    t = '''

Admit permissions:

   admit 4256  ja1 ad3
   admit 7611 6124
   admit 9724  ja1
   admit 9774  ja1

Declared attitudes:
   defend   ad3
   hostile  ez0
   neutral  hv5  hx7

Unclaimed items:

      qty  name				     weight
      ---  ----				     ------
    4,330  gold [1]				  0  
	5  riding horses [52]		      5,000  ride 750
      100  stone [78]			     10,000  

    '''
    ret = {'ad': [to_int('ad3')],
           'ah': [to_int('ez0')],
           'am': [['4256', '52341', '50033'],
                  ['7611', '6124'],
                  ['9724', '52341'],
                  ['9774', '52341']],
           'an': [to_int('hv5'), to_int('hx7')],
           'il': ['1', '4330',
                  '52', '5',
                  '78', '100']}
    data = {'1000': {}}
    turnparser.parse_faction(t, '1000', data)
    assert data['1000'] == ret


def test_analyze_garrison_list():
    t = '''  2617	aj08   10   20	 50   15   8103 4797 7271 6839	... 2527
  4514	aj09   10   20	 50   15   8103 4797 7271 6839	... 2527    '''
    data = {}
    r = {'10708': {'LI': {'hl': ['2617']}},
         '10709': {'LI': {'hl': ['4514']}},
         '207': {'PL': {'un': ['2617', '4514']}},
         '2617': {'CH': {'at': ['60'],
                         'df': ['60'],
                         'gu': ['1'],
                         'he': ['-1'],
                         'lk': ['4'],
                         'lo': ['207']},
                  'CM': {},
                  'LI': {'wh': ['10708']},
                  'MI': {'ca': ['g'], 'gc': ['8103']},
                  'firstline': ['2617 char garrison'],
                  'il': ['12', '10']},
         '4514': {'CH': {'at': ['60'],
                         'df': ['60'],
                         'gu': ['1'],
                         'he': ['-1'],
                         'lk': ['4'],
                         'lo': ['207']},
                  'CM': {},
                  'LI': {'wh': ['10709']},
                  'MI': {'ca': ['g'], 'gc': ['8103']},
                  'firstline': ['4514 char garrison'],
                  'il': ['12', '10']}}
    turnparser.analyze_garrison_list(t, data, everything=True)
    assert data == r


def test_parse_garrison_log():
    # XXXv2
    pass


def test_resolve_fake_items():
    # XXXv0 should test potion, palantir, farcast, auraculum

    data = {'59111': {'firstline': ['59111 item 0'],
                      'na': ['Magic potion'],
                      'IT': {'wt': ['1'], 'un': ['1111']},
                      'fake': 'yes'},
            '65001': {'firstline': ['65001 item palantir'],
                      'na': ['Magic potion'],
                      'IT': {'wt': ['2'], 'un': ['1111']},
                      'fake': 'yes'},
            '65002': {'firstline': ['65002 item palantir'],
                      'na': ['Magic potion'],
                      'IT': {'wt': ['2'], 'un': ['1111']},
                      'fake': 'yes'},
            '67001': {'firstline': ['67001 item 0'],
                      'na': ['Magic potion'],
                      'IT': {'wt': ['1'], 'un': ['1111']},
                      'fake': 'yes'},
            '71001': {'firstline': ['671001 item 0'],
                      'na': ['Magic potion'],
                      'IT': {'wt': ['3'], 'un': ['1111']},
                      'fake': 'yes'},
            '1111': {'firstline': ['1111 char 0']}}

    turnparser.global_days = {'1111': '''
01: > Use 691
01: Created foo [a111].
01: > Use 894
01: Produced one foo [h001]
01: > use 849 ab00
01: > use 849 aa00
01: > use 851
01: Created foo [k001].
01: > use 881 38
01: Produced one foo [q001]
'''}

    turnparser.resolve_fake_items(data)

    print(data['59111'])
    assert data['59111']['IM']['uk'][0] == '2'

    assert data['65001']['IM']['uk'][0] == '4'
    assert data['65002']['IM']['uk'][0] == '4'

    assert data['67001']['IM']['uk'][0] == '5'
    assert data['67001']['IM']['pc'][0] == '10000'

    assert data['71001']['IM']['au'][0] == '38'
    assert data['1111']['CM']['ar'][0] == '71001'

    del data['65002']  # this one is still fake
    for ident in data:
        if ' item ' in data[ident]['firstline'][0]:
            assert 'fake' not in data[ident]


def test_parse_character():
    t = '''
Osswid the Destroyer [7271]
------------------------------------------------------------------------
 0: > stop
 0: Interrupt current order.
 0: Trained nine soldiers.
 1: > press 0
 1: Press posted.
 1: > train 12
11: Trained 11 soldiers.
12: > make 74
12: Don't have any iron [79].
12: > train 20
12: Don't have any longswords [74].
12: > wait item 10 1
14: Received ten peasants [10] from Osswid the Brave [2597].
14: Wait finished: Osswid the Destroyer has ten peasants.
14: Received two iron [79] from Osswid the Brave [2597].
14: > train 12
23: Trained ten soldiers.
29: Received ten peasants [10] from Osswid the Brave [2597].
30: Collected 1,479 gold from owned provinces.
30: Collected 265 gold in taxes.
30: Paid maintenance of 944 gold.
   
   Location:	   Amber Keep [4256], in Inte [v25], in province
		   Mountain [bc19], in Grinter
   Loyalty:	   Oath-2
   Health:	   100%
   Combat:	   attack 89, defense 168, missile 50
		   behind 0  (front line in combat)
   Break point:    0% (fight to the death)
   use  638 1      (concealing self)
   Receive Vision: 2 protection
   Pledged to:	   Yoyo 6 [6839]
   Pledged to us:  Tom [1753]
		   Gus McCrae [2554]
		   Moriarity [4168]
		   Yoyo [4797]
		   Francisco Lopez [6710]
		   Tom [8578]
   
   Current aura:   4
   Maximum aura:   4
   
   Declared attitudes:
      defend   qm9  zb1
   
   Skills known:
      Shipcraft [600]
	    Sailing [601], apprentice
	    Shipbuilding [602], apprentice
	    Fishing [603], apprentice
      Combat [610]
	    Survive fatal wound [611]
	    Fight to the death [612]
	    Construct catapult [613], apprentice
	    Defense [614], adept
	    Archery [615], apprentice
	    Swordplay [616], adept
	    Weaponsmithing [617], master
      Construction [680]
	    Construct siege tower [681], apprentice
	    Stone quarrying [682], apprentice
      Mining [720]
	    Mine iron [721], apprentice
	    Mine gold [722], apprentice
      Scrying [840]
	    Scry location [841], apprentice
	    Ciphered writing of Areth-Pirn [842], apprentice
	    Create magical barrier [845], apprentice
   
   Partially known skills:
      Magic [800], 7/28
      Gatecraft [860], 7/35
   
   Inventory:
	 qty  name				weight
	 ---  ----				------
      26,834  gold [1]				     0	
	  10  peasants [10]			 1,000	cap 1,000 (1,1,0)
	 380  soldiers [12]			38,000	cap 38,000 (5,5,0)
	   1  pikeman [16]			   100	cap 100 (5,30,0)
	  29  blessed soldiers [17]		 2,900	cap 2,900 (5,5,0)
	  28  swordsmen [20]			 2,800	cap 2,800 (15,15,0)
	 303  stone [78]			30,300	
	   2  iron [79]				    20	
	  11  woven baskets [94]		    11	
	   1  drum [98]				     2	
						======
						75,133

   Capacity:  30,333/44,900 land (67%)
   
   Pending trades:
   
      trade    price	qty   item
      -----    -----	---   ----
       sell	   7	100   clay pot [95]
   
    '''
    ret = {'50033': {'PL': {'kn': ['600', '601', '602', '603', '610', '611', '612',
                                   '613', '614', '615', '616', '617', '680', '681',
                                   '682', '720', '721', '722', '840', '841', '842',
                                   '845', '800', '860'],
                            'un': ['7271']}},
           '7271': {'firstline': ['7271 char 0'],
                    'na': ['Osswid the Destroyer'],
                    'il': ['1', '26834',
                           '10', '10',
                           '12', '380',
                           '16', '1',
                           '17', '29',
                           '20', '28',
                           '78', '303',
                           '79', '2',
                           '94', '11',
                           '98', '1'],
                    'CH': {'ad': [to_int('qm9'), to_int('zb1')],
                           'at': ['89'],
                           'bp': ['0'],
                           'df': ['168'],
                           'he': ['100'],
                           'lk': ['2'],
                           'lo': ['50033'],
                           'lr': ['2'],
                           'mi': ['50'],
                           'sl': ['600', '2', '21', '0', '0',
                                  '601', '2', '14', '0', '0',
                                  '602', '2', '14', '0', '0',
                                  '603', '2', '14', '0', '0',
                                  '610', '2', '21', '0', '0',
                                  '611', '2', '28', '0', '0',
                                  '612', '2', '28', '0', '0',
                                  '613', '2', '14', '0', '0',
                                  '614', '2', '14', '12', '0',
                                  '615', '2', '21', '0', '0',
                                  '616', '2', '14', '12', '0',
                                  '617', '2', '14', '21', '0',
                                  '680', '2', '21', '0', '0',
                                  '681', '2', '14', '0', '0',
                                  '682', '2', '14', '0', '0',
                                  '720', '2', '21', '0', '0',
                                  '721', '2', '14', '0', '0',
                                  '722', '2', '14', '0', '0',
                                  '840', '2', '35', '0', '0',
                                  '841', '2', '21', '0', '0',
                                  '842', '2', '21', '0', '0',
                                  '845', '2', '21', '0', '0',
                                  '800', '1', '7', '0', '0',
                                  '860', '1', '7', '0', '0']},
                    'CM': {'ca': ['4'],
                           'hs': ['1'],
                           'im': ['1'],
                           'ma': ['4'],
                           'hs': ['1'],
                           'pl': ['6839'],
                           'vp': ['2']},
                    'LI': {'wh': ['4256']}}}
    data = {}
    turnparser.parse_character('Osswid the Destroyer', '7271', '50033', t, data)
    assert data == ret


def test_parse_location():
    t = '''Forest [bf23], forest, in Grinter, safe haven, civ-2
------------------------------------------------------------------------
Routes leaving Forest:
   North, to Forest [bd23], 8 days
   East, to Ocean [bf24], Great Sea, impassable
   South, to Ocean [bg23], Great Sea, impassable
   West, to Forest [bf22], 8 days

Inner locations:
   Wildefort [h63], port city, safe haven, 1 day
   A magical barrier surrounds Wildefort [h63].

Seen here:
   Gus McCrae [2554], with five peasants, accompanied by:
      New noble [6386], with one peasant, one worker

    '''
    r = {'12323': {'LI': {'wh': ['Grinter']},
                   'LO': {'pd': [0, 0, '12423', 0]},
                   'firstline': ['12323 loc forest'],
                   'il': ['77', '30', '10', '10', '96', '50', '101', '1', '276', '1', '274', '1'],
                   'na': ['Forest']},
         '12422': {'LI': {'wh': ['Grinter']},
                   'LO': {'pd': [0, '12423', 0, 0]},
                   'firstline': ['12422 loc forest'],
                   'il': ['77', '30', '10', '10', '96', '50', '101', '1', '276', '1', '274', '1'],
                   'na': ['Forest']},
         '12423': {'LI': {'hl': ['57423'], 'wh': ['Grinter']},
                   'LO': {'pd': ['12323', '12424', '12523', '12422']},
                   'SL': {'sh': ['1']},
                   'firstline': ['12423 loc forest'],
                   'il': ['77', '30', '10', '10', '96', '50', '101', '1', '276', '1', '274', '1'],
                   'na': ['Forest']},
         '12424': {'LI': {'wh': ['Great Sea']},
                   'LO': {'pd': [0, 0, 0, '12423']},
                   'firstline': ['12424 loc ocean'],
                   'il': ['59', '30', '87', '50', '274', '1', '275', '1', '276', '1'],
                   'na': ['Ocean']},
         '12523': {'LI': {'wh': ['Great Sea']},
                   'LO': {'pd': ['12423', 0, 0, 0]},
                   'firstline': ['12523 loc ocean'],
                   'il': ['59', '30', '87', '50', '274', '1', '275', '1', '276', '1'],
                   'na': ['Ocean']},
         '57423': {'LI': {'wh': ['12423']},
                   'SL': {'sh': ['1']},
                   'firstline': ['57423 loc city'],
                   'il': ['10', '10', '294', '1', '277', '5', '96', '100', '101', '1'],
                   'na': ['Wildefort']}}

    data = {}
    turnparser.parse_location(t, to_int('ja1'), False, data)
    assert data == r
