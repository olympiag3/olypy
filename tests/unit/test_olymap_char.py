import olymap.char


def test_get_char_attack():
    tests = (
        ({}, 0),
        ({'CH': {'at': ['60']}}, 60),
        ({'CH': {'de': ['1234']}}, 0),
        ({'IM': {'at': ['1234']}}, 0),
    )

    for box, answer in tests:
        assert olymap.char.get_char_attack(box) == answer


def test_get_char_behind():
    tests = (
        ({}, '0'),
        ({'CH': {'bh': ['1']}}, '1'),
        ({'CH': {'bh': ['0']}}, '0'),
        ({'CH': {'at': ['1']}}, '0'),
        ({'IM': {'bh': ['1']}}, '0'),
    )

    for box, answer in tests:
        assert olymap.char.get_char_behind(box) == answer


def test_get_char_defense():
    tests = (
        ({}, 0),
        ({'CH': {'df': ['60']}}, 60),
        ({'CH': {'at': ['1234']}}, 0),
        ({'IM': {'df': ['1234']}}, 0),
    )

    for box, answer in tests:
        assert olymap.char.get_char_defense(box) == answer


def test_get_char_missile():
    tests = (
        ({}, 0),
        ({'CH': {'mi': ['60']}}, 60),
        ({'CH': {'at': ['1234']}}, 0),
        ({'IM': {'mi': ['1234']}}, 0),
    )

    for box, answer in tests:
        assert olymap.char.get_char_missile(box) == answer


def test_get_current_aura():
    tests = (
        ({}, 0),
        ({'CM': {'ca': ['60']}}, 60),
        ({'CM': {'at': ['1234']}}, 0),
        ({'IM': {'ca': ['1234']}}, 0),
    )

    for box, answer in tests:
        assert olymap.char.get_current_aura(box) == answer


def test_get_faction():
    data = {'50033': {'firstline': ['50033 player pl_regular'], 'na': ['Test Faction']}}
    tests = (
        ({}, None),
        ({'CH': {'lo': ['50033']}}, {'id': '50033', 'oid': 'ad3', 'name': 'Test Faction'}),
        ({'CH': {'lo': ['50022']}}, None),
        ({'CH': {'at': ['50033']}}, None),
        ({'IM': {'lo': ['50033']}}, None),
    )

    for box, answer in tests:
        assert olymap.char.get_faction(box, data) == answer


# same unit test as xlate_loyalty in utilities
def test_get_loyalty():
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
        assert olymap.char.get_loyalty(box) == answer


# same unit test as xlate_rank in utilities
def test_get_rank():
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
        assert olymap.char.get_rank(box) == answer


def test_get_vision_protection():
    tests = (
        ({}, None),
        ({'CM': {'vp': ['60']}}, '60'),
        ({'CM': {'at': ['1234']}}, None),
        ({'IM': {'vp': ['1234']}}, None),
    )

    for box, answer in tests:
        assert olymap.char.get_vision_protection(box) == answer
