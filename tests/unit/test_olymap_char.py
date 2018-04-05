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


def test_get_char_break_point():
    tests = (
        ({}, '0% (fight to the death)'),
        ({'CH': {'bp': ['50']}}, '50%'),
        ({'IM': {'bp': ['1234']}}, '0% (fight to the death)'),
    )

    for box, answer in tests:
        assert olymap.char.get_break_point(box) == answer


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


def test_get_char_combat():
    tests = (
        ({}, {'attack': 0, 'defense': 0, 'missile': 0, 'behind': '0', 'behind_text': '(front line in combat)'}),
        ({'CH': {'at': ['10'], 'df': ['10'], 'mi': ['10'], 'bh': ['4']}}, {'attack': 10, 'defense': 10, 'missile': 10, 'behind': '4', 'behind_text': '(stay behind in combat)'}),
    )

    for box, answer in tests:
        assert olymap.char.get_combat(box) == answer


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


def test_get_current_aura():
    tests = (
        ({}, 0),
        ({'CM': {'ca': ['60']}}, 60),
        ({'CM': {'at': ['1234']}}, 0),
        ({'IM': {'ca': ['1234']}}, 0),
    )

    for box, answer in tests:
        assert olymap.char.get_current_aura(box) == answer


def test_get_faction():
    data = {'50033': {'firstline': ['50033 player pl_regular'], 'na': ['Test Faction']}}
    tests = (
        ({}, None),
        ({'CH': {'lo': ['50033']}}, {'id': '50033', 'oid': 'ad3', 'name': 'Test Faction'}),
        ({'CH': {'lo': ['50022']}}, None),
        ({'CH': {'at': ['50033']}}, None),
        ({'IM': {'lo': ['50033']}}, None),
    )

    for box, answer in tests:
        assert olymap.char.get_faction(box, data) == answer


def test_get_health():
    tests = (
        ({}, 'n/a'),
        ({'CH': {'he': ['100']}}, {'health': '100', 'status': None}),
        ({'CH': {'he': ['60']}}, {'health': '60', 'status': '(getting better)'}),
        ({'CH': {'he': ['60'], 'si': ['1']}}, {'health': '60', 'status': '(getting worse)'}),
        ({'CH': {'he': ['60'], 'si': ['0']}}, {'health': '60', 'status': '(getting better)'}),
        ({'CH': {'he': ['-1']}}, {'health': 'n/a', 'status': None}),
        ({'CM': {'he': ['100']}}, 'n/a'),
    )

    for box, answer in tests:
        assert olymap.char.get_health(box) == answer


def test_get_loc():
    data = {'10001': {'firstline': ['10001 loc forest'], 'na': ['Forest']},
            '1234': {'firstline': ['1234 char 0'], 'na': ['Socrates']}}
    tests = (
        ({}, None),
        ({'LI': {'wh': ['10001']}}, {'id': '10001', 'oid': 'aa01', 'name': 'Forest', 'kind': 'loc', 'subkind': 'forest'}),
        ({'LI': {'wh': ['1234']}}, {'id': '1234', 'oid': '1234', 'name': 'Socrates', 'kind': 'char', 'subkind': '0'}),        
        ({'LI': {'wh': ['10002']}}, None),
        ({'LI': {'at': ['10001']}}, None),
        ({'IM': {'wh': ['10001']}}, None),
    )

    for box, answer in tests:
        assert olymap.char.get_loc(box, data) == answer


# same unit test as xlate_loyalty in utilities
def test_get_loyalty():
    tests = (
        ({}, 'Undefined'),
        ({'CH': {'lk': [0], 'lr': [0]}}, 'Undefined'),
        ({'CH': {'lk': ['0'], 'lr': ['0']}}, 'Unsworn'),
        ({'CH': {'lk': ['1'], 'lp': ['250']}}, 'Undefined'),
        ({'CH': {'lk': ['1'], 'lr': ['250']}}, 'Contract-250'),
        ({'CH': {'lk': ['2'], 'lp': ['1']}}, 'Undefined'),
        ({'CH': {'lk': ['2'], 'lr': ['1']}}, 'Oath-1'),
        ({'CH': {'lk': ['3'], 'lp': ['10']}}, 'Undefined'),
        ({'CH': {'lk': ['3'], 'lr': ['10']}}, 'Fear-10'),
        ({'CH': {'lk': ['4'], 'lp': ['10']}}, 'Undefined'),
        ({'CH': {'lk': ['4'], 'lr': ['10']}}, 'Npc-10'),
        ({'CH': {'lk': ['5']}}, 'Summon'),
        ({'CH': {'lk': ['6']}}, 'Undefined'),
    )

    for box, answer in tests:
        assert olymap.char.get_loyalty(box) == answer


# same unit test as xlate_rank in utilities
def test_get_rank():
    tests = (
        ({}, 'undefined'),
        ({'CH': {'ra': [0]}}, 'undefined'),
        ({'CH': {'ra': ['10']}}, 'lord'),
        ({'CH': {'ra': ['20']}}, 'knight'),
        ({'CH': {'ra': ['30']}}, 'baron'),
        ({'CH': {'ra': ['40']}}, 'count'),
        ({'CH': {'ra': ['50']}}, 'earl'),
        ({'CH': {'ra': ['60']}}, 'marquess'),
        ({'CH': {'ra': ['70']}}, 'duke'),
        ({'CH': {'ra': ['80']}}, 'king'),
        ({'CH': {'rb': ['80']}}, 'undefined'),
    )

    for box, answer in tests:
        assert olymap.char.get_rank(box) == answer


def test_get_stacked_over():
    data = {'1234': {'firstline': ['1234 char 0'], 'na': ['Stack Leader'], 'LI': {'hl': ['1235', '1236']}},
            '1235': {'firstline': ['1235 char 0'], 'na': ['Minion 1']},
            '1236': {'firstline': ['1236 char 0'], 'na': ['Minion 2']}}
    tests = (
        ({}, None),
        ({'firstline': ['1234 char 0'], 'na': ['Stack Leader'], 'LI': {'hl': ['1235', '1236']}}, [{'id': '1235', 'oid': '1235', 'name': 'Minion 1'}, {'id': '1236', 'oid': '1236', 'name': 'Minion 2'}]),
        ({'firstline': ['1234 char 0'], 'na': ['Stack Leader']}, None),
    )
    for box, answer in tests:
        assert olymap.char.get_stacked_over(box, data) == answer


def test_get_vision_protection():
    tests = (
        ({}, None),
        ({'CM': {'vp': ['60']}}, '60'),
        ({'CM': {'at': ['1234']}}, None),
        ({'IM': {'vp': ['1234']}}, None),
    )

    for box, answer in tests:
        assert olymap.char.get_vision_protection(box) == answer


def test_get_where():
    data = {'10001': {'firstline': ['10001 loc forest'], 'na': ['Forest']}, 'LI': {'wh': ['40001']},
            '10002': {'firstline': ['10002 loc yew grove'], 'na': ['Yew Grove'], 'LI': {'wh': ['10001']}},
            '1234': {'firstline': ['1234 char 0'], 'na': ['Socrates'], 'LI': {'wh': ['10001']}},
            '1235': {'firstline': ['1235 char 0'], 'na': ['Plato'], 'LI': {'wh': ['1234']}},
            '40001': {'firstline': ['40001 loc region'], 'na': ['Test Region']}}
    tests = (
        ({}, None),
        ({'firstline': ['1234 char 0'], 'LI': {'wh': ['10001']}}, None),
        ({'firstline': ['1235 char 0'], 'LI': {'wh': ['1234']}}, {'id': '10001', 'oid': 'aa01', 'name': 'Forest'}),        
        ({'firstline': ['1235 char 0'], 'LI': {'wh': ['10002']}}, {'id': '10001', 'oid': 'aa01', 'name': 'Forest'}),        
        ({'firstline': ['1234 char 0'], 'LI': {'wh': ['10003']}}, None),
        ({'firstline': ['1234 char 0'], 'LI': {'at': ['10001']}}, None),
        ({'firstline': ['1234 char 0'], 'IM': {'wh': ['10001']}}, None),
    )

    for box, answer in tests:
        assert olymap.char.get_where(box, data) == answer
