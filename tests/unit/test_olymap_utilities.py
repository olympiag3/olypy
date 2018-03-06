import olymap.utilities


def test_is_prisoner():
    tests = (
        ({}, False),
        ({'CH': {'pr': [0]}}, False),
        # g2 has 1,2,3 here, game code only sets TRUE/FALSE, meh
        #({'CH': {'pr': ['1']}}, True),
        ({'CH': {'pr': ['2']}}, True),
        #({'CH': {'pr': ['3']}}, True),
    )

    for v, answer in tests:
        assert olymap.utilities.is_prisoner(v) == answer
