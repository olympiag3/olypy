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


