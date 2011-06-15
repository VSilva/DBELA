"""
This script contains the calculations required for a DBELA. The portfolio is generated somewhere else.
"""

import linecache
import numpy
import math


def parse_input(path,ith):
    
    line = linecache.getline(path, ith)
        
    return line  
    
def compute_collapse_type(height_up,height_gf,beam_length,beam_depth,column_depth,number_storeys):
    
    r_gf = (beam_depth/beam_length)/(column_depth/height_gf)
    r_uf = 0
    
    if number_storeys > 1:
        r_uf=(beam_depth/beam_length)/(column_depth/height_up)
    
    if max(r_gf, r_uf) > 1.5:
        collapse_type = 'Column Sway'
        
    if max(r_gf, r_uf) <= 1.5:
        collapse_type = 'Beam Sway'
    
    return collapse_type
    
    
def compute_bs_efh(number_storeys):
    
    if number_storeys <= 4:
        efh = 0.64
    
    elif number_storeys > 4 and number_storeys < 20 :
        efh = 0.64-0.0125*(number_storeys-4)
        
    elif number_storeys >= 20:
        efh = 0.44
        
    return efh
    

def compute_cs_efh(steel_modulos,steel_yield,es_ls2,es_ls3,ey):
    
    efh = []
    efh.append(0.67)
    efh.append(0.67-0.17*(es_ls2-ey)/es_ls2)
    efh.append(0.67-0.17*(es_ls3-ey)/es_ls3)

    return efh
    
    
def compute_height(height_up,height_gf,number_storeys):
    
    height = height_gf + (number_storeys-1)*height_up
    
    return height

def compute_bs_ductility(es_ls2,es_ls3,ec_ls2,ec_ls3,ey,beam_length,beam_depth,structureType,betas):
    
    ductilities = []
    
    if structureType == 'Bare_Frame':    
        ductilities.append(1.0)
        ductilities.append(1+(ec_ls2 + es_ls2 - 1.7*ey)*beam_depth/(ey*beam_length))
        ductilities.append(1+(ec_ls3 + es_ls3 - 1.7*ey)*beam_depth/(ey*beam_length))  
    
    if structureType == 'Infilled_Frame':    
        ductilities.append(1.0)
        ductilities.append(1+(ec_ls2 + es_ls2 - 1.7*ey)*beam_depth*betas[1]/(ey*beam_length))
        ductilities.append(1+(ec_ls3 + es_ls3 - 1.7*ey)*beam_depth*betas[2]/(ey*beam_length))  
      
    
    return ductilities
    

def compute_cs_ductility(es_ls2,es_ls3,ec_ls2,ec_ls3,ey,column_depth,height,efh,structureType,betas):

    ductilities = []
    
    if structureType == 'Bare_Frame':
        ductilities.append(1.0)
        ductilities.append(1.0+(ec_ls2 + es_ls2 - 2.14*ey)*column_depth/(0.86*efh[1]*height*ey))
        ductilities.append(1.0+(ec_ls3 + es_ls3 - 2.14*ey)*column_depth/(0.86*efh[2]*height*ey))

    if structureType == 'Infilled_Frame':
        ductilities.append(1.0)
        ductilities.append(1.0+(ec_ls2 + es_ls2 - 2.14*ey)*column_depth*betas[1]/(0.86*efh[1]*height*ey))
        ductilities.append(1.0+(ec_ls3 + es_ls3 - 2.14*ey)*column_depth*betas[2]/(0.86*efh[2]*height*ey))


    return ductilities
    
    
def compute_periods(height,ductilities,structureType):
    
    periods = []
    if structureType == 'Bare_Frame':
        periods.append(0.1*height)
    
    if structureType == 'Infilled_Frame':
        periods.append(0.055*height)
    
    periods.append(periods[0]*math.sqrt(ductilities[1]))
    periods.append(periods[0]*math.sqrt(ductilities[2]))
            
    return periods

def compute_cs_disps(efh,height,ey,es_ls2,es_ls3,ec_ls2,ec_ls3,height_up,height_gf,column_depth,number_storeys,structureType,betas):
    
    column_height = (height_gf+(number_storeys-1)*height_up)/number_storeys
    displacements = []  
    
    if structureType == 'Bare_Frame':
        displacements.append(0.43*efh[0]*height*ey*column_height/column_depth)
        displacements.append(0.43*efh[1]*height*ey*column_height/column_depth+0.5*(ec_ls2+es_ls2-2.14*ey)*height_gf)
        displacements.append(0.43*efh[2]*height*ey*column_height/column_depth+0.5*(ec_ls3+es_ls3-2.14*ey)*height_gf)
    
    if structureType == 'Infilled_Frame':
        displacements.append(0.43*efh[0]*height*ey*column_height/column_depth*betas[0])
        displacements.append(0.43*efh[1]*height*ey*column_height/column_depth*betas[0]+0.5*(ec_ls2+es_ls2-2.14*ey)*height_gf*betas[1])
        displacements.append(0.43*efh[2]*height*ey*column_height/column_depth*betas[0]+0.5*(ec_ls3+es_ls3-2.14*ey)*height_gf*betas[2])
                
    return displacements
    
def compute_bs_disps(efh,height,ey,es_ls2,es_ls3,ec_ls2,ec_ls3,beam_depth,beam_length,structureType,betas):

    displacements = []  
    
    if structureType == 'Bare_Frame':
        displacements.append(0.5*efh*height*ey*beam_length/beam_depth)
        displacements.append(0.5*efh*height*ey*beam_length/beam_depth+0.5*(ec_ls2+es_ls2-1.7*ey)*efh*height)
        displacements.append(0.5*efh*height*ey*beam_length/beam_depth+0.5*(ec_ls3+es_ls3-1.7*ey)*efh*height)
    
    if structureType == 'Infilled_Frame':
        displacements.append(0.5*efh*height*ey*beam_length/beam_depth*betas[0])
        displacements.append(0.5*efh*height*ey*beam_length/beam_depth*betas[0]+0.5*(ec_ls2+es_ls2-1.7*ey)*efh*height*betas[1])
        displacements.append(0.5*efh*height*ey*beam_length/beam_depth*betas[0]+0.5*(ec_ls3+es_ls3-1.7*ey)*efh*height*betas[2]) 
                      
    return displacements

