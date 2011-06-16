"""
This script produces a virtual building portfolio based on information stored in a common text file. 
We might update this to NRML or something so we can refactor it a hundred times per week..
"""
EXPOSURE = '/Users/vitorsilva/Documents/PhD/DBELA/data/parameters_porfolio.txt'

import numpy
import scipy
from scipy import sqrt
from scipy import log
import math
from scipy import stats

def parse_input(path):
    
    file = open(path)
    lines = file.readlines()
    file.close
    return lines

def buildings_counter(lines):
    
    number_categories = len(lines)
    number_assets = []
    
    for line in lines:
        number_assets.append(int(line.split('\t')[4].strip()))
        
    return number_categories,number_assets 

def compute_continuous_prob_value(parameters, distribution, rvs):
    mean = float(parameters[0])
    stddev = float(parameters[1])/100*mean
    A = float(parameters[2])
    B = float(parameters[3])
    result = float('-inf')
       
    if rvs is None:
        while result <= A or result > B:

            if distribution == "normal":    
                rvs = stats.norm.rvs
                result = rvs(mean,stddev)
        
            elif distribution == "lognormal":
                variance = stddev ** 2.0
                mu = log(mean ** 2.0 / sqrt(variance + mean ** 2.0) )
                sigma = sqrt(log((variance / mean ** 2.0) + 1.0))
                rvs = stats.lognorm.rvs
                result = rvs(sigma, scale=scipy.exp(mu))

            elif distribution == "gamma":
                betha = (stddev)**2/mean
                alpha = mean/betha
                rvs = stats.gamma.rvs
                result = rvs(alpha,scale = betha)
    else:
        result = 1            

    return result
    
def compute_discrete_prob_value(parameters):
    
    x_values = parameters[0].split('-')
    PMF = parameters[1].split('-')
    A = float(parameters[2])
    B = float(parameters[3])
    result = float('-inf')
    
    CPMF = []
    CPMF.append(0)
    for i in range(len(PMF)):
        CPMF.append(CPMF[i]+float(PMF[i]))
        
    rand_value = stats.uniform.rvs()
    for i in range(len(PMF)):
        while result <= A or result > B:
            if rand_value > CPMF[i] and rand_value < CPMF[i+1]: 
                result = x_values[i]   
    
    return result
    

def create_asset(line, rvs=None):
    
    # data 0 - structure type
    # data 1 - code level
    # data 2 - steel strain
    # data 3 - steel strengh
    # data 4 - Upper floor height
    # data 5 - Ground/upper floor height ratio	
    # data 6 - Column depth
    # data 7 - Beam length
    # data 8 - Beam depth  
    # data 9 - number of storeys
																	
    asset=[]
    asset.append(line.split()[2]) # structure type (bare-frame, dual frame wall)
    asset.append(line.split()[3]) # code level
    pos=0
    
    for i in range(7):
        parameters=[]
        parameters.append(line.split()[int(6+pos+i*3)])
        parameters.append(line.split()[int(7+pos+i*3)])
        parameters.append(line.split()[int(8+pos+i*3)])
        parameters.append(line.split()[int(9+pos+i*3)])
        distribution = line.split()[int(10+pos+i*3)]
        pos=pos+2
            
        if distribution != 'discrete':
            asset.append(compute_continuous_prob_value(parameters,distribution, rvs))
        else:
            asset.append(compute_discrete_prob_value(parameters))          
    
    asset.append(line.split()[5]) # number of storeys
        
    return asset
    