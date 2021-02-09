from wvg import wvg
import computesv
import unittest
import numpy as np

class TestCreateDPTable(unittest.TestCase):
    def test_all_zeroes(self):
        test_wvg = wvg(5)
        result = computesv.create_DP_table(test_wvg.weights)
        correct_table = np.array(
            [
             [[1,1,0,0,0]],
             [[1,2,1,0,0]],
             [[1,3,3,1,0]],
             [[1,4,6,4,1]]
            ]
        )
        equality = np.array_equal(result, correct_table)
        self.assertTrue(equality)
