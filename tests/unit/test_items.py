from olypy.items import item, item_plural


def test_items():
    assert item(71) == 'pretus bones'
    assert item('71') == 'pretus bones'
    assert item_plural(71) == 'pretus bones'
    assert item_plural('295') == 'hounds'
    assert item_plural(25) == 'elves'
    assert item_plural(20) == 'swordsmen'
