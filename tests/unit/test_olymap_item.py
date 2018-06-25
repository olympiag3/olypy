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


def test_get_fly_capacity():
    tests = (
        ({}, None),
        ({'IT': {'fc': ['100']}}, '100'),
        ({'IT': {'fc': ['0']}}, '0'),
        ({'IT': {'de': ['60']}}, None),
        ({'IM': {'fc': ['60']}}, None),
    )

    for box, answer in tests:
        assert olymap.item.get_fly_capacity(box) == answer


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


def test_get_item_bonuses():
    tests = (
        ({}, {'attack_bonus': 0, 'defense_bonus': 0, 'missile_bonus': 0, 'aura_bonus': None}),
        ({'IM': {'ab': ['60'], 'mb': ['61'], 'db': ['62'], 'ba': ['63']}}, {'attack_bonus': 60, 'defense_bonus': 62, 'missile_bonus': 61, 'aura_bonus': '63'}),
        ({'IM': {'ab': ['60']}}, {'attack_bonus': 60, 'defense_bonus': 0, 'missile_bonus': 0, 'aura_bonus': None}),
    )

    for box, answer in tests:
        assert olymap.item.get_item_bonuses(box) == answer


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


def test_get_land_capacity():
    tests = (
        ({}, None),
        ({'IT': {'lc': ['100']}}, '100'),
        ({'IT': {'lc': ['0']}}, '0'),
        ({'IT': {'de': ['60']}}, None),
        ({'IM': {'lc': ['60']}}, None),
    )

    for box, answer in tests:
        assert olymap.item.get_land_capacity(box) == answer


def test_get_lore():
    tests = (
        ({}, None),
        ({'IM': {'lo': ['100']}}, '100'),
        ({'IM': {'lo': ['0']}}, '0'),
        ({'IM': {'de': ['60']}}, None),
        ({'IT': {'lo': ['60']}}, None),
    )

    for box, answer in tests:
        assert olymap.item.get_lore(box) == answer


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


def test_get_plural():
    tests = (
        ({}, None),
        ({'na': ['single'], 'IT': {'pl': ['plural']}}, 'plural'),
        ({'na': ['single']}, 'single'),
        ({'na': ['single'], 'IT': {'de': ['plural']}}, 'single'),
        ({'na': ['single'], 'IM': {'pl': ['plural']}}, 'single'),
    )

    for box, answer in tests:
        assert olymap.item.get_plural(box) == answer


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


def test_get_ride_capacity():
    tests = (
        ({}, None),
        ({'IT': {'rc': ['100']}}, '100'),
        ({'IT': {'rc': ['0']}}, '0'),
        ({'IT': {'de': ['60']}}, None),
        ({'IM': {'rc': ['60']}}, None),
    )

    for box, answer in tests:
        assert olymap.item.get_ride_capacity(box) == answer


