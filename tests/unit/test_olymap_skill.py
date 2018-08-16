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


def test_get_required_skill():
    tests = (
            ({}, None),
            ({'SK': {'rs': ['632']}}, {'id': '632', 'oid': '632', 'name': 'Determine inventory of character'}),
            ({'SK': {'rs': ['630']}}, {'id': '630', 'oid': '630', 'name': 'Stealth'}),
            ({'SK': {'re': ['632']}}, None),
            ({'SL': {'rs': ['632']}}, None),
    )
    data = {'630': {'firstline': ['630 skill 0'], 'na': ['Stealth'], 'SK': {'tl': ['28'], 'of': ['631', '632', '633', '634', '635'], 're': ['636', '637', '638', '639']}},
            '632': {'firstline': ['632 skill 0'], 'na': ['Determine inventory of character'], 'SK': {'tl': ['14'], 'rs': ['630']}}}
 
    for box, answer in tests:
        assert olymap.skill.get_required_skill(box, data) == answer
