# import usb.core
# import usb.util
#
# VENDOR_ID = 0x10c4
# PRODUCT_ID = 0xeac9
#
#
# # find our device
# dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
# # was it found?
# if dev is None:
#     raise ValueError('Device not found')
#
# # set the active configuration. With no arguments, the first
# # configuration will be the active one
# dev.set_configuration()
#
# # get an endpoint instance
# cfg = dev.get_active_configuration()
# intf = cfg[(0,0)]
#
# ep = usb.util.find_descriptor(
#     intf,
#     # match the first OUT endpoint
#     custom_match = \
#     lambda e: \
#         usb.util.endpoint_direction(e.bEndpointAddress) == \
#         usb.util.ENDPOINT_OUT)
#
# assert ep is not None
#
# # write the data
# ep.write('test')


import hid
import sys
import time

sys.path.append('./../')
from moRFeus_class import moRFeus

moRFeusObject = moRFeus()
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
        
# def initMoRFeus(mode,func,value):                                                      # init routine for moRFeus
#     print("Opening the device")
#     device = hid.device()
#     device.open(0x10c4, 0xeac9)                                             # moRFeus VendorID/ProductID
#     print("MoRFeus opened")
#     # enable non-blocking mode
#     device.set_nonblocking(0)
#
#     output = []
#     # this sets the mode, 0: get and 1: set
#     while True:
#         for x in range(0,2):
#             if mode == 1:
#                 moRFeusObject.msgArray[x] = moRFeusObject.setMsg[x]
#                 output.append(moRFeusObject.msgArray[x])
#             else:
#                 moRFeusObject.msgArray[x] = moRFeusObject.getMsg[x]
#                 output.append(moRFeusObject.msgArray[x])
#         print(output)
#         # we have an variable array with out mode...
#         # now we should set the function... it always at the same position
#         output.append(func)
#         print(output)
#
#         # set the value_array (cur,freq)
#         if func == 129 and mode == 1:
#             freq = int(value * moRFeusObject.mil)
#             input_array = moRFeusObject.int_to_bytes(freq,8)
#             for x in range(3,11):
#                 moRFeusObject.msgArray[x] = input_array[x-3]
#                 output.append(moRFeusObject.msgArray[x])
#             print(output)
#             for x in range(0,6):
#                 output.append(moRFeusObject.sixZero[x])
#             print(output)
#             device.write(output)
#         else:
#             input_array = moRFeusObject.int_to_bytes(value,8)
#             for x in range(3,11):
#                 moRFeusObject.msgArray[x] = input_array[x-3]
#                 output.append(moRFeusObject.msgArray[x])
#             print(output)
#             for x in range(0,6):
#                 output.append(moRFeusObject.sixZero[x])
#             print(output)
#             device.write(output)
#             break
#     # device.write(moRFeusCMD.getLCD)
    # while True:
    #     read_array = device.read(16)
    #     print(read_array)
    #     if read_array:
    #         for x in range(3,11):
    #             moRFeusCMD.getLCD[x] = read_array[x-1]
    #             moRFeusCMD.buffer_array[x-3] = moRFeusCMD.getLCD[x]
    #         print('data: ', read_array)
    #         gen = int.from_bytes(moRFeusCMD.buffer_array,byteorder='big', signed=False)
    #         print(hex(gen)[0:])
            # if gen == 0:
            #     print("Mixer")
            # else:
            #     print("Generator")
        # for x in range(3,11):
        #     moRF.setFreq[x] = d[x-3]
        #     startValue = int.from_bytes(d, byteorder='big', signed=False)
        #     print(startValue)
        # device.write(moRF.setFreq)
        # time.sleep(1)
        # return device

initMoRFeus()
