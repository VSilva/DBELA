LOG_PATH = '/Users/vitorsilva/Documents/PhD/CoSimulationTrial/Portfolio.txt'
LOG_PATH1 = '/Users/vitorsilva/Documents/PhD/CoSimulationTrial/Vul_codes.txt'
FILEPATH = '/Users/vitorsilva/Documents/PhD/CoSimulationTrial/LA.csv'

import math
from numpy import numarray
import os

os.remove(LOG_PATH)
log_file = open(LOG_PATH, 'a')
log_file1 = open(LOG_PATH1, 'a')

def log(msg):
	log_file.write(msg)

def log1(msg):
	log_file1.write(msg)	

def parse_input(path):
	
	file = open(path)
	lines = file.readlines()
	file.close
	
	Latitude=[]
	Longitude=[]
	UniqueLocations=[]
	UniqueAreas=[]
	NumberUniqueLocations=1
	Area=[]
	Population=[]
	numberAssets = len(lines)
	
	for line in lines:
		Longitude.append(line.split(',')[0].strip())
		Latitude.append(line.split(',')[1].strip())
		Area.append(line.split(',')[2].strip())
		Population.append(int(line.split(',')[3].strip()))	
	
	UniqueLocations.append(str(Longitude[0]) + ','+ str(Latitude[0]))
	UniqueAreas.append(float(Area[0]))
	addLocation = 0;
	
	for i in range(numberAssets):
#	for i in range(100):
		for j in range(NumberUniqueLocations): 
			if str(Longitude[i]) + ',' + str(Latitude[i]) == UniqueLocations[j]:
				addLocation = 0
				
		if addLocation == 1:
			UniqueLocations.append(str(Longitude[i]) + ','+ str(Latitude[i]))
			UniqueAreas.append(float(Area[i]))
			NumberUniqueLocations=NumberUniqueLocations+1
		addLocation = 1;		
	
	SumPopulation = numarray.zeros(NumberUniqueLocations)
	
	for i in range(numberAssets):
		for j in range(NumberUniqueLocations): 
			if str(Longitude[i]) + ','+ str(Latitude[i]) == UniqueLocations[j]:
				SumPopulation[j]=SumPopulation[j]+Population[i]
				
	Ratios=[0.1, 0.1 ,0.2, 0.3, 0.3]
	VulnerabilityFunction=['HAZUS_W1_MC','HAZUS_C1L_MC','HAZUS_C1M_MC','HAZUS_C1H_MC','HAZUS_S1H_MC']
	Periods=['0.00', '0.30', ' 0.8', '1.50', '2.20']
	Results=[]
	
	print SumPopulation
	print UniqueLocations
		
	for typoligies in range(5):
		for j in range(NumberUniqueLocations): 
			print typoligies
			Results.append(UniqueLocations[j]+','+str(UniqueAreas[j]*float(SumPopulation[j])*Ratios[typoligies]*1000*1000*100)+','+Periods[typoligies])
	
	for j in range(NumberUniqueLocations*5):
		log(str(Results[j]+'\n'))
	
	for typoligies in range(5):
		for j in range(NumberUniqueLocations):
			log1(VulnerabilityFunction[typoligies]+'\n')

	print Results
		
		
if __name__ == "__main__":
	parse_input(FILEPATH)
	
	log_file.close()
	log_file1.close()