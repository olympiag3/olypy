import olymap.utilities


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
