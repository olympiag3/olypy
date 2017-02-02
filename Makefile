.PHONY: dist distclean

init:
	pip install -r requirements.txt

pytest:
	py.test

test: pytest
	(cd tests; ./test.sh)

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
	PYTHONPATH=. py.test --cov-report= --cov-append --cov=olypy tests
	(cd tests; PYTHONPATH=.. COVERAGE='coverage run -a --source ../scripts,olypy' ./test.sh)
#	(cd sim; coverage run -a --source=..,. ./run-tests.py test-inputs/nothing.yml)
	touch sim/.coverage
# TODO: qa
	coverage combine .coverage tests/.coverage sim/.coverage
	coverage report

defaultlib:
	(cd qa-lib/modified-lib; mkdir -p html orders spool fact)
# TODO lore?
	(cd qa-lib; python ../modifylib.py mapgen-lib)
	(cd qa-lib/modified-lib; tar cjf ../../sim/defaultlib.tar.gz .)

register:
	python setup.py register -r https://pypi.python.org/pypi

distclean:
	rm dist/*

dist: distclean
	python ./setup.py --long-description | rst2html --exit-status=2 2>&1 > /dev/null
	python ./setup.py bdist_wheel
	twine upload dist/* -r pypi
