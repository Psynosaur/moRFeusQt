# moRFeus_Qt

GUI tool for controlling moRFeus mixer/RF generator
on a Windows/Linux machine via the HID protocol.

Product information : https://outernet.is/pages/morfeus

This tool was written in Python3 using :

1. ##### hidapi :   `https://github.com/trezor/cython-hidapi`

2. ##### PyQt4  :   `http://pyqt.sourceforge.net/Docs/PyQt4/`

Installation  
============

### For Windows:

##### Download Python 3

    https://www.python.org/downloads/release/python-365/

In the command line navigate to your download directory:

    $ git clone https://github.com/Psynosaur/moRFeus_Qt
    $ cd moRFeus_Qt
    $ python setup.py install
    $ moRFeusQt.exe

### For Linux:
#### Prerequisites

  `$ sudo apt install python3-pip python3-dev libudev-dev libusb-1.0-0-dev`

##### moRFeus_Qt Installation

       $ git clone https://github.com/Psynosaur/moRFeus_Qt
       $ cd moRFeus_Qt
       $ sudo python3 setup.py install
       $ moRFeusQt


#### Windows :

![alt text][moRFeus]

[moRFeus]: ./moRFeusQt/imgs/windows.png "moRFeus_Qt"

#### Linux :

Ubuntu - moRFeus_Qt:

![alt text][moRFeusLinux]

[moRFeusLinux]: ./moRFeusQt/imgs/linux.png "moRFeus_Qt_linux"
