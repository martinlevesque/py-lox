
compile:
	python setup.py build_ext --inplace

dev:
	find interpreter/ -name '*.c' | entr -d make compile;

test: compile
	PYTHONPATH=. pytest

test-watch:
	find ./ -name '*.c' -o -name '*.py' | entr -d sh -c 'black . && make test'
