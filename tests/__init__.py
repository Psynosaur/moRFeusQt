import unittest
import tests.test_mrf


def mRF_test_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_mrf)
    return suite
