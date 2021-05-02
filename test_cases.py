from wvg import wvg
import compute_sv
import unittest
import numpy as np
from ttg import ttg

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
        result = compute_sv.create_DP_table(test_wvg.weights)
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

# Tests the compute_sv snd brute_force_sv functions 
class TestComputeSV(unittest.TestCase):
    def test_total(self):
        test_wvg = wvg([1,2,3,4,5], 8)
        totalBrute = 0
        totalDP = 0
        for i in range(test_wvg.get_num_players()):
            totalBrute += compute_sv.brute_force_sv(test_wvg.v, i, test_wvg.get_num_players())
            totalDP += compute_sv.compute_shapley_value(test_wvg, i)

        self.assertEqual(round(totalDP, 3), 1)
        self.assertEqual(round(totalBrute, 3), 1)

    def test_case_SVs(self):
        test_wvg = wvg([1,2,3,4,5], 10)
        for i in range(5):
            brute = compute_sv.brute_force_sv(test_wvg.v, i, test_wvg.get_num_players())
            dp = compute_sv.compute_shapley_value(test_wvg, i)
            self.assertAlmostEqual(brute, dp, 3)

    def test_bad_inputs(self):
        test_wvg = wvg([1,2,3,4,5], 10)
        with self.assertRaises(IndexError):
            compute_sv.brute_force_sv(test_wvg.v, 5, test_wvg.get_num_players()+1)

        with self.assertRaises(IndexError):
            compute_sv.brute_force_sv(test_wvg.v, 6, test_wvg.get_num_players())

    def test_wvg_vs_ttg(self):
        # Make sure ttg with 1 task of value 1 is same as wvg
        test_ttg = ttg([1,2,3,4,5], [(10,1)])
        test_wvg = wvg([1,2,3,4,5], 10)
        sv = compute_sv.compute_shapley_value_ttg(test_ttg, 2)
        sv2 = compute_sv.compute_shapley_value(test_wvg, 2)

        self.assertEqual(sv, sv2)

        # Test if value is 2 it will double shapley value
        test_ttg = ttg([1,2,3,4,5], [(10,2)])
        sv = compute_sv.compute_shapley_value_ttg(test_ttg, 2)
        self.assertEqual(sv, 2*sv2)

        # Test if it will always take the better task
        test_ttg = ttg([1,2,3,4,5], [(10,1), (10,2)])
        sv = compute_sv.compute_shapley_value_ttg(test_ttg, 2)
        self.assertEqual(sv, 2*sv2)

        # ToDo: Test complicated TTG example

    def test_brute_force_ttg(self):
        test_ttg = ttg([1,2,3,4,5], [(10,1)])
        sv = compute_sv.brute_force_sv(test_ttg.v, 3, 5)
        
        self.assertEqual(sv, .25)

if __name__ == '__main__':
    unittest.main()