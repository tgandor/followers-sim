# Just for py2exe, because this program works standalone.
# https://stackoverflow.com/a/113014/1338797

# run with:
# > python setup.py py2exe

# this currently works only with python 3.4
# for anaconda try:
# > conda install -c kieranharding py2exe

from distutils.core import setup
# noinspection PyUnresolvedReferences
import py2exe

setup(
    options={'py2exe': {'bundle_files': 3, 'compressed': True}},
    windows=[{'script': "main.py"}],
    zipfile=None,
)
