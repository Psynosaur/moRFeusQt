import hid
from time import sleep


# init routine for moRFeus
def initmorf():
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
class MorseCode(object):
    def __init__(self, device):
        self.device = device

    # added some additional morse code characters '@','!' and '&'
    MORSE = {' ': ' ', "'": '.----.', '(': '-.--.-', ')': '-.--.-', ',': '--..--', '-': '-....-', '.': '.-.-.-',
             '/': '-..-.', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
             '6': '-....', '7': '--...', '8': '---..', '9': '----.', ':': '---...', ';': '-.-.-.', '?': '..--..',
             'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
             'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
             'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
             'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '_': '..--.-', '+': '.-.-.',
             '=': '-...-', '@': '.--.-.', '!': '-.-.--', '&': '.-...'}

    def switch(self, state):
        moRFeus = MoRFeus(self.device)
        moRFeus.message(moRFeus.SET, moRFeus.funcCurrent, state)

    def dot(self):
        self.switch(1)
        sleep(0.2)
        self.switch(0)
        sleep(0.2)

    def dash(self):
        self.switch(1)
        sleep(0.5)
        self.switch(0)
        sleep(0.2)


class MoRFeus(object):
    def __init__(self, device):
        self.device = device

    # Information based of the protocol description by Abhishek on the othernet forum :
    # https://forums.othernet.is/t/rf-product-morfeus-frequency-converter-and-signal-generator/5025/59

    # Constants
    LOmax = 5400000000  # Local Oscillator max (5400MHz)
    LOmin = 85000000  # Local Oscillator min (85Mhz)
    mil = 1000000  # Saves some zero's here and there
    SET = 1
    GET = 0

    msgArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    getMsg = [0, 114]
    setMsg = [0, 119]
    # 8 byte value carrier
    read_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
    buffer_array = bytearray(read_buffer)
    # 6 byte trailers
    sixZero = [0, 0, 0, 0, 0, 0]
    # Function Constants
    funcFrequency = 129
    funcMixGen = 130
    funcCurrent = 131  # 0 - 7
    funcBiasTee = 132  # 1 On : 0 Off
    funcLCD = 133  # 0 : Always on, 1 : 10s, 2 : 60s
    funcFW = 134
    funcRegister = 0

    # Housekeeping for remembering GUI vars when pressing the noise button
    initFreq = 0

    # Convert integer(input) value to an length(8) byte sized array
    # to be used for inserting our custom array starting at
    # setFreq[3] to setFreq[10]
    @classmethod
    def int_to_bytes(cls, value, length):
        result = []
        for i in range(0, length):
            result.append(int(value) >> (i * 8) & 0xff)
        result.reverse()
        # return the result
        return result

    def writemsgbytes(self, value, array):
        input_array = self.int_to_bytes(value, 8)
        for x in range(3, 11):
            self.msgArray[x] = input_array[x - 3]
            array.append(self.msgArray[x])
        for x in range(0, 6):
            array.append(self.sixZero[x])
        self.device.write(array)

    def message(self, mode, func, value):
        outputarray = []
        # this sets the mode, 0: get and 1: set
        while True:
            for x in range(0, 2):
                if mode == self.SET:
                    self.msgArray[x] = self.setMsg[x]
                    outputarray.append(self.msgArray[x])
                else:
                    self.msgArray[x] = self.getMsg[x]
                    outputarray.append(self.msgArray[x])
            # we have an variable array with our mode set...
            # now we should set the function... its always at the same position
            outputarray.append(func)
            # set the value_array
            if func == self.funcFrequency and mode == self.SET:
                freq = int(value * self.mil)
                self.writemsgbytes(freq, outputarray)
                break
            else:
                self.writemsgbytes(value, outputarray)
                break

    # read function byte and return values accordingly
    def readDevice(self):
        read_array = self.device.read(16)
        if read_array:
            for x in range(3, 11):
                self.msgArray[x] = read_array[x - 1]
                # reads byte array and places it in 8 byte array to
                self.buffer_array[x - 3] = self.msgArray[x]
            init_values = int.from_bytes(self.buffer_array, byteorder='big', signed=False)
            if read_array[1] == self.funcFrequency:
                print('Freq :', str.format('{0:.6f}', init_values / self.mil))
                return init_values / self.mil
            if read_array[1] == self.funcCurrent:
                print('Curr :', init_values)
                return init_values
            if read_array[1] == self.funcMixGen:
                if init_values == 0:
                    print("Func : Mixer")
                else:
                    print("Func : Generator")
            if read_array[1] == self.funcLCD:
                if init_values == 0:
                    print("LCD  : Always On")
                if init_values == 1:
                    print("LCD  : 10s")
                else:
                    print("LCD  : 60s")
            if read_array[1] == self.funcBiasTee:
                if init_values == 0:
                    print("Bias : Off")
                if init_values == 1:
                    print("Bias : On")

    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='|'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
        # Print New Line on Complete
        if iteration == total:
            print()


