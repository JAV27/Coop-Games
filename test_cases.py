from wvg import wvg
import computesv
import unittest
import numpy as np

# Test the WVG class
class TestWVG(unittest.TestCase):

    # Test if no quota is given that it is set to 0
    def test_no_quota_given(self):
        test_wvg = wvg([0,0,0,0,0])
        self.assertEqual(test_wvg.get_quota(), 1)

    # Test if not giving a weights array promts a zero array
    def test_no_weights_array_given(self):
        test_wvg = wvg(None, 10)
        equality = np.array_equal(np.zeros((1)), test_wvg.get_weights())
        self.assertTrue(equality)

    # Test if set_weights correctly sets
    def test_set_weights(self):
        test_wvg = wvg([0,0,0,0,0])
        test_wvg.set_weights([1,2,3,4,5])
        equality = np.array_equal([1,2,3,4,5], test_wvg.get_weights())
        self.assertTrue(equality)

    # Test if updating weights array with wrong len throws errror
    def test_set_weights_error(self):
        test_wvg = wvg([1,2,3,4,5])
        with self.assertRaises(Exception):
            test_wvg.set_weights([1,2,3,4,5,6])

        equality = np.array_equal([1,2,3,4,5], test_wvg.get_weights())        
        self.assertTrue(equality)
    
    def test_nothing_given(self):
        test_wvg = wvg()
        equality = np.array_equal([0], test_wvg.get_weights())  
        self.assertTrue(equality)
        self.assertEqual(1, test_wvg.get_quota())
    

# Tests the create DP table function
class TestCreateDPTable(unittest.TestCase):
    
    # Tests correct output with weights array of all 0s
    def test_all_zeroes(self):
        test_wvg = wvg([0,0,0,0,0])
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

class TestComputeSV(unittest.TestCase):
    def test_total_CSV(self):
        test_wvg = wvg([1,2,3,4,5,6,7,8,9,10], 15)
        total = 0
        for i in range(test_wvg.get_num_players()):
            total += computesv.compute_shapley_value(test_wvg, i)

        self.assertEqual(round(total, 3), 1)

    def test_total_brute_force(self):
        test_wvg = wvg([1,2,3,4,5], 8)
        total = 0
        for i in range(test_wvg.get_num_players()):
            total += computesv.brute_force_sv(test_wvg, i)

        self.assertEqual(round(total, 3), 1)

if __name__ == '__main__':
    unittest.main()