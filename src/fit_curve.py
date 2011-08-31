import numpy
import math
from scipy.optimize import leastsq
import scipy 
from scipy import stats
from numpy import random
from scipy import linalg
from numpy import numarray
import portfolio_builder

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
    
def generate_synthetic_datasets(imlDamageStates,damageStates,numberDatasets):

    IMLs = extract_IMLs(imlDamageStates,'PGA')
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
        for j in range(int(sizeDataset)):
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
    
def compute_statistics(setIMLs,LS1PEs,LS2PEs,LS3PEs):
    
    numberDatasets = len(setIMLs)
    sizeDataset = len(setIMLs[0])
    LS1mean = []
    LS1sigma = []
    LS2mean = []
    LS2sigma = []
    LS3mean = []
    LS3sigma = []

    x1, flag = leastsq(residuals, [-2,0.6], args=(LS1PEs[0], setIMLs[0]))
    x2, flag = leastsq(residuals, [-1,0.6], args=(LS2PEs[0], setIMLs[0]))
    x3, flag = leastsq(residuals, [ 0,0.6], args=(LS3PEs[0], setIMLs[0]))
    
    for i in range(numberDatasets):
        LS1solution, flag = leastsq(residuals, x1, args=(LS1PEs[i], setIMLs[i]))
        LS2solution, flag = leastsq(residuals, x2, args=(LS2PEs[i], setIMLs[i]))
        LS3solution, flag = leastsq(residuals, x3, args=(LS3PEs[i], setIMLs[i]))
        print i
        
        LS1mean.append(LS1solution[0])
        LS1sigma.append(LS1solution[1])  
        LS2mean.append(LS2solution[0])
        LS2sigma.append(LS2solution[1])
        LS3mean.append(LS3solution[0])
        LS3sigma.append(LS3solution[1])
        
    statistics = [LS1mean,LS1sigma,LS2mean,LS2sigma,LS3mean,LS3sigma]
    correlationFactors = numpy.corrcoef(statistics)
    covarianceMatrix = numpy.cov(statistics)
        
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
    
    means=[LS1Mean_mean, LS1Mean_sigma, LS2Mean_mean, LS2Mean_sigma, LS3Mean_mean, LS3Mean_sigma]
                 
    return means, correlationFactors,covarianceMatrix 


def compute_correlation_coefficient(PEs,IMLs,solution):
    
    PEsEst =  cumulative_lognormal_model(IMLs, solution)
        
    return numpy.corrcoef(PEs, PEsEst)[0][1]
    
    
def compute_best_curves(imlDamageStates,damageStates,IMTs):
    
    for IMT in IMTs:
        IMLs = extract_IMLs(imlDamageStates,IMT)
        print IMT
        for DS in range(3):
            PEs = extract_PEs(damageStates,DS)
            x0 = [-2,0.6]
            solution, flag = leastsq(residuals, x0, args=(PEs, IMLs))
            print solution[0], solution[1], compute_correlation_coefficient(PEs,IMLs,solution)
            
    
def compute_set_mean_stddev(statistics,n):
    
    meansVector = statistics[0]
    covarianceMatrix = statistics[2]

    setMeanStddev = numpy.random.multivariate_normal(meansVector,covarianceMatrix,n)
    
    return setMeanStddev
    
def compute_vulnerability_functions(imlDamageStates, setMeanStddev, noIMLs):
    
    IMLs = extract_IMLs(imlDamageStates,'PGA')
    minIML = min(IMLs)
    maxIML = max(IMLs)
    imls = scipy.linspace(minIML, maxIML, noIMLs)
    vulFunc = []
    
    for MeanStddev in setMeanStddev:
        fragCurve = []
        condPO = []
        for i in range(0,len(MeanStddev),2):
            mu = MeanStddev[i]
            sigma = MeanStddev[i+1]
            fragCurve.append(stats.lognorm.cdf(imls,sigma, scale=scipy.exp(mu)))

        for i in range(len(MeanStddev)/2+1):
            DR = damage_ratio_provider(i)
            if i == 0:
                condPO.append((1-fragCurve[0])*DR)
            elif i == len(MeanStddev)/2:
                condPO.append((fragCurve[len(MeanStddev)/2-1])*DR)
            else:
                condPO.append((fragCurve[i-1]-fragCurve[i])*DR)
        
        vulFunc.append(sum(condPO))
    
    return imls, vulFunc
    
    
def damage_ratio_provider(damageState):
    
    #Consequence function:
    consFunc = numpy.array([[0.0001, 0.0001, 0.0001, 0.28],[5, 5, 5, 5]])
    
    parameters = []
    parameters.append(consFunc[0][damageState]) #Mean of Heff/Ht
    parameters.append(consFunc[1][damageState])   #COV of Heff/Ht
    parameters.append(0) #Lower bound
    parameters.append(2) #Upper bound
    distribution = 'normal'
    
    #damageRatio = portfolio_builder.compute_continuous_prob_value(parameters,distribution,rvs=None) 
    damageRatio = consFunc[0][damageState]
    return damageRatio
    
    
def compute_final_vulnerability_function(imls, vulFunc):
    
    setLossRatios = numpy.array(vulFunc).transpose()
    finalCurve = []
    for i in range(len(setLossRatios)):
        lossRatios = setLossRatios[i]
        expLossRatios = []
        for j in range(len(lossRatios)):
            expLossRatios.append(math.log(lossRatios[j]))
            
        mu,sigma = stats.norm.fit(expLossRatios, loc=0, scale=1)

        mean = math.exp(mu + sigma**2/2)
        stddev = math.sqrt((math.exp(sigma**2)-1)*math.exp(2*mu+sigma**2))
    
        finalCurve.append([imls[i], mean, stddev/mean])
        
    return finalCurve
    


