import olymap.utilities


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


# def test_is_impassable()


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
