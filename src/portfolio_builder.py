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
		number_assets.append(int(line.split('	')[4].strip()))
		
	return number_categories,number_assets 

def compute_prob_value(parameters, distribution, rvs):
	mean = float(parameters[0])
	stddev = float(parameters[1])/100*mean
	
	if distribution == "normal":
		
		if rvs is None:
			rvs = stats.norm.rvs
		result = rvs(mean,stddev)
		
	elif distribution == "lognormal":
		variance = stddev ** 2.0
		mu = log(mean ** 2.0 / sqrt(variance + mean ** 2.0) )
		sigma = sqrt(log((variance / mean ** 2.0) + 1.0))
		
		if rvs is None:
			rvs = stats.lognorm.rvs
		result = rvs(sigma, scale=scipy.exp(mu))

	elif distribution == "gamma":
		betha = (stddev)**2/mean
		alpha = mean/betha
		
		if rvs is None:
			rvs = stats.gamma.rvs
		result = rvs(alpha,scale = betha)
	
	return result
	

def create_asset(line, rvs=None):

	asset=[]
	asset.append(line.split()[2])	
	asset.append(line.split()[3])
	for i in range(8):
		parameters=[]
		parameters.append(line.split()[int(6+i*3)])
		parameters.append(line.split()[int(7+i*3)])
		distribution = line.split()[int(8+i*3)]
		asset.append(compute_prob_value(parameters,distribution, rvs))
	
	asset.append(line.split()[5])
		
	return asset
	