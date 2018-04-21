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

#### There seems to be a error running this app on X-Server :

`$ sudo -H apt install python3-pip`

`$ sudo -H apt install libudev-dev`

##### Build hidapi from source when at step 3 opt for hidraw API instead of libusb:

`$ python setup.py build --without-libusb`

`$ sudo -H apt install python-qt4`

`$ sudo -H pip3 install --user hidapi`

##### To remove the root requirement when accessing the raw hidapi

Inside one of the rules files in /etc/udev/rules.d/

Add this line :

`SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0664", GROUP="plugdev"`

Then add yourself to the plugdev group.

`$ sudo adduser username plugdev`

Reload udev to reflect changes

`$ sudo udevadm control --reload`

`$ sudo udevadm trigger`

`$ chmod +x moRFeus.py`

Usage
=====
Application does not run when the device hasn't been connected.
#### Windows
`$ start pythonw moRFeus.pyw`

Windows - moRFeus_Qt:

![alt text][moRFeus]

[moRFeus]: ./MoRFeus_Qt.PNG "moRFeus_Qt"

#### Linux
`$ ./moRFeus.py`

Ubuntu - moRFeus_Qt:

![alt text][moRFeusLinux]

[moRFeusLinux]: ./linux.png "moRFeus_Qt_linux"
