from wvg import wvg
import computesv
import unittest
import numpy as np

# Test the WVG class
class TestWVG(unittest.TestCase):
    def test_player_and_weights_difference(self):
        n = 10
        weights = np.zeros(5)
        with self.assertRaises(Exception):
            wvg(n,weights)
    

# Tests the create DP table function
class TestCreateDPTable(unittest.TestCase):
    
    # Tests correct output with weights array of all 0s
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



if __name__ == '__main__':
    unittest.main()