import olymap.utilities


def test_is_concealed():
    tests = (
        ({}, False),
        ({'CH': {'hs': [0]}}, False),
        ({'CH': {'hs': ['1']}}, True),
    )

    for v, answer in tests:
        assert olymap.utilities.is_concealed(v) == answer


# def test_is_fighter()


def test_is_hidden():
    tests = (
        ({}, False),
        ({'LO': {'hi': [0]}}, False),
        ({'LO': {'hi': ['1']}}, True),
    )

    for v, answer in tests:
        assert olymap.utilities.is_hidden(v) == answer


# def test_is_impassable()


def test_is_magician():
    tests = (
        ({}, False),
        ({'CM': {'im': [0]}}, False),
        ({'CM': {'im': ['1']}}, True),
    )

    for v, answer in tests:
        assert olymap.utilities.is_magician(v) == answer


def test_is_man_item():
    tests = (
        ({}, False),
        ({'IT': {'mu': [0]}}, False),
        ({'IT': {'mu': ['1']}}, True),
    )

    for v, answer in tests:
        assert olymap.utilities.is_man_item(v) == answer


def test_is_on_guard():
    tests = (
        ({}, False),
        ({'CH': {'gu': [0]}}, False),
        ({'CH': {'gu': ['1']}}, True),
    )

    for v, answer in tests:
        assert olymap.utilities.is_on_guard(v) == answer


def test_is_orb():
    tests = (
        ({}, False),
        ({'IM': {'uk': [0]}}, False),
        ({'IM': {'uk': ['9']}}, True),
        ({'IM': {'uk': ['5']}}, False),
    )

    for v, answer in tests:
        assert olymap.utilities.is_orb(v) == answer


def test_is_priest():
    tests = (
        ({}, False),
        ({'CH': {'sl': ['800', '2']}}, False),
        ({'CH': {'sl': ['750', '1']}}, False),
        ({'CH': {'sl': ['750', '2']}}, True),
    )

    for v, answer in tests:
        assert olymap.utilities.is_priest(v) == answer


def test_is_prisoner():
    tests = (
        ({}, False),
        ({'CH': {'pr': [0]}}, False),
        # g2 has 1,2,3 here, game code only sets TRUE/FALSE, meh
        ({'CH': {'pr': ['1']}}, True),
        ({'CH': {'pr': ['2']}}, False),
        #({'CH': {'pr': ['3']}}, True),
    )

    for v, answer in tests:
        assert olymap.utilities.is_prisoner(v) == answer


def test_is_prominent():
    tests = (
        ({}, False),
        ({'IT': {'pr': [0]}}, False),
        ({'IT': {'pr': ['1']}}, True),
    )

    for v, answer in tests:
        assert olymap.utilities.is_prominent(v) == answer


def test_is_projected_cast():
    tests = (
        ({}, False),
        ({'IM': {'uk': [0]}}, False),
        ({'IM': {'uk': ['9']}}, False),
        ({'IM': {'uk': ['5']}}, True),
    )

    for v, answer in tests:
        assert olymap.utilities.is_projected_cast(v) == answer


def test_is_road_or_gate():
    tests = (
        ({}, False),
        ({'GA': {'tl': [0]}}, True),
        ({'GA': {'tl': ['1']}}, True),
    )

    for v, answer in tests:
        assert olymap.utilities.is_road_or_gate(v) == answer
