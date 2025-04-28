from setuptools import setup, Extension

module = Extension('scanner', sources=['interpreter/scanner.c'])

setup(
    name='loxinterpreter',
    version='1.0',
    ext_modules=[module],
)
