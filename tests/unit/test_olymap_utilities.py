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


def test_get_use_key():
    tests = (
        ({}, None),
        ({'IM': {'uk': ['1']}}, '1'),
        ({'IM': {'uk': ['2']}}, '2'),
        ({'IM': {'ut': ['2']}}, None),
    )

    for box, answer in tests:
        assert olymap.utilities.get_use_key(box) == answer


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


def test_return_type():
    tests = (
        ({'firstline': ['6614 char 0']}, '0'),
        ({'firstline': ['54289 player pl_regular']}, 'pl_regular'),
        ({'firstline': ['32132 loc tunnel']}, 'tunnel'),
        ({'firstline': ['1074 ship roundship']}, 'roundship'),
        ({'firstline': ['600 skill 0']}, '0'),
        ({'firstline': ['1 item 0']}, '0'),
    )

    for box, answer in tests:
        assert olymap.utilities.return_type(box) == answer


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
