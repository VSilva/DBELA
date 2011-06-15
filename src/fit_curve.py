import numpy
import math
from scipy.optimize import leastsq
import scipy 
from scipy import stats
from numpy import random


def extract_POs(damageStates,DS):
    
    POs=[]
    totalAssets=sum(damageStates[0])
    numberAccs=len(damageStates)
    damageStates=numpy.array(damageStates)/totalAssets
    for i in range(numberAccs):
        POs.append(damageStates[i][DS])
    
    return POs

def extract_PEs(damageStates,LS):

    PEs=[]
    totalAssets=sum(damageStates[0])
    numberAccs=len(damageStates)
    cumDamageStates=numpy.zeros(numpy.array(damageStates.shape))
    damageStates=numpy.array(damageStates)/totalAssets
    for i in range(numberAccs):
        cumDamageStates[i][1]=damageStates[i][1]+damageStates[i][2]+damageStates[i][3]
        cumDamageStates[i][2]=damageStates[i][2]+damageStates[i][3]
        cumDamageStates[i][3]=damageStates[i][3]
        PEs.append(cumDamageStates[i][LS+1])

    return PEs    
    
def extract_IMLs(imlDamageStates,IMT):

    IMLs=[]
    if IMT=='PGA':
        IMTindex=0
    elif IMT=='PGV':
        IMTindex=1
    elif IMT=='Sa03':
        IMTindex=2
    elif IMT=='Saelastic':
        IMTindex=3
        
    numberAccs=len(imlDamageStates)
    
    for i in range(numberAccs):
        IMLs.append(imlDamageStates[i][IMTindex])

    return IMLs

def compute_first_approach(PEs,IMLs):

    numberAccs = len(PEs)
    LowerIMLs = []
    UpperIMLs = []
    
    for i in range(numberAccs):
        if PEs[i] < 0.2:
            LowerIMLs.append(IMLs[i]) 
        if PEs[i] > 0.8:    
            UpperIMLs.append(IMLs[i])
    
    numpy.sort(LowerIMLs)
    numpy.sort(UpperIMLs)
    n = len(LowerIMLs)
    LowerIML = numpy.mean([LowerIMLs[n-1], LowerIMLs[n-2], LowerIMLs[n-3]])
    UpperIML = numpy.mean([UpperIMLs[0], UpperIMLs[1], UpperIMLs[2]])   
 
    mu= (math.log(LowerIML)+math.log(UpperIML))/2
    sigma= abs(math.log(UpperIML)-math.log(LowerIML))/4
    
    return mu, sigma
    

def gaussian_model(IMLs,coeffs):
    return 1/(    math.sqrt(2*math.pi*abs(coeffs[0]))   )     *    numpy.exp( -   (    (IMLs-coeffs[1])**2   /   (2*coeffs[0]**2)      ))
    
def cumulative_lognormal_model(IMLs, coeffs):
    return stats.lognorm.cdf(IMLs, coeffs[1], scale=scipy.exp(coeffs[0]))

def residuals(coeffs, y, x):
    
    res = []
    for i in range(len(y)):
        res.append(y[i] - cumulative_lognormal_model(x[i], coeffs))
    return res
    
def generate_synthetic_datasets(IMLs,damageStates,numberDatasets):
    
    sizeDataset=len(IMLs)
    setIMLs = []
    LS1PEs = []
    LS2PEs = []
    LS3PEs = []
    
    allPEs=[extract_PEs(damageStates,0),extract_PEs(damageStates,1) ,extract_PEs(damageStates,2)]
            
    for i in range(numberDatasets):
        subsetIMLs=[]
        subLS1PEs=[]
        subLS2PEs=[]
        subLS3PEs=[]
        for j in range(sizeDataset):
            k = random.random_integers(0,sizeDataset-1)
            subsetIMLs.append(IMLs[k])
            subLS1PEs.append(allPEs[0][k])
            subLS2PEs.append(allPEs[1][k])
            subLS3PEs.append(allPEs[2][k])
        setIMLs.append(subsetIMLs)
        LS1PEs.append(subLS1PEs)   
        LS2PEs.append(subLS2PEs)  
        LS3PEs.append(subLS3PEs)  
    
    return setIMLs,LS1PEs,LS2PEs,LS3PEs
    
def compute_confident_intervals(setIMLs,LS1PEs,LS2PEs,LS3PEs,x0):
    
    numberDatasets = len(setIMLs)
    sizeDataset = len(setIMLs[0])
    LS1mean = []
    LS1sigma = []
    LS2mean = []
    LS2sigma = []
    LS3mean = []
    LS3sigma = []
    
    for i in range(numberDatasets):
        LS1solution, flag = leastsq(residuals, x0, args=(LS1PEs[i], setIMLs[i]))
        LS2solution, flag = leastsq(residuals, x0, args=(LS2PEs[i], setIMLs[i]))
        LS3solution, flag = leastsq(residuals, x0, args=(LS3PEs[i], setIMLs[i]))
        
        LS1mean.append(LS1solution[0])
        LS1sigma.append(LS1solution[1])  
        LS2mean.append(LS2solution[0])
        LS2sigma.append(LS2solution[1])
        LS3mean.append(LS3solution[0])
        LS3sigma.append(LS3solution[1])
    
  #  for i in range(numberDatasets):
  #      print LS1mean[i]
        
  #  for i in range(numberDatasets):
  #      print LS2mean[i]
    
  #  for i in range(numberDatasets):
  #      print LS3mean[i]
    
  #  for i in range(numberDatasets):  
  #      print LS1sigma[i]
    
  #  for i in range(numberDatasets):  
  #      print LS2sigma[i]
              
  #  for i in range(numberDatasets):  
  #      print LS3sigma[i]    
    
        
    
    statistics = [LS1mean,LS1sigma,LS2mean,LS2sigma,LS3mean,LS3sigma]
    print numpy.corrcoef(statistics)
        
    LS1Mean_mean = scipy.mean(LS1mean)
    LS1StdDev_mean = scipy.std(LS1mean,ddof=1)
    LS1Mean_sigma = scipy.mean(LS1sigma)
    LS1StdDev_sigma = scipy.std(LS1sigma,ddof=1) 
    
    LS2Mean_mean = scipy.mean(LS2mean)
    LS2StdDev_mean = scipy.std(LS2mean,ddof=1)
    LS2Mean_sigma = scipy.mean(LS2sigma)
    LS2StdDev_sigma = scipy.std(LS2sigma,ddof=1)
    
    LS3Mean_mean = scipy.mean(LS3mean)
    LS3StdDev_mean = scipy.std(LS3mean,ddof=1)
    LS3Mean_sigma = scipy.mean(LS3sigma)
    LS3StdDev_sigma = scipy.std(LS3sigma,ddof=1)
    
  #  LS1LL_mean = LS1Mean_mean-1.96*LS1StdDev_mean
  #  LS1UL_mean = LS1Mean_mean+1.96*LS1StdDev_mean 
  #  LS1LL_sigma = LS1Mean_sigma-1.96*LS1StdDev_sigma
  #  LS1UL_sigma = LS1Mean_sigma+1.96*LS1StdDev_sigma    
                 
    return LS1Mean_mean, LS1Mean_sigma, LS1StdDev_mean, LS1StdDev_sigma, LS2Mean_mean, LS2Mean_sigma, LS2StdDev_mean, LS2StdDev_sigma, LS3Mean_mean, LS3Mean_sigma, LS3StdDev_mean, LS3StdDev_sigma  

def compute_correlation_coefficient(PEs,IMLs,solution):
    
    PEsEst =  cumulative_lognormal_model(IMLs, solution)
        
    return numpy.corrcoef(PEs, PEsEst)[0][1]
    
def compute_CI(mu,sigma,n,confidenceLevel):
    
    chisq050 = 170
    chisq950 = 255
    t90 = 1.645
    
    muUL = mu - 1.645*sigma/math.sqrt(n-1)
    muLL = mu + 1.645*sigma/math.sqrt(n-1)
    sigmaLL = sigma*math.sqrt(n-1)/chisq950
    sigmaUL = sigma*math.sqrt(n-1)/chisq050
    
    return mu, sigma
    
    
#solution, flag = leastsq(residuals, x0, args=(POs, IMLs))

IMLs = [0.1 , 0.2 , 0.4 , 0.6, 1.0]
damageStates= numpy.array([[ 6. , 0. ,  1., 42.],[  4.  , 0.,   0.,  45.],[  7.,   0.,   0.,  42.],[  8.,   0.,   0.,  41.],[ 16.,   9.,   6.,  18.]])

x0=numpy.array([-2, 0.3], dtype=float)

setIMLs, LS1PEs,LS2PEs,LS3PEs  = generate_synthetic_datasets(IMLs,damageStates,2)

compute_confident_intervals(setIMLs,LS1PEs,LS2PEs,LS3PEs,x0)

