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

test_coverage: clean_coverage
	py.test --cov-report= --cov-append --cov oid --cov formatters
	(cd tests; COVERAGE='coverage run -a --source=..' ./test.sh)
	coverage combine tests/.coverage .coverage
	coverage report

