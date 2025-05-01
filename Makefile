
compile:
	python setup.py build_ext --inplace

dev:
	find interpreter/ -name '*.c' | entr -d make compile;
