import hid
import unittest
from moRFeusQt import mRFsClass


class TestMRFs(unittest.TestCase):

    def mockdevice(self):
        td = hid.device()
        td.open(0x10c4, 0xeac9)
        td.set_nonblocking(1)
        return td

    def test_initmorf(self):
        cond = mRFsClass.MoRFeus.findmorfeus()
        if cond:
            td1 = mRFsClass.MoRFeus.initdevice()
            td2 = self.mockdevice()
            self.assertEqual(type(td1), type(td2))
            td1.close()
            td2.close()
            print("\ntest_initmorf : Passed")
        else:
            self.assertIsNotNone(cond, "\n\ntest_initmorf : Failed - No Device")


if __name__ == "__main__":
    unittest.main()
