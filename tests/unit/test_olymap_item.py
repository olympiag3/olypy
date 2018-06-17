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


