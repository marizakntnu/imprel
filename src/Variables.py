"""
Implementation of the of random variables for Structural Reliability Analysis
(Classic and Imprecise). There are five classes for variables: Deterministic, 
Interval, Cdf, Pbox, Hist.

"""

import abc
from scipy.interpolate import interp1d
#from utils import calculate_cdf         # use this line for tests
from . import *                          # instead of this

class BaseVariable:
    """Abstract Random variable.

    Concrete subclasses should define method:
        `get_bounds`

    """
    @abc.abstractmethod
    def get_bounds(self, x):
        pass

    def isinstanceof(self, cls):
        return isinstance(self, cls)
    
    def value_check(self, x):
        if x<0 or x>1:
            raise ValueError('Probability value is out of bounds [0,1].') 

class Deterministic(BaseVariable):
    """Class for assigning Deterministic variable.
    Requests constant (int or float type).
    
    Example:
    -------
    x = Deterministic('name', constant)
    """
    def __init__(self, name: str, value):
        self.name = name
        self.value = value

    def get_bounds(self, x):
        self.value_check(x)
        return (self.value, self.value)

class Interval(BaseVariable):
    """Class for assigning Interval variable.
    Requests two constants (int or float type) for lower and upper bounds.
    
    Example:
    -------
    x = Cdf('name', constant1, constant2)
    """
    def __init__(self, name: str, lb, ub, goal=None):
        self.name = name
        self.lb = min(lb, ub)
        self.ub = max(lb, ub)

    def get_bounds(self, x):
        self.value_check(x)
        return (self.lb, self.ub)


class Cdf(BaseVariable):
    """Class for assigning Cdf variable. 
    Requests scipy_rv.
    
    Example:
    -------
    import scipy.stats as stats
    x = Interval('name', stats.norm(loc=0., scale=1.))
    """
    def __init__(self, name: str, scipy_rv):
        self.name = name
        self.rv = scipy_rv

    def get_bounds(self, x):
        self.value_check(x)
        cdf_value = self.rv.ppf(x)
        return (cdf_value, cdf_value)

class Pbox(BaseVariable):
    """Class for assigning Cdf variable. 
    Requests a list of scipy_rvs.
    
    Example:
    -------
    import scipy.stats as stats
    x = Pbox('name', [stats.norm(loc=0., scale=1.),
                      stats.norm(loc=1., scale=1.)])
    """
    def __init__(self, name: str, scipy_rvs, goal=None):
        self.name = name
        self.rvs = scipy_rvs

    def get_bounds(self, x):
        self.value_check(x)
        ppfs = [rv.ppf(x) for rv in self.rvs]
        return (min(ppfs), max(ppfs))


class Hist(BaseVariable):
    """Class for assigning Cdf variable. 
    Requests a list of scipy_rvs.
    
    Example:
    -------
    import scipy.stats as stats
    x = Hist('name', [i for i in range(10,100,2)])
    y = Hist('name', stats.norm(loc=0., scale=1.).rvs(100))
    """
    def __init__(self, name: str, hist: list):
        self.name = name
        self.hist = hist
        self.sorted_data, self.cdf_values = calculate_cdf(self.hist)
        self.inv_cdf = interp1d(self.cdf_values, self.sorted_data, bounds_error=False, 
                                    fill_value=(self.sorted_data[0], self.sorted_data[-1]))

    def get_bounds(self, x):
        self.value_check(x)
        hist_value = float(self.inv_cdf(x))
        return (hist_value, hist_value)
    
def initiate_variable(var_type: str, name: str, arg, goal=None):
    """Function to asign variable universally without spicifying the class,
    but only the first letter of the class name and variable features
    as arguments.
    
    Example:
    -------
    import scipy.stats as stats
    x1 = initiate_variable('d', 'name', 1)
    x2 = initiate_variable('i', 'name', 1, 2)
    x3 = initiate_variable('c', 'name', scipy.stats.norm(loc=0., scale=1.))
    x4 = initiate_variable('p', 'name', [stats.norm(loc=0., scale=1.),
                                        stats.norm(loc=1., scale=1.)])
    x5 = initiate_variable('h', 'name', [i for i in range(10,100,2)])
    
    """
    var_types = {
        'd': Deterministic,
        'i': Interval,
        'p': Pbox,
        'c': Cdf,
        'h': Hist
    }
    if goal!=None:
        return var_types[var_type](name, arg, goal)
    if not var_type in var_types.keys():
        raise TypeError('Choose the appropriate type of variable.')
    try:
        return var_types[var_type](name, arg)
    except:
        raise ValueError('Check the way of assigning the variable.')
        