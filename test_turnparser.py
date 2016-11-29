import pytest

from oid import to_int
from turnparser import (parse_inventory, parse_admit, parse_attitudes,
                        parse_skills, parse_partial_skills, parse_pending_trades,
                        analyze_regions,
                        match_line, remove_visions, parse_turn_header, parse_faction,
                        parse_garrison_log, parse_character, parse_location)

def test_parse_inventory():
    t = '''

      qty  name				     weight
      ---  ----				     ------
    3,929  gold [1]				  0  
	1  riding horse [52]		      1,000  ride 150

    '''
    ret = ['1', '3929', '52', '1']
    assert parse_inventory(t) == ret

def test_parse_admit():
    t = '''

   admit 1933  zb1 1001
	       1002 2001 3001
   admit 8738  qm9  ez0

    '''
    ret = [['1933', to_int('zb1'), '1001', '1002', '2001', '3001'],
           ['8738', to_int('qm9'), to_int('ez0')]]
    assert parse_admit(t) == ret

def test_parse_attitudes():
    t = '''

      defend   ad3  ez0  ig7  ja1  qm9
      Hostile  ad3
      neutral  ad3

    '''
    ret = {'defend': ['ad3', 'ez0', 'ig7', 'ja1', 'qm9'],
           'hostile': ['ad3'],
           'neutral': ['ad3']}
    assert parse_attitudes(t) == ret

    t = '''

   defend   ad3  dk3  dq4  
            jq9  ju1  lr2
            vh3  yc5  ye8

    '''
    ret = {'defend': ['ad3', 'dk3', 'dq4', 'jq9', 'ju1', 'lr2', 'vh3', 'yc5', 'ye8']}
    assert parse_attitudes(t) == ret

def test_parse_skills():
    t = '''
   Skills known:
      Combat [610]
	    Survive fatal wound [611]
      Stealth [630]
	    Conceal self [638], journeyman
    '''
    ret = [ '610', '2', '21', '0', '0',
            '611', '2', '28', '0', '0',
            '630', '2', '28', '0', '0',
            '638', '2', '28', '5', '0',]
    assert parse_skills(t) == ret

def test_parse_partial_skills():
    t = '''
      Locate character [847], 7/21
      Raise undead [901], 0/21
    '''
    ret = ['847', '1', '7', '0', '0',
           '901', '0', '0', '0', '0',]
    assert parse_partial_skills(t) == ret

def test_parse_pending_trades():
    t = '''

      trade    price	qty   item
      -----    -----	---   ----
       sell	   7  9,849   clay pot [95]
       sell	   2  8,565   fish [87]
    '''
    ret = ['2', '95', '9849', '7', '0',  '0',  '0',  '0',
           '2', '87', '8565', '2', '0',  '0',  '0',  '0',]
    assert parse_pending_trades(t) == ret

def test_analyze_regions():
    t = '''A
 B
C
D
 E
    '''
    ret = {'A':['C', 'D'], 'C':['D']}
    region_after = {}
    analyze_regions(t, region_after)
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
    health, = match_line(t, 'Health:', capture=r'(\d+)')
    assert health == '71'

    attack, defense, missile = match_line(t, 'attack', capture=r'(\d+), defense (\d+), missile (\d+)')
    assert attack == '80'
    assert defense == '81'
    assert missile == '0'

    ca, = match_line(t, 'Current aura:')
    assert ca == '36'

    foo, = match_line(t, 'Foo:')
    assert foo == None

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
    s, visions = remove_visions(t)
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
    ret = {'52341': { 'firstline': ['52341 player pl_regular'],
                      'na': ["Oleg's Olympians"],
                      'PL': {'fs': ['200'],
                             'ft': ['1'],
                             'kn': [],
                             'lt': ['2'],
                             'np': ['11'],
                             'uf': ['8012', '6124', '4547', '5157', '3518'],
                             'un': [],
                            },
                     }
           }

    assert parse_turn_header({}, t) == ('52341', '2', ret)

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
                            'un': []
                           },
                     'firstline': ['52341 player pl_regular'],
                     'na': ["Oleg's Olympians"]
                    }
          }
    assert parse_turn_header({}, t) == ('52341', '1', ret)

def test_parse_faction():
    t = '''

Admit permissions:

   admit 4256  ja1 ad3
   admit 7611 6124
   admit 9724  ja1
   admit 9774  ja1

Unclaimed items:

      qty  name				     weight
      ---  ----				     ------
    4,330  gold [1]				  0  
	5  riding horses [52]		      5,000  ride 750
      100  stone [78]			     10,000  

    '''
    ret = {'am': [['4256', '52341', '50033'],
                  ['7611', '6124'],
                  ['9724', '52341'],
                  ['9774', '52341']],
           'il': ['1', '4330', '52', '5', '78', '100']}

    assert parse_faction(t) == ret

def test_parse_garrison_log():
    # XXXv2
    assert 1 == 1

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
    ret = {'firstline': ['7271 char 0'],
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
           'CH': {'ad': ['qm9', 'zb1'],
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
           'LI': {},
    }
    assert parse_character('Osswid the Destroyer', '7271', '50033', t) == ret

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
#XXXv0    assert parse_location(t) == ret
