ACCELEROGRAMS = '/Users/vitorsilva/Documents/PhD/DBELA/data/accelerograms/'
SPECTRA = '/Users/vitorsilva/Documents/PhD/DBELA/data/spectra/'
EXPOSURE = '/Users/vitorsilva/Documents/PhD/DBELA/data/parameters_porfolio.txt'
IMTVALUES = '/Users/vitorsilva/Documents/PhD/DBELA/data/imtvalues.txt'
VULFUNC = '/Users/vitorsilva/Documents/PhD/DBELA/vulnerabilityfunction.txt'

import numpy
from scipy import stats
from scipy import sqrt
from scipy import log
from scipy.optimize import leastsq
from numpy import numarray
import math
import portfolio_builder
import capacity_calculations
import demand_calculations
import damage_allocator
import fit_curve

# COMPUTE THE SPECTRA BASED ON A SET OF ACCELEROGRAMS
minPeriod = 0.05
maxPeriod = 10.0
step = 0.04
damping = 0.05
spectraPeriods = demand_calculations.compute_spectra_periods(minPeriod,maxPeriod,step)
spectraDisp = demand_calculations.compute_spectra(minPeriod,maxPeriod,step,damping,ACCELEROGRAMS,SPECTRA)
numberAccs = len(spectraDisp)
print 'Spectra produced'

# READ THE PORFOLIO OF BUILDINGS
lines = portfolio_builder.parse_input(EXPOSURE)
assets_count = portfolio_builder.buildings_counter(lines)
number_categories = int(assets_count[0])
number_assets = assets_count[1]

# CREATE THE VECTOR FOR THE DAMAGE STATES AND BETA FOR INFILLED FRAMES
damageStates= numarray.zeros(4)
IMTs=['PGA','PGV','Sa03','Saelastic']
elasticPeriods = []
betas = [0.52, 0.46, 0.28] 

# COMPUTE THE DISPLACAMENT FOR EACH BUILDING
for asset_category in range(number_categories):
    for asset in range(number_assets[asset_category]):

        data = portfolio_builder.create_asset(lines[asset_category])
        code=data[1]

        if code == "Low_Code":
            ec_ls2 = 0.0035
        #    ec_ls3 = 0.0075
            es_ls2 = 0.0150
        #    es_ls3 = 0.0350
        #    ec_ls2 =  portfolio_builder.compute_continuous_prob_value([0.0035,1,0,'inf'], 'lognormal', rvs=None)
            ec_ls3 =  portfolio_builder.compute_continuous_prob_value([0.0075,30,0,'inf'], 'normal', rvs=None)
        #    es_ls2 =  portfolio_builder.compute_continuous_prob_value([0.015,2,0,'inf'], 'normal', rvs=None)
            es_ls3 =  portfolio_builder.compute_continuous_prob_value([0.035,30,0,'inf'], 'normal', rvs=None)          
        
        if code == "High_Code":
            ec_ls2 = 0.0035
            ec_ls3 = 0.020
            es_ls2 = 0.035
            es_ls3 = 0.060
        
        data.append(ec_ls2)
        data.append(ec_ls3)
        data.append(es_ls2)
        data.append(es_ls3)
        data.append(betas)
        
   #     print data
           
        collapse_type = capacity_calculations.compute_collapse_type(data)        
        collapse_type = 'Beam Sway'
        #Compute capacity displacement        
        capacityDisp = capacity_calculations.compute_disps(data,collapse_type)
        ductilities = capacity_calculations.compute_ductility(capacityDisp)           
        periods = capacity_calculations.compute_periods(data,ductilities) 
        elasticPeriods.append(periods[0])  
                 
        #Compute demand displacement
        demandDisp = demand_calculations.compute_demand_displacement(data,periods,spectraDisp,spectraPeriods,damping,ACCELEROGRAMS,ductilities)
        DSpositions = damage_allocator.damage_state_position(capacityDisp, demandDisp)
        damageStates=damageStates+DSpositions
        print capacityDisp
 #       print demandDisp
#        print ductilities
 #       print periods

# Compute the imls for each accelerogram    
imlDamageStates = demand_calculations.compute_imls_damage_states(elasticPeriods,ACCELEROGRAMS,IMTs,IMTVALUES)

# Compute the best logarithmic mean and standard deviation for each curve
fit_curve.compute_best_curves(imlDamageStates,damageStates,IMTs)          

# Compute statistics for each fragility curve
setIMLs,LS1PEs,LS2PEs,LS3PEs = fit_curve.generate_synthetic_datasets(imlDamageStates,damageStates,5)
statistics = fit_curve.compute_statistics(setIMLs,LS1PEs,LS2PEs,LS3PEs)

# Compute Vulnerability functions
                                                            
setMeanStddev = fit_curve.compute_set_mean_stddev(statistics,25)
imls, vulFunc = fit_curve.compute_vulnerability_functions(imlDamageStates, setMeanStddev,25)
finalVulFunc = fit_curve.compute_final_vulnerability_function(imls, vulFunc)
print finalVulFunc

# Extract values
damage_allocator.print_vulnerability_function_ASCII(finalVulFunc,VULFUNC)
damage_allocator.print_results(damageStates,imlDamageStates)
