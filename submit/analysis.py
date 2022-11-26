from SAT import *
from dpll import *
import time
import numpy as np
import matplotlib.pyplot as plt

#%%
# 9x9

## Read Files
backtracks_dict = {}
iterations_dict = {}
assignments_dict = {}

for heuristic in (1,2,3):
    
    file = f"4x4_S{heuristic}_v3.txt"

    
    backtracks_dict.get(heuristic, [])
    iterations_dict.get(heuristic, [])
    
    with open(file, 'r') as f:
        lines = f.readlines()
        backtracks_dict[heuristic] = [int(i) for i in lines[1:1011]]
        iterations_dict[heuristic] = [float(lines[1014])]


np.mean(backtracks_dict[1])
np.mean(backtracks_dict[2])
np.mean(backtracks_dict[3])

np.std(backtracks_dict[1])
np.std(backtracks_dict[2])
np.std(backtracks_dict[3])

# Analyze 

import scipy.stats as stats

def t_test(sample1, sample2, name):
    test = stats.ttest_ind(sample1, sample2)
    print(f"t-test for {name} with {round(test[0],5)} with p-value {round(test[1],5)}")
    return test

# Backtracks
stats.f_oneway(backtracks_dict[1], backtracks_dict[2], backtracks_dict[3])        
    
# S1 vs. S2
s1s2 = t_test(backtracks_dict[1], backtracks_dict[2], "backtracks")

# S2 vs. S3
s2s3 = t_test(backtracks_dict[2], backtracks_dict[3], "backtracks")

# S1 vs. S3
s1s3 = t_test(backtracks_dict[1], backtracks_dict[3], "backtracks")


np.mean(backtracks_dict[1])
np.mean(backtracks_dict[2])
np.mean(backtracks_dict[3])

np.std(backtracks_dict[1])
np.std(backtracks_dict[2])
np.std(backtracks_dict[3])

iterations_dict

#%%
# 9x9

## Read Files
backtracks_dict = {}
iterations_dict = {}

for heuristic in (1,3):
    
    file = f"500_S{heuristic}.txt"

    
    backtracks_dict.get(heuristic, [])
    iterations_dict.get(heuristic, [])
    
    with open(file, 'r') as f:
        lines = f.readlines()
        backtracks_dict[heuristic] = [int(i) for i in lines[1:501]]
        iterations_dict[heuristic] = [float(i) for i in lines[1008 : 1508]]


# Analyze 

import scipy.stats as stats

def t_test(sample1, sample2, name):
    test = stats.ttest_ind(sample1, sample2)
    print(f"t-test for {name} with {round(test[0],5)} with p-value {round(test[1],5)}")
    return test

# Backtracks
stats.f_oneway(backtracks_dict[1], backtracks_dict[3]) 
       
stats.f_oneway(iterations_dict[1], iterations_dict[3])        


# Backtracks
bt_comp = t_test(backtracks_dict[1], backtracks_dict[3], "backtracks")

# S2 vs. S3
it_comp = t_test(iterations_dict[1], iterations_dict[3], "iterations")


np.mean(backtracks_dict[1])
np.mean(backtracks_dict[3])
np.std(backtracks_dict[1])
np.std(backtracks_dict[3])

np.mean(iterations_dict[1])
np.mean(iterations_dict[3])
np.std(iterations_dict[1])
np.std(iterations_dict[3])


#%%


