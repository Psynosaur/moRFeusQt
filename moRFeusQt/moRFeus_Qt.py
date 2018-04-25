#!/usr/bin/env python
# moRFeus python script for interfacing directly via the HID protocol

import os
import sys
import time
from moRFeusQt import moRFeus_class
from moRFeusQt import moRFeusUI

# from threading import Thread
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMainWindow

class moRFeusQt(QMainWindow):
    def __init__(self):
        # super().__init__()
        self.ui = moRFeusUI.Ui_moRFeus_Qt()
        super(moRFeusQt, self).__init__()
        self.device = moRFeus_class.initMoRFeus()
        self.moRFeusObject = moRFeus_class.moRFeus(self.device)
        self.moRFmorse = moRFeus_class.morseCode(self.device)
        self.ui.setupUi(self)
        # QtGui.QMainWindow.__init__(self)
        # Ui_MainWindow.__init__(self)
        # button actions when clicked
        self.ui.genButton.clicked.connect(self.genQt)
        self.ui.mixButton.clicked.connect(self.mixQt)
        self.ui.noiseButton.clicked.connect(self.noiseQt)
        self.ui.sweepButton.clicked.connect(self.sweepQt)
        self.ui.biasOn.clicked.connect(self.biasOnQt)
        self.ui.biasOff.clicked.connect(self.biasOffQt)
        self.ui.startFreq.valueChanged.connect(self.setEnd)
        self.ui.morseButton.clicked.connect(self.sendMorse)
        # self.morseInput.returnPressed.connect(self.sendMorse)
        self.ui.readRegButton.clicked.connect(self.getReg)
        self.ui.steps.valueChanged.connect(self.setEnd)

    # The Get functions
    def getStats(self):
        self.getFunc()
        self.getCur()
        self.getFreq()
        self.getLCD()

    # Get frequency from device and set Qt spinbox accordingly
    def getFreq(self):
        # Get Frequency message :
        # Object(moRFeus) sends message to device : a '0'(get) frequency
        self.moRFeusObject.message(0, self.moRFeusObject.funcFrequency, 0)
        # read and then set response from device
        self.ui.startFreq.setValue(self.moRFeusObject.readDevice())

    # Get current from device and set Qt spinbox accordingly
    def getCur(self):
        # Get Current message :
        # Object(moRFeus) sends message to device : a '0'(get) current
        self.moRFeusObject.message(0, self.moRFeusObject.funcCurrent, 0)
        # read and then set response from device
        self.ui.powerInput.setValue(self.moRFeusObject.readDevice())

    # Get function from device : 1 for Generator 0 for Mixer mode
    def getFunc(self):
        # Get Function message :
        # Object(moRFeus) sends message to device : a '0'(get) function
        self.moRFeusObject.message(0, self.moRFeusObject.funcMixGen, 0)
        # read and then set response from device
        self.moRFeusObject.readDevice()

    # Get register '0' from device and set Qt hex text accordingly
    def getReg(self):
        self.moRFeusObject.message(0, self.moRFeusObject.funcRegister, 0)
        while True:
            read_array = self.device.read(16)
            if read_array:
                for x in range(0, 16):
                    self.moRFeusObject.msgArray[x] = read_array[x]
                for y in range(3, 11):
                    self.moRFeusObject.buffer_array[y-3] = self.moRFeusObject.msgArray[y]
                print('read_data: ', read_array)
                reg = int.from_bytes(self.moRFeusObject.buffer_array,byteorder='big', signed=False)
                hexy = hex(reg)[0:]
                self.ui.readReg.setText(hexy)
                break

    # Get LCD value from device
    def getLCD(self):
        # Get LCD message :
        # Object(moRFeus) sends message to device : a '0'(get) LCD
        self.moRFeusObject.message(0, self.moRFeusObject.funcLCD, 0)
        # read and then set response from device
        self.moRFeusObject.readDevice()


    # set endFreq by startfreq value + stepInput
    def setEnd(self):
        self.ui.endFreq.setValue(self.ui.startFreq.value () + (self.ui.stepSize.value() / 1000 * self.ui.steps.value()))

    # loop for moving upward in frequency (increases with step)
    def freqRange(self, start, end, step):
        while start <= end:
            yield start
            start += step

    # loop for moving downward in frequency (descreases with step)
    def freqRangeReverse(self, start, end, step):
        while end >= start:
            yield end
            end -= step

    # Setting of the device LCD
    # 0 : 'Always On', 1 : '10s', 2 : '60s'
    def setLCD(self):
        # Set LCD message :
        # Object(moRFeus) sends message to device : a '1'(set) LCD
        self.moRFeusObject.message(1, self.moRFeusObject.funcLCD, 1)

    # Setting of the device biasTee On
    def biasOnQt(self):
        self.moRFeusObject.message(1, self.moRFeusObject.funcBiasTee, 1)

    # Setting of the device biasTee Off
    def biasOffQt(self):
        self.moRFeusObject.message(1, self.moRFeusObject.funcBiasTee, 0)

    # Setting of the device current
    def curQt(self):
        cur = self.ui.powerInput.value()
        self.moRFeusObject.message(1, self.moRFeusObject.funcCurrent, cur)

    # setFrequency for Qt applet,
    # mixer/generator mode which only uses a static frequency
    def statfreqQt(self):
        sFreq = self.ui.startFreq.value()
        self.moRFeusObject.message(1, self.moRFeusObject.funcFrequency, sFreq)

    # Set moRFeus to generator mode
    # Generator static frequency
    def genQt(self):
        self.curQt()
        self.moRFeusObject.message(1, self.moRFeusObject.funcMixGen, 1)
        self.statfreqQt()

    # Set moRFeus to mixer mode
    # Mixer static frequency
    def mixQt(self):
        self.curQt()
        self.moRFeusObject.message(1, self.moRFeusObject.funcMixGen, 0)
        self.statfreqQt()

    # Set to max mixer frequency to create wideband noise
    def noiseQt(self):
        self.moRFeusObject.message(1, self.moRFeusObject.funcMixGen, 1)
        self.curQt()
        self.moRFeusObject.message(1, self.moRFeusObject.funcFrequency, 5400)

    # Frequency sweep routine, still needs a means to break out of
    # loop on some event..
    def sweepQt(self):
        startFreq = self.ui.startFreq.value()
        startFreq = int(startFreq * self.moRFeusObject.mil)
        endFreq = self.ui.endFreq.value()
        endFreq = int(endFreq * self.moRFeusObject.mil)
        step  = self.ui.stepSize.value()
        step = int(step * 1000)
        delay = self.ui.delay.value()
        # hops = abs(end - start)/step
        self.moRFeusObject.message(1, self.moRFeusObject.funcMixGen, 1)
        self.curQt()
        # get steps
        condition = True
        y = 1
        while condition:
            for x in self.freqRange(startFreq, endFreq, step):
                self.moRFeusObject.message(1, self.moRFeusObject.funcFrequency, (x/self.moRFeusObject.mil))
                print(y,':', x/self.moRFeusObject.mil, "MHz")
                time.sleep(delay/1000)
                y = y + 1
            yx = y - 1
            for x in self.freqRangeReverse(startFreq, endFreq, step):
                self.moRFeusObject.message(1, self.moRFeusObject.funcFrequency, (x/self.moRFeusObject.mil))
                time.sleep(delay/1000)
                print(yx,':', x/self.moRFeusObject.mil, "MHz")
                yx = yx - 1
            break

    # Sending of morse code via current switch, 0 is off 1 is on
    def sendMorse(self):
        while True:
            morseInput = self.ui.morseInput.text()
            for letter in morseInput:
                for symbol in self.moRFmorse.MORSE[letter.upper()]:
                    if symbol == '-':
                        self.moRFmorse.dash()
                    else:
                        if symbol == '.':
                            self.moRFmorse.dot()
                        else:
                            time.sleep(0.5)
                time.sleep(0.5)
            break
        self.curQt()

    # The close event
    def closeEvent(self, event):
        self.device.close()
        print("\n--------------------\nmoRFeus Device Bye\n--------------------")
        super(QtGui.QMainWindow, self).closeEvent(event)
