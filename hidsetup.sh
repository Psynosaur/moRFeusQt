#!/bin/bash

# hidapi usb raw access console_scripts
# removes moRFeusQt sudo requirement

# assumes it was just installed, so its creates the file
touch /etc/udev/rules.d/10-local.rules
# adds the moRFeus to the allowed subsystem
echo 'SUBSYSTEM=="usb", ATTRS{product}=="moRFeus", MODE="0664", GROUP="plugdev"' >> /etc/udev/rules.d/10-local.rules

# adduser $SUDO_USER plugdev

# reload udevadm
udevadm control --reload
udevadm trigger
