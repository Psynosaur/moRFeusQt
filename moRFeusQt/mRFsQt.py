#!/usr/bin/env python
# moRFeus python script for interfacing directly via the HID protocol


import sys
import time
from moRFeusQt import mRFsClass
from moRFeusQt import mRFsUI
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow
# # from threading import Thread

class moRFeusQt(QMainWindow,mRFsUI.Ui_mRFsMain):
    def __init__(self):
        super(moRFeusQt, self).__init__()
        self.setupUi(self)
        self.device = mRFsClass.initMoRFeus()
        self.moRFeus = mRFsClass.moRFeus(self.device)
        self.morse = mRFsClass.morseCode(self.device)
        # button actions when triggered
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
        print("\n--------------------\nSee you next time...\n--------------------")
        self.device.close()
        super().closeEvent(event)

    # The Get functions

    def getStats(self):
        self.getFunc()
        self.getFreq()
        self.getBias()
        self.getCur()
        self.getLCD()

    # Get frequency from device and set Qt spinbox accordingly
    def getFreq(self):
        # Get Frequency message :
        # Object(moRFeus) sends message to device : a '0'(get) frequency
        self.moRFeus.message(0, self.moRFeus.funcFrequency, 0)
        # read and then set response from device
        self.startFreq.setValue(self.moRFeus.readDevice())

    # Get current from device and set Qt spinbox accordingly
    def getCur(self):
        # Get Current message :
        # Object(moRFeus) sends message to device : a '0'(get) current
        self.moRFeus.message(0, self.moRFeus.funcCurrent, 0)
        # read and then set response from device
        self.powerInput.setValue(self.moRFeus.readDevice())

    # Get function from device : 1 for Generator 0 for Mixer mode
    def getFunc(self):
        # Get Function message :
        # Object(moRFeus) sends message to device : a '0'(get) function
        self.moRFeus.message(0, self.moRFeus.funcMixGen, 0)
        # read and then set response from device
        self.moRFeus.readDevice()

    # Get register '0' from device and set Qt hex text accordingly
    def getReg(self):
        self.moRFeus.message(0, self.moRFeus.funcRegister, 0)
        while True:
            read_array = self.device.read(16)
            if read_array:
                for x in range(0, 16):
                    self.moRFeus.msgArray[x] = read_array[x]
                for y in range(3, 11):
                    self.moRFeus.buffer_array[y-3] = self.moRFeus.msgArray[y]
                print('read_data: ', read_array)
                reg = int.from_bytes(self.moRFeus.buffer_array,byteorder='big', signed=False)
                hexy = hex(reg)[0:]
                self.readReg.setText(hexy)
                break

    # Get LCD value from device
    def getLCD(self):
        # Get LCD message :
        # Object(moRFeus) sends message to device : a '0'(get) LCD
        self.moRFeus.message(0, self.moRFeus.funcLCD, 0)
        # read and then set response from device
        self.moRFeus.readDevice()

    # Get LCD value from device
    def getBias(self):
        # Get BiasTee message :
        # Object(moRFeus) sends message to device : a '0'(get) biasTee
        self.moRFeus.message(0, self.moRFeus.funcBiasTee, 0)
        # read and then set response from device
        self.moRFeus.readDevice()

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
        self.moRFeus.message(1, self.moRFeus.funcLCD, 1)

    # Setting of the device biasTee On
    def biasOnQt(self):
        self.moRFeus.message(1, self.moRFeus.funcBiasTee, 1)

    # Setting of the device biasTee Off
    def biasOffQt(self):
        self.moRFeus.message(1, self.moRFeus.funcBiasTee, 0)

    # Setting of the device current
    def curQt(self):
        while self.device:
            try:
                cur = self.powerInput.value()
                self.moRFeus.message(1, self.moRFeus.funcCurrent, cur)
                break
            except ValueError:
                break

    # setFrequency for Qt applet,
    # mixer/generator mode which only uses a static frequency
    def statfreqQt(self):
        while self.device:
            try:
                sFreq = self.startFreq.value()
                self.moRFeus.message(1, self.moRFeus.funcFrequency, sFreq)
                break
            except ValueError:
                break

    # Set moRFeus to generator mode
    # Generator static frequency
    def genQt(self):
        self.curQt()
        self.moRFeus.message(1, self.moRFeus.funcMixGen, 1)

    # Set moRFeus to mixer mode
    # Mixer static frequency
    def mixQt(self):
        self.curQt()
        self.moRFeus.message(1, self.moRFeus.funcMixGen, 0)

    # Set to max mixer frequency to create wideband noise
    def noiseQt(self):
        self.moRFeus.message(1, self.moRFeus.funcMixGen, 1)
        self.curQt()
        self.moRFeus.message(1, self.moRFeus.funcFrequency, 5400)
        self.startFreq.setValue(5400)
        print('Such Noise . . .')

    # Frequency sweep routine, still needs a means to break out of
    # loop on some event..
    def sweepQt(self):
        startFreq = self.startFreq.value()
        startFreq = int(startFreq * self.moRFeus.mil)
        endFreq = self.endFreq.value()
        endFreq = int(endFreq * self.moRFeus.mil)
        step  = self.stepSize.value()
        step = int(step * 1000)
        delay = self.delay.value()
        # hops = abs(end - start)/step
        self.moRFeus.message(1, self.moRFeus.funcMixGen, 1)
        self.curQt()
        # get steps
        condition = True
        y = 1
        while condition:
            for x in self.freqRange(startFreq, endFreq, step):
                self.moRFeus.message(1, self.moRFeus.funcFrequency, (x/self.moRFeus.mil))
                print('FWD step', y, ':', x/self.moRFeus.mil, "MHz")
                time.sleep(delay/1000)
                y = y + 1
            y = 1
            for x in self.freqRangeReverse(startFreq, endFreq, step):
                self.moRFeus.message(1, self.moRFeus.funcFrequency, (x/self.moRFeus.mil))
                time.sleep(delay/1000)
                print('BWD step', y, ':', x/self.moRFeus.mil, "MHz")
                y = y + 1
            break

    # Sending of morse code via current switch, 0 is off 1 is on
    def sendMorse(self):
        while True:
            morseInput = self.morseInput.text()
            for letter in morseInput:
                for symbol in self.morse.MORSE[letter.upper()]:
                    if symbol == '-':
                        self.morse.dash()
                    else:
                        if symbol == '.':
                            self.morse.dot()
                        else:
                            time.sleep(0.5)
                time.sleep(0.5)
            break
        self.curQt()
