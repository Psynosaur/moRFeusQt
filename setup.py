import sys

if sys.version_info < (3, 5):
    print("You need at least Python 3.5 for this application!")
    if sys.version_info[0] < 3:
        print("try running with python3 {}".format(" ".join(sys.argv)))
    sys.exit(1)

try:
    from setuptools import setup
except ImportError:
    print("Could not find setuptools")
    print("Try installing them with pip install setuptools")
    sys.exit(1)


setup(
    name='moRFeusQt',
    url='https://github.com/Psynosaur/moRFeus_Qt',
    version='1.693',
    author='Ohan Smit',
    author_email='psynosaur@gmail.com',
    packages=['moRFeusQt'],
    license='LICENSE.txt',
    entry_points={
        'console_scripts': [
              'moRFeusQt = moRFeusQt.__main__:main'
        ],
    },
   install_requires=[
       'PyQt5',
       'hidapi',
   ],
)
