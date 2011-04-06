'This script alocates each building in a damage state'

import numpy
from numpy import numarray
import os

def damage_state_position(capacityDisp, demandDisp):
	
	numberAccs = len(demandDisp)
	numberLS = len(capacityDisp)
	dsPositions = []
	
	for i in range(numberAccs):
		dsPositionsAcc = numarray.zeros(4)
		dsPositionsAcc[3] = dsPositionsAcc[3] + 1.0
		for j in range(numberLS):
			if demandDisp[i][j] < capacityDisp[j]:
				dsPositionsAcc[j] = dsPositionsAcc[j] + 1.0
				dsPositionsAcc[3] = dsPositionsAcc[3] - 1.0
				break	
	
		dsPositions.append(dsPositionsAcc)
	
	return dsPositions
	
	
def print_results(damageStates,imlDamageStates):
	
	totalAssets=sum(damageStates[0])
	numberAccs=len(damageStates)
	numberDSs=len(damageStates[0])
	cumDamageStates=numpy.zeros(numpy.array(damageStates.shape))

	out_file = open(os.path.join('/Users/vitorsilva/Documents/PhD/DBELA/Results.txt'),"w")
	out_file2 = open(os.path.join('/Users/vitorsilva/Documents/PhD/DBELA/Results2.txt'),"w")
	out_file3 = open(os.path.join('/Users/vitorsilva/Documents/PhD/DBELA/Results3.txt'),"w")

	for numberDS in range(numberDSs-1):
		for i in range(numberAccs):
			for j in range(int(damageStates[i][numberDS+1])):
				out_file3.write(str(imlDamageStates[i][3])+',')
		
		if numberDS!=numberDSs-2:
			out_file3.write('\n')
	
	damageStates=numpy.array(damageStates)/totalAssets
	for i in range(numberAccs):
		cumDamageStates[i][1]=damageStates[i][1]+damageStates[i][2]+damageStates[i][3]
		cumDamageStates[i][2]=damageStates[i][2]+damageStates[i][3]
		cumDamageStates[i][3]=damageStates[i][3]
		
		out_file.write(str(imlDamageStates[i][0])+','+str(imlDamageStates[i][1])+','+str(imlDamageStates[i][2])+','+str(imlDamageStates[i][3])+','+str(cumDamageStates[i][1])+','+str(cumDamageStates[i][2])+','+str(cumDamageStates[i][3])+'\n')
		out_file2.write(str(imlDamageStates[i][0])+','+str(imlDamageStates[i][1])+','+str(imlDamageStates[i][2])+','+str(imlDamageStates[i][3])+','+str(damageStates[i][0])+','+str(damageStates[i][1])+','+str(damageStates[i][2])+','+str(damageStates[i][3])+'\n')	
			
	out_file.close()
	out_file2.close()
	out_file3.close()
		
if __name__ == "__main__":
	print 'ok'
	