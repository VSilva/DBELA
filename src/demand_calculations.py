"Demand calculor - given an integration algorithm and a directory with many accelerograms, this code return the displacements for the 3 period"
ACCELEROGRAMS = '/Users/vitorsilva/Documents/PhD/DBELA/data/accelerograms2/'
SPECTRA= '/Users/vitorsilva/Documents/PhD/DBELA/data/spectra/'
IMTVALUES= '/Users/vitorsilva/Documents/PhD/DBELA/data/imtvalues.txt'

import spec_newmark
import os
import math
import numpy
from scipy import interpolate

def parse_acc(path):
    
    file=open(path)
    lines=file.readlines()
    file.close
    accelerogram=[] 
    for line in lines:
        accelerogram.append( [float(line.split()[0]),float(line.split()[1])])
    
    return accelerogram
    
    
def parse_at2_acc(path):
    
    file=open(path)
    lines=file.readlines()
    file.close
    accelerogram=[]
    counter=1
    mult=1
    if lines[0] == 'European Strong-Motion Data\r\n':
        mult=1/9.81

    for line in lines:
        if counter==4:
            dt = float(line.split()[1])
            time = -dt
        if counter>4:
            values = line.strip().split()
            for i in range(len(values)):
                time=time+dt
                accelerogram.append([time,float(values[i])*mult])
            
        counter = counter +1
        
    return accelerogram


def parse_spectrum(path):
    
    file=open(path)
    lines=file.readlines()
    file.close
    spectrum=[] 
    for line in lines:
        spectrum.append(float(line.split()[1]))
    
    return spectrum


def compute_spectra(minPeriod,maxPeriod,step,damping,ACCELEROGRAMS,SPECTRA):

    accs = [x for x in os.listdir(ACCELEROGRAMS) if x.upper()[-4:] == '.AT2']
    spectra = []
    
    for acc in accs:
        save = 0
        spec_file = acc.split('.')[0]+'-'+str(minPeriod)+'-'+str(maxPeriod)+'-'+str(step)+'.txt'
        if os.path.exists(SPECTRA+spec_file):
            spectrum = parse_spectrum(SPECTRA+spec_file)
        else:   
            timeHistories = parse_at2_acc(ACCELEROGRAMS+acc)
            accValues=[]
            for i in range(len(timeHistories)):
                accValues.append(timeHistories[i][1])
            accStep=timeHistories[2][0]-timeHistories[1][0] 
            spectrum = []
            period = minPeriod
            save = 1
            while period <= maxPeriod:
                spectrum.append(spec_newmark.compute_disp(accValues, accStep, period, damping)[0])
                period = period + step
        if save == 1:
            save_spectrum(minPeriod,maxPeriod,step,spectrum,SPECTRA,spec_file)
        spectra.append(spectrum)
        print 'Spectrum '+ acc + ' computed'
    return spectra
    
    
def save_spectrum(minPeriod,maxPeriod,step,spectrum,SPECTRA,spec_file):

    periods = compute_spectra_periods(minPeriod,maxPeriod,step)
    out_file = open(os.path.join(SPECTRA+spec_file),"w")
    for i in range(len(spectrum)):
        out_file.write(str(periods[i])+'    '+str(spectrum[i])+'\n')
    out_file.close()

    
def compute_spectra_periods(minPeriod,maxPeriod,step):
    
    spectraPeriods = []
    period = minPeriod
    while period <= maxPeriod:
        spectraPeriods.append(period)
        period = period + step
    
    return spectraPeriods   


def compute_demand_displacement(data,periods,spectraDisp,spectraPeriods,damping,ACCELEROGRAMS,ductilities):
    
    structureType=data[0]
    minPeriod = min(spectraPeriods)
    maxPeriod = max(spectraPeriods)
    accs = [x for x in os.listdir(ACCELEROGRAMS) if x.upper()[-4:] == '.AT2']
    numberAccs=len(spectraDisp)
    demandDisp=[]
    
    equivalentDampings = compute_equivalent_damping(structureType,ductilities)
    #print equivalentDampings
    correctionFactors = compute_correction_factors(equivalentDampings) 
    #print correctionFactors
    
    for accelerogram in range(numberAccs):
        setDisp = []
        
        for i in range(len(periods)):
            if periods[i] > maxPeriod or periods[i] < minPeriod:
                timeHistories = parse_at2_acc(ACCELEROGRAMS+accs[accelerogram])
                accValues = []
                for j in range(len(timeHistories)):
                    accValues.append(timeHistories[j][1])
                accStep=timeHistories[2][0]-timeHistories[1][0]
                print accs[accelerogram]
                setDisp.append(spec_newmark.compute_disp(accValues, accStep, periods[i], damping)[0]*correctionFactors[i])
            else:
                interpolator = interpolate.interp1d(spectraPeriods,spectraDisp[accelerogram], kind = 'linear')
                setDisp.append(float(interpolator(periods[i]))*correctionFactors[i])
                                   
        demandDisp.append(setDisp)
        
    return demandDisp
    
    
def compute_Beta():

    parameters = []
    parameters.append(0.12) #Mean of Heff/Ht
    parameters.append(60)   #COV of Heff/Ht
    parameters.append(0.04) #Lower bound
    parameters.append(0.40) #Upper bound
    distribution = 'normal'
    Beta = portfolio_builder.compute_continuous_prob_value(parameters,distribution,rvs=None)

    return Beta
    

def compute_equivalent_damping(structureType,parameters):
    
    equivalentDampings=[]
    
    if structureType == 'Bare_Frame' or structureType == 'Infilled_Frame' :
        for ductility in parameters:
            equivalentDampings.append(0.05+0.565*(ductility-1)/(ductility*math.pi))

    if structureType == 'Frame_Wall':
        Beta = compute_Beta()
        for ductility in parameters:
            Ew = 0.05+0.444*(ductility-1)/(ductility*math.pi)
            Ef = 0.05+0.565*(ductility-1)/(ductility*math.pi)
            equivalentDampings.append((Ew*Beta+Ef*(1-Beta))/Beta)
            
    if structureType == 'Masonry_Timber' or structureType == 'Masonry_Concrete':
        equivalentDampings.append(0.05)
        equivalentDampings.append(0.10)
        equivalentDampings.append(0.15)  
    
    return equivalentDampings


def compute_correction_factors(equivalentDampings):
    
    correctionFactors=[]
    for damping in equivalentDampings:
        correctionFactors.append(math.sqrt(7/(2+damping*100)))

    return correctionFactors
    
    
def compute_velValues(accValues,accStep):
    
    velValues = []
    velValues.append(0)
    for i in range(len(accValues)-1):
        velValues.append((velValues[i]+(accValues[i]*9.81+accValues[i+1]*9.81)*accStep*0.5))
    
    return velValues
        
    
def compute_imls_damage_states(elasticPeriods,ACCELEROGRAMS,IMTs,IMTVALUES):
    
    accs = [x for x in os.listdir(ACCELEROGRAMS) if x.upper()[-4:] == '.AT2']
    numberAccs=len(accs)
    meanPeriod = numpy.mean(elasticPeriods)
    print meanPeriod
    IMLs=[]
    
    if os.path.exists(IMTVALUES):
        imtValues=parse_IMT_values(IMTVALUES)
    
    for accelerogram in range(numberAccs):
        print accs[accelerogram]
        setIMLs = []
        position = -1
        
        accValues = []
        timeHistories = parse_at2_acc(ACCELEROGRAMS+accs[accelerogram])
        for i in range(len(timeHistories)):
            accValues.append(timeHistories[i][1])
            accStep=timeHistories[2][0]-timeHistories[1][0]   
        
        if os.path.exists(IMTVALUES):
            for i in range(len(imtValues)):
                if imtValues[i][0] == accs[accelerogram]:
                    position = i
        
        if position >= 0:
            for j in range(3):
                setIMLs.append(float(imtValues[position][j+1]))
        else:    
        
            for IMT in IMTs:

                if IMT == 'PGA':
                    setIMLs.append(max([max(accValues) ,math.fabs(min(accValues))]))
                    
                if IMT == 'PGV':
                    velValues=compute_velValues(accValues,accStep)
                    setIMLs.append(max([max(velValues) , math.fabs(min(velValues))]))
            
                if IMT =='Sa03':
                    setIMLs.append(spec_newmark.compute_disp(accValues, accStep, 0.3, 0.05)[1])  
      
        setIMLs.append(spec_newmark.compute_disp(accValues, accStep,meanPeriod,0.05)[1])                

        IMLs.append(setIMLs)
    
    save_imlValues(IMTVALUES,accs,IMLs)
    
    return IMLs
    
    
def save_imlValues(IMTVALUES,accs,IMLs):
    
    out_file = open(IMTVALUES,"w")
    for i in range(len(accs)):
        out_file.write(accs[i]+','+str(IMLs[i][0])+','+str(IMLs[i][1])+','+str(IMLs[i][2])+'\n')
    out_file.close()

    
def parse_IMT_values(path):
    
    file=open(path)
    lines=file.readlines()
    file.close
    imtValues=[]
    for line in lines:
        imtValues.append( [line.split(',')[0], line.split(',')[1], line.split(',')[2], line.strip('\n').split(',')[3]])

    return imtValues

    
    
