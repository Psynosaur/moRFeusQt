import hid
import unittest
import os, sys
from moRFeusQt import mrf
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestMRFs(unittest.TestCase):

    @classmethod
    def mockdevice(cls, vid=mrf.MoRFeus.vendorID, pid=mrf.MoRFeus.productID, index=0):
        # hard code the opening of the morfeus device and return
        mrfdevice = hid.enumerate(vid, pid)[index]
        td = hid.device()
        td.open_path(mrfdevice['path'])
        td.set_nonblocking(0)
        return td

    def test_find(self):
        # If the device isn't found, test do not continue
        cond = mrf.MoRFeus.find()
        self.assertTrue(cond)

    def test_initdevice(self):
        # init two test devices, one from morfeus class and another from mockdevice
        devicecount = mrf.MoRFeus.find()
        devices = []
        testdevices = []
        for i in range(0, devicecount):
            devices.append(mrf.MoRFeus.initdevice(i))
            # testdevices.append(self.mockdevice(i))
            # Check types
            self.assertEqual(type(devices), type(testdevices))
            # Check if 'td1' is and instance of type 'td2'(hard opened hid.device)
            # self.assertIsInstance(td1, type(td2))
            # Close the devices
            # td1.close()
            # td2.close()


if __name__ == "__main__":
    unittest.main()
