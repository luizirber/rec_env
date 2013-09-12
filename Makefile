all:

clean:
	- rm coverage.xml tests.xml pylint_*
	- find . -iname "*.pyc" -exec rm {} +;
	- find . -iname "*__pycache__*" -exec rm -rf {} +;

test:
	python setup.py test

test_all:
	tox
