
import os
import yaml
import sys
import re

sys.path.append('../')

from oid import to_int

def run_one_test(name, y):
    if y.get('lib', '') != 'defaultlib':
        raise ValueError('Sorry, defaultlib is the only supported lib atm.')
    ret = os.system('rm -rf lib')
    if ret != 0:
        raise ValueError('some problem removing lib')
    ret = os.system('mkdir -p lib')
    if ret != 0:
        raise ValueError('some problem creating lib')
    ret = os.system('cd lib; tar xf ../{}.tar.gz'.format(y['lib']))
    if ret != 0:
        raise ValueError('some problem unpacking lib')

    pass_counts = {}
    for k in y:
        if k.endswith(' orders'):
            f, _ = k.split(' ', maxsplit=1)
            with open('lib/spool/m.'+f, 'w') as fd:
                fd.write('From l@p.c\n\nbegin {} "{}"\n\n'.format(f, 'xxxxxxxx'))
                fd.write(y[k])
            pass_counts[f] = len(re.findall(r'^\s*assert\s+', y[k], flags=re.M))

    ret = os.system('./oly -e')
    if ret != 0:
        raise ValueError('some problem ingesting orders')
    ret = os.system('./oly -rMS')
    if ret != 0:
        raise ValueError('some problem running the actual sim')

    expected_pass_count = 0
    actual_pass_count = 0
    for f in pass_counts:
        expected_pass_count += pass_counts[f]
        fname = 'lib/save/2/' + to_int(f)
        if not os.path.exists(fname):
            raise ValueError('expected {} to exist'.format(fname))
        with open(fname, 'r') as fd:
            for line in fd:
                if line.endswith('PASS\n'):
                    actual_pass_count += 1

    print('{}: {}/{} '.format(name, actual_pass_count, expected_pass_count), end='')

    if actual_pass_count == expected_pass_count:
        print('PASS')
    else:
        print('FAIL')

tests = os.listdir('test-inputs')
for t in tests:
    if not t.endswith('.yml'):
        continue
    with open('test-inputs/' + t, 'r') as f:
        run_one_test(t, yaml.safe_load(f))
