# moRFeus python script for interfacing directly via the HID protocol
from __future__ import print_function
# pip install hidapi
import hid
import os
#import msvcrt
import sys
import time

sys.path.append('./../')
from moRFeus_morse import morseCode
from moRFeus_class import moRFeus

moRF = moRFeus()
class moRFeusCmd(object):

    def int_to_bytes(self,value, length):                                       # Convert integer(input) value to an length(8) byte sized array
        result = []                                                             # to be used for inserting our custom array starting at
        for i in range(0, length):                                              # setFreq[3] to setFreq[10]
            result.append(int(value) >> (i * 8) & 0xff)
        result.reverse()
        return result                                                           # return the result

    def moRFeusCheck(self):                                                     # Is there a device?
        while True:
            try:
                device = hid.device()
                device.open(0x10c4, 0xeac9)
                break
            except IOError:
                return 1

    def initMoRFeus(self):                                                      # init routine for moRFeus
        print("Opening the device")
        device = hid.device()
        device.open(0x10c4, 0xeac9)                                             # moRFeus VendorID/ProductID
        print("MoRFeus opened")
        # enable non-blocking mode
        device.set_nonblocking(0)
        return device

    def closeMoRFeus(self,device):                                              # close routine for moRFeus
        print("Closing the device")
        device.close()

    def freqRange(self,start,end,step):                                         # loop for moving upward in frequency (increases with step)
        while start <= end:
            yield start
            start += step

    def freqRangeReverse(self,start,end,step):                                  # loop for moving downward in frequency (descreases with step)
        while end >= start:
            yield end
            end -= step

    def setCurrents(self,device):                                               # setCurrent for cmdline applet
        while True:
            try:
                cur=int(input('Please select current 0-7: \n'))
            except ValueError:
                print("Not a integer...")
            else:
                if cur <= 7 and cur >= 0:
                    print("Current set to:", cur)
                else:
                    print("Value not between 0 and 7...")
                    continue
                for x in range(3,11):
                    moRF.setCur[x] = cur
                device.write(moRF.setCur)
                break

    def setFreqStatic(self,device):                                             # setFrequency for cmdline applet, mixer mode which only uses
        while True:                                                             # a static frequency
            try:
                freq=float(input('Please enter a frequency from 85 - 5400MHz: \n'))
            except ValueError:
                print("Not a float...")
            else:
                freq = int(freq * moRF.mil)
                input_array = self.int_to_bytes(freq,8)
                if freq <= moRF.LOmax and freq >= moRF.LOmin:
                    print("Frequency set to:", freq)
                else:
                    print("Value not between 85 - 5400MHz...")
                    continue
                for x in range(3,11):
                    moRF.setFreq[x] = input_array[x-3]
                device.write(moRF.setFreq)
                break

    def setfreqRange(self,evice,start,end,step):                                # Set the frequency range for the sweep feature
        while True:                                                             # this will loop indefinitely until escape key is pressed
            print("Sweeping range",start,"-",end,
            "Hz - Press Esc to cancel(loop will finish...)")
            for x in self.freqRange(start,end,step):
                input_array = self.int_to_bytes(x,8)
                for y in range(3,11):
                    moRF.setFreq[y] = input_array[y-3]                          # The y-3 offset is for the start position[0] of the input_array(i_a)
                device.write(moRF.setFreq)                                      # to be placed inside of the setFreq array at y(3) offset
            if msvcrt.kbhit():                                                  # example to be clear : i_a[0-7] a 8 byte array gets placed inside the
    	           if ord(msvcrt.getch()) == 27:                                # setFreq[0, 119, 129, i_a[0], i_a[1], i_a[2], i_a[3], i_a[4], i_a[5], i_a[6], i_a[7], 96, 0, 0, 2, 31, 0]
    	                  break
            for x in self.freqRangeReverse(start,end,step):
                input_array = self.int_to_bytes(x,8)
                for y in range(3,11):
                    moRF.setFreq[y] = input_array[y-3]
                device.write(moRF.setFreq)
            if msvcrt.kbhit():
    	           if ord(msvcrt.getch()) == 27:
    	                  break

    def morse(self,device):                                                     # Set moRFeus to mixer mode
        while True:
            morse = morseCode()
            morseInput = input('What would you like to send? ')
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

    def mixer(self,device):
        device.write(moRF.setMix)
        self.setCurrents(device)
        self.setFreqStatic(device)
        self.closeMoRFeus(device)
        time.sleep(0.5)

    def generator(self,device):                                                             # Set moRFeus to generator mode
        while True:
            try:
                print("Generator - Mode")
                gentype = int(input('Please select Generator type:\n1->CW\n2->Sweep\n'))    # Set moRFeus generator type: CW or Sweep
            except ValueError:
                print("Not a integer...")
            else:
                if gentype == 1:
                    device.write(moRF.setGen)
                    self.setCurrents(device)
                    self.setFreqStatic(device)
                    break
                else:
                    if gentype == 2:
                            try:
                                startFreq = float(input('Please enter the start frequency from 85 - 5400MHz: \n'))
                                startFreq = int(startFreq * moRF.mil)
                            except ValueError:
                                print("Not a float...")
                            else:
                                try:
                                    endFreq = float(input('Please enter the end frequency from 85 - 5400MHz: \n'))
                                    endFreq = int(endFreq * moRF.mil)
                                except ValueError:
                                    print("Not a float...")
                                else:
                                    if startFreq <= moRF.LOmax and startFreq >= moRF.LOmin and endFreq <= moRF.LOmax and endFreq >= moRF.LOmin:
                                        print("Frequency range set to ", (startFreq/moRF.mil),"-",(endFreq/moRF.mil),"MHz")
                                        device.write(moRF.setGen)
                                        self.setCurrents(device)
                                        step = float(input('Please enter the step in KHz: \n'))
                                        step = int(step * 1000)
                                        self.setfreqRange(device,startFreq,endFreq,step)
                                        break
                                    else:
                                        print("Values not between 85 - 5400MHz...")
                                        continue
                    else:
                        print("not a valid selection")
                        continue
        self.closeMoRFeus(device)
        time.sleep(0.5)

    def whitenoise(self,device):                                                # Set moRFeus to whitenoise mode, LO at 5400MHz
        print("WhiteNoise - Mode")                                              # creates uneven whitenoise from DC to 1700MHz(my airspy limit)
        device.write(moRF.setGen)
        self.setCurrents(device)
        device.write(moRF.whiteNoise)
        self.closeMoRFeus(device)
        time.sleep(0.5)

if __name__ == '__main__':
    cmd = moRFeusCmd()
    while True:
        # main program
        if cmd.moRFeusCheck() == 1:
            print("No Device found, will retry in 3 seconds")
            time.sleep(3)
        else:
            device = cmd.initMoRFeus()
            os.system("cls")
            try:
                mode=int(input('Please select Operation mode:\n1->Mixer\n2->Generator\n3->Random Noise Generator\n4->Morse Code\n'))
            except ValueError:
                continue
            else:
                if mode in (1,2,3,4):
                    if mode == 1:
                        cmd.mixer(device)
                    else:
                        if mode == 2:
                            cmd.generator(device)
                        else:
                            if mode == 3:
                                cmd.whitenoise(device)
                            else:
                                if mode == 4:
                                    cmd.morse(device)
                    continue
