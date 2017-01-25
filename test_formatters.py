import pytest

import formatters


def test_print_one_thing():
    with pytest.raises(KeyError):
        formatters.print_one_thing({'asdf': 'asdf'})
