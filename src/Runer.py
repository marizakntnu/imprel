"""
Implementation of the Structural Reliability Analysis (SRA) and
Imprecise Structural Reliability Analysis (ISRA). The implementation is
based on the following resources:

    `Thoft-Cristensen, P., & Baker, M. J. (2012). Structural reliability 
    theory and its applications. Springer Science & Business Media.`
    
    `Schöbi, R., & Sudret, B. (2017). Structural reliability analysis for
    p-boxes using multi-level meta-models. Probabilistic Engineering
    Mechanics, 48, 27-38.`

"""

import numpy as np
import time
import os
import pickle
from scipy.optimize import minimize
#from utils import pf, get_reliability_index         # use this line for tests
from . import *                                      # instead of this 

# class of analysis
class Analysis:
    methods = {
        'scipy': 'scipy_analyse'
        }

    def __init__(self, variables: list, obj_function: callable, method='scipy', nsamples=10):
        if not method in self.methods:
            raise ValueError("Invalid method specified: {}".format(method))
        self.method = method
        self.nsamples = nsamples
        self.variables = variables
        self.obj_function = obj_function

        t = time.time()
        self.samples = self.sampling(nsamples)
        self.results = getattr(self, self.methods[method])(self.samples)
        t = round(time.time()-t)
        self.time = t
        print(f'Time spent: {t} s')
        self.print_results()

    def sampling(self, nsamples):
        """Function to generate nsamples from [0,1]."""
        num_var = len(self.variables)
        return np.random.uniform(size=(nsamples, num_var))

    def scipy_analyse(self, samples):
        """Function for analysis.
        In the case of appearence of Pbox or Interval variables
        the Imprecise Structural Reliability Analysis (ISRA) is held,
        otherwise Structural Reliability Analysis (SRA) is utilized."""
        results = {}
        variables = self.variables
        t = ''
        for var in variables:
            t += str(type(var))

        if (('Pbox' in t) or ('Interval' in t)):
            print('Imprecise Structural Reliability Analysis (ISRA) has been started...')
            for num, sample in enumerate(samples):
                bounds = [v.get_bounds(sample0) for v,sample0 in zip(variables,sample)]
                
                # Searching for min value
                x0 = tuple([np.random.uniform(var_bound[0],var_bound[1]) for var_bound in bounds])
                res_min = minimize(self.obj_function, x0=x0, bounds=bounds, method='SLSQP')
                if not res_min.success:
                    raise ValueError(f"Could not find lower bound. {res_min.message}")

                # Searching for max value
                x0 = tuple([np.random.uniform(var_bound[0],var_bound[1]) for var_bound in bounds])
                res_max = minimize(lambda x: -self.obj_function(x), x0=x0, bounds=bounds, method='SLSQP')
                if not res_max.success:
                    raise ValueError(f"Could not find upper bound. {res_max.message}")
                    
                results[num] = {'min': {'y': res_min.fun, 'x': res_min.x}, 'max': {'y': -res_max.fun, 'x': res_max.x}}

        else:
            print('Structural Reliability Analysis (SRA) has been started...!')
            xs = [[v.get_bounds(s)[0] for v, s in zip(variables, sample)] for sample in samples]
            ys = [*map(self.obj_function, xs)]
            results = {num: {"min": {"y":y, "x":x}, 'max': {'y': np.inf, 'x': np.inf}} for num, (x, y) in enumerate(zip(xs, ys))}
        
        return results

    def print_results(self):
        """Function to print the results."""
        self.ymin = [num['min']['y'] for num in self.results.values()]
        self.ymax = [num['max']['y'] for num in self.results.values()]
        self.pf = (pf(self.ymin), pf(self.ymax))
        self.b = (get_reliability_index(self.pf[0]),
                  get_reliability_index(self.pf[1]))
        self.reliability = {
            'lower': {
                'y': self.ymin,
                'pf': self.pf[0],
                'b': self.b[0]
            },
            'upper': {
                'y': self.ymax,
                'pf': self.pf[1],
                'b': self.b[1]
            }
        }
        print('Lower:\n pf   =', self.pf[0], '\n beta =', self.b[0])
        print('Upper:\n pf   =', self.pf[1], '\n beta =', self.b[1])

    def save_to_file(self, filename):
        """Function to save results of the analysis to the .pkl file."""
        # Create the 'results' directory if it doesn't exist
        if not os.path.exists('results'):
            os.makedirs('results')

        # Save the file in the 'results' directory
        with open(f'results/{filename}.pkl', 'wb') as f:
            pickle.dump({
                'method': self.method,
                'nsamples': self.nsamples,
                'time': self.time,
                'pf': self.pf,
                'b': self.b,
                'variables': [{k: v for k, v in var.__dict__.items() if k != '_func'} for var in self.variables],
                'results': self.results
            }, f)