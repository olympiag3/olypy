import pytest

import olypy.formatters


def test_print_one_thing():
    with pytest.raises(KeyError):
        olypy.formatters.print_one_thing({'asdf': 'asdf'})
