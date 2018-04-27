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

moRF = moRFeus()
def initMoRFeus():                                                      # init routine for moRFeus
    print("Opening the device")
    device = hid.device()
    device.open(0x10c4, 0xeac9)                                             # moRFeus VendorID/ProductID
    print("MoRFeus opened")
    # enable non-blocking mode
    device.set_nonblocking(0)
    device.write(moRFeus.readRegister)
    while True:
        read_array = device.read(16)
        print(read_array)
        if read_array:
            for x in range(3,11):
                moRF.readRegister[x] = read_array[x-1]
                moRF.buffer_array[x-3] = moRF.readRegister[x]
            print('data: ', read_array)
            gen = int.from_bytes(moRF.buffer_array,byteorder='big', signed=False)
            print(hex(gen)[0:])
            # if gen == 0:
            #     print("Mixer")
            # else:
            #     print("Generator")
        # for x in range(3,11):
        #     moRF.setFreq[x] = d[x-3]
        #     startValue = int.from_bytes(d, byteorder='big', signed=False)
        #     print(startValue)
        # device.write(moRF.setFreq)
        time.sleep(1)
        return device

initMoRFeus()
