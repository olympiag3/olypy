'''
Transforming Olympia ids to/from string and int
'''

import string
import re

letters = string.ascii_lowercase
letters2 = 'abcdfghjkmnpqrstvwxz' # the cut-down list that Olympia uses

letter2_to_int = { 'a': 0, 'b': 1, 'c': 2, 'd': 3, 'f': 4, 'g': 5, 'h': 6,
                  'j': 7, 'k': 8, 'm': 9, 'n': 10, 'p': 11, 'q': 12, 'r': 13,
                  's': 14, 't': 15, 'v': 16, 'w': 17, 'x': 18, 'z': 19 }

def to_oid(oid_int):
    if oid_int < 10000: # character or item
        return str(oid_int)
    elif oid_int < 50000: # location
        oid_int -= 10000
        lets = oid_int // 100
        residue = oid_int % 100
        first = lets // 20
        second = lets % 20
        return letters2[first] + letters2[second] + '{:02d}'.format(residue)
    elif oid_int < 56760: # CCN
        oid_int -= 50000
        lets = oid_int // 10
        residue = oid_int % 10
        first = lets // 26
        second = lets % 26
        return letters[first] + letters[second] + str(residue)
    elif oid_int < 58760: # CNN
        oid_int -= 56760
        residue = oid_int % 100
        first = oid_int // 100
        return letters[first] + '{:02d}'.format(residue)
    elif oid_int < 59000:
        return str(oid_int)
    elif oid_int < 79000: # CNNN
        oid_int -= 59000
        residue = oid_int % 1000
        first = oid_int // 1000
        return letters[first] + '{:03d}'.format(residue)
    else: # storms, controlled units, etc
        return str(oid_int)

def to_int(oid):
    if re.fullmatch(r'[a-z][a-z]\d', oid): # CCN
        return _i(oid[0]) * 26 * 10 + _i(oid[1]) * 10 + int(oid[2]) + 50000
    elif re.fullmatch(r'[a-z]\d\d', oid): # CNN
        return _i(oid[0]) * 100 + int(oid[1:]) + 56760
    elif re.fullmatch(r'[a-z][a-z]\d\d', oid): # CCNN, location
        return letter2_to_int[oid[0]]*20*100 + letter2_to_int[oid[1]]*100 + int(oid[2:]) + 10000
    elif re.fullmatch(r'[a-z]\d\d\d', oid): # CNNN
        return _i(oid[0]) * 1000 + int(oid[1:]) + 59000
    elif re.fullmatch(r'\d\d\d\d', oid): # NNNN
        return int(oid)
    elif re.fullmatch(r'\d\d\d\d\d', oid): # NNNNN
        return int(oid)
    elif re.fullmatch(r'1\d\d\d\d\d', oid): # 1NNNNN
        return int(oid)
    else:
        raise ValueError('invalid id value')

def _i(c):
    return ord(c) - 97
