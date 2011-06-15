ACC = '/Users/vitorsilva/Documents/PhD/DBELA/data/sakaria.txt'
LOG_PATH = '/Users/vitorsilva/Documents/PhD/DBELA/data/log.txt'

import os
import numpy
import math
from scipy import sqrt
from scipy import log
from scipy import interpolate
from numpy import numarray
import datetime

os.remove(LOG_PATH)
log_file = open(LOG_PATH, 'a')


def log(msg):
		log_file.write(msg + '\n')
		

def parse_acc(path):

	file=open(path)
	lines=file.readlines()
	file.close
	accelerogram=[]	
	for line in lines:
		accelerogram.append( [float(line.split()[0]),float(line.split()[1])])

	return accelerogram
	

def compute_disp(accs, accstep, period, damping):
	
#	interpolator = interpolate.interp1d(times,accs, kind = 'linear')
	fraction = 1/0.02

	pNocount = 0
	lfine = 0
	np = len(accs)
	pNocount=pNocount+1
	
	MaxSteps = (np+1) * (round(int(accstep*fraction/period)) + 1) +1
	ugh=numarray.zeros(MaxSteps)

	
	fine = round(int(accstep * fraction / period)) + 1
	if fine != lfine:
		L = 1
		i = 1
		while (i <=1 + (np - 1) * fine ):
			i=i+fine
			L=L+1
	
	
	dt = accstep / fine
	lfine = fine
	M = 1 + (np - 1) * fine

	pNocount = 0
	xie = damping
	maxug = max(accs)
	lfine =0

	pNocount = 1

	fine = round(int(accstep * fraction / period)) + 1
	if fine != lfine:
		L = -1
		i = 0
		while (i <= (np - 1) * fine ):
			i=i+fine
			L=L+1
			
			ugh[i] = accs[L]
			
			for M in range(int(fine)):
				ugh[i-M+1] = ugh[i - fine] + (ugh[i] - ugh[i - fine]) * (fine - M +1) / fine

	lfine = fine
	M = 1 + (np - 1) * fine
	dt = accstep / fine
	ncf = 2.0 * 3.14159265 / period
	
	fraction = 1.0/0.02
	Gamma_Parm = 0.5
	Beta_Parm = 0.25
	damp = 0.05
	THdsps = []
	THvels = []
	THaccs = []
	
	U0 = 0.0
	U1 = 0.0
	V0 = 0.0
	V1 = 0.0
	A0 = 0.0
	A1 = 0.0
	xie = damping
	for i in range(int(M)):
		U1 = (-ugh[i+1] + U0 / Beta_Parm / (dt*dt) + V0 / Beta_Parm / dt + (1.0 / 2.0 / Beta_Parm - 1.0) * A0 + (U0 * Gamma_Parm / Beta_Parm / dt + (Gamma_Parm / Beta_Parm - 1.0) * V0 + (Gamma_Parm / 2.0 / Beta_Parm - 1.0) * dt * A0) * 2.0 * xie * ncf) / (1.0 / Beta_Parm / (dt*dt) + 2.0 * xie * ncf * Gamma_Parm / Beta_Parm / dt + (ncf*ncf))
		V1 = (U1 - U0) * Gamma_Parm / Beta_Parm / dt + (1.0 - Gamma_Parm / Beta_Parm) * V0 + (1.0 - Gamma_Parm / 2.0 / Beta_Parm) * dt * A0
		A1 = (U1 - U0) / Beta_Parm / (dt*dt) - V0 / Beta_Parm / dt + (1.0 - 1.0 / 2.0 / Beta_Parm) * A0
		U0 = U1
		V0 = V1
		A0 = A1
		THdsps.append(U1)
#		THvels.append(V1)
		THaccs.append(A1+ugh[i+1])
		
	Sa = max([math.fabs(min(THaccs)),max(THaccs)])
#	Sv = max([math.fabs(min(THvels)),max(THvels)])*9.81
	Sd = max([math.fabs(min(THdsps)),max(THdsps)])*9.81	
	
	return Sd,Sa
	
	
	