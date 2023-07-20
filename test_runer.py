"""
Unittests for file Runer.py.

"""

import unittest
import Runer
import Variables
import scipy.stats as stats

def beta(mr, sr, ms, ss):
    "Beta for g(x)=R-S"
    return (mr-ms)/(sr**2+ss**2)**.5

class TestBeta(unittest.TestCase):
    
    def test_beta(self):
        print('test_beta')
        mr = 1.
        sr = .14
    
        ms = .2
        ss = .2
        b = beta(mr, sr, ms, ss)
    
        assert b == 3.276927682076162

class TestRuner(unittest.TestCase):
#class TestUtils(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        print('\n***Runer.py tests:***\n') 
        
    @classmethod
    def tearDownClass(self):
        print('\n***Runer.py tests have finished***\n') 
        
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
   
    def test_Analysis_classic(self):
        print('test_Analysis_classic')
        
        mr = 1.
        sr = .14
    
        ms = .2
        ss = .2
        
        def obj_func(x):
            return x[0]-x[1]
        
        variables=[Variables.initiate_variable('c', 'r', stats.norm(mr, sr)),
                   Variables.initiate_variable('c', 's', stats.norm(ms, ss))]
        
        res = Runer.Analysis(variables, obj_function=obj_func,
                             method='scipy', nsamples=10000)
        
        b = res.b[0]
        bf = beta(mr, sr, ms, ss)
        
        diff = abs(bf - b)
        self.assertGreater(0.2, diff)
        
    def test_Analysis_r_pbox1(self):
        print('test_Analysis_r_pbox1')
        
        mr1 = .7
        sr1 = .14
        
        mr2 = .8
        sr2 = .14
    
        ms = .2
        ss = .2
        
        def obj_func(x):
            return x[0]-x[1]
        
        variables = [Variables.initiate_variable('p', 'r', [stats.norm(mr1, sr1),
                                                          stats.norm(mr2, sr2)]),
                   Variables.initiate_variable('c', 's', stats.norm(ms, ss))]
        
        res = Runer.Analysis(variables, obj_function=obj_func,
                             method='scipy', nsamples=10000)
        
        b1 = res.b[0]
        b2 = res.b[1]
        bf1 = beta(mr1, sr1, ms, ss)
        bf2 = beta(mr2, sr2, ms, ss)
        
        diff1 = abs(bf1 - b1)
        diff2 = abs(bf2 - b2)
        print(b1, bf1)
        print(b2, bf2)
        
        self.assertGreater(0.2, diff1)
        self.assertGreater(0.2, diff2)   
    
    def test_Analysis_r_pbox2(self):
        print('test_Analysis_r_pbox2')
        
        mr1 = .8
        sr1 = .14
        
        mr2 = .8
        sr2 = .05
    
        ms = .2
        ss = .2
        
        def obj_func(x):
            return x[0]-x[1]
        
        variables=[Variables.initiate_variable('p', 'r', [stats.norm(mr1, sr1),
                                                          stats.norm(mr2, sr2)]),
                   Variables.initiate_variable('c', 's', stats.norm(ms, ss))]
        
        res = Runer.Analysis(variables, obj_function=obj_func,
                             method='scipy', nsamples=10000)
        
        b1 = res.b[0]
        b2 = res.b[1]
        bf1 = beta(mr1, sr1, ms, ss)
        bf2 = beta(mr2, sr2, ms, ss)
        
        diff1 = abs(bf1 - b1)
        diff2 = abs(bf2 - b2)
        print(b1, bf1)
        print(b2, bf2)
        
        self.assertGreater(0.2, diff1)
        self.assertGreater(0.2, diff2)
    
    def test_Analysis_s_pbox1(self):
        print('test_Analysis_s_pbox1')
        
        mr = .8
        sr = .14
    
        ms1 = .2
        ss1 = .2
        
        ms2 = .1
        ss2 = .2
        
        def obj_func(x):
            return x[0]-x[1]
        
        variables=[Variables.initiate_variable('c', 'r', stats.norm(mr, sr)),
                   Variables.initiate_variable('p', 's', [stats.norm(ms1, ss1),
                                                          stats.norm(ms2, ss2)])]
        
        res = Runer.Analysis(variables, obj_function=obj_func,
                             method='scipy', nsamples=10000)
        
        b1 = res.b[0]
        b2 = res.b[1]
        bf1 = beta(mr, sr, ms1, ss1)
        bf2 = beta(mr, sr, ms2, ss2)
        
        diff1 = abs(bf1 - b1)
        diff2 = abs(bf2 - b2)
        print(b1, bf1)
        print(b2, bf2)
        
        self.assertGreater(0.2, diff1)
        self.assertGreater(0.2, diff2)
        
    def test_Analysis_s_pbox2(self):
        print('test_Analysis_s_pbox2')
        
        mr = .8
        sr = .14
    
        ms1 = .2
        ss1 = .25
        
        ms2 = .2
        ss2 = .2
        
        def obj_func(x):
            return x[0]-x[1]
        
        variables=[Variables.initiate_variable('c', 'r', stats.norm(mr, sr)),
                   Variables.initiate_variable('p', 's', [stats.norm(ms1, ss1),
                                                          stats.norm(ms2, ss2)])]
        
        res = Runer.Analysis(variables, obj_function=obj_func,
                             method='scipy', nsamples=10000)
        
        b1 = res.b[0]
        b2 = res.b[1]
        bf1 = beta(mr, sr, ms1, ss1)
        bf2 = beta(mr, sr, ms2, ss2)
        
        diff1 = abs(bf1 - b1)
        diff2 = abs(bf2 - b2)
        print(b1, bf1)
        print(b2, bf2)
        
        self.assertGreater(0.2, diff1)
        self.assertGreater(0.2, diff2)

if __name__ == "__main__":
    unittest.main()
