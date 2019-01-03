import hid
import time as t
from moRFeusQt import mrftcp
from moRFeusQt import mrfplot


class MoRFeus(object):
    # Information based of the protocol description by Abhishek on the othernet forum :
    # https://forums.othernet.is/t/rf-product-morfeus-frequency-converter-and-signal-generator/5025/59

    # Constants
    LOmax = 5400000000  # Local Oscillator max (5400MHz)
    LOmin = 85000000  # Local Oscillator min (85Mhz)
    mil = 1000000  # Saves some zero's here and there
    SET = 1
    GET = 0
    vendorID = 0x10c4
    productID = 0xeac9

    msgArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    getMsg = [0, 114]
    setMsg = [0, 119]
    # 8 byte value carrier
    read_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
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
    initFreq = 433.92

    def __init__(self, device):
        self.device = device

    @classmethod
    def find(cls) -> int:
        while True:
                try:
                    count = 0
                    for d in hid.enumerate(0, 0):
                        keys = list(d.keys())
                        for key in keys:
                            if d[key] == cls.productID:
                                count += 1
                    if count == 0:
                        raise OSError
                    else:
                        return count
                except OSError:
                    print('\nNo moRFeus found... Retrying in 5 seconds')
                    t.sleep(5)
                    continue

    # init routine for moRFeus
    @classmethod
    def initdevice(cls, vid=vendorID, pid=productID, index=0):
            mrfdevice = hid.enumerate(vid, pid)[index]
            device = hid.device()
            # moRFeus VendorID/ProductID
            device.open_path(mrfdevice['path'])
            device.set_nonblocking(0)
            return device

    def writemsgbytes(self, value, array):
        input_array = value.to_bytes(len(self.read_buffer), 'big')
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
                self.read_buffer[x - 3] = self.msgArray[x]
            init_values = int.from_bytes(self.read_buffer, byteorder='big', signed=False)
            if read_array[1] == self.funcFrequency:
                print('Freq :', str.format('{0:.6f}', init_values / self.mil))
                self.initFreq = init_values / self.mil
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

    # loop for moving upward in frequency (increases with step)
    def freqRange(self, start, end, step):
        while start <= end:
            yield start
            start += step

    # Frequency sweep routine, still needs a means to break out of
    # loop on some event..
    def sweepfreq(self, start, end, step, delay):
        start_freq = start
        start_freq = int(start_freq * self.mil)
        end_freq = end
        end_freq = int(end_freq * self.mil)
        step = step
        step = int(step * 1000)
        stepcount = int((end_freq - start_freq) / step)
        delay = delay
        self.message(self.SET, self.funcMixGen, 1)
        # self.curQt()
        y = 0
        sock = mrftcp.GqRX('127.0.0.1')
        powah = []
        freq = []
        self.printProgressBar(0, stepcount, prefix='Sweep :', suffix='', length=43)
        while True:
            if stepcount == 0:
                print("NULL Range  :")
                break
            else:
                if sock.IsConnected():
                    starttime = t.time()
                    for x in self.freqRange(start_freq, end_freq, step):
                        self.message(self.SET, self.funcFrequency, (x / self.mil))
                        sock.SetFreq("{0:8.6f}".format(x))
                        self.printProgressBar(y, stepcount, prefix='Sweep Prog    : ', suffix='', length=43)
                        t.sleep(delay / 1000)
                        y += 1
                        power = sock.GetStrength()
                        freq.append(x / self.mil)
                        # powah.append((float(power[:-2]) + 26))
                        powah.append(float(power[:-2]))
                        # mrfplot.MorfeusPlot.liveplot(x/self.moRFeus.mil, float(power[:-2]))
                        # print(x, float(power[:-2]))
                        # print(freq, powah)
                    self.message(self.SET, self.funcFrequency, start)
                    endtime = t.time()
                    sock.SetFreq("{0:8.6f}".format(start_freq))
                    sock.Close()
                    dwelltime = (delay, 'ms dwell', (endtime - starttime), 'sec',
                                 (step / 1000), 'MHz')
                    mrfplot.MorfeusPlot.drawgraph(freq, powah, dwelltime)
                    break
                else:
                    starttime = t.time()
                    for x in self.freqRange(start_freq, end_freq, step):
                        self.message(self.SET, self.funcFrequency, (x / self.mil))
                        self.printProgressBar(y, stepcount, prefix='Sweep Prog    : ', suffix='', length=43)
                        t.sleep(delay / 1000)
                        y += 1
                    self.message(self.SET, self.funcFrequency, start)
                    endtime = t.time()
                    print(endtime - starttime)
                    break

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
        if iteration >= 1:
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
            # Print New Line on Complete
            if iteration == total:
                print()


