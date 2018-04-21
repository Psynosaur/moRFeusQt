from __future__ import print_function
import time
from moRFeusClass import moRFeus

# morse code source : https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/resources/morse_code.py
class morseCode(object):
    MORSE = {' ': ' ',     "'": '.----.','(': '-.--.-',')': '-.--.-',',': '--..--','-': '-....-','.': '.-.-.-','/': '-..-.',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.', ':': '---...',';': '-.-.-.','?': '..--..',              'A': '.-',    'B': '-...',
            'C': '-.-.',  'D': '-..',   'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
            'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',  'Q': '--.-',  'R': '.-.',
            'S': '...',   'T': '-',     'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',  'Z': '--..',
            '_': '..--.-','+': '.-.-.', '=': '-...-', '_': '..--.-','@': '.--.-.'}

    def switch(self,device,state):
        for x in range(3,11):
            moRFeus.setCur[x] = state
        device.write(moRFeus.setCur)

    def dot(self,device):
    	self.switch(device,1)
    	time.sleep(0.2)
    	self.switch(device,0)
    	time.sleep(0.2)

    def dash(self,device):
    	self.switch(device,1)
    	time.sleep(0.5)
    	self.switch(device,0)
    	time.sleep(0.2)
