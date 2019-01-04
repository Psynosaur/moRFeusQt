import sys

if sys.version_info < (3, 6):
    print("You need at least Python 3.6 for this application!")
    if sys.version_info[0] < 3:
        print("try running with python3 {}".format(" ".join(sys.argv)))
    sys.exit(1)

try:
    from setuptools import setup, find_packages
except ImportError:
    print("Could not find setuptools")
    print("Try installing them with pip install setuptools")
    sys.exit(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='moRFeusQt',
    url='https://github.com/Psynosaur/moRFeus_Qt',
    version='3.333',
    author='Ohan Smit',
    author_email='psynosaur@gmail.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='LICENSE.txt',
    entry_points={
        'console_scripts': [
            'moRFeusQt = moRFeusQt.__main__:main'
        ],
    },
    install_requires=[
        'PyQt5==5.11.2',
        'hidapi',
        'matplotlib',
    ],
    test_suite='tests.mRF_test_suite',

)
