# moRFeus_Qt

GUI tool for controlling moRFeus mixer/RF generator
on a Windows/Linux machine via the HID protocol.

Product information : https://outernet.is/pages/morfeus

This tool was written in Python3 using :

hidapi(RAW) : https://github.com/trezor/cython-hidapi

PyQt4  : http://pyqt.sourceforge.net/Docs/PyQt4/

Installation  
============

#### For Windows:

`Download Python 3`

https://www.python.org/downloads/release/python-365/

`Download PyQt4`

https://download.lfd.uci.edu/pythonlibs/u2yrk7ps/PyQt4-4.11.4-cp36-cp36m-win_amd64.whl

In the command line navigate to download directory:

`$ pip3 install --user hidapi`

`$ pip3 install --user PyQt4-4.11.4-cp36-cp36m-win_amd64.whl`


#### For Linux:

`$ sudo -H apt install python3-pip`

##### Build hidapi from source when at step 3 opt for hidraw API instead of libusb:

`$ python setup.py build --without-libusb`

`$ sudo -H apt install python-qt4`

`$ sudo -H pip3 install --user hidapi`

Usage
=====
Application does not run when the device hasn't been connected.
#### Windows
`$ start pythonw moRFeus.pyw`

Windows - moRFeus_Qt:

![alt text][moRFeus]

[moRFeus]: ./MoRFeus_Qt.PNG "moRFeus_Qt"

#### Linux
`$ sudo python moRFeus.py`

Ubuntu - moRFeus_Qt:

![alt text][moRFeusLinux]

[moRFeusLinux]: ./linux.png "moRFeus_Qt_linux"
