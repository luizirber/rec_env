all:

clean:
	- rm coverage.xml tests.xml pylint_*

test:
	python setup.py test

test_all:
	tox
