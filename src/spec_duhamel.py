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
	w = 2.0 * math.pi / period
	e = 0.05
	times = []
	accs = []
	THdisp = []
	THvel = []
	THacc = []
		
	for i in range(number_values):
		times.append(accelerogram[i][0])
		accs.append(accelerogram[i][1])

	interpolator = interpolate.interp1d(times,accs, kind = 'linear')
	dt = times[2]-times[1]

	for i in range(int(number_values-1)):
		time=(i+1)*dt
		number_taus = max([50,int(2*time/dt)])
		tau = time/number_taus
		expo = []
		seno = []
		produto = []
		trap = []
		sum = 0.0		
		
		for j in range(number_taus+1):
			aTau = j * tau
			acc = interpolator(aTau)
			expo.append(math.exp(-damping * w * (time-aTau)))
			seno.append(math.sin(w * (time-aTau)))
			produto.append(acc * expo[j] * seno[j])

			if j == 0 or j == number_taus:
				trap.append(produto[j])
	         
			if j > 0 and j < number_taus :
				trap.append(2 * produto[j])
				
			sum=sum + trap[j]
		
		print aTau	
		sum=sum*tau/2.0
		sum=sum/w	
		log('%s,%s' % (aTau,sum*981))
		THdisp.append(sum)
	
	THvel.append(0)
	THacc.append(max([-min(accs),max(accs)]))
	for i in range(int(number_values)-2):
		  THvel.append((THdisp[i+1]-THdisp[i])/(dt));
		  THacc.append((THvel[i+1]-THvel[i])/(dt));
		
	print 'disp', max([math.fabs(min(THdisp)) , max(THdisp)])*981
	print 'vel', max([math.fabs(min(THvel)) , max(THvel)])*981
	print 'acc', max([math.fabs(min(THacc)) , max(THacc)])	
	
	
	return THdisp

log_file.close()