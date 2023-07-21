"""
Unittests for file Variables.py.

"""

import unittest
import Variables
import numpy as np
import scipy.stats as stats

class TestVariables(unittest.TestCase):
#class TestUtils(unittest.TestCase):
        
    @classmethod
    def setUpClass(self):
        print('\n***Variables.py tests:***\n') 
        
    @classmethod
    def tearDownClass(self):
        print('\n***Variables.py tests have finished***\n') 
        
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_Deterministic(self):
        print('test_Deterministic')
        for val in [2, 0.1, -5, -0.2]:
            v = Variables.Deterministic('v', val)
            self.assertEqual(v.get_bounds(.1), (val, val))
            
        self.assertRaises(ValueError, v.get_bounds, -1)
        self.assertRaises(ValueError, v.get_bounds, 2)
        self.assertEqual(v.isinstanceof(Variables.Deterministic), True)
        
    def test_Interval(self):
        print('test_Interval')
        for val1, val2 in zip([1, 0.1, -5, -0.2, 4], [2, 0.3, -4, -0.1, 4]):
            v = Variables.Interval('v', val1, val2)
            self.assertEqual(v.get_bounds(.1), (min(val1, val2), 
                                                max(val1, val2)))
        v = Variables.Interval('v', 2, 1)                                      # invert order
        self.assertEqual(v.get_bounds(.2), (1, 2))
        
        self.assertRaises(ValueError, v.get_bounds, -1)
        self.assertRaises(ValueError, v.get_bounds, 2)
        self.assertEqual(v.isinstanceof(Variables.Interval), True)
        
    def test_Cdf(self):
        print('test_Cdf')
        v = Variables.Cdf('v', stats.norm(loc=0, scale=.1))
        self.assertEqual(v.get_bounds(.5), (0, 0))
        
        v = Variables.Cdf('v', stats.norm(loc=1, scale=.1))
        self.assertEqual(v.get_bounds(.5), (1, 1))
        
        v = Variables.Cdf('v', stats.norm(loc=36, scale=.5))
        self.assertEqual(v.get_bounds(.9), (36.6407757827723,
                                            36.6407757827723))
        
        v = Variables.Cdf('v', stats.norm(loc=-4, scale=.3))
        self.assertEqual(v.get_bounds(.4), (-4.07600413094074,
                                            -4.07600413094074))
        
        v = Variables.Cdf('v', stats.norm(loc=1, scale=.1))
        self.assertEqual(v.get_bounds(0), (-np.inf, -np.inf))
        self.assertEqual(v.get_bounds(1), (np.inf, np.inf))
        self.assertRaises(ValueError, v.get_bounds, -1)
        self.assertRaises(ValueError, v.get_bounds, 2)
        self.assertEqual(v.isinstanceof(Variables.Cdf), True)
        
        # should I ensure positive scale for cdf?
        
        self.assertEqual(v.isinstanceof(Variables.Cdf), True)
        
    def test_Pbox(self):
        print('test_Pbox')
        v = Variables.Pbox('v', [stats.norm(loc=0, scale=.1),
                                 stats.norm(loc=1, scale=.1)])
        self.assertEqual(v.get_bounds(.5), (0, 1))
        
        v = Variables.Pbox('v', [stats.norm(loc=1, scale=.1),                  # invert order
                                 stats.norm(loc=0, scale=.1)])
        self.assertEqual(v.get_bounds(.5), (0, 1))
        
        v = Variables.Pbox('v', [stats.norm(loc=0, scale=.1),
                      stats.norm(loc=1, scale=.1),
                      stats.norm(loc=-1, scale=.1)])
        self.assertEqual(v.get_bounds(.5), (-1, 1))
        
        v = Variables.Pbox('v', [stats.norm(loc= 0, scale=.1),
                                 stats.norm(loc=-1, scale=.1)])
        self.assertEqual(v.get_bounds(.5), (-1, 0))
        self.assertEqual(v.get_bounds(1), (np.inf, np.inf))
        self.assertEqual(v.get_bounds(0), (-np.inf, -np.inf))
        
        # should I ensure positive scale for cdf?
        
        self.assertRaises(ValueError, v.get_bounds, -1)
        self.assertRaises(ValueError, v.get_bounds, 2)
        self.assertEqual(v.isinstanceof(Variables.Pbox), True)
        
        
    def test_Hist(self):
        print('test_Hist')
        v = Variables.Hist('v', [0,1,2,3,4,5])
        self.assertEqual(v.get_bounds(.5), (2., 2.))
        self.assertEqual(v.get_bounds(0), (0, 0))
        self.assertEqual(v.get_bounds(1), (5, 5))
        
        v = Variables.Hist('v', [1,2,3,4,5])
        self.assertEqual(v.get_bounds(.5), (2.5, 2.5))
        
        # Is it ok to do like this?
        hist = list(stats.norm(1,0.1).rvs(100))
        v = Variables.Hist('v', hist)
        self.assertAlmostEqual(round(v.get_bounds(.5)[0],1), 1)
        self.assertEqual(v.get_bounds(0), (min(hist), min(hist)))
        self.assertEqual(v.get_bounds(1), (max(hist), max(hist)))

    def test_initiate_variable(self):
        print('test_initiate_variable')
        test_var = Variables.initiate_variable('d', 'd', 1)
        self.assertEqual(test_var.isinstanceof(Variables.Deterministic), True)
        
        test_var = Variables.initiate_variable('i', 'i', 1, 2)
        self.assertEqual(test_var.isinstanceof(Variables.Interval), True)
        
        test_var = Variables.initiate_variable('p', 'p', [stats.norm(1,0.1),
                                                          stats.norm(2,0.2)])
        self.assertEqual(test_var.isinstanceof(Variables.Pbox), True)
        
        test_var = Variables.initiate_variable('c', 'c', stats.norm(1,0.1))
        self.assertEqual(test_var.isinstanceof(Variables.Cdf), True)
        
        test_var = Variables.initiate_variable('h', 'h', [1,2,4])
        self.assertEqual(test_var.isinstanceof(Variables.Hist), True)
        
        self.assertRaises(TypeError, Variables.initiate_variable, 'b', 'b', 2)
        self.assertRaises(ValueError, Variables.initiate_variable, 'h', 'h', 3)


if __name__ == "__main__":
    unittest.main()
