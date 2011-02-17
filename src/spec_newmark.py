ACC = '/Users/vitorsilva/Documents/PhD/DBELA/data/sakaria.txt'
LOG_PATH = '/Users/vitorsilva/Documents/PhD/DBELA/data/log.txt'

import os
import numpy
import math
from scipy import sqrt
from scipy import log
from scipy import interpolate

os.remove(LOG_PATH)
log_file = open(LOG_PATH, 'a')

def parse_acc(path):
	
	file = open(path)
	lines = file.readlines()
	file.close
	
	accelerogram=[]	
	acc=[]
	for line in lines:
		accelerogram.append( [float(line.split()[0]),float(line.split()[1])])

	return accelerogram


def log(msg):
		log_file.write(msg + '\n')
	

def compute_disp(accelerogram, period, damping):
	
	number_values = len(accelerogram)
	times = []
	accs = []
	for i in range(number_values):
		times.append(accelerogram[i][0])
		accs.append(accelerogram[i][1])
	print max(accs)
	
	interpolator = interpolate.interp1d(times,accs, kind = 'linear')
	w = 2.0 * math.pi / period
	Gamma = 0.5
	Beta = 0.25
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
	accstep = accelerogram[2][0]-accelerogram[1][0]
	dt = min([0.02*period,accstep])
	print(dt)
	i=0
	
	while i*dt < max(times):
		acc = interpolator(i*dt)
		U1 = (-acc + U0 / Beta / (dt*dt) + V0 / Beta / dt + (1.0 / 2.0 / Beta - 1.0) * A0 + (U0 * Gamma / Beta / dt + (Gamma / Beta - 1.0) * V0 + (Gamma / 2.0 / Beta - 1.0) * dt * A0) * 2.0 * damp * w) / (1.0 / Beta / (dt*dt) + 2.0 * damp * w * Gamma / Beta / dt + (w*w))	
		V1 = (U1 - U0) * Gamma / Beta / dt + (1.0 - Gamma / Beta) * V0 + (1.0 - Gamma / 2.0 / Beta) * dt * A0
		A1 = (U1 - U0) / Beta / (dt*dt) - V0 / Beta / dt + (1.0 - 1.0 / 2.0 / Beta) * A0
		U0 = U1
		V0 = V1
		A0 = A1
		i=i+1
		THdsps.append(U1)
		THvels.append(V1)
		THaccs.append(A1+acc)
		log('%s,%s' % (i*dt,U1*981))

	print 'disp', max(THdsps)*981	
	print 'vel', max(THvels)*981	
	print 'acc', max(THaccs)	
	return THdsps

accelerogram = parse_acc(ACC)
damping = 0.05
period = 0.5
print 'period', period
disp = compute_disp(accelerogram, period, damping)
log_file.close()
	
	
	