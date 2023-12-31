import imprel
import scipy.stats as stats

def obj_func(x):
    return x[0]-x[1]



# Structural Reliability Analysis case
mr = 1.
sr = .14

ms = .2
ss = .2

variables = [imprel.initiate_variable('c', 'r', stats.norm(mr, sr)),
             imprel.initiate_variable('c', 's', stats.norm(ms, ss))]

res_sra = imprel.Analysis(variables, obj_function=obj_func, nsamples=10000)
 

                  
# Imprecise Structural Reliability Analysis case
mr1 = .7
sr1 = .14

mr2 = .8
sr2 = .14

ms1 = .2
ss1 = .2

ms2 = .1
ss2 = .2

variables = [imprel.initiate_variable('p', 'r', [stats.norm(mr1, sr1),
                                                 stats.norm(mr2, sr2)]),
             imprel.initiate_variable('p', 'r', [stats.norm(ms1, ss1),
                                                 stats.norm(ms2, ss2)])]

res_isra = imprel.Analysis(variables, obj_function=obj_func, nsamples=10000)