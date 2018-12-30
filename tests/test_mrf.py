import hid
import unittest
import os, sys
from moRFeusQt import mrf
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestMRFs(unittest.TestCase):

    @classmethod
    def mockdevice(cls):
        # hard code the opening of the morfeus device and return
        td = hid.device()
        td.open(mrf.MoRFeus.vendorID, mrf.MoRFeus.productID)
        td.set_nonblocking(0)
        return td

    def test_find(self):
        # If the device isn't found, tests do not continue
        cond = mrf.MoRFeus.find()
        print(cond, "Devices found")
        self.assertTrue((cond >= 1))

    def test_initdevice(self):
        # init test devices from morfeus class, as many as are connected
        devicecount = mrf.MoRFeus.find()
        devices = []
        testdevices = []
        for i in range(0, devicecount):
            devices.append(mrf.MoRFeus.initdevice(index=i))
            testdevices.append(devices[i])
            # testdevices.append(self.mockdevice())
            # Check types
            self.assertEqual(type(devices[i]), type(testdevices[i]))
            # Check if 'devices[i]' is and instance of type 'testdevice[i]'
            self.assertIsInstance(devices[i], type(testdevices[i]))
            # Close the devices
            devices[i].close()
            testdevices[i].close()

    # def test_tcp(self):
        # g = GqRX('127.0.0.1')
        # print(g.IsConnected())
        # print(g.GetFreq())
        # print(g.GetStrength())
        # print(g.GetMod())
        # print(g.GetSQL())
        # print(g.GetAudioRec())
        # print(g.SetFreq('85000000'))
        # print(g.SetMod('FM', '10000'))
        # print(g.SetSQL('-140.0'))
        # print(g.Close())


if __name__ == "__main__":
    unittest.main()
