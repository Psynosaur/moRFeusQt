# There is now a need to get information from the device,
# We use the getFrequency msg to get the current frequency
# from the device, so that we can with that value set out
# initial Qt applet start frequency accordingly
import time
import hid

# init routine for moRFeus
def initMoRFeus():
    while True:
        try:
            device = hid.device()
            # moRFeus VendorID/ProductID
            device.open(0x10c4, 0xeac9)
            device.set_nonblocking(0)
            return device
        except IOError:
            print('No moRFeus found... Retrying in 3 seconds')
            time.sleep(3)
            continue


# morse code source : https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/resources/morse_code.py
class morseCode(object):
    def __init__(self, device):
        self.device = device

    MORSE = {' ': ' ',     "'": '.----.','(': '-.--.-',')': '-.--.-',',': '--..--','-': '-....-','.': '.-.-.-','/': '-..-.',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.', ':': '---...',';': '-.-.-.','?': '..--..',              'A': '.-',    'B': '-...',
            'C': '-.-.',  'D': '-..',   'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
            'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',  'Q': '--.-',  'R': '.-.',
            'S': '...',   'T': '-',     'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',  'Z': '--..',
            '_': '..--.-','+': '.-.-.', '=': '-...-', '@': '.--.-.'}

    def switch(self,state):
        moRFeusObject = moRFeus(self.device)
        moRFeusObject.message(1, moRFeusObject.funcCurrent, state)

    def dot(self):
    	self.switch(1)
    	time.sleep(0.2)
    	self.switch(0)
    	time.sleep(0.2)

    def dash(self):
    	self.switch(1)
    	time.sleep(0.5)
    	self.switch(0)
    	time.sleep(0.2)

class moRFeus(object):
    def __init__(self, device):
        self.device = device

    # Constants
    LOmax        = 5400000000                                                       # Local Oscillator max (5400MHz)
    LOmin        = 85000000                                                         # Local Oscillator min (85Mhz)
    mil          = 1000000                                                          # Saves some zero's here and there
    msgArray     = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    getMsg       = [0,114]
    setMsg       = [0,119]
    # 8 byte value carrier
    read_buffer  = [0, 0, 0, 0, 0, 0, 0, 0]
    buffer_array = bytearray(read_buffer)
    sixZero      = [0, 0, 0, 0, 0, 0]
    # Function Constants
    funcFrequency    = 129
    funcMixGen       = 130
    funcCurrent      = 131 # 0 - 7
    funcBiasTee      = 132 # 1 On : 0 Off
    funcLCD          = 133 # 0 : Always on, 1 : 10s, 2 : 60s
    funcfirmwareMode = 134
    funcRegister     = 0
    # Byte Arrays known to the moRFeus device
    # Setting functions [0, 119, . . .]

    # setGen       = [0, 119, 130, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]          # Generator mode
    # setMix       = [0, 119, 130, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]          # Mixer mode
    # biasOn       = [0, 119, 132, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]          # BiasTee on
    # biasOff      = [0, 119, 132, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]          # BiasTee off
    # firmwareMode = [0, 119, 134, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # setLCD       = [0, 119, 133, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]          # with our custom 8byte current array
    # whiteNoise   = [0, 119, 129, 0, 0, 0, 1, 65, 221, 118, 0, 96, 0, 0, 2, 31, 0]     # setFrequency to 5400 000 000 Hz
    # setFrequency = [0, 119, 129, 0, 0, 0, 1, 65, 221, 118, 0, 96, 0, 0, 2, 31, 0]   # setFrequency bytearray template

    # getCurrent   = [0, 114, 131, 0, 0, 0, 0, 0, 0, 0, 1, 0, 96, 0, 0, 2, 0]
    # getFunction  = [0, 114, 130, 0, 0, 0, 0, 0, 0, 0, 1, 0, 96, 0, 0, 2, 0]
    # getBiasTee   = [0, 114, 132, 0, 0, 0, 0, 0, 0, 0, 0, 0, 96, 0, 0, 2, 0]
    # # register
    # msgRegister  = [0, 114, 0, 0, 0, 0, 0, 0, 0, 190, 251, 0, 0, 96, 0, 0, 0]
    #
    # getLCD       = [0, 114, 133, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

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

    def message(self, mode, func, value):
        output = []
        # this sets the mode, 0: get and 1: set
        while True:
            for x in range(0,2):
                if mode == 1:
                    self.msgArray[x] = self.setMsg[x]
                    output.append(self.msgArray[x])
                else:
                    self.msgArray[x] = self.getMsg[x]
                    output.append(self.msgArray[x])
            # print(output)
            # we have an variable array with our mode set...
            # now we should set the function... it always at the same position
            output.append(func)
            # print(output)

            # set the value_array
            if func == 129 and mode == 1:
                freq = int(value * self.mil)
                input_array = self.int_to_bytes(freq,8)
                for x in range(3,11):
                    self.msgArray[x] = input_array[x-3]
                    output.append(self.msgArray[x])
                # print(output)
                for x in range(0,6):
                    output.append(self.sixZero[x])
                # print(output)
                self.device.write(output)
                break
            else:
                input_array = self.int_to_bytes(value,8)
                for x in range(3,11):
                    self.msgArray[x] = input_array[x-3]
                    output.append(self.msgArray[x])
                # print(output)
                for x in range(0,6):
                    output.append(self.sixZero[x])
                # print(output)
                self.device.write(output)
                break

    # read function byte and return values accordingly
    def readDevice(self):
        read_array = self.device.read(16)
        if read_array:
            for x in range(3,11):
                self.msgArray[x] = read_array[x-1]
                # reads byte array and places it in 8 byte array to
                self.buffer_array[x-3] = self.msgArray[x]
            # convert to an int to init the Qt widget's ---
            init_values = int.from_bytes(self.buffer_array,byteorder='big', signed=False)
            if read_array[1] == self.funcFrequency:
                print('Freq:', init_values/self.mil)
                return (init_values/self.mil)
            if read_array[1] == self.funcCurrent:
                print('Current:', init_values)
                return init_values
            if read_array[1] == self.funcMixGen:
                if init_values == 0:
                    print("Function: Mixer")
                else:
                    print("Function: Generator")
            if read_array[1] == self.funcLCD:
                if init_values == 0:
                    print("LCD : Always On")
                if init_values == 1:
                    print("LCD : 10s")
                else:
                    print("LCD : 60s")
