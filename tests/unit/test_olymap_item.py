import olymap.item
def test_get_animal():
    tests = (
        ({}, None),
        ({'IT': {'an': ['1']}}, True),
        ({'IT': {'an': ['0']}}, None),
        ({'IT': {'de': ['1']}}, None),
        ({'IM': {'an': ['1']}}, None),
    )

    for box, answer in tests:
        assert olymap.item.get_animal(box) == answer


def test_get_attack_bonus():
    tests = (
        ({}, 0),
        ({'IM': {'ab': ['60']}}, 60),
        ({'IM': {'ab': ['0']}}, 0),
        ({'IM': {'de': ['60']}}, 0),
        ({'IT': {'ab': ['60']}}, 0),
    )

    for box, answer in tests:
        assert olymap.item.get_attack_bonus(box) == answer


def test_get_aura_bonus():
    tests = (
        ({}, None),
        ({'IM': {'ba': ['60']}}, '60'),
        ({'IM': {'ba': ['0']}}, '0'),
        ({'IM': {'de': ['60']}}, None),
        ({'IT': {'ba': ['60']}}, None),
    )

    for box, answer in tests:
        assert olymap.item.get_aura_bonus(box) == answer


def test_get_defense_bonus():
    tests = (
        ({}, 0),
        ({'IM': {'db': ['60']}}, 60),
        ({'IM': {'db': ['0']}}, 0),
        ({'IM': {'de': ['60']}}, 0),
        ({'IT': {'db': ['60']}}, 0),
    )

    for box, answer in tests:
        assert olymap.item.get_defense_bonus(box) == answer


def test_get_item_attack():
    tests = (
        ({}, None),
        ({'IT': {'at': ['60']}}, '60'),
        ({'IT': {'at': ['0']}}, '0'),
        ({'IT': {'de': ['60']}}, None),
        ({'IM': {'at': ['60']}}, None),
    )

    for box, answer in tests:
        assert olymap.item.get_item_attack(box) == answer


def test_get_item_defense():
    tests = (
        ({}, None),
        ({'IT': {'de': ['60']}}, '60'),
        ({'IT': {'de': ['0']}}, '0'),
        ({'IT': {'at': ['60']}}, None),
        ({'IM': {'de': ['60']}}, None),
    )

    for box, answer in tests:
        assert olymap.item.get_item_defense(box) == answer


def test_get_item_missile():
    tests = (
        ({}, None),
        ({'IT': {'mi': ['60']}}, '60'),
        ({'IT': {'mi': ['0']}}, '0'),
        ({'IT': {'de': ['60']}}, None),
        ({'IM': {'mi': ['60']}}, None),
    )

    for box, answer in tests:
        assert olymap.item.get_item_missile(box) == answer


def test_get_man_item():
    tests = (
        ({}, None),
        ({'IT': {'mu': ['1']}}, True),
        ({'IT': {'mu': ['0']}}, None),
        ({'IT': {'de': ['1']}}, None),
        ({'IM': {'mu': ['1']}}, None),
    )

    for box, answer in tests:
        assert olymap.item.get_man_item(box) == answer


def test_get_missile_bonus():
    tests = (
        ({}, 0),
        ({'IM': {'mb': ['60']}}, 60),
        ({'IM': {'mb': ['0']}}, 0),
        ({'IM': {'mi': ['60']}}, 0),
        ({'IT': {'mb': ['60']}}, 0),
    )

    for box, answer in tests:
        assert olymap.item.get_missile_bonus(box) == answer


def test_get_prominent():
    tests = (
        ({}, None),
        ({'IT': {'pr': ['1']}}, True),
        ({'IT': {'pr': ['0']}}, None),
        ({'IT': {'de': ['1']}}, None),
        ({'IM': {'pr': ['1']}}, None),
    )

    for box, answer in tests:
        assert olymap.item.get_prominent(box) == answer





