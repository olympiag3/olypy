import pytest

from oio import write_oly_file, read_oly_file

'''
This test isn't super-comprehensive; the roundtrip
tests exercise all of this code.
'''

example_data = {
    '6666': {
        'firstline': [ '6666 the first line' ],
        'na': [ 'Mitu Foo' ],
        'il': [ 10, 10, 101, 1 ],
        # skipping 'an' on purpose
        'ad': [ 54289, 56511 ],
        'CH': { 'ni': [ 123 ],
                'sl': [ 610, 2, 21, 11, 0, 612, 2, 28, 1, 0, ],
              },
        'LI': { 'wh': [ 54321 ],
              },
    }
}

example_output = '''6666 the first line
na Mitu Foo
il	10 10 \\
	101 1
ad 54289 56511 
LI
 wh 54321
CH
 ni 123
 sl	610 2 21 11 0 \\
	612 2 28 1 0

'''

def test_formatters(capsys):
    write_oly_file(example_data, [])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == example_output

    data = read_oly_file(example_output.split('\n'))
    assert len(data) == 1
    write_oly_file(data)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == example_output
