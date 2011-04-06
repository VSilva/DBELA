ACCELEROGRAMS = '/Users/vitorsilva/Documents/PhD/DBELA/data/accelerograms/'
SPECTRA= '/Users/vitorsilva/Documents/PhD/DBELA/data/spectra/'
EXPOSURE = '/Users/vitorsilva/Documents/PhD/DBELA/data/parameters_porfolio.txt'
IMTVALUES= '/Users/vitorsilva/Documents/PhD/DBELA/data/imtvalues.txt'

import numpy
from scipy import stats
from scipy import sqrt
from scipy import log
from numpy import numarray
import math
import portfolio_builder
import capacity_calculations
import demand_calculations
import damage_allocator

# COMPUTE THE SPECTRA BASED ON A SET OF ACCELEROGRAMS

minPeriod = 0.1
maxPeriod = 7
step = 0.02
damping = 0.05
spectraPeriods = demand_calculations.compute_spectra_periods(minPeriod,maxPeriod,step)
spectraDisp = demand_calculations.compute_spectra(minPeriod,maxPeriod,step,damping,ACCELEROGRAMS,SPECTRA)
print 'Spectra produced'

# READ THE PORFOLIO OF BUILDINGS
lines = portfolio_builder.parse_input(EXPOSURE)
assets_count = portfolio_builder.buildings_counter(lines)
number_categories = int(assets_count[0])
number_assets = assets_count[1]

# CREATE THE VECTOR DOR THE DAMAGE STATES

damageStates= numarray.zeros(4)
IMTs=['PGA','PGV','Sa03','Sa10','Sd03','Saelastic']
elasticPeriods = []

# COMPUTE THE DISPLACAMENT FOR EACH BUILDING
for asset_category in range(number_categories):
    for asset in range(number_assets[asset_category]):
    
        data = portfolio_builder.create_asset(lines[asset_category])
        structureType=data[0]
        code=data[1]
        steel_modulos=float(data[2])
        steel_yield=float(data[3])
        height_up=float(data[4])
        height_gf=float(data[5])
        column_length=float(data[6])
        column_depth=float(data[7])
        beam_length=float(data[8])
        beam_depth=float(data[9])
        number_storeys=int(data[10])
        ey = steel_yield/steel_modulos
        
        if code == "low_code":
            ec_ls2 = 0.0035
            ec_ls3 = 0.0075
            es_ls2 = 0.0150
            es_ls3 = 0.0350
        
        if code == "high_code":
            ec_ls2 = 0.0035
            ec_ls3 = 0.0150
            es_ls2 = 0.0150
            es_ls3 = 0.0500 
    
        collapse_type = capacity_calculations.compute_collapse_type(height_up,height_gf,beam_length,beam_depth,column_depth,number_storeys)
        
        height = capacity_calculations.compute_height(height_up,height_gf,number_storeys)   
        
        if collapse_type == "Beam Sway":
            efh = capacity_calculations.compute_bs_efh(number_storeys)  
            ductilities = capacity_calculations.compute_bs_ductility(es_ls2,es_ls3,ec_ls2,ec_ls3,ey,beam_length,beam_depth)
            periods = capacity_calculations.compute_periods(height,ductilities)
            capacityDisp = capacity_calculations.compute_bs_disps(efh,height,ey,es_ls2,es_ls3,ec_ls2,ec_ls3,beam_depth,beam_length,number_storeys)
        
        elif collapse_type == "Column Sway":    
            efh = capacity_calculations.compute_cs_efh(steel_modulos,steel_yield,es_ls2,es_ls3,ey)  
            ductilities = capacity_calculations.compute_cs_ductility(es_ls2,es_ls3,ec_ls2,ec_ls3,ey,column_depth,height,efh)
            periods = capacity_calculations.compute_periods(height,ductilities)
            capacityDisp = capacity_calculations.compute_cs_disps(efh,height,ey,es_ls2,es_ls3,ec_ls2,ec_ls3,height_up,height_gf,column_depth,number_storeys)
        
        else:
            raise RuntimeError("unknown collapse type %s" % collapse_type)
        
        elasticPeriods.append(periods[0])           
        demandDisp = demand_calculations.compute_demand_displacement(periods,spectraDisp,spectraPeriods,damping,ACCELEROGRAMS,structureType,ductilities)
        DSpositions = damage_allocator.damage_state_position(capacityDisp, demandDisp)

        damageStates=damageStates+DSpositions
        
# Compute the imls for each accelerogram    
imlDamageStates = demand_calculations.compute_imls_damage_states(elasticPeriods,ACCELEROGRAMS,IMTs,IMTVALUES)
damage_allocator.print_results(damageStates,imlDamageStates)


