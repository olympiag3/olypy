.PHONY: dist distclean

init:
	pip install -r requirements.txt

pytest:
	PYTHONPATH=. py.test -v -v

test: pytest
	(cd tests; PYTHONPATH=.. ./test.sh)

pylint:
	PYTHONPATH=. pylint *.py

clean_coverage:
	rm -f .coverage
	rm -f .coverage.*
	rm -f tests/.coverage
	rm -f tests/.coverage.*
	rm -f qa-lib/.coverage
	rm -f qa-lib/.coverage.*
	rm -f sim/.covereage
	rm -f sim/.covereage.*

test_coverage: clean_coverage
	PYTHONPATH=. py.test --cov-report= --cov-append --cov=olypy --cov=olymap tests
	(cd tests; PYTHONPATH=.. COVERAGE='coverage run -a --source ../scripts,olypy' ./test.sh)
#	(cd sim; coverage run -a --source=..,. ./run-tests.py test-inputs/nothing.yml)
	touch sim/.coverage
	coverage combine -a tests/.coverage sim/.coverage
	coverage report

missing:
	coverage report -m

defaultlib:
	rm -r qa-lib/modified-lib/*
	(cd qa-lib/modified-lib; mkdir -p html orders spool fact)
	(cd qa-lib; python ../scripts/modify-qa-lib mapgen-lib)
	(cd qa-lib/modified-lib; tar cjf ../../sim/defaultlib.tar.gz .)

register:
	python setup.py register -r https://pypi.python.org/pypi

distclean:
	rm -rf dist/*

dist: distclean
# if error: invalid command 'bdist_wheel', you need to make init
	python ./setup.py bdist_wheel
	twine upload dist/* -r pypi

maps: g2 g4 qa

g2:
	PYTHONPATH=. python scripts/make-oly-map lib.g2 lib.g2.out g2
	cp -p olymap/map.css lib.g2.out
	cp -p olymap/grey.gif lib.g2.out
	cp -p olymap/sorttable.js lib.g2.out

g4:
	PYTHONPATH=. python scripts/make-oly-map lib.g4-minus-grinter lib.g4.out g4
	cp -p olymap/map.css lib.g4.out
	cp -p olymap/grey.gif lib.g4.out
	cp -p olymap/sorttable.js lib.g4.out

qa:
	PYTHONPATH=. python scripts/make-oly-map lib.qa lib.qa.out qa
	cp -p olymap/map.css lib.qa.out
	cp -p olymap/grey.gif lib.qa.out
	cp -p olymap/sorttable.js lib.qa.out


