# moRFeusQt

Simple cross platform tool for controlling moRFeus mixer/RF generator via the HID protocol.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d44e40b29adb45a994760b56facb284b)](https://www.codacy.com/app/Psynosaur/moRFeus_Qt?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Psynosaur/moRFeus_Qt&amp;utm_campaign=Badge_Grade)


Product information : https://othernet.is/products/morfeus-1

This tool was written in Python3 using :

1. ##### hidapi :   `https://github.com/trezor/cython-hidapi`

2. ##### PyQt5  :   `https://pypi.org/project/PyQt5/`

Installation and Usage
============
##### The following instructions assume that you have a git environment installed...

### For Windows:
#### Prerequisites
###### Python 3 :

    https://www.python.org/downloads/release/python-365/

##### moRFeusQt Installation

    $ git clone https://github.com/Psynosaur/moRFeus_Qt
    $ cd moRFeus_Qt
    $ python setup.py install
    $ moRFeusQt.exe

### For Linux:
#### Prerequisites
###### Python, libudev & libusb:
    $ sudo apt install python3.6-dev python3-setuptools python3-pip libudev-dev libusb-1.0-0-dev

##### moRFeusQt Installation

    $ git clone https://github.com/Psynosaur/moRFeus_Qt && cd moRFeus_Qt

###### Removing sudo requirement for udev usb raw access :

    $ sudo ./hidsetup.sh

###### Install local package
    $ python3 setup.py install
    $ moRFeusQt

### For Mac OS:
#### Prerequisites
###### Homebrew
From : https://brew.sh/

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

###### Python :

    $ brew install python

##### moRFeus_Qt Installation

    $ git clone https://github.com/Psynosaur/moRFeus_Qt && cd moRFeus_Qt
    $ python3 setup.py install
    $ moRFeusQt

#### Unit Tests
    
    $ python setup.py test
