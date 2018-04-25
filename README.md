# moRFeus_Qt

GUI tool for controlling moRFeus mixer/RF generator
on a Windows/Linux machine via the HID protocol.

Product information : https://outernet.is/pages/morfeus

This tool was written in Python3 using :

1. ##### hidapi :

       https://github.com/trezor/cython-hidapi

2. ##### PyQt4  :

       http://pyqt.sourceforge.net/Docs/PyQt4/

Installation  
============

### For Windows:

##### Download Python 3

    https://www.python.org/downloads/release/python-365/

##### Download PyQt4`

    https://www.lfd.uci.edu/~gohlke/pythonlibs/
    Search: `PyQt4'
    Download : PyQt4‑4.11.4‑cp36‑cp36m‑win_amd64.whl
    
   `$ pip3 install --user PyQt4-4.11.4-cp36-cp36m-win_amd64.whl`

In the command line navigate to your download directory:

    $ git clone https://github.com/Psynosaur/moRFeus_Qt
    $ cd moRFeus_Qt
    $ pip3 install --user hidapi
    $ python -m pip install .

### For Linux:
#### Prerequisites

  `$ sudo apt install python3-pip python3-dev libudev-dev libusb-1.0-0-dev python3-PyQt4`


##### Build hidapi from source when at step 3 opt for hidraw API instead of libusb:
1. Download cython-hidapi archive:

       $ git clone https://github.com/trezor/cython-hidapi.git
       $ cd cython-hidapi
       $ git submodule update --init
       $ python3 setup.py build --without-libusb
       $ sudo python3 setup.py install

##### moRFeus_Qt Installation

       $ git clone https://github.com/Psynosaur/moRFeus_Qt
       $ cd moRFeus_Qt
       $ python3 -m pip install .

##### (Optional) To remove the root requirement when accessing the raw hidapi

##### Inside one of the rules files in /etc/udev/rules.d/

###### Add this line :

    SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0664", GROUP="plugdev"


###### Then add yourself to the plugdev group.

    $ sudo adduser $USERNAME plugdev

###### Reload udev to reflect changes

    $ sudo udevadm control --reload
    $ sudo udevadm trigger

Usage
=====
#### When device isn't connected

Device not found:

![alt text][DNF]

[DNF]: ./moRFeusQt/imgs/dnf.png "moRFeus_Qt"

#### Windows
    $ moRFeusQt

Windows - moRFeus_Qt:

![alt text][moRFeus]

[moRFeus]: ./moRFeusQt/imgs/windows.png "moRFeus_Qt"

#### Linux
    $ moRFeusQt

Ubuntu - moRFeus_Qt:

![alt text][moRFeusLinux]

[moRFeusLinux]: ./moRFeusQt/imgs/linux.png "moRFeus_Qt_linux"
