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
	py.test --cov-report= --cov-append --cov oid --cov formatters --cov oio --cov data --cov items --cov turnparser
	(cd tests; COVERAGE='coverage run -a --source=..' ./test.sh)
#	(cd sim; coverage run -a --source=..,. ./run-tests.py test-inputs/nothing.yml)
	touch sim/.coverage
	coverage combine .coverage tests/.coverage sim/.coverage
	coverage report

defaultlib:
	(cd qa-lib/modified-lib; mkdir -p html orders spool fact)
	(cd qa-lib; python ../modifylib.py mapgen-lib)
	(cd qa-lib/modified-lib; tar cjf ../../sim/defaultlib.tar.gz .)
