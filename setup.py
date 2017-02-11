#!/usr/bin/env python

import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


packages = [
    'olypy',
]

requires = []
test_requirements = ['pytest>=3.0.0', 'coverage', 'pytest-cov']

scripts = ['scripts/box-to-json',
           'scripts/build-player-lib',
           'scripts/copylib',
           'scripts/modify-qa-lib',
           'scripts/monkeypatch',
           'scripts/oid',
           'scripts/roundtriplib',
           'scripts/run-player-turn',
           'scripts/run-qa-tests']

with open('olypy/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = open('README.md').read()

# XXX need to add data_files for all the crap that's text

setup(
    name='olypy',
    version=version,
    description='Python code to assist the game Olympia',
    long_description=description,
    author='Greg Lindahl and others',
    author_email='lindahl@pbm.com',
    url='https://github.com/olympiag3/olypy',
    packages=packages,
    install_requires=requires,
    scripts=scripts,
    license='Apache 2.0',
    zip_safe=True,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ),
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
)
