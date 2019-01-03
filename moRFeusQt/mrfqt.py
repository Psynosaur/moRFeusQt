#!/usr/bin/env python
# moRFeus python script for interfacing directly via the HID protocol
import time
from moRFeusQt import mrf
from moRFeusQt import mrfmorse
from moRFeusQt import mrfui
from moRFeusQt import mrfplot
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt


class MoRFeusQt(QMainWindow, mrfui.Ui_mRFsMain):
    def __init__(self, devindex):
        super(MoRFeusQt, self).__init__()
        self.setupUi(self)
        self.device = mrf.MoRFeus.initdevice(index=devindex)
        self.devindex = devindex
        self.moRFeus = mrf.MoRFeus(self.device)
        self.morseCode = mrfmorse.MorseCode(self.device)
        # button actions when triggered
        self.startFreq.editingFinished.connect(self.statfreqQt)
        self.startFreq.valueChanged.connect(self.setEnd)
        self.stepSize.valueChanged.connect(self.setStep)
        self.stepSize.editingFinished.connect(self.setStep)
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

        # I don't believe that leaving the device at 5400Mhz should be
        # allowed in this application on close, unless you started
        # with that frequency. Disconnect OUT once done

        self.check5400()
        self.device.close()
        mrfplot.MorfeusPlot.close()
        super().closeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def check5400(self):
        if self.startFreq.value() == 5400:
            self.moRFeus.message(self.moRFeus.SET, self.moRFeus.funcFrequency, self.moRFeus.initFreq)
            self.startFreq.setValue(self.moRFeus.initFreq)

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
        self.moRFeus.message(self.moRFeus.GET, self.moRFeus.funcFrequency, 0)
        # read and then set response from device
        self.startFreq.setValue(self.moRFeus.readDevice())

    # Get current from device and set Qt spinbox accordingly
    def getCur(self):
        # Get Current message :
        # Object(moRFeus) sends message to device : a '0'(get) current
        self.moRFeus.message(self.moRFeus.GET, self.moRFeus.funcCurrent, 0)
        # read and then set response from device
        self.powerInput.setValue(self.moRFeus.readDevice())

    # Get function from device : 1 for Generator 0 for Mixer mode
    def getFunc(self):
        # Get Function message :
        # Object(moRFeus) sends message to device : a '0'(get) function
        self.moRFeus.message(self.moRFeus.GET, self.moRFeus.funcMixGen, 0)
        # read and then set response from device
        self.moRFeus.readDevice()

    # Get register '0' from device and set Qt hex text accordingly
    def getReg(self):
        self.moRFeus.message(self.moRFeus.GET, self.moRFeus.funcRegister, 0)
        while True:
            read_array = self.device.read(16)
            if read_array:
                for x in range(0, 16):
                    self.moRFeus.msgArray[x] = read_array[x]
                for y in range(3, 11):
                    self.moRFeus.read_buffer[y - 3] = self.moRFeus.msgArray[y]
                print(self.devindex, 'Read Data   : ', read_array)
                reg = int.from_bytes(self.moRFeus.read_buffer, byteorder='big', signed=False)
                hexy = hex(reg)[0:]
                self.readReg.setText(hexy)
                break

    # Get LCD value from device
    def getLCD(self):
        # Get LCD message :
        # Object(moRFeus) sends message to device : a '0'(get) LCD
        self.moRFeus.message(self.moRFeus.GET, self.moRFeus.funcLCD, 0)
        # read and then set response from device
        self.moRFeus.readDevice()

    # Get LCD value from device
    def getBias(self):
        # Get BiasTee message :
        # Object(moRFeus) sends message to device : a '0'(get) biasTee
        self.moRFeus.message(self.moRFeus.GET, self.moRFeus.funcBiasTee, 0)
        # read and then set response from device
        self.moRFeus.readDevice()

    # The Set functions
    def setHops(self):
        self.endFreq.setValue(self.startFreq.value() + ((self.stepSize.value() / 1000) * self.steps.value()))
        # self.stepSize.setValue(abs(self.endFreq.value() - self.startFreq.value()))

    def setStep(self):
        self.steps.setValue(abs(self.endFreq.value() - self.startFreq.value()) / (self.stepSize.value() / 1000))

    # set endFreq by startfreq value + stepInput
    def setEnd(self):
        self.endFreq.setValue(self.startFreq.value() + (self.stepSize.value() / 1000 * self.steps.value()))

    # Setting of the device LCD
    # 0 : 'Always On', 1 : '10s', 2 : '60s'
    def setLCD(self):
        # Set LCD message :
        # Object(moRFeus) sends message to device : a '1'(set) LCD
        self.moRFeus.message(self.moRFeus.SET, self.moRFeus.funcLCD, 1)

    # Setting of the device biasTee On
    def biasOnQt(self):
        self.moRFeus.message(self.moRFeus.SET, self.moRFeus.funcBiasTee, 1)
        print(self.devindex, "Bias         :  On")

    # Setting of the device biasTee Off
    def biasOffQt(self):
        self.moRFeus.message(self.moRFeus.SET, self.moRFeus.funcBiasTee, 0)
        print(self.devindex, "Bias         :  Off")

    # Setting of the device current
    def curQt(self, cur=None):
        while self.device:
            try:
                if cur in range(0, 7):
                    self.moRFeus.message(self.moRFeus.SET, self.moRFeus.funcCurrent, cur)
                    print(self.devindex, "Current     : ", cur)
                    break
                else:
                    cur = self.powerInput.value()
                    self.moRFeus.message(self.moRFeus.SET, self.moRFeus.funcCurrent, cur)
                    print(self.devindex, "Current     : ", cur)
                    break
            except ValueError:
                break

    # setFrequency for Qt applet,
    # mixer/generator mode which only uses a static frequency
    def statfreqQt(self):
        while self.device:
            try:
                s_freq = self.startFreq.value()
                self.moRFeus.message(self.moRFeus.SET, self.moRFeus.funcFrequency, s_freq)
                print(self.devindex, "Frequency   :  {0:8.6f}".format(s_freq), "MHz")
                break
            except ValueError:
                break

    # Set moRFeus to generator mode
    # Generator static frequency
    def genQt(self):
        self.check5400()
        self.moRFeus.message(self.moRFeus.SET, self.moRFeus.funcMixGen, 1)
        print(self.devindex, "Generator   :")

    # Set moRFeus to mixer mode
    # Mixer static frequency
    def mixQt(self):
        self.check5400()
        self.moRFeus.message(self.moRFeus.SET, self.moRFeus.funcMixGen, 0)
        print(self.devindex, "Mixer       :")

    # Set to max mixer frequency to create wideband noise
    def noiseQt(self):
        self.moRFeus.message(self.moRFeus.SET, self.moRFeus.funcMixGen, 1)
        self.curQt()
        self.moRFeus.message(self.moRFeus.SET, self.moRFeus.funcFrequency, 5400)
        self.startFreq.setValue(5400)
        print(self.devindex, 'Such Noise  :')

    # Frequency sweep routine, still needs a means to break out of
    # loop on some event..
    def sweepQt(self):
        # self.curQt()
        self.moRFeus.sweepfreq(self.startFreq.value(), self.endFreq.value(), self.stepSize.value(), self.delay.value())

    # Sending some mors code
    def sendMorse(self):
        # set the current to 0 for the first character to be visible if the CW was there
        self.curQt(0)
        # sleep some time, same as end of message
        time.sleep(0.5)
        # send the message
        self.morseCode.send(self.devindex, self.morseInput.text())
        # set the current back to what it was
        self.curQt(self.powerInput.value())
