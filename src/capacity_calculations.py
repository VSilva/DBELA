"""
This script contains the calculations required for a DBELA. The portfolio is generated somewhere else.
"""

import linecache
import numpy
import math
import portfolio_builder


def parse_input(path,ith):
    
    line = linecache.getline(path, ith)
        
    return line  
    
def compute_collapse_type(data):
    
    structureType=data[0]
    number_storeys=data[2]
    height_up=data[5]
    height_gf=data[10]
    column_depth=data[7]
    beam_length=data[8]
    beam_depth=data[9]
      
    if structureType == 'Frame_Wall':
        collapse_type = 'Mixed Sway'
        
    else:
        r_gf = (beam_depth/beam_length)/(column_depth/height_gf)
        r_uf = 0
    
        if number_storeys > 1:
            r_uf=(beam_depth/beam_length)/(column_depth/height_up)
    
        if max(r_gf, r_uf) > 1.5:
            collapse_type = 'Column Sway'
        else:
            collapse_type = 'Beam Sway'
    
    return collapse_type
    
    
def compute_efh(data,collapse_type):
    
    structureType=data[0]
    number_storeys=data[2]    
    steel_modulos=data[3]
    steel_yield=data[4]
    ec_ls2=data[12]
    ec_ls3=data[13]
    es_ls2=data[14]
    es_ls3=data[15]
    ey = steel_yield/steel_modulos
    
    if structureType == 'Bare_Frame' or structureType == 'Infilled_Frame':
        
        if collapse_type == 'Beam Sway':
        
            if number_storeys <= 4:
                efh = 0.64
            elif number_storeys > 4 and number_storeys < 20 :
                efh = 0.64-0.0125*(number_storeys-4)
            elif number_storeys >= 20:
                efh = 0.44
            
        if collapse_type == 'Column Sway': 
            efh = []
            efh.append(0.67)
            efh.append(0.67-0.17*(es_ls2-ey)/es_ls2)
            efh.append(0.67-0.17*(es_ls3-ey)/es_ls3)
            
    if structureType == 'Frame_Wall':
        
        parameters = []
        parameters.append(0.61) #Mean of Heff/Ht
        parameters.append(11)   #COV of Heff/Ht
        parameters.append(0.5) #Lower bound
        parameters.append(0.7) #Upper bound
        distribution = 'normal'
        efh = portfolio_builder.compute_continuous_prob_value(parameters,distribution,rvs=None)
        
    return efh
    

def compute_ductility(capacityDisp):
    
    ductilities = []
    
    for i in range(len(capacityDisp)):
        ductilities.append(capacityDisp[i]/capacityDisp[0])

    return ductilities
    
    
def compute_periods(data,ductilities):
    
    structureType=data[0]
    height=data[11] 
    
    periods = []
    
    if structureType == 'Bare_Frame':
        periods.append(0.1*height)
    
    if structureType == 'Infilled_Frame':
        periods.append(0.055*height)
        
    if structureType == 'Frame_Wall':
        periods.append(0.097*height)
    
    periods.append(periods[0]*math.sqrt(ductilities[1]))
    periods.append(periods[0]*math.sqrt(ductilities[2]))
            
    return periods

   
def compute_disps(data,collapse_type,efh): 
    
    structureType=data[0]
    number_storeys=data[2]
    steel_modulos=data[3]
    steel_yield=data[4]
    height_up=data[5]
    height_gf=data[10]
    
    if structureType == 'Bare_Frame' or structureType == 'Infilled_Frame':
        column_depth=data[7]
        beam_length=data[8]
        beam_depth=data[9]
        height=data[11]
        ec_ls2=data[12]
        ec_ls3=data[13]
        es_ls2=data[14]
        es_ls3=data[15]
        betas=data[16]  
        
    if structureType == 'Frame_Wall':
        steel_ult=data[7]
        wall_length=data[8]
        rebar_diameter=data[9]
        height=data[11]
        ec_ls2=data[12]
        ec_ls3=data[13]
        es_ls2=data[14]
        es_ls3=data[15]
        betas=data[16]
    
    ey = steel_yield/steel_modulos

    displacements = [] 

    if structureType == 'Bare_Frame':
        
        if collapse_type == 'Beam Sway':
            displacements.append(0.5*efh*height*ey*beam_length/beam_depth)
            displacements.append(0.5*efh*height*ey*beam_length/beam_depth+0.5*(ec_ls2+es_ls2-1.7*ey)*efh*height)
            displacements.append(0.5*efh*height*ey*beam_length/beam_depth+0.5*(ec_ls3+es_ls3-1.7*ey)*efh*height)
                      
        if collapse_type == 'Column Sway':
            column_height = (height_gf+(number_storeys-1)*height_up)/number_storeys 
            displacements.append(0.43*efh[0]*height*ey*column_height/column_depth)
            displacements.append(0.43*efh[1]*height*ey*column_height/column_depth+0.5*(ec_ls2+es_ls2-2.14*ey)*height_gf)
            displacements.append(0.43*efh[2]*height*ey*column_height/column_depth+0.5*(ec_ls3+es_ls3-2.14*ey)*height_gf)
                        
    if structureType == 'Infilled_Frame':
            
        if collapse_type == 'Beam Sway':
            displacements.append(0.5*efh*height*ey*beam_length/beam_depth*betas[0])
            displacements.append(0.5*efh*height*ey*beam_length/beam_depth*betas[0]+0.5*(ec_ls2+es_ls2-1.7*ey)*efh*height*betas[1])
            displacements.append(0.5*efh*height*ey*beam_length/beam_depth*betas[0]+0.5*(ec_ls3+es_ls3-1.7*ey)*efh*height*betas[2])
            
        if collapse_type == 'Column Sway':
            column_height = (height_gf+(number_storeys-1)*height_up)/number_storeys      
            displacements.append(0.43*efh[0]*height*ey*column_height/column_depth*betas[0])
            displacements.append(0.43*efh[1]*height*ey*column_height/column_depth*betas[0]+0.5*(ec_ls2+es_ls2-2.14*ey)*height_gf*betas[1])
            displacements.append(0.43*efh[2]*height*ey*column_height/column_depth*betas[0]+0.5*(ec_ls3+es_ls3-2.14*ey)*height_gf*betas[2])
                        
    return displacements

