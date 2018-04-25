import sys
from setuptools import setup


if sys.version_info < (3, 6):
    print("You need at least Python 3.6 for this application!")
    if sys.version_info[0] < 3:
        print("try running with python3 {}".format(" ".join(sys.argv)))
    sys.exit(1)

try:
    from setuptools import setup, Extension
    from setuptools.command.build_ext import build_ext as _build_ext
except ImportError:
    print("Could not find setuptools")
    print("Try installing them with pip install setuptools")
    sys.exit(1)


setup(
    name='moRFeusQt',
    url='https://github.com/Psynosaur/moRFeus_Qt',
    version='0.969',
    author='Ohan Smit',
    author_email='psynosaur@gmail.com',
    packages=['moRFeusQt'],
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    entry_points={
        'console_scripts': [
              'moRFeusQt = moRFeusQt.__main__:main'
        ],
    },
#    install_requires=[
#        'PyQt4',
#        'hidapi',
#    ],
)
# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/
