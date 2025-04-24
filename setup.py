from setuptools import setup, Extension
from Cython.Build import cythonize

ext = Extension(
    name="mymodule",  # no package prefix
    sources=["somelibs/mymodule.pyx"],
)

setup(
    ext_modules=cythonize(ext),
)