
import os
import yaml
import sys
import re

sys.path.append('../')

from oid import to_int

def run_one_test(y):
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

    for f in pass_counts:
        name = 'lib/save/2/' + to_int(f)
        if not os.path.exists(name):
            raise ValueError('expected {} to exist'.format(name))
        pass_count = 0
        with open(name, 'r') as fd:
            for line in fd:
                if line.endswith('PASS\n'):
                    pass_count += 1

        if pass_counts[f] == pass_count:
            print('pass count for {} looks correct'.format(f))
        else:
            print('pass count of {} for {} looks incorrect, expected {}'.format(pass_count, f, pass_counts[f]))

tests = os.listdir('test-inputs')
for t in tests:
    if not t.endswith('.yml'):
        continue
    with open('test-inputs/' + t, 'r') as f:
        run_one_test(yaml.load(f))
