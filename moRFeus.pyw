# moRFeus python script for interfacing directly via the HID protocol
from __future__ import print_function
from PyQt4      import QtCore, QtGui, uic

import hid
import os
import sys
import time

# I have not bothered to implement the get Functions from the moRFeus tool, since it doesn't really serve a purpose
# since there seems to be a LED screen, ya know. . .

def int_to_bytes(value, length):                                                # Convert integer(input) value to an length(8) byte sized array
    result = []                                                                 # to be used for inserting our custom array starting at
    for i in range(0, length):                                                  # setFreq[3] to setFreq[10]
        result.append(int(value) >> (i * 8) & 0xff)
    result.reverse()
    return result                                                               # return the result

def initMoRFeus():                                                              # init routine for moRFeus
    device = hid.device()
    device.open(0x10c4, 0xeac9)                                                 # moRFeus VendorID/ProductID
    return device

def freqRange(start,end,step):                                                  # loop for moving upward in frequency (increases with step)
    while start <= end:
        yield start
        start += step

def freqRangeReverse(start,end,step):                                           # loop for moving downward in frequency (descreases with step)
    while end >= start:
        yield end
        end -= step

class moRFeus(object):
    # Constants
    LOmax        = 5400000000                                                       # Local Oscillator max (5400MHz)
    LOmin        = 85000000                                                         # Local Oscillator min (85Mhz)
    mil          = 1000000                                                          # Saves some zero's here and there
    # Byte Arrays known to the moRFeus device
    readReg      = [0, 114, 0, 0, 0, 0, 0, 0, 0, 190, 250, 0, 0, 96, 0, 0, 0]       # heh?
    setGen       = [0, 119, 130, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]          # Generator mode
    setMix       = [0, 119, 130, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]          # Mixer mode
    biasOn       = [0, 119, 132, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]          # BiasTee on
    biasOff      = [0, 119, 132, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]          # BiasTee off
    whiteNoise   = [0, 119, 129, 0, 0, 0, 1, 65, 221, 118, 0, 96, 0, 0, 2, 31, 0]   # setFrequency to 5400 000 000 Hz

    setCurrent   = [0, 119, 131, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]          # setCurrent bytearray template
    setCur       = bytearray(setCurrent)                                            # we declare it a bytearray for manipulation of setCur[x]
                                                                                    # with our custom 8byte current array
    setFrequency = [0, 119, 129, 0, 0, 0, 1, 65, 221, 118, 0, 96, 0, 0, 2, 31, 0]   # setFrequency bytearray template
    setFreq      = bytearray(setFrequency)                                          # we declare it a bytearray for manipulation of setFreq[x]
                                                                                    # with our custom 8byte frequency array
Ui_MainWindow, QtBaseClass = uic.loadUiType('morfeus_pyqt.ui')
class moRFeusQt(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
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

    def closeEvent(self, event):
        # here you can terminate your threads and do other stuff
        device.close()
        # and afterwards call the closeEvent of the super-class
        super(QtGui.QMainWindow, self).closeEvent(event)

    def biasOnQt(self):
        device.write(moRFeus.biasOn)

    def biasOffQt(self):
        device.write(moRFeus.biasOff)

    def curQt(self,):
        cur = self.powerInput.value()
        for x in range(3,11):
            moRFeus.setCur[x] = cur
        device.write(moRFeus.setCur)

    def statfreqQt(self):                                                       # setFrequency for cmdline applet, mixer mode which only uses a static frequency
        sFreq = self.startfreq.value()
        freq = int(sFreq * moRFeus.mil)
        input_array = int_to_bytes(freq,8)
        for x in range(3,11):
            moRFeus.setFreq[x] = input_array[x-3]
        device.write(moRFeus.setFreq)

    def genQt(self):                                                            # Generator static frequency
        device.write(moRFeus.setGen)
        self.curQt()
        self.statfreqQt()

    def mixQt(self):                                                            # Mixer static frequency
        device.write(moRFeus.setMix)
        self.curQt()
        self.statfreqQt()

    def noiseQt(self):
        device.write(moRFeus.setGen)
        self.curQt()
        device.write(moRFeus.whiteNoise)

    def sweepQt(self):
        startFreq = self.startfreq.value()
        startFreq = int(startFreq * moRFeus.mil)
        endFreq = self.endfreq.value()
        endFreq = int(endFreq * moRFeus.mil)
        step  = self.stepInput.value()
        t_end = time.time() + self.time.value()
        step = int(step * 1000)
        delay = self.delay.value()
        # hops = abs(end - start)/step
        device.write(moRFeus.setGen)
        self.curQt()
        while time.time() < t_end:                                              # Set the frequency range for the sweep feature
            for x in freqRange(startFreq,endFreq,step):                         # this will loop until the timeout or cancel key is pressed
                input_array = int_to_bytes(x,8)
                for y in range(3,11):
                    moRFeus.setFreq[y] = input_array[y-3]                       # The y-3 offset is for the start position[0] of the input_array(i_a)
                device.write(moRFeus.setFreq)                                   # to be placed inside of the setFreq array at y(3) offset
                time.sleep(delay/1000)                                          # example to be clear : i_a[0-7] a 8 byte array gets placed inside the
            for x in freqRangeReverse(startFreq,endFreq,step):                  # setFreq[0, 119, 129, i_a[0], i_a[1], i_a[2], i_a[3], i_a[4], i_a[5], i_a[6], i_a[7], 96, 0, 0, 2, 31, 0]
                input_array = int_to_bytes(x,8)
                for y in range(3,11):
                    moRFeus.setFreq[y] = input_array[y-3]
                device.write(moRFeus.setFreq)
                time.sleep(delay/1000)
                break


if __name__ == '__main__':
# main program
    device = initMoRFeus()
    app = QtGui.QApplication(sys.argv)
    window = moRFeusQt()
    window.show()
    sys.exit(app.exec_())
