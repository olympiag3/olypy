import olymap.utilities


def test_calc_exit_distance():
    tests = (
        (None, None, 0),  # None=>None
        (None, {'firstline': ['12536 loc mountain']}, 0),  # forest=>None
        ({'firstline': ['12536 loc forest']}, None, 0),  # None=>mountain
        ({'firstline': ['12536 loc forest']}, {'firstline': ['12536 loc mountain']}, 10), # forest=>mountain
        ({'firstline': ['12536 loc forest']}, {'firstline': ['12536 loc ocean']}, 2), # forest=>ocean
        ({'firstline': ['12536 loc ocean']}, {'firstline': ['12536 loc forest']}, 2),  # ocean=>forest
        ({'firstline': ['12536 loc forest']}, {'firstline': ['12536 loc swamp']}, 14),  # forest=>swamp
        ({'firstline': ['12536 loc forest']}, {'firstline': ['12536 loc desert']}, 8),  # forest=>desert
        ({'firstline': ['12536 loc forest']}, {'firstline': ['12536 loc plain']}, 7),  # forest=>plain
        ({'firstline': ['12536 loc forest']}, {'firstline': ['12536 loc pit']}, 28),  # forest=>pit
        ({'firstline': ['12536 loc pit']}, {'firstline': ['12536 loc mountain']}, 28),  # pit=>mountain
        ({'firstline': ['12536 loc forest']}, {'firstline': ['12536 loc tower']}, 0),  # forest=>tower
        ({'firstline': ['12536 loc forest']}, {'firstline': ['12536 loc yew grove']}, 1),  # forest=>yew grove
        ({'firstline': ['12536 loc yew grove']}, {'firstline': ['12536 loc forest']}, 1),  # yew grove=>forest
        ({'firstline': ['12536 loc city']}, {'firstline': ['12536 loc castle']}, 0),  # city=>castle
        ({'firstline': ['12536 loc castle']}, {'firstline': ['12536 loc tower']}, 0),  # castle=>tower
        ({'firstline': ['12536 loc city']}, {'firstline': ['12536 loc sewer']}, 0),  # city=>sewer
        ({'firstline': ['12536 loc sewer']}, {'firstline': ['12536 loc city']}, 0),  # sewer=>city
        ({'firstline': ['12536 loc ocean']}, {'firstline': ['12536 loc city']}, 1),  # ocean=>city
        ({'firstline': ['12536 loc city']}, {'firstline': ['12536 loc ocean']}, 1),  # city=>ocean
        ({'firstline': ['12536 loc forest']}, {'firstline': ['12536 loc city']}, 1),  # forest=>city
        ({'firstline': ['12536 loc city']}, {'firstline': ['12536 loc forest']}, 1),  # city=>forest
        ({'firstline': ['12536 loc sewer']}, {'firstline': ['12536 loc tunnel']}, 0),  # sewer=>tunnel
        ({'firstline': ['12536 loc tunnel']}, {'firstline': ['12536 loc sewer']}, 0),  # tunnel=>sewer
        ({'firstline': ['12536 loc tunnel']}, {'firstline': ['12536 loc tunnel']}, 5),  # tunnel=>tunnel
        ({'firstline': ['12536 loc tunnel']}, {'firstline': ['12536 loc chamber']}, 5),  # tunnel=>chamber
    )

    for loc1, loc2, answer in tests:
        assert olymap.utilities.calc_exit_distance(loc1, loc2) == answer


def test_get_auraculum_aura():
    tests = (
        ({}, 0),
        ({'IM': {'au': ['10']}}, 10),
        ({'IM': {'uk': ['2']}}, 0),
        ({'IM': {'au': ['0']}}, 0),
    )

    for box, answer in tests:
        assert olymap.utilities.get_auraculum_aura(box) == answer


def test_get_auraculum_id():
    tests = (
        ({}, None),
        ({'CM': {'ar': ['1234']}}, '1234'),
        ({'CM': {'uk': ['1234']}}, None),
        ({'IM': {'ar': ['1234']}}, None),
    )

    for box, answer in tests:
        assert olymap.utilities.get_auraculum_id(box) == answer


def test_get_item_weight():
    tests = (
        ({}, 0),
        ({'IT': {'wt': ['24']}}, 24),
        ({'CM': {'wt': ['24']}}, 0),
        ({'IT': {'ga': ['24']}}, 0),
    )

    for box, answer in tests:
        assert olymap.utilities.get_item_weight(box) == answer


def test_get_max_aura():
    tests = (
        ({}, 0),
        ({'CM': {'ma': ['10']}}, 10),
        ({'CM': {'ma': ['0']}}, 0),
        ({'CM': {'uk': ['2']}}, 0),
        ({'IM': {'au': ['0']}}, 0),
    )

    for box, answer in tests:
        assert olymap.utilities.get_max_aura(box) == answer


def test_get_pledged_to():
    data = {'7271': {'firstline': ['7271 char 0'], 'na': ['Osswid the Destroyer']}}
    tests = (
        ({}, None),
        ({'CM': {'pl': ['7271']}}, {'id': '7271', 'oid': '7271', 'name': 'Osswid the Destroyer'}),
        ({'CM': {'un': ['7271']}}, None),
        ({'IT': {'pl': ['1234']}}, None),
    )

    for box, answer in tests:
        assert olymap.utilities.get_pledged_to(box, data) == answer


def test_get_ship_capacity():
    tests = (
        ({}, 0),
        ({'SL': {'ca': ['25000']}}, 25000),
        ({'CM': {'ca': ['25000']}}, 0),
        ({'SL': {'ga': ['25000']}}, 0),
    )

    for box, answer in tests:
        assert olymap.utilities.get_ship_capacity(box) == answer


def test_get_ship_damage():
    tests = (
        ({}, 0),
        ({'SL': {'da': ['10']}}, 10),
        ({'CM': {'da': ['10']}}, 0),
        ({'SL': {'ga': ['10']}}, 0),
    )

    for box, answer in tests:
        assert olymap.utilities.get_ship_damage(box) == answer


def test_get_use_key():
    tests = (
        ({}, None),
        ({'IM': {'uk': ['1']}}, '1'),
        ({'IM': {'uk': ['2']}}, '2'),
        ({'IM': {'ut': ['2']}}, None),
    )

    for box, answer in tests:
        assert olymap.utilities.get_use_key(box) == answer


def test_get_who_has():
    data = {'1234': {'firstline': ['1234 char 0'], 'na': ['Test Unit']}}
    tests = (
        ({}, None),
        ({'IT': {'un': ['1234']}}, {'id': '1234', 'oid': '1234', 'name': 'Test Unit', 'kind': 'char'}),
        ({'CM': {'un': ['1234']}}, None),
        ({'IT': {'ga': ['1234']}}, None),
    )

    for box, answer in tests:
        assert olymap.utilities.get_who_has(box, data) == answer


def test_is_absorb_aura_blast():
    tests = (
        ({}, False),
        ({'CH': {'sl': [0]}}, False),
        ({'CH': {'sl': ['909', '2']}}, True),
        ({'CH': {'sl': ['909', '1']}}, False),
        ({'CH': {'sl': ['908', '2']}}, False),
    )

    for box, answer in tests:
        assert olymap.utilities.is_absorb_aura_blast(box) == answer


def test_is_castle():
    tests = (
        ({'firstline': ['10 loc 0']}, False),
        ({'firstline': ['10 char castle']}, False),
        ({'firstline': ['1234 loc castle']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_castle(box) == answer


def test_is_char():
    tests = (
        ({'firstline': ['10 item 0']}, False),
        ({'firstline': ['1234 char 0']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_char(box) == answer


def test_is_city():
    tests = (
        ({'firstline': ['10 loc 0']}, True),
        ({'firstline': ['10 char city']}, False),
        ({'firstline': ['1234 loc city']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_loc(box) == answer


def test_is_concealed():
    tests = (
        ({}, False),
        ({'CH': {'hs': [0]}}, False),
        ({'CH': {'hs': ['1']}}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_concealed(box) == answer


def test_is_faeryhill():
    tests = (
        ({'firstline': ['10 loc 0']}, False),
        ({'firstline': ['10 char faery hill']}, False),
        ({'firstline': ['1234 loc faery hill']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_faeryhill(box) == answer


def test_is_fighter():
    tests = (
        ({'firstline': ['10 item 0']}, False),
        ({'firstline': ['10 item 0'], 'IT': {'hi': [0]}}, False),
        ({'firstline': ['10 item 0'], 'IT': {'at': ['1']}}, True),
        ({'firstline': ['10 item 0'], 'IT': {'df': ['1']}}, True),
        ({'firstline': ['10 item 0'], 'IT': {'mi': ['1']}}, True),
        ({'firstline': ['18 item 0']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_fighter(box) == answer


def test_is_garrison():
    tests = (
        ({'firstline': ['10 loc 0']}, False),
        ({'firstline': ['10 char garrison']}, True),
        ({'firstline': ['1234 loc garrison']}, False),
    )

    for box, answer in tests:
        assert olymap.utilities.is_garrison(box) == answer


def test_is_graveyard():
    tests = (
        ({'firstline': ['10 loc 0']}, False),
        ({'firstline': ['10 char graveyard']}, False),
        ({'firstline': ['1234 loc graveyard']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_graveyard(box) == answer


def test_is_hidden():
    tests = (
        ({}, False),
        ({'LO': {'hi': [0]}}, False),
        ({'LO': {'hi': ['1']}}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_hidden(box) == answer


def test_is_impassable():
    data = {'11416': {'firstline': ['11416 loc ocean'], 'na': ['Ocean'], 'LI': {'wh': ['58760']}, 'LO': {'pd': ['56980', '11417', '11516', '11415']}},
            '11316': {'firstline': ['11316 loc plain'], 'na': ['Plain'], 'LI': {'wh': ['58762'], 'hl': ['3545', '56980', '148781', '138710']}, 'LO': {'pd': ['0', '0', '11416', '0']}},
            '56980': {'firstline': ['56980 loc city'], 'na': ['Skyllith'], 'LI': {'wh': ['11316']}},
            '11398': {'firstline': ['11398 loc mountain'], 'LI': {'wh': ['58764'], 'hl': ['74172', '63682', '78615', '70776', '89613']}, 'LO': {'pd': ['11298', '11399', '11498', '11397'], 'dg': ['3'], 'lc': ['1']}, 'na': ['Mountain']},
            '11298': {'firstline': ['11298 loc mountain'], 'LI': {'wh': ['58764'], 'hl': ['60692', '58415', '76459', '118952']}, 'LO': {'pd': ['11198', '11299', '11398', '11297'], 'dg': ['3'], 'lc': ['3']}, 'na': ['Mountain']},
            '11299': {'firstline': ['11299 loc ocean'], 'LI': {'wh': ['58761'], 'hl': ['59143', '93515']}, 'LO': {'pd': ['11199', '11200', '11399', '11298'], 'dg': ['2']}, 'na': ['Ocean']},
            '59143': {'firstline': ['59143 road 0'], 'na': ['Secret sea route'], 'LI': {'wh': ['11299']}, 'GA': {'tl': ['11398'], 'rh': ['1']}},
            '63682': {'firstline': ['63682 road 0'], 'na': ['Secret sea route'], 'LI': {'wh': ['11398']}, 'GA': {'tl': ['11299'], 'rh': ['1']}}
}
    tests = (
        ({'firstline': ['12536 loc ocean']}, {'firstline': ['12537 loc mountain']}, 'north', True),
        ({'firstline': ['12537 loc mountain']}, {'firstline': ['12536 loc ocean']}, 'south', True),
        ({'firstline': ['12536 loc ocean']}, {'firstline': ['12540 loc ocean']}, 'north', False),
        ({'firstline': ['12541 loc forest']}, {'firstline': ['12537 loc mountain']}, 'north', False),
        ({'firstline': ['12536 loc ocean']}, {'firstline': ['57068 loc city']}, 'north', False),
        ({'firstline': ['11416 loc ocean']},{'firstline': ['11316 loc plain'], 'na': ['Plain'], 'LI': {'wh': ['58762'], 'hl': ['3545', '56980', '148781', '138710']}},'North', True),
        ({'firstline': ['59143 road 0'], 'na': ['Secret sea route'], 'LI': {'wh': ['11299']}, 'GA': {'tl': ['11398'], 'rh': ['1']}}, {'firstline': ['11298 loc mountain'], 'LI': {'wh': ['58764'], 'hl': ['60692', '58415', '76459', '118952']}, 'LO': {'pd': ['11198', '11299', '11398', '11297'], 'dg': ['3'], 'lc': ['3']}, 'na': ['Mountain']}, 'Secret sea route', False),
        ({'firstline': ['11299 loc ocean']}, {'firstline': ['11298 loc mountain']}, 'West', True),
        ({'firstline': ['63682 road 0'], 'na': ['Secret sea route'], 'LI': {'wh': ['11398']}, 'GA': {'tl': ['11299'], 'rh': ['1']}}, {'firstline': ['11299 loc ocean']}, 'Secret sea route', False)
    )

    for loc1, loc2, direction, answer in tests:
        assert olymap.utilities.is_impassable(loc1, loc2, direction, data) == answer


def test_is_item():
    tests = (
        ({'firstline': ['10 item 0']}, True),
        ({'firstline': ['10 char graveyard']}, False),
        ({'firstline': ['1234 item 0']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_item(box) == answer


def test_is_loc():
    tests = (
        ({'firstline': ['10 loc 0']}, True),
        ({'firstline': ['10 char graveyard']}, False),
        ({'firstline': ['1234 loc graveyard']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_loc(box) == answer


def test_is_magician():
    tests = (
        ({}, False),
        ({'CM': {'im': [0]}}, False),
        ({'CM': {'im': ['1']}}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_magician(box) == answer


def test_is_man_item():
    tests = (
        ({}, False),
        ({'IT': {'mu': [0]}}, False),
        ({'IT': {'mu': ['1']}}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_man_item(box) == answer


def test_is_mountain():
    tests = (
        ({'firstline': ['10 item 0']}, False),
        ({'firstline': ['10 char mountain']}, False),
        ({'firstline': ['1234 loc mountain']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_mountain(box) == answer


def test_is_ocean():
    tests = (
        ({'firstline': ['10 item 0']}, False),
        ({'firstline': ['10 char ocean']}, False),
        ({'firstline': ['1234 loc ocean']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_ocean(box) == answer


def test_is_on_guard():
    tests = (
        ({}, False),
        ({'CH': {'gu': [0]}}, False),
        ({'CH': {'gu': ['1']}}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_on_guard(box) == answer


def test_is_orb():
    tests = (
        ({}, False),
        ({'IM': {'uk': [0]}}, False),
        ({'IM': {'uk': ['9']}}, True),
        ({'IM': {'uk': ['5']}}, False),
    )

    for box, answer in tests:
        assert olymap.utilities.is_orb(box) == answer


def test_is_player():
    tests = (
        ({'firstline': ['zb1 player 0']}, True),
        ({'firstline': ['zb1 char graveyard']}, False),
        ({'firstline': ['zb1 player graveyard']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_player(box) == answer


def test_is_port_city():
    data = {'12536': {'firstline': ['12536 loc forest'], 'LI': {'wh': ['58767']}, 'LO': {'pd': ['12436', '12537', '12636', '12535']}},
            '57068': {'firstline': ['57068 loc city'], 'LI': {'wh': ['12536']}},
            '1775': {'firstline': ['1775 loc castle'], 'LI': {'wh': ['57068']}},
            '12436': {'firstline': ['12436 loc ocean']},
            '57579': {'firstline': ['57579 loc city'], 'LI': {'wh': ['11154']}},
            '11154': {'firstline': ['11154 loc plain'], 'LO': {'pd': ['11054', '11155', '11254', '11153']}},
            '11054': {'firstline': ['11054 loc swamp']},
            '11155': {'firstline': ['11155 loc plain']},
            '11254': {'firstline': ['11254 loc plain']},
            '11153': {'firstline': ['11153 loc plain']},
            '56777': {'firstline': ['56777 loc city'], 'LI': {'wh': ['11729']}},
            '11729': {'firstline': ['11729 loc mountain'], 'LO': {'pd': ['11629', '11730', '11829', '11728'], 'lc': ['1']}}}
    tests = (
        ({'firstline': ['57068 loc city'], 'LI': {'wh': ['12536']}}, True),
        ({'firstline': ['1775 loc castle'], 'LI': {'wh': ['57068']}}, False),
        ({'firstline': ['57579 loc city'], 'LI': {'wh': ['11154']}}, False),
        ({'firstline': ['56777 loc city'], 'LI': {'wh': ['11729']}}, False)
    )

    for box, answer in tests:
        assert olymap.utilities.is_port_city(box, data) == answer


def test_is_priest():
    tests = (
        ({}, False),
        ({'CH': {'sl': ['800', '2']}}, False),
        ({'CH': {'sl': ['750', '1']}}, False),
        ({'CH': {'sl': ['750', '2']}}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_priest(box) == answer


def test_is_prisoner():
    tests = (
        ({}, False),
        ({'CH': {'pr': [0]}}, False),
        # g2 has 1,2,3 here, game code only sets TRUE/FALSE, meh
        ({'CH': {'pr': ['1']}}, True),
        ({'CH': {'pr': ['2']}}, False),
        #({'CH': {'pr': ['3']}}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_prisoner(box) == answer


def test_is_prominent():
    tests = (
        ({}, False),
        ({'IT': {'pr': [0]}}, False),
        ({'IT': {'pr': ['1']}}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_prominent(box) == answer


def test_is_projected_cast():
    tests = (
        ({}, False),
        ({'IM': {'uk': [0]}}, False),
        ({'IM': {'uk': ['9']}}, False),
        ({'IM': {'uk': ['5']}}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_projected_cast(box) == answer


def test_is_region():
    tests = (
        ({'firstline': ['10 loc 0']}, False),
        ({'firstline': ['10 char region']}, False),
        ({'firstline': ['1234 loc region']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_region(box) == answer


def test_is_road_or_gate():
    tests = (
        ({}, False),
        ({'GA': {'tl': [0]}}, True),
        ({'GA': {'tl': ['1']}}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_road_or_gate(box) == answer


def test_is_ship():
    tests = (
        ({'firstline': ['10 ship 0']}, True),
        ({'firstline': ['10 char graveyard']}, False),
        ({'firstline': ['1234 ship roundship']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_ship(box) == answer


def test_is_skill():
    tests = (
        ({'firstline': ['10 skill 0']}, True),
        ({'firstline': ['10 char skill']}, False),
        ({'firstline': ['1234 skill Ship']}, True),
    )

    for box, answer in tests:
        assert olymap.utilities.is_skill(box) == answer


def test_loc_depth():
    tests = (
        ('rubbish', 0),
        ('region', 1),
        ('mountain', 2),
        ('ocean', 2),
        ('bog', 3),
        ('city', 3),
        ('temple', 4),
        ('sewer', 4),
    )

    for loc_type, answer in tests:
        assert olymap.utilities.loc_depth(loc_type) == answer


def test_province():
    data = {'12536': {'firstline': ['12536 loc forest'], 'LI': {'wh': ['58767']}},
            '57068': {'firstline': ['57068 loc city'], 'LI': {'wh': ['12536']}},
            '58767': {'firstline': ['58767 loc region']},
            '1775': {'firstline': ['1775 loc castle'], 'LI': {'wh': ['57068']}},
            '8578': {'firstline': ['8578 char 0'], 'LI': {'wh': ['1775']}},
            '5301': {'firstline': ['5301 loc tower'], 'LI': {'wh': ['1775']}}}
    tests = (
        ('1775', '12536'), # castle in city
        ('57068', '12536'), # city d08 in province
        ('12536', '12536'), # forest bg36
        ('58767', 0), # region
        ('8578', '12536'), # character in castle
        ('5301', '12536'),  # tower in castle
    )

    for who, answer in tests:
        assert olymap.utilities.province(who, data) == answer


def test_province_has_port_city():
    data = {'12536': {'firstline': ['12536 loc forest'], 'LI': {'wh': ['58767'], 'hl': ['8241', '57068', '77868', '78071', '144999']}, 'LO': {'pd': ['12436', '12537', '12636', '12535']}},
            '57068': {'firstline': ['57068 loc city'], 'LI': {'wh': ['12536']}},
            '1775': {'firstline': ['1775 loc castle'], 'LI': {'wh': ['57068']}},
            '12436': {'firstline': ['12436 loc ocean']},
            '57579': {'firstline': ['57579 loc city'], 'LI': {'wh': ['11154']}},
            '11154': {'firstline': ['11154 loc plain'], 'LI': {'hl': ['57579', '60861']},'LO': {'pd': ['11054', '11155', '11254', '11153']}},
            '11054': {'firstline': ['11054 loc swamp']},
            '11155': {'firstline': ['11155 loc plain']},
            '11254': {'firstline': ['11254 loc plain']},
            '11153': {'firstline': ['11153 loc plain']},
            '56777': {'firstline': ['56777 loc city'], 'LI': {'wh': ['11729']}},
            '11729': {'firstline': ['11729 loc mountain'], 'LI': {'hl': ['56777', '9261']}, 'LO': {'pd': ['11629', '11730', '11829', '11728']}}}
    tests = (
        ({'firstline': ['12536 loc forest'], 'LI': {'wh': ['58767'], 'hl': ['8241', '57068', '77868', '78071', '144999']}}, '57068'),
        ({'firstline': ['1775 loc castle'], 'LI': {'wh': ['57068']}}, None),
        ({'firstline': ['11154 loc plain'], 'LI': {'hl': ['57579', '60861']}}, None),
        ({'firstline': ['11729 loc mountain'], 'LI': {'hl': ['56777', '9261']}}, None)
    )

    for box, answer in tests:
        assert olymap.utilities.province_has_port_city(box, data) == answer


def test_region():
    data = {'12536': {'firstline': ['12536 loc forest'], 'LI': {'wh': ['58767']}},
            '57068': {'firstline': ['57068 loc city'], 'LI': {'wh': ['12536']}},
            '58767': {'firstline': ['58767 loc region']},
            '1775': {'firstline': ['1775 loc castle'], 'LI': {'wh': ['57068']}},
            '8578': {'firstline': ['8578 char 0'], 'LI': {'wh': ['1775']}},
            '5301': {'firstline': ['5301 loc tower'], 'LI': {'wh': ['1775']}}}
    tests = (
        ('1775', '58767'), # castle in city
        ('57068', '58767'), # city d08 in province
        ('12536', '58767'), # forest bg36
        ('58767', '58767'), # region
        ('8578', '58767'), # character in castle
        ('5301', '58767'),  # tower in castle
    )

    for who, answer in tests:
        assert olymap.utilities.region(who, data) == answer


def test_return_firstline():
    tests = (
        ({'firstline': ['6614 char 0']}, '6614 char 0'),
        ({'firstline': ['54289 player pl_regular']}, '54289 player pl_regular'),
        ({'firstline': ['32132 loc tunnel']}, '32132 loc tunnel'),
        ({'firstline': ['1074 ship roundship']}, '1074 ship roundship'),
        ({'firstline': ['600 skill 0']}, '600 skill 0'),
        ({'firstline': ['1 item 0']}, '1 item 0'),
    )

    for box, answer in tests:
        assert olymap.utilities.return_firstline(box) == answer


def test_return_kind():
    tests = (
        ({'firstline': ['6614 char 0']}, 'char'),
        ({'firstline': ['54289 player pl_regular']}, 'player'),
        ({'firstline': ['32132 loc tunnel']}, 'loc'),
        ({'firstline': ['1074 ship roundship']}, 'ship'),
        ({'firstline': ['600 skill 0']}, 'skill'),
        ({'firstline': ['1 item 0']}, 'item'),
    )

    for box, answer in tests:
        assert olymap.utilities.return_kind(box) == answer


def test_return_subkind():
    tests = (
        ({'firstline': ['6614 char 0']}, '0'),
        ({'firstline': ['54289 player pl_regular']}, 'pl_regular'),
        ({'firstline': ['32132 loc tunnel']}, 'tunnel'),
        ({'firstline': ['1074 ship roundship']}, 'roundship'),
        ({'firstline': ['600 skill 0']}, '0'),
        ({'firstline': ['1 item 0']}, '0'),
    )

    for box, answer in tests:
        assert olymap.utilities.return_subkind(box) == answer


def test_return_unitid():
    tests = (
        ({'firstline': ['6614 char 0']}, '6614'),
        ({'firstline': ['54289 player pl_regular']}, '54289'),
        ({'firstline': ['32132 loc tunnel']}, '32132'),
        ({'firstline': ['1074 ship roundship']}, '1074'),
        ({'firstline': ['600 skill 0']}, '600'),
        ({'firstline': ['1 item 0']}, '1'),
    )

    for box, answer in tests:
        assert olymap.utilities.return_unitid(box) == answer


def test_xlate_loyalty():
    tests = (
        ({}, 'Undefined'),
        ({'CH': {'lk': [0], 'lr': [0]}}, 'Undefined'),
        ({'CH': {'lk': ['0'], 'lr': ['0']}}, 'Unsworn'),
        ({'CH': {'lk': ['1'], 'lp': ['250']}}, 'Undefined'),
        ({'CH': {'lk': ['1'], 'lr': ['250']}}, 'Contract-250'),
        ({'CH': {'lk': ['2'], 'lp': ['1']}}, 'Undefined'),
        ({'CH': {'lk': ['2'], 'lr': ['1']}}, 'Oath-1'),
        ({'CH': {'lk': ['3'], 'lp': ['10']}}, 'Undefined'),
        ({'CH': {'lk': ['3'], 'lr': ['10']}}, 'Fear-10'),
        ({'CH': {'lk': ['4'], 'lp': ['10']}}, 'Undefined'),
        ({'CH': {'lk': ['4'], 'lr': ['10']}}, 'Npc-10'),
        ({'CH': {'lk': ['5']}}, 'Summon'),
        ({'CH': {'lk': ['6']}}, 'Undefined'),
    )

    for box, answer in tests:
        assert olymap.utilities.xlate_loyalty(box) == answer


# def test_top_ruler():
#     data = {'7271': {'firstline': ['7271 char 0'], 'na': ['Osswid the Destroyer'], 'il': ['1', '1666', '11', '10', '12', '35', '13', '45', '16', '129', '17', '29', '20', '105', '21', '76', '78', '303', '94', '11', '98', '1'], 'tl': ['2', '95', '100', '7', '0', '0', '0', '0'], 'LI': {'wh': ['4256'], 'hl': ['7651']}, 'CH': {'lo': ['56511'], 'he': ['100'], 'lk': ['2'], 'lr': ['2'], 'sl': ['600', '2', '21', '0', '0', '601', '2', '14', '0', '0', '602', '2', '14', '0', '0', '603', '2', '14', '0', '0', '610', '2', '21', '0', '0', '611', '2', '28', '0', '0', '612', '2', '28', '0', '0', '613', '2', '14', '0', '0', '614', '2', '14', '35', '0', '615', '2', '21', '5', '0', '616', '2', '14', '35', '0', '617', '2', '14', '35', '0', '680', '2', '21', '0', '0', '681', '2', '14', '0', '0', '682', '2', '14', '0', '0', '720', '2', '21', '0', '0', '721', '2', '14', '0', '0', '722', '2', '14', '0', '0'], 'bp': ['0'], 'at': ['89'], 'df': ['736'], 'mi': ['50']}, 'CM': {'vp': ['6'], 'pl': ['6839']}, 'CO': {'li': ['seek'], 'ar': ['0', '0', '0', '0', '0', '0', '0', '0'], 'cs': ['2'], 'wa': ['1'], 'st': ['1'], 'de': ['6'], 'po': ['1'], 'pr': ['3']}},
#             '6839': {'firstline': ['6839 char 0'], 'na': ['Yoyo 6'], 'il': ['54', '2', '60624', '1', '60986', '1', '61166', '1', '61725', '1', '61780', '1', '61952', '1', '63136', '1', '64675', '1', '65004', '1', '65274', '1', '67037', '1', '67129', '1', '67380', '1', '67999', '1', '69173', '1', '69839', '1', '69887', '1', '72255', '1', '72270', '1', '73291', '1', '73302', '1', '76747', '1', '77844', '1'], 'LI': {'wh': ['58253'], 'hl': ['1084']}, 'CH': {'lo': ['52147'], 'he': ['61'], 'lk': ['2'], 'lr': ['1'], 'sl': ['610', '2', '21', '0', '0', '611', '2', '28', '0', '0', '612', '2', '28', '0', '0', '630', '2', '28', '0', '0', '638', '2', '28', '0', '0', '639', '2', '21', '0', '0', '670', '2', '28', '0', '0', '671', '2', '14', '0', '0', '800', '2', '28', '0', '0', '801', '2', '14', '0', '0', '802', '2', '14', '0', '0', '803', '2', '14', '0', '0', '804', '2', '21', '0', '0', '805', '2', '21', '0', '0', '806', '2', '21', '0', '0', '808', '2', '21', '5', '0', '813', '2', '21', '35', '0', '840', '2', '35', '0', '0', '841', '2', '21', '35', '0', '842', '2', '21', '0', '0', '843', '2', '14', '5', '0', '844', '2', '21', '0', '0', '845', '2', '21', '12', '0', '846', '2', '21', '5', '0', '847', '2', '21', '5', '0', '849', '2', '21', '21', '0', '851', '2', '21', '5', '0', '900', '2', '42', '0', '0', '901', '2', '21', '0', '0', '902', '2', '21', '0', '0', '903', '2', '21', '0', '0', '904', '2', '21', '0', '0', '905', '2', '21', '0', '0', '906', '2', '21', '0', '0', '907', '2', '28', '0', '0', '908', '2', '21', '0', '0', '909', '2', '21', '0', '0', '911', '2', '28', '0', '0'], 'bh': ['9'], 'bp': ['0'], 'at': ['80'], 'df': ['80'], 'mi': ['0']}, 'CM': {'im': ['1'], 'ma': ['30'], 'ca': ['36'], 'pl': ['1147']}},
#             '1147': {'firstline': ['1147 char 0'], 'na': ['Scout 2'], 'il': ['1', '996', '54', '3'], 'LI': {'wh': ['27151']}, 'CH': {'lo': ['50033'], 'he': ['100'], 'lk': ['3'], 'lr': ['7'], 'sl': ['600', '2', '21', '0', '0', '601', '2', '14', '12', '0', '602', '2', '14', '0', '0', '610', '2', '21', '0', '0', '611', '2', '28', '0', '0', '612', '2', '28', '0', '0', '614', '2', '14', '5', '0', '615', '2', '21', '5', '0', '616', '2', '14', '0', '0', '617', '2', '14', '35', '0', '630', '2', '28', '0', '0', '638', '2', '28', '0', '0', '700', '2', '21', '0', '0', '702', '2', '14', '35', '0', '703', '2', '14', '35', '0'], 'bp': ['0'], 'at': ['119'], 'df': ['124'], 'mi': ['84']}, 'CM': {'hs': ['1'], 'pl': ['9308']}, 'CO': {'li': ['explore'], 'ar': ['0', '0', '0', '0', '0', '0', '0', '0'], 'cs': ['2'], 'wa': ['3'], 'st': ['1'], 'de': ['4'], 'pr': ['3']}},
#             '9308': {'firstline': ['9308 char 0'], 'na': ['Tycho Brahe'], 'il': ['1', '200', '54', '2', '84', '9', '60825', '1', '61797', '1', '63572', '1', '64343', '1', '64726', '1', '65133', '1', '65717', '1', '66149', '1', '66225', '1', '66881', '1', '68011', '1', '69080', '1', '69101', '1', '69585', '1', '69809', '1', '70297', '1', '70322', '1', '70641', '1', '70893', '1', '71750', '1', '71803', '1', '71804', '1', '71865', '1', '72119', '1', '72599', '1', '74168', '1', '74275', '1', '75247', '1', '75538', '1', '75590', '1', '76054', '1', '76174', '1', '76696', '1', '76874', '1', '76914', '1', '76915', '1', '77090', '1', '77560', '1', '77710', '1', '77726', '1', '78668', '1'], 'tl': ['2', '95', '9855', '7', '0', '0', '0', '0'], 'an': ['5285', '8719'], 'LI': {'wh': ['6710']}, 'CH': {'lo': ['52035'], 'he': ['100'], 'lk': ['3'], 'lr': ['95'], 'sl': ['610', '2', '21', '0', '0', '611', '2', '28', '0', '0', '612', '2', '28', '0', '0', '630', '2', '28', '0', '0', '638', '2', '28', '0', '0', '639', '2', '21', '0', '0', '670', '2', '28', '0', '0', '671', '2', '14', '0', '0', '673', '2', '14', '0', '0', '674', '2', '21', '0', '0', '690', '2', '28', '0', '0', '691', '2', '21', '21', '0', '692', '2', '21', '12', '0', '693', '2', '21', '0', '0', '694', '2', '21', '0', '0', '695', '2', '14', '0', '0', '696', '2', '21', '0', '0', '697', '2', '28', '0', '0'], 'bp': ['0'], 'at': ['80'], 'df': ['80'], 'mi': ['0']}, 'CM': {'vp': ['6'], 'pl': ['8412']}},
#             '8412': {'firstline': ['8412 char 0'], 'na': ['Kelly'], 'il': ['1', '2827', '54', '1', '77', '270', '60457', '1', '61282', '1', '64273', '1', '65304', '1', '66565', '1', '67002', '1', '67526', '1', '71359', '1', '74189', '1'], 'LI': {'wh': ['1775']}, 'CH': {'lo': ['51290'], 'he': ['49'], 'lk': ['2'], 'lr': ['2'], 'sl': ['610', '2', '21', '0', '0', '611', '2', '28', '0', '0', '612', '2', '28', '0', '0', '617', '2', '14', '5', '0', '630', '2', '28', '0', '0', '638', '2', '28', '0', '0', '800', '2', '28', '0', '0', '801', '2', '14', '5', '0', '802', '2', '14', '35', '0', '803', '2', '14', '0', '0', '804', '2', '21', '0', '0', '805', '2', '21', '0', '0', '806', '2', '21', '0', '0', '808', '2', '21', '5', '0', '809', '2', '21', '0', '0', '811', '2', '21', '0', '0', '813', '2', '21', '35', '0', '814', '2', '21', '0', '0', '820', '2', '35', '0', '0', '821', '2', '21', '0', '0', '822', '2', '21', '5', '0', '823', '2', '21', '0', '0', '824', '2', '21', '5', '0', '827', '2', '21', '0', '0', '829', '2', '21', '5', '0', '832', '2', '21', '0', '0', '840', '2', '35', '0', '0', '841', '2', '21', '35', '0', '842', '2', '21', '0', '0', '844', '2', '21', '0', '0', '845', '2', '21', '0', '0', '846', '2', '21', '0', '0', '847', '2', '21', '0', '0', '848', '2', '21', '0', '0', '849', '2', '21', '5', '0', '851', '2', '21', '5', '0', '852', '2', '21', '0', '0', '880', '2', '43', '0', '0', '881', '2', '14', '0', '0', '882', '2', '21', '0', '0', '883', '2', '21', '0', '0', '884', '2', '21', '0', '0', '920', '2', '42', '0', '0', '921', '2', '28', '0', '0', '922', '2', '28', '5', '0'], 'bp': ['0'], 'at': ['80'], 'df': ['80'], 'mi': ['0']}, 'CM': {'im': ['1'], 'ma': ['9'], 'ca': ['73'], 'hs': ['1'], 'kw': ['1'], 'pl': ['2527'], 'ar': ['61282']}},
#             '2527': {'firstline': ['2527 char 0'], 'na': ['Tom'], 'il': ['10', '69', '11', '3', '13', '10', '21', '324', '22', '111', '61', '2', '77', '8', '85', '126', '65189', '1', '68533', '1'], 'LI': {'wh': ['8578']}, 'CH': {'lo': ['54289'], 'he': ['100'], 'lk': ['2'], 'lr': ['2'], 'sl': ['610', '2', '21', '0', '0', '611', '2', '28', '0', '0', '612', '2', '28', '0', '0', '613', '2', '14', '0', '0', '614', '2', '14', '5', '0', '615', '2', '21', '21', '0', '616', '2', '14', '5', '0', '617', '2', '14', '21', '0', '650', '2', '28', '0', '0', '651', '2', '21', '0', '0', '652', '2', '28', '0', '0', '653', '2', '28', '0', '0', '654', '2', '28', '5', '0', '655', '2', '14', '0', '0', '657', '2', '21', '0', '0', '661', '2', '21', '0', '0'], 'bh': ['9'], 'bp': ['0'], 'at': ['123'], 'df': ['155'], 'mi': ['65']}, 'CM': {'vp': ['6']}, 'CO': {'li': ['train 21 '], 'ar': ['21', '0', '0', '10', '0', '0', '0', '0'], 'cs': ['2'], 'wa': ['-1'], 'st': ['1'], 'de': ['10'], 'po': ['1'], 'pr': ['3']}}
#             }
#     tests = (
#         ({'firstline': ['8747 char 0'], 'na': ['Test Unit']}, None),
#         ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['0']}}, None),
#         ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['0'], 'ma': ['4']}}, None),
#         ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'ma': ['4']}}, None),
#         ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['4']}}, None),
#         ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['9']}}, 'Conjurer'),
#         ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['11']}}, 'Mage'),
#         ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['11'], 'ar': ['61282']}}, '2nd Black Circle'),
#         ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['11'], 'ar': ['61283']}}, 'Sorcerer'),
#         ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['11'], 'ar': ['61284']}}, 'Mage'),
#     )
#
#     for box, answer in tests:
#         print('{} {}'.format(box, data))
#         assert olymap.utilities.top_ruler(box, data) == answer


def test_xlate_magetype():
    data = {'61282': {'firstline': ['61282 item auraculum'], 'na': ['Jeweled crown'], 'IT': {'wt': ['2'], 'un': ['8747']}, 'IM': {'au': ['60']}},
            '61283': {'firstline': ['61283 item auraculum'], 'na': ['Jeweled crown 2'], 'IT': {'wt': ['2'], 'un': ['8747']}, 'IM': {'au': ['10']}},
            '61284': {'firstline': ['61283 item auraculum'], 'na': ['Jeweled crown 3'], 'IT': {'wt': ['2'], 'un': ['8747']}}
            }
    tests = (
        ({'firstline': ['8747 char 0'], 'na': ['Test Unit']}, None),
        ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['0']}}, None),
        ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['0'], 'ma': ['4']}}, None),
        ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'ma': ['4']}}, None),
        ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['4']}}, None),
        ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['9']}}, 'Conjurer'),
        ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['11']}}, 'Mage'),
        ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['11'], 'ar': ['61282']}}, '2nd Black Circle'),
        ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['11'], 'ar': ['61283']}}, 'Sorcerer'),
        ({'firstline': ['8747 char 0'], 'na': ['Test Unit'], 'CM': {'im': ['1'], 'ma': ['11'], 'ar': ['61284']}}, 'Mage'),
    )

    for box, answer in tests:
        print('{} {}'.format(box, data))
        assert olymap.utilities.xlate_magetype(box, data) == answer


def test_xlate_rank():
    tests = (
        ({}, 'undefined'),
        ({'CH': {'ra': [0]}}, 'undefined'),
        ({'CH': {'ra': ['10']}}, 'lord'),
        ({'CH': {'ra': ['20']}}, 'knight'),
        ({'CH': {'ra': ['30']}}, 'baron'),
        ({'CH': {'ra': ['40']}}, 'count'),
        ({'CH': {'ra': ['50']}}, 'earl'),
        ({'CH': {'ra': ['60']}}, 'marquess'),
        ({'CH': {'ra': ['70']}}, 'duke'),
        ({'CH': {'ra': ['80']}}, 'king'),
        ({'CH': {'rb': ['80']}}, 'undefined'),
    )

    for box, answer in tests:
        assert olymap.utilities.xlate_rank(box) == answer


def test_xlate_usekey():
    tests = (
        ('z', 'undefined'),
        ('1', 'Death Potion'),
        ('2', 'Healing Potion'),
        ('3', 'Slave Potion'),
        ('4', 'Palantir'),
        ('5', 'Projected Cast'),
        ('6', 'Quick Cast Potion'),
        ('7', 'Drum'),
        ('8', 'Elf Stone'),
        ('9', 'Orb'),
        ('10', 'undefined'),
    )

    for value, answer in tests:
        assert olymap.utilities.xlate_use_key(value) == answer


