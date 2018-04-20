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

`install python3`

`pip install hidapi`

`pip install PyQt4`

Usage
=====
Application does not run when the device hasn't been connected.
##### Windows
`start pythonw moRFeus.pyw`

moRFeus_Qt:

![alt text][moRFeus]

[moRFeus]: ./MoRFeus_Qt.PNG "moRFeus_Qt"
