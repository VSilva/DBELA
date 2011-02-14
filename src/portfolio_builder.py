"""
This script produces a virtual building portfolio based on information stored in a common text file. 
We might update this to NRML or something so we can refactor it a hundred times per week..
"""
EXPOSURE = '/Users/vitorsilva/Documents/GEM/openquake/tests/data/Parameters_porfolio.txt'

import numpy
import math
#from numpy import scipy

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

def compute_prob_value(mean, cov, distribution):
	
	if distribution == normal:
		result = scipy.stats.
		
	if distribution == lognormal:
		result = scipy.stats.

	if distribution == gamma:
		result = scipy.stats.
	
	return result
	

def create_asset(lines, number_category):
	print(lines[number_category])
	asset=[]
	asset.append(lines[number_category].split()[3])
	asset.append(200000)
	asset.append(400)
	asset.append(3)
	asset.append(3)
	asset.append(2)
	asset.append(0.6)
	asset.append(0.5)
	asset.append(10)
	print(asset)
		
	return asset
	


	
if __name__ == "__main__":
	print parse_input(EXPOSURE)