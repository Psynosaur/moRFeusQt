#!/usr/bin/env python
# moRFeus python script for interfacing directly via the HID protocol
from __future__ import print_function

import usb.core
import usb.util
import os
import sys
import time

from PyQt4      import QtCore, QtGui, uic
from threading  import Thread
sys.path.append('./../')
from moRFeus_class import moRFeus
from moRFeus_morse import morseCode

moRFeusCMD = moRFeus()
Ui_MainWindow, QtBaseClass = uic.loadUiType('morfeus_pyqt.ui')

class moRFeusQt(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(moRFeusQt, self).__init__()
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # button actions when clicked
        self.genbutton.clicked.connect(self.genQt)
        self.mixbutton.clicked.connect(self.mixQt)
        self.noisebutton.clicked.connect(self.noiseQt)
        self.sweepbutton.clicked.connect(self.sweepQt)
        self.biason.clicked.connect(self.biasOnQt)
        self.biasoff.clicked.connect(self.biasOffQt)
        self.powerInput.valueChanged.connect(self.curQt)
        self.startfreq.valueChanged.connect(self.statfreqQt)
        self.morsebutton.clicked.connect(self.sendMorse)

    # Convert integer(input) value to an length(8) byte sized array
    # to be used for inserting our custom array starting at
    # setFreq[3] to setFreq[10]
    def int_to_bytes(self,value, length):
        result = []
        for i in range(0, length):
            result.append(int(value) >> (i * 8) & 0xff)
        result.reverse()
        # return the result
        return result

    # init routine for moRFeus
    def initMoRFeus(self):
        while True:
            try:
                # find our device
                device = usb.core.find(idVendor=0x10c4, idProduct=0xeac9)
                # was it found?
                if device is None:
                    raise ValueError('Device not found')
                return device
                break
            except IOError:
                print('No moRFeus found... Retrying in 3 seconds')
                time.sleep(3)

        # loop for moving upward in frequency (increases with step)
    def freqRange(self,start,end,step):
        while start <= end:
            yield start
            start += step

     # loop for moving downward in frequency (descreases with step)
    def freqRangeReverse(self,start,end,step):
        while end >= start:
            yield end
            end -= step

    # The close event
    def closeEvent(self, event):
        device.close()
        super(QtGui.QMainWindow, self).closeEvent(event)

    # Setting of the device biasTee On
    def biasOnQt(self):
        device.write(moRFeusCMD.biasOn)

    # Setting of the device biasTee Off
    def biasOffQt(self):
        device.write(moRFeusCMD.biasOff)

    # Setting of the device current
    def curQt(self):
        cur = self.powerInput.value()
        for x in range(3,11):
            moRFeusCMD.setCur[x] = cur
        device.write(moRFeusCMD.setCur)

    # setFrequency for Qt applet,
    # mixer/generator mode which only uses a static frequency
    def statfreqQt(self):
        sFreq = self.startfreq.value()
        freq = int(sFreq * moRFeusCMD.mil)
        input_array = self.int_to_bytes(freq,8)
        for x in range(3,11):
            moRFeusCMD.setFreq[x] = input_array[x-3]
        device.write(moRFeusCMD.setFreq)

    # Set moRFeus to generator mode
    # Generator static frequency
    def genQt(self):
        device.write(moRFeusCMD.setGen)
        self.curQt()
        self.statfreqQt()

    # Set moRFeus to mixer mode
    # Mixer static frequency
    def mixQt(self):
        device.write(moRFeusCMD.setMix)
        self.curQt()
        self.statfreqQt()

    # Set to max LO to create noise
    def noiseQt(self):
        device.write(moRFeusCMD.setGen)
        self.curQt()
        device.write(moRFeusCMD.whiteNoise)

    # Frequency sweep routine, still needs a means to break out of
    # loop on some event..
    # Set the frequency range for the sweep feature
    # this will loop until the timeout or cancel key is pressed
    def sweepQt(self,event):
        startFreq = self.startfreq.value()
        startFreq = int(startFreq * moRFeusCMD.mil)
        endFreq = self.endfreq.value()
        endFreq = int(endFreq * moRFeusCMD.mil)
        step  = self.stepInput.value()
        t_end = time.time() + self.time.value()
        step = int(step * 1000)
        delay = self.delay.value()
        # hops = abs(end - start)/step
        device.write(moRFeusCMD.setGen)
        self.curQt()
        condition = time.time() < t_end
        while condition:
            for x in self.freqRange(startFreq,endFreq,step):
                input_array = self.int_to_bytes(x,8)
                # The y-3 offset is for the start position[0] of the input_array(i_a)
                # to be placed inside of the setFreq array at y(3) offset
                # example to be clear : i_a[0-7] a 8 byte array gets placed inside the
                # setFreq[0, 119, 129, i_a[0], i_a[1], i_a[2], i_a[3], i_a[4], i_a[5], i_a[6], i_a[7], 96, 0, 0, 2, 31, 0] array
                for y in range(3,11):
                    moRFeus.setFreq[y] = input_array[y-3]
                device.write(moRFeusCMD.setFreq)
                time.sleep(delay/1000)
            for x in self.freqRangeReverse(startFreq,endFreq,step):
                input_array = self.int_to_bytes(x,8)
                for y in range(3,11):
                    moRFeus.setFreq[y] = input_array[y-3]
                device.write(moRFeusCMD.setFreq)
                time.sleep(delay/1000)
            break

    # Sending of morse code via current switch, 0 is off 1 is on
    def sendMorse(self):
        while True:
            morse = morseCode()
            morseInput = self.morseInput.text()
            for letter in morseInput:
                for symbol in morse.MORSE[letter.upper()]:
                    if symbol == '-':
                        morse.dash(device)
                    else:
                        if symbol == '.':
                            morse.dot(device)
                        else:
                            time.sleep(0.5)
                time.sleep(0.5)
            break

if __name__ == '__main__':
# main program
    app = QtGui.QApplication(sys.argv)
    window = moRFeusQt()
    device = window.initMoRFeus()
    window.show()
    sys.exit(app.exec_())
