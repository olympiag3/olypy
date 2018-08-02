import olymap.skill
def test_learn_time():
    tests = (
        ({}, None),
        ({'SK': {'tl': ['14']}}, '14'),
        ({'SK': {'an': ['0']}}, None),
        ({'IT': {'tl': ['1']}}, None),
        ({'SK': {'an': ['1']}}, None),
    )

    for box, answer in tests:
        assert olymap.skill.get_learn_time(box) == answer


