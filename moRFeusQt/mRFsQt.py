#!/usr/bin/env python
# moRFeus python script for interfacing directly via the HID protocol


import sys
import time
from moRFeusQt import mRFsClass
from moRFeusQt import mRFsUI
from PyQt5.QtGui import QCloseEvent
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
# # from threading import Thread

class moRFeusQt(QMainWindow,mRFsUI.Ui_mRFsMain):
    def __init__(self):
        super(moRFeusQt, self).__init__()
        self.setupUi(self)
        self.device = mRFsClass.initMoRFeus()
        self.moRFeusObject = mRFsClass.moRFeus(self.device)
        self.moRFmorse = mRFsClass.morseCode(self.device)
        # button actions when clicked
        self.startFreq.editingFinished.connect(self.statfreqQt)
        self.startFreq.valueChanged.connect(self.setEnd)
        self.stepSize.valueChanged.connect(self.setStep)
        self.powerInput.editingFinished.connect(self.curQt)
        self.steps.editingFinished.connect(self.setHops)
        self.mixButton.clicked.connect(self.mixQt)
        self.genButton.clicked.connect(self.genQt)
        self.noiseButton.clicked.connect(self.noiseQt)
        self.sweepButton.clicked.connect(self.sweepQt)
        self.biasOn.clicked.connect(self.biasOnQt)
        self.biasOff.clicked.connect(self.biasOffQt)
        self.morseButton.clicked.connect(self.sendMorse)
        # self.morseInput.returnPressed.connect(self.sendMorse)
        self.readRegButton.clicked.connect(self.getReg)

    def closeEvent(self, event: QCloseEvent):
        print("\n--------------------\nmoRFeus Device Bye\n--------------------")
        self.device.close()
        super().closeEvent(event)

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
        self.startFreq.setValue(self.moRFeusObject.readDevice())

    # Get current from device and set Qt spinbox accordingly
    def getCur(self):
        # Get Current message :
        # Object(moRFeus) sends message to device : a '0'(get) current
        self.moRFeusObject.message(0, self.moRFeusObject.funcCurrent, 0)
        # read and then set response from device
        self.powerInput.setValue(self.moRFeusObject.readDevice())

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
                self.readReg.setText(hexy)
                break

    # Get LCD value from device
    def getLCD(self):
        # Get LCD message :
        # Object(moRFeus) sends message to device : a '0'(get) LCD
        self.moRFeusObject.message(0, self.moRFeusObject.funcLCD, 0)
        # read and then set response from device
        self.moRFeusObject.readDevice()

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

    # The Set functions

    def setHops(self):
        self.endFreq.setValue(self.startFreq.value () + ((self.stepSize.value()/1000) * self.steps.value()))
        # self.stepSize.setValue(abs(self.endFreq.value() - self.startFreq.value()))

    def setStep(self):
        self.steps.setValue(abs(self.endFreq.value () - self.startFreq.value ()) / (self.stepSize.value()/1000))

    # set endFreq by startfreq value + stepInput
    def setEnd(self):
        self.endFreq.setValue(self.startFreq.value () + (self.stepSize.value() / 1000 * self.steps.value()))

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
        while self.device:
            try:
                cur = self.powerInput.value()
                self.moRFeusObject.message(1, self.moRFeusObject.funcCurrent, cur)
                break
            except ValueError:
                break

    # setFrequency for Qt applet,
    # mixer/generator mode which only uses a static frequency
    def statfreqQt(self):
        while self.device:
            try:
                sFreq = self.startFreq.value()
                self.moRFeusObject.message(1, self.moRFeusObject.funcFrequency, sFreq)
                break
            except ValueError:
                break

    # Set moRFeus to generator mode
    # Generator static frequency
    def genQt(self):
        self.curQt()
        self.moRFeusObject.message(1, self.moRFeusObject.funcMixGen, 1)

    # Set moRFeus to mixer mode
    # Mixer static frequency
    def mixQt(self):
        self.curQt()
        self.moRFeusObject.message(1, self.moRFeusObject.funcMixGen, 0)

    # Set to max mixer frequency to create wideband noise
    def noiseQt(self):
        self.moRFeusObject.message(1, self.moRFeusObject.funcMixGen, 1)
        self.curQt()
        self.moRFeusObject.message(1, self.moRFeusObject.funcFrequency, 5400)

    # Frequency sweep routine, still needs a means to break out of
    # loop on some event..
    def sweepQt(self):
        startFreq = self.startFreq.value()
        startFreq = int(startFreq * self.moRFeusObject.mil)
        endFreq = self.endFreq.value()
        endFreq = int(endFreq * self.moRFeusObject.mil)
        step  = self.stepSize.value()
        step = int(step * 1000)
        delay = self.delay.value()
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
            morseInput = self.morseInput.text()
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
