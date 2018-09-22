import hid
import unittest
from moRFeusQt import mrf

class TestMRFs(unittest.TestCase):

    @classmethod
    def mockdevice(cls):
        td = hid.device()
        td.open(mrf.MoRFeus.vendorID, mrf.MoRFeus.productID)
        td.set_nonblocking(1)
        return td

    def test_findmorfeus(self):
        cond = mrf.MoRFeus.findmorfeus()
        if cond:
            self.assertTrue(mrf.MoRFeus.findmorfeus())
            print("\ntest_findmorfeus : Passed")
            pass
        else:
            self.assertIsNotNone(cond, "\n\ntest_findmorfeus : Failed - No Device")

    def test_initdevice(self):
        cond = mrf.MoRFeus.findmorfeus()
        if cond:
            td1 = mrf.MoRFeus.initdevice()
            td2 = self.mockdevice()
            self.assertEqual(type(td1), type(td2))
            td1.close()
            td2.close()
            print("\ntest_initdevice : Passed")
        else:
            self.assertIsNotNone(cond, "\n\ntest_initdevice : Failed - No Device")


if __name__ == "__main__":
    unittest.main()
