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

test_coverage: clean_coverage
	py.test --cov-report= --cov-append --cov oid --cov formatters
	(cd tests; COVERAGE='coverage run -a --source=..' ./test.sh)
	# strictly speaking the following isn't a test, I should make a proper test
	(cd qa-lib; coverage run -a --source=.. ../modifylib.py mapgen-lib/)
	# ditto
	coverage run -a --source=. ./id.py w65
	coverage combine tests/.coverage qa-lib/.coverage .coverage
	coverage report

defaultlib:
	(cd qa-lib; python modifylib.py mapgen-lib/)
	(cd qa-lib/modified-lib; tar cjf ../../sim/defaultlib.tar.gz .)
