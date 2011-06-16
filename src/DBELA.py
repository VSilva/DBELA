ACCELEROGRAMS = '/Users/vitorsilva/Documents/PhD/DBELA/data/accelerograms/'
SPECTRA= '/Users/vitorsilva/Documents/PhD/DBELA/data/spectra/'
EXPOSURE = '/Users/vitorsilva/Documents/PhD/DBELA/data/parameters_porfolio.txt'
IMTVALUES= '/Users/vitorsilva/Documents/PhD/DBELA/data/imtvalues.txt'

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
        print data
        structureType=data[0]
        code=data[1]
        steel_modulos=float(data[2])
        steel_yield=float(data[3])
        height_up=float(data[4])
        ratio_guf=float(data[5])
        column_depth=float(data[6])
        beam_length=float(data[7])
        beam_depth=float(data[8])
        number_storeys=int(data[9])
        ey = steel_yield/steel_modulos
        height_gf=height_up*ratio_guf

        if code == "Low_Code":
            ec_ls2 = 0.0035
            ec_ls3 = 0.0075
            es_ls2 = 0.0150
            es_ls3 = 0.0350
        
        if code == "High_Code":
            ec_ls2 = 0.0035
            ec_ls3 = 0.0150
            es_ls2 = 0.0150
            es_ls3 = 0.0500
        
        collapse_type = capacity_calculations.compute_collapse_type(structureType,height_up,height_gf,beam_length,beam_depth,column_depth,number_storeys)
        height = capacity_calculations.compute_height(height_up,height_gf,number_storeys)   
        
        #Compute capacity displacement        
        efh = capacity_calculations.compute_efh(collapse_type,number_storeys,steel_modulos,steel_yield,es_ls2,es_ls3,ey)
        ductilities = capacity_calculations.compute_ductility(collapse_type,es_ls2,es_ls3,ec_ls2,ec_ls3,ey,beam_length,column_depth,beam_depth,height,efh,structureType,betas)           
        periods = capacity_calculations.compute_periods(height,ductilities,structureType) 
        capacityDisp = capacity_calculations.compute_disps(collapse_type,efh,height,ey,es_ls2,es_ls3,ec_ls2,ec_ls3,height_gf,height_up,column_depth,number_storeys,beam_depth,beam_length,structureType,betas)
            
        elasticPeriods.append(periods[0])  
                 
        #Compute demand displacement
        demandDisp = demand_calculations.compute_demand_displacement(periods,spectraDisp,spectraPeriods,damping,ACCELEROGRAMS,structureType,ductilities)
        DSpositions = damage_allocator.damage_state_position(capacityDisp, demandDisp)

        damageStates=damageStates+DSpositions

# Compute the imls for each accelerogram    
imlDamageStates = demand_calculations.compute_imls_damage_states(elasticPeriods,ACCELEROGRAMS,IMTs,IMTVALUES)
for IMT in IMTs:
    IMLs = fit_curve.extract_IMLs(imlDamageStates,IMT)
    print IMT
    for DS in range(3):
        PEs = fit_curve.extract_PEs(damageStates,DS)
        x0 = [-2,0.6]
        solution, flag = leastsq(fit_curve.residuals, x0, args=(PEs, IMLs))
        print solution[0], solution[1], fit_curve.compute_correlation_coefficient(PEs,IMLs,solution)

#setIMLs,LS1PEs,LS2PEs,LS3PEs = fit_curve.generate_synthetic_datasets(IMLs,damageStates,100)
#Result = fit_curve.compute_confident_intervals(setIMLs,LS1PEs,LS2PEs,LS3PEs,solution)
#print Result

#damage_allocator.print_results(damageStates,imlDamageStates)


