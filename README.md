# moRFeusQt

Simple cross platform tool for controlling moRFeus mixer/RF generator via the HID protocol.

##### Features currently in development 
- [x] Multi Device Support
- [x] TCP Support Basic Sending to GQRX
- [x] Draws a power reading plot from GQRX
- [ ] VSWR sequence
- [ ] TCP server to control device remotely
- [ ] Support for Multiple SDR TCP protocols(rtl_tcp, soapytcp, etc.)
- [ ] Threading and progress bars
    
Product information : https://othernet.is/products/morfeus-1

This tool was written in Python3 using :

1. ##### hidapi :   `https://github.com/trezor/cython-hidapi`

2. ##### PyQt5  :   `https://pypi.org/project/PyQt5/`

Installation and Usage
============
### For Windows:
#### Prerequisites
###### Python 3 :

    https://www.python.org/downloads/release/python-365/

##### moRFeusQt installation and execution (PowerShell or cmd)

    pip install morfeusqt
    moRFeusQt

### For Linux:
#### Prerequisites
###### Python, libudev & libusb: 
    sudo apt install git python3.6-dev python3-setuptools python3-pip libudev-dev libusb-1.0-0-dev python3-tk

##### moRFeusQt Installation

    git clone https://github.com/Psynosaur/moRFeus_Qt && cd moRFeus_Qt

###### Removing sudo requirement for udev usb raw access :

    sudo ./hidsetup.sh

###### Install local package
    pip install .
    moRFeusQt

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
