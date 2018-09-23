import hid
import unittest
from moRFeusQt import mrf


class TestMRFs(unittest.TestCase):

    @classmethod
    def mockdevice(cls):
        # hard code the opening of the morfeus device and return
        td = hid.device()
        td.open(mrf.MoRFeus.vendorID, mrf.MoRFeus.productID)
        td.set_nonblocking(1)
        return td

    def test_find(self):
        # If the device isn't found, test do not continue
        cond = mrf.MoRFeus.find()
        self.assertTrue(cond)

    def test_initdevice(self):
        # init two test devices, one from morfeus class and another from mockdevice
        td1 = mrf.MoRFeus.initdevice()
        td2 = self.mockdevice()
        # Check types
        self.assertEqual(type(td1), type(td2))
        # Check if 'td1' is and instance of type 'td2'(hard opened hid.device)
        self.assertIsInstance(td1, type(td2))
        # Close the devices
        td1.close()
        td2.close()


if __name__ == "__main__":
    unittest.main()
