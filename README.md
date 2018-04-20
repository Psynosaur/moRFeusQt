# moRFeus_Qt

GUI tool for controlling moRFeus mixer/RF generator
on a Windows machine via the HID protocol.

(Linux support in testing)

Product information : https://outernet.is/pages/morfeus

This tool was written in Python using :

hidapi : https://github.com/trezor/cython-hidapi

PyQt4  : http://pyqt.sourceforge.net/Docs/PyQt4/

Installation  
============

#### For Windows:

`Download Python 3`

`Download PyQt4`

https://download.lfd.uci.edu/pythonlibs/u2yrk7ps/PyQt4-4.11.4-cp36-cp36m-win32.whl`

In the command line navigate to download directory:

`pip install hidapi`

`pip install PyQt4-4.11.4-cp36-cp36m-win32.whl`


#### For Linux:

`sudo -H apt install python-pip`

`sudo -H apt install python-qt4`

`sudo -H apt-get install python-dev libusb-1.0-0-dev libudev-dev`

`pip install hidapi`

Usage
=====
Application does not run when the device hasn't been connected.
#### Windows
`start pythonw moRFeus.pyw`

moRFeus_Qt:

![alt text][moRFeus]

[moRFeus]: ./MoRFeus_Qt.PNG "moRFeus_Qt"

#### Linux
`sudo python moRFeus.py`

moRFeus_Qt:

![alt text][moRFeusLinux]

[moRFeusLinux]: ./linux.png "moRFeus_Qt_linux"
