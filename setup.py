#!/usr/bin/env python

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
    'olymap',
]

requires = ['PyYAML', 'pngcanvas']
test_requirements = ['pytest>=3.0.0', 'coverage', 'pytest-cov']

scripts = ['scripts/box-to-json',
           'scripts/build-player-lib',
           'scripts/copylib',
           'scripts/make-oly-map',
           'scripts/modify-qa-lib',
           'scripts/monkeypatch',
           'scripts/oid',
           'scripts/roundtriplib',
           'scripts/run-player-turn',
           'scripts/run-qa-tests']

try:
    import pypandoc
    description = pypandoc.convert_file('README.md', 'rst')
except (IOError, ImportError):
    description = open('README.md').read()

setup(
    name='olypy',
    use_scm_version=True,
    description='Python code to assist the game Olympia',
    long_description=description,
    author='Greg Lindahl and others',
    author_email='lindahl@pbm.com',
    url='https://github.com/olympiag3/olypy',
    packages=packages,
    python_requires=">=3.5.*",
    include_package_data=True,
    setup_requires=['setuptools_scm'],
    install_requires=requires,
    scripts=scripts,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
)
