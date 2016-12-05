import pytest
from oid import to_oid, to_int, allocate_oid

oid_to_int = {
    '1': 1,
    '6940': 6940,
    'aa01': 10001,
    'ab01': 10101,
    'ba01': 12001,
    'za99': 48099,
    'zz99': 49999,
    'nn1': 53511,
    'b01': 56861,
    'w65': 58525,
    'c000': 61000,
    '99999': 99999,
    '199999': 199999,
}

invalid_oid = ('aa001', 'a0000', 'aaa0')

def test_oid():
    for oid, oint in oid_to_int.items():
        assert to_int(oid) == str(oint)
        assert to_oid(oint) == oid
        assert to_oid(int(oint)) == oid

    with pytest.raises(ValueError):
        for oid in invalid_oid:
            to_int(oid)

    for oint in range(1000,100002):
        assert to_int(to_oid(oint)) == str(oint)

    # TODO: what about 1..999 ?

    data = {}
    intoid = allocate_oid(data, 'NNNN')
    oid = to_oid(intoid)
    assert len(oid) == 4
    assert oid.isdigit()
    intoid = allocate_oid(data, 'CCNN')
    oid = to_oid(intoid)
    assert len(oid) == 4
    assert oid[0:2].isalpha()
    assert oid[2:].isdigit()
