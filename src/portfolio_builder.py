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
    CPMF.append(0.0)
    for i in range(len(PMF)):
        CPMF.append(CPMF[i]+float(PMF[i]))

    while result <= A or result > B:
        rand_value = stats.uniform.rvs()
        for i in range(len(PMF)):
            if rand_value > CPMF[i] and rand_value < CPMF[i+1]: 
                result = float(x_values[i])
    
    return result
    

def create_asset(line, rvs=None):
    
    #FOR FRAME STRUCTURES
    # data 0  - Structure type
    # data 1  - Code level
    # data 2  - Number of storeys
    # data 3  - Steel modulus
    # data 4  - Steel yield strength
    # data 5  - Upper floor height
    # data 6  - Ground/upper floor height ratio	
    # data 7  - Column depth
    # data 8  - Beam length
    # data 9  - Beam depth  
    # data 10 - Height ground floor
    # data 11 - Total height
    
    #FOR FRAME-WALL STRUCTURES
    # data 0  - Structure type
    # data 1  - Code level
    # data 2  - Number of storeys
    # data 3  - Steel modulus
    # data 4  - Steel yield strength
    # data 5  - Upper floor height
    # data 6  - Ground/upper floor height ratio	 
    # data 7  - Steel ultimate strength
    # data 8  - Wall length
    # data 9  - Diameter of vertical rebars
    # data 10 - Height ground floor
    # data 11 - Total height
    
    #FOR MASONRY STRUCTURES
    # data 0  - Structure type
    # data 1  - Code level
    # data 2  - Number of storeys
    # data 3  - Height per floor
    # data 4  - Pier height
    # data 5  - Yield drift
    # data 6  - LS2 drift
    # data 7  - LS3 drift
    # data 8  - k1
    # data 9  - k2
    # data 10 - Total height
    # data 11 - Total pier height
																	
    asset=[]
    asset.append(line.split()[2]) # structure type (bare-frame, dual frame wall)
    asset.append(line.split()[3]) # code level
    asset.append(int(line.split()[5])) # number of storeys
    pos=0
    noParameters = (len(line.split())-6)/5

    for i in range(noParameters):
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
    
    structureType = asset[0]
    number_storeys = asset[2]
    
    if structureType == 'Masonry_Timber' or structureType == 'Masonry_Concrete':
        total_height = number_storeys*asset[3]
        total_Pheight = number_storeys*asset[4]
        asset.append(total_Pheight)
        asset.append(total_height)
              
    else:
        height_up = asset[5]
        height_gf = asset[5]*asset[6]
        height = compute_height(height_up,height_gf,number_storeys)
        asset.append(height_gf)
        asset.append(height)
    
    return asset
    
def compute_height(height_up,height_gf,number_storeys):

    height = height_gf + (number_storeys-1)*height_up

    return height
    