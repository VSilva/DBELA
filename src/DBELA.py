EXPOSURE2 = '/Users/vitorsilva/Documents/GEM/openquake/tests/data/input.txt'
EXPOSURE = '/Users/vitorsilva/Documents/GEM/openquake/tests/data/Parameters_porfolio.txt'

#Limit States need to be defined depending on the level od code

import numpy
import scipy
import math
import portfolio_builder
import dbela_calculations

lines = portfolio_builder.parse_input(EXPOSURE)
assets_count = portfolio_builder.buildings_counter(lines)
print(assets_count)
number_categories = int(assets_count[0])
number_assets = assets_count[1]


for asset_category in range(number_categories):
	for asset in range(number_assets[asset_category]):
	
		data = portfolio_builder.create_asset(lines, asset_category)
		print(asset)
		code=data[0]
		steel_modulos=float(data[1])
		steel_yield=float(data[2])
		height_up=float(data[3])
		height_gf=float(data[4])
		beam_length=float(data[5])
		beam_depth=float(data[6])
		column_depth=float(data[7])
		number_storeys=int(data[8])
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

#TODO - The above values also need to follow a probabilistic distribution but I'm not quite which. Talk to Naveed!
	
		collapse_type = dbela_calculations.compute_collapse_type(height_up,height_gf,beam_length,beam_depth,column_depth,number_storeys)
		print(collapse_type)
		
		height = dbela_calculations.compute_height(height_up,height_gf,number_storeys)
		print(height)	
		
		if collapse_type == "Beam Sway":
			efh = dbela_calculations.compute_bs_efh(number_storeys)	
			ductilities = dbela_calculations.compute_bs_ductility(es_ls2,es_ls3,ec_ls2,ec_ls3,ey,beam_length,beam_depth)
			periods = dbela_calculations.compute_periods(height,ductilities)
			displacements = dbela_calculations.compute_bs_disps(efh,height,ey,es_ls2,es_ls3,ec_ls2,ec_ls3,beam_depth,beam_length)
		
		if collapse_type == "Column Sway":	
			efh = dbela_calculations.compute_cs_efh(steel_modulos,steel_yield,es_ls2,es_ls3,ey)	
	 		ductilities = dbela_calculations.compute_cs_ductility(es_ls2,es_ls3,ec_ls2,ec_ls3,ey,column_depth,height,efh)
			periods = dbela_calculations.compute_periods(height,ductilities)
			displacements = dbela_calculations.compute_cs_disps(efh,height,ey,es_ls2,es_ls3,ec_ls2,ec_ls3,height_up,height_gf,column_depth)

#	print(collapse_type)	
#	print(height)		
#	print(efh)
#	print(ductilities)
#	print(periods)
#	print(displacements)
	
	

	
	
	