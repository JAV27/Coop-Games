from wvg import wvg
import computesv
import unittest
import numpy as np

# Test the WVG class
class TestWVG(unittest.TestCase):

    # Test if no quota is given that it is set to 0
    def test_no_quota_given(self):
        test_wvg = wvg(5, [0,0,0,0,0])
        self.assertEqual(test_wvg.get_quota(), 0)

    # Test if not giving a weights array promts a zero array
    def test_no_weights_array_given(self):
        test_wvg = wvg(5, None, 0)
        equality = np.array_equal(np.zeros((5)), test_wvg.get_weights())
        self.assertTrue(equality)

    # Test if having len(weights) and num_players as different throws an error
    def test_player_and_weights_difference(self):
        n = 10
        weights = np.zeros(5)
        with self.assertRaises(Exception):
            wvg(n,weights,0)

    # Test if set_weights correctly sets
    def test_set_weights(self):
        test_wvg = wvg(5)
        test_wvg.set_weights([1,2,3,4,5])
        equality = np.array_equal([1,2,3,4,5], test_wvg.get_weights())
        self.assertTrue(equality)

    # Test if updating weights array with wrong len throws errror
    def test_set_weights_error(self):
        test_wvg = wvg(5)
        with self.assertRaises(Exception):
            test_wvg.set_weights([1,2,3,4,5,6])

        equality = np.array_equal(np.zeros((5)), test_wvg.get_weights())        
        self.assertTrue(equality)
    

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