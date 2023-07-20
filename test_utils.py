"""
Unittests for file utils.py.

"""

import unittest
import utils
import numpy as np

class TestUtils(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        print('\n***utils.py tests:***\n') 
        
    @classmethod
    def tearDownClass(self):
        print('\n***utils.py tests have finished***\n') 
        
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
        
    def test_get_lognorm_param(self):
        print('test_get_lognorm_param')
        self.assertEqual(utils.get_lognorm_param(1,0.1), (0.0997513451195927, 0.9950371902099893))
        self.assertEqual(utils.get_lognorm_param(-1,-1), (0.8325546111576977, 0.7071067811865475))
        
    def test_pf(self):
        print('test_pf')
        
        self.assertEqual(utils.pf([1, -1, 1, -1]), 0.5)
        self.assertEqual(utils.pf([1, 1, 1, 1]), 0)
        self.assertEqual(utils.pf([-1, -1, -1, -1]), 1)
        
        # Should I do such test for every function?
        self.assertRaises(TypeError, utils.pf, 'str')                          # string
        self.assertRaises(TypeError, utils.pf, 1)                              # int
        self.assertRaises(TypeError, utils.pf, .1)                             # float
        self.assertRaises(TypeError, utils.pf, ['str', 0])                     # list
        self.assertRaises(TypeError, utils.pf, True)                           # boolean
        self.assertRaises(TypeError, utils.pf, (1, 'r', 3))                    # tuple
        self.assertRaises(TypeError, utils.pf, {'name': 'John'})               # dict 
        self.assertRaises(TypeError, utils.pf, {1, 2})                         # set
        
    def test_get_reliability_index(self):
        print('test_get_reliability_index')
        
        self.assertEqual(utils.get_reliability_index(0.5), 0)
        self.assertEqual(utils.get_reliability_index(0.2), 0.8416212335729143)
        
        self.assertRaises(ValueError, utils.get_reliability_index, 2)   
        self.assertRaises(ValueError, utils.get_reliability_index, -1)  
        
        self.assertEqual(utils.get_reliability_index(0), np.inf)
        self.assertEqual(utils.get_reliability_index(1), -np.inf)
        
    def test_get_probability_of_failure(self):
        print('test_get_probability_of_failure')
        self.assertEqual(utils.get_probability_of_failure(0), 0.5)
        self.assertEqual(utils.get_probability_of_failure(3), 0.0013498980316301035)
        self.assertEqual(utils.get_probability_of_failure(-10), 1)
        
    def test_get_cdf(self):
        print('test_get_cdf (pass)')
        pass


if __name__ == "__main__":
    unittest.main()
