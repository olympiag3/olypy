#!/usr/bin/env python

from os import path

from setuptools import setup

packages = [
    'olypy',
    'olymap',
]

requires = [
    'PyYAML',
    'pngcanvas',
    'Jinja2',
]

test_requirements = ['pytest>=3.0.0', 'pytest-cov']

extras_require = {
    'test': test_requirements,  # setup no longer tests, so make them an extra
}

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

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    description = f.read()

setup(
    name='olypy',
    use_scm_version=True,
    description='Python code to assist the game Olympia',
    long_description=description,
    long_description_content_type='text/markdown',
    author='Greg Lindahl and others',
    author_email='lindahl@pbm.com',
    url='https://github.com/olympiag3/olypy',
    packages=packages,
    python_requires=">=3.6.*",
    extras_require=extras_require,
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
        #'Programming Language :: Python :: 3.5',  # setuptools_scm>=6 has fstrings
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
