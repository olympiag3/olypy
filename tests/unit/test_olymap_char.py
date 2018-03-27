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
