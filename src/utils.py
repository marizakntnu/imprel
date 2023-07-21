"""
Implementation of some useful functions in process of
Structural Reliability Analysis.
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def get_lognorm_param(m,s):
    """Function to obtain parameters of lognormal distribution."""
    m_ln = np.log(m**2/(np.sqrt(m**2+s**2)))
    s_ln = np.sqrt(np.log(1+s**2/m**2))
    return s_ln, np.exp(m_ln)

def pf(arr):
    """Function to calculate probability of failure from samples."""
    try:
        num_negative = len(np.array(arr)[np.array(arr) < 0])
        proportion = num_negative / len(arr)
        return proportion
    except:
        raise TypeError('Provide an array or tuple of float or integer elements')

def get_reliability_index(pf):
    """
    Function to calculate reliability index corresponding
    to given probability of failure.
    """
    if pf<0 or pf>1:
        raise ValueError('Probability of failure is out of bounds [0,1]')
    elif pf==0:
        return np.inf
    elif pf==1:
        return -np.inf
    else:
        return stats.norm.ppf(1.0 - pf, loc=0., scale=1.)

def get_probability_of_failure(ri):
    """
    Function to calculate probability of failure corresponding
    to given reliability index.
    """
    return 1.0 - stats.norm.cdf(ri, loc=0., scale=1.)
   
# There are two ways defined to obtain CDF from the array of values.
    
def get_cdf(data, pplot=True):
    """There are two ways defined to obtain CDF from the array of values:
    get_cdf() and calculate_cdf()."""
    bins = np.linspace(-3, 3, 100)
    count, bins_count = np.histogram(data, bins=bins)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    if pplot==True:
        plt.plot(bins[1:], cdf)
    return cdf, bins[1:]

def calculate_cdf(data):
    """There are two ways defined to obtain CDF from the array of values:
    get_cdf() and calculate_cdf()."""
    # Sort the data in ascending order and calculate the CDF
    sorted_data = np.sort(data)
    n = len(sorted_data)
    cdf_values = np.arange(1, n + 1) / n
    return sorted_data, cdf_values
