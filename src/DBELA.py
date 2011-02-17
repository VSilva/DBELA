EXPOSURE2 = '/Users/vitorsilva/Documents/PhD/DBELA/data/input.txt'
EXPOSURE = '/Users/vitorsilva/Documents/PhD/DBELA/data/parameters_porfolio.txt'

import numpy
from scipy import stats
from scipy import sqrt
from scipy import log
import math
import portfolio_builder
import dbela_calculations


lines = portfolio_builder.parse_input(EXPOSURE)
assets_count = portfolio_builder.buildings_counter(lines)
number_categories = int(assets_count[0])
number_assets = assets_count[1]
print(lines[0])

for asset_category in range(number_categories):
	for asset in range(number_assets[asset_category]):
	
		data = portfolio_builder.create_asset(lines, asset_category)
		code=data[0]
		steel_modulos=float(data[1])
		steel_yield=float(data[2])
		height_up=float(data[3])
		height_gf=float(data[4])
		column_length=float(data[5])
		column_depth=float(data[6])
		beam_length=float(data[7])
		beam_depth=float(data[8])
		number_storeys=int(data[9])
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
	
		collapse_type = dbela_calculations.compute_collapse_type(height_up,height_gf,beam_length,beam_depth,column_depth,number_storeys)
		
		height = dbela_calculations.compute_height(height_up,height_gf,number_storeys)	
		
		if collapse_type == "Beam Sway":
			efh = dbela_calculations.compute_bs_efh(number_storeys)	
			ductilities = dbela_calculations.compute_bs_ductility(es_ls2,es_ls3,ec_ls2,ec_ls3,ey,beam_length,beam_depth)
			periods = dbela_calculations.compute_periods(height,ductilities)
			displacements = dbela_calculations.compute_bs_disps(efh,height,ey,es_ls2,es_ls3,ec_ls2,ec_ls3,beam_depth,beam_length)
		
		elif collapse_type == "Column Sway":	
			efh = dbela_calculations.compute_cs_efh(steel_modulos,steel_yield,es_ls2,es_ls3,ey)	
	 		ductilities = dbela_calculations.compute_cs_ductility(es_ls2,es_ls3,ec_ls2,ec_ls3,ey,column_depth,height,efh)
			periods = dbela_calculations.compute_periods(height,ductilities)
			displacements = dbela_calculations.compute_cs_disps(efh,height,ey,es_ls2,es_ls3,ec_ls2,ec_ls3,height_up,height_gf,column_depth)
		
		else:
			raise RuntimeError("unknown collapse type %s" % collapse_type)
		
		print(collapse_type)	
		print(height)		
		print(efh)
		print(ductilities)
		print(periods)
		print(displacements)
	
	

	
	
	