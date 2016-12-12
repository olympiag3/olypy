import pytest

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


def test_parse_inventory():
    t = '''

      qty  name				     weight
      ---  ----				     ------
    3,929  gold [1]				  0  
	1  riding horse [52]		      1,000  ride 150
        1  Amulet of Halhere [b999]              10  +1 aura
        1  Dior [n999]                           10  +100 defense
        1  639 - Sneak in structure [b132]         1  

    '''
    data = {}
    ret = ['1', 'gold', '0', '3929', 0, '',
           '52', 'riding horse', '1000', '1', 0, '',
           '60132', '639 - Sneak in structure', '1', '1', 0, '',
           '60999', 'Amulet of Halhere', '10', '1', '1', 'aura',
           '69999', 'Dior', '10', '1', '100', 'defense']
    assert turnparser.parse_inventory(t, '1000', data) == ret
    unique_item_data = {'60132': {'IT': {'un': ['1000'], 'wt': ['1']},
                                  'firstline': ['60132item 0'],
                                  'na': ['Fake 639 - Sneak in structure']},
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
                                          'Acaren',))


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
    South, to Ocean [ac21], Great Sea, impassable
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
         {'destination': '10221',
          'dir': 'south',
          'impassable': 1,
          'kind': 'ocean',
          'name': 'Ocean',
          'region': 'Great Sea'},
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
    stack = ['6940', '1771', 'down', '2480', 'up', '2370', '3622', 'down', '2259', 'down', '3984']
    things = {'1771': {'firstline': ['1771 char 0'], 'il': {'10': [19]}, 'na': ['Woodrow Call']},
              '2259': {'firstline': ['2259 char 0'], 'il': {'11': [20]}, 'na': ['Yoyo 2']},
              '2370': {'firstline': ['2370 char 0'], 'il': {'10': [15], '11': [5]}, 'na': ['Eric']},
              '2480': {'firstline': ['2480 char 0'], 'il': {'10': [2]}, 'na': ['Pea Eye Parker']},
              '3622': {'firstline': ['3622 ship roundship-in-progress'], 'SL': {'eg': ['230'], 'er': [500]}, 'na': ['Tub 1']},
              '3984': {'firstline': ['3984 char 0'], 'il': {'10': [2], '19': [6]}, 'na': ['Yoyo 5']},
              '6940': {'firstline': ['6940 char 0'], 'il': {'10': [14], '11': [11]}, 'na': ['Oleg the Loudmouth']}}

    s, t = turnparser.parse_inner_locations(t)
    assert s == stack
    assert t == things


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
    r = ['1',           '95', '17',   '7', '0', '0', '0', '0',
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

    assert turnparser.parse_market_report(t) == r


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
    ret = {'A': ['C', 'D'], 'C': ['D']}
    region_after = {}
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
28: foo
    '''
    r = '''
26: Received 2 gold from Garrison [2346].
28: foo
    '''
    v = '''27: Osswid the Brave [7651] receives a vision of RC-2080 [2080]:
27:
27: Location:       Tomb in swamp [4082], in province Swamp [aq21], in
'''
    s, visions = turnparser.remove_visions(t)
    assert s == r
    assert len(visions) == 1
    assert visions[0] == v


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
    ret = {'52341': {'firstline': ['52341 player pl_regular'],
                     'na': ["Oleg's Olympians"],
                     'PL': {'fs': ['200'],
                            'ft': ['1'],
                            'kn': [],
                            'lt': ['2'],
                            'np': ['11'],
                            'uf': ['8012', '6124', '4547', '5157', '3518'],
                            'un': []},
                     }
           }

    assert turnparser.parse_turn_header({}, t) == ('52341', '2', ret)

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
    ret = {'52341': {'PL': {'fs': ['200'],
                            'ft': ['1'],
                            'kn': [],
                            'lt': ['1'],
                            'np': ['18'],
                            'uf': ['7815', '1933', '8012', '6124', '4547'],
                            'un': []},
                     'firstline': ['52341 player pl_regular'],
                     'na': ["Oleg's Olympians"]}}
    assert turnparser.parse_turn_header({}, t) == ('52341', '1', ret)


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
           'il': ['1', 'gold', '0', '4330', 0, '',
                  '52', 'riding horses', '5000', '5', 0, '',
                  '78', 'stone', '10000', '100', 0, '']}
    data = {'1000': {}}
    turnparser.parse_faction(t, '1000', data)
    assert data['1000'] == ret


def test_analyze_garrison_list():
    t = '''  2617	aj08   10   20	 50   15   8103 4797 7271 6839	... 2527
  4514	aj09   10   20	 50   15   8103 4797 7271 6839	... 2527    '''
    data = {}
    r = {'2617': {'CH': {'at': [60],
                         'df': [60],
                         'gu': [1],
                         'he': [-1],
                         'lk': [4],
                         'lo': [207]},
                  'CM': {'dg': [1]},
                  'LI': {'wh': ['10708']},
                  'MT': {'ca': ['g']},
                  'firstline': ['2617 char garrison']},
         '4514': {'CH': {'at': [60],
                         'df': [60],
                         'gu': [1],
                         'he': [-1],
                         'lk': [4],
                         'lo': [207]},
                  'CM': {'dg': [1]},
                  'LI': {'wh': ['10709']},
                  'MT': {'ca': ['g']},
                  'firstline': ['4514 char garrison']}}
    assert turnparser.analyze_garrison_list(t, data) == r


def test_parse_garrison_log():
    # XXXv2
    pass


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
    ret = {'7271': {'firstline': ['7271 char 0'],
                    'na': ['Osswid the Destroyer'],
                    'il': ['1', 'gold', '0', '26834', 0, '',
                           '10', 'peasants', '1000', '10', 0, '',
                           '12', 'soldiers', '38000', '380', 0, '',
                           '16', 'pikeman', '100', '1', 0, '',
                           '17', 'blessed soldiers', '2900', '29', 0, '',
                           '20', 'swordsmen', '2800', '28', 0, '',
                           '78', 'stone', '30300', '303', 0, '',
                           '79', 'iron', '20', '2', 0, '',
                           '94', 'woven baskets', '11', '11', 0, '',
                           '98', 'drum', '2', '1', 0, ''],
                    'CH': {'ad': [to_int('qm9'), to_int('zb1')],
                           'at': ['89'],
                           'bp': ['0'],
                           'df': ['168'],
                           'he': ['100'],
                           'lk': '2',
                           'lo': ['50033'],
                           'lr': '2',
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
                                  '800', '1', '7', '0', '0',
                                  '860', '1', '7', '0', '0']},
                    'CM': {'hs': ['1'], 'pl': '6839'},
                    'LI': {}}}
    data = {}
    assert turnparser.parse_character('Osswid the Destroyer', '7271', '50033', t, data) == ret
    assert data == {}  # unique items

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

Seen here:
   Gus McCrae [2554], with five peasants, accompanied by:
      New noble [6386], with one peasant, one worker

    '''
    ret = {}
    # XXXv0    assert parse_location(t) == ret
