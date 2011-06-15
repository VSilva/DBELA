ACCELEROGRAMS = '/Users/vitorsilva/Documents/PhD/DBELA/data/accelerograms/'
EXPOSURE = '/Users/vitorsilva/Documents/PhD/DBELA/data/parameters_porfolio.txt'

import numpy
import unittest
from scipy import stats
from scipy import sqrt
from scipy import log
from numpy import numarray
import math
import portfolio_builder
import capacity_calculations
import demand_calculations
import damage_allocator
import fit_curve
import os

class ReadPortfolioBuildings(unittest.TestCase):

    def setUp(self):
        print 'test 1'
        self.exposure_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/parameters_porfolio_sample.txt'

    def test_parse_portfolio(self):
        lines = portfolio_builder.parse_input(self.exposure_path)
        parameters = portfolio_builder.buildings_counter(lines)
        number_categories = parameters[0]
        number_assets = parameters[1]
        self.assertEqual(number_categories, 2)
        self.assertEqual(number_assets, [7, 4])      

class CreateAsset(unittest.TestCase):

    def setUp(self):
        print 'test 2'
        self.line = '34.057	-118.238	Bare_Frame	Low_Code	7	3	210000	5	normal	371.13	24	normal	2.84	8	normal	3	10	normal	0.45	12	0.3	0.6	normal	3.37	38	gamma	0.30-0.36-0.42-0.48-0.54-0.60 0.596-0.242-0.099-0.040-0.016-0.007	0	0	discrete'

    def test_create_asset(self):
        
        def stub_rvs(alpha,scale = None):
            return 1
           
        data = portfolio_builder.create_asset(self.line, rvs=stub_rvs)
        print data
        
        # data 0 - structure type
        # data 1 - code level
        # data 2 - steel strain
        # data 3 - steel strengh
        # data 4 - Upper floor height
        # data 5 - Ground/upper floor height ratio	
        # data 6 - Column depth
        # data 7 - Beam length
        # data 8 - Beam depth  
        # data 9 - number of storeys
        
        steel_modulos=float(data[2])
        steel_strength=float(data[3])
        height_up=float(data[4])
        height_gf=float(data[5])
        column_depth=float(data[6])
        beam_length=float(data[7])
        beam_depth=float(data[8])
        number_storeys=float(data[9])
        
        self.assertEqual(data[0],'Bare_Frame')
        self.assertEqual(data[1],'Low_Code')
        self.assertEqual(int(data[2]),1)
        self.assertEqual(int(data[3]),1)
        self.assertEqual(int(data[4]),1)
        self.assertEqual(int(data[5]),1)
        self.assertEqual(int(data[6]),1)
        self.assertEqual(int(data[7]),1)
        self.assertEqual(int(data[9]),3)

class Compute_collapse_type(unittest.TestCase):        
        
    def test_compute_collapse_type(self):
        print 'test 3'
        collapse_type_cs = capacity_calculations.compute_collapse_type(3,4.5,6,0.7,0.28,2)
        collapse_type_bs = capacity_calculations.compute_collapse_type(3,4.5,6,0.7,0.4,4)   
        self.assertEqual(collapse_type_cs,'Column Sway')
        self.assertEqual(collapse_type_bs,'Beam Sway')      

class Compute_effective_height(unittest.TestCase):
    
    def test_compute_effective_height(self):
        print 'test 4'
        efh_cs = capacity_calculations.compute_cs_efh(200000,462,0.015,0.035,0.00231)
        efh_bs = capacity_calculations.compute_bs_efh(9)
        self.assertEqual(efh_bs,0.5775)
        self.assertTrue(numpy.allclose([0.6700,0.52618,0.51122],efh_cs))

class Compute_effective_height(unittest.TestCase):

    def test_compute_height(self):
        print 'test 5'
        height = capacity_calculations.compute_height(3.0,4.5,9)
        self.assertTrue(numpy.allclose(height,28.5))   
       
class Compute_ductility(unittest.TestCase):

    def test_compute_ductility(self):
        print 'test 6'
        ductility_bs = capacity_calculations.compute_bs_ductility(0.015,0.035,0.0035,0.0075,0.00231,6.0,0.75)
        ductility_cs = capacity_calculations.compute_cs_ductility(0.015,0.035,0.0035,0.0075,0.00231,0.6,28.5,[0.6700,0.52618,0.51122])
        self.assertTrue(numpy.allclose(ductility_bs,[1.0,1.78858,3.08728]))
        self.assertTrue(numpy.allclose(ductility_cs,[1.0,1.27303,1.77853]))  

  
class Compute_periods(unittest.TestCase):

    def test_compute_periods(self):
        print 'test 7'
        periods = capacity_calculations.compute_periods(28.5,[1.0,1.78858,3.08728],'Bare_Frame')
        self.assertTrue(numpy.allclose(periods,[2.85000,3.81153,5.00764]))  
    
class Compute_displacements(unittest.TestCase):

    def test_compute_displcaments(self):
        print 'test 8'
        disp_cs = capacity_calculations.compute_cs_disps([0.6700,0.52618,0.51122],28.5,0.00231,0.015,0.035,0.0035,0.0075,3.0,4.5,0.6,9,'Bare_Frame',[0,0,0])
        disp_bs = capacity_calculations.compute_bs_disps(0.5775,28.5,0.00231,0.015,0.035,0.0035,0.0075,0.75,6,'Bare_Frame',[0,0,0])
        self.assertTrue(numpy.allclose(disp_cs,[0.10010395,0.10911831,0.16088316]))
        self.assertTrue(numpy.allclose(disp_bs,[0.15207885,0.27200553,0.46951053])) 
          
class ParseAT2accelerogram(unittest.TestCase):

    def setUp(self):
        print 'test 9'
        self.acc_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/MCF000.AT2'
        
    def test_parse_at2_acc(self):
        accelerogram = demand_calculations.parse_at2_acc(self.acc_path)
        self.assertEqual(accelerogram[4], [0.020,-.3841249E-04]) 

class Parse_accelerogram(unittest.TestCase):

    def setUp(self):
        print 'test 10'
        self.acc_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/sakaria.txt'

    def test_parse_acc(self):
        accelerogram = demand_calculations.parse_acc(self.acc_path)
        self.assertEqual(accelerogram[4], [0.040,-0.009])

class Parse_save_spectrum(unittest.TestCase):

    def setUp(self):
        print 'test 11'
        self.spec_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/MCF000-0.1-7-0.02.txt'
        self.spectra_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/'
        
    def test_parse_save_spectrum(self):
        self.spectrum = demand_calculations.parse_spectrum(self.spec_path)
        demand_calculations.save_spectrum(0.1,7,0.02,self.spectrum,self.spectra_path,'test.txt')
        self.assertTrue(numpy.allclose(self.spectrum[4],0.00351506719458))
        self.assertTrue(os.path.exists(self.spectra_path + 'test.txt'))
        
    def tearDown(self):
        os.remove(self.spectra_path + 'test.txt')      
        
class Compute_load_spectra(unittest.TestCase):        
        
    def setUp(self):
        print 'test 12'
        self.accs_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/accelerograms/'
        self.spectra_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/spectra/'
           
    def test_compute_spectra(self):            
        spectra=demand_calculations.compute_spectra(1.0,2.0,0.5,0.05,self.accs_path,self.spectra_path)
        self.assertEqual(len(spectra),3)
    
    def tearDown(self):
        os.remove(self.spectra_path + '189042-1.0-2.0-0.5.txt')
        os.remove(self.spectra_path + '189132-1.0-2.0-0.5.txt')
 
            
class Save_spectrum(unittest.TestCase):
 
    def setUp(self): 
        print 'test 13'
        self.accs_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/accelerograms/'
        self.spectra_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/spectra/'
        
class Compute_spectra_periods(unittest.TestCase):

    def test_compute_periods(self):
        print 'test 14'
        periods = demand_calculations.compute_spectra_periods(1.0,2.0,0.5)
        self.assertTrue(numpy.allclose(periods[0],1.0))     
        self.assertTrue(numpy.allclose(periods[1],1.5))           
        self.assertTrue(numpy.allclose(periods[2],2.0))           

class Compute_demand_parameters(unittest.TestCase):
    
    def test_compute_equivalent_damping(self):  
        print 'test 15' 
        equivalent_dampings_bf = demand_calculations.compute_equivalent_damping('Bare_Frame',[1, 2, 3])
        equivalent_dampings_wf = demand_calculations.compute_equivalent_damping('Wall_Frame',[1, 2, 3])
        self.assertTrue(numpy.allclose(equivalent_dampings_bf,[0.0500000,0.1399225,0.1698967]))     
        self.assertTrue(numpy.allclose(equivalent_dampings_wf,[0.0500000,0.1206648,0.1442197]))        
                
    def test_compute_correction_factor(self):   
        correction_factores = demand_calculations.compute_correction_factors([0.0500000,0.1399225,0.1698967])
        self.assertTrue(numpy.allclose(correction_factores,[1.847872871,1.808631095,1.796095761]))  
        
    def test_velocity_values(self):
        velValues = demand_calculations.compute_velValues([0.1,0.2,-0.15,0.1],0.1)
        self.assertTrue(numpy.allclose(velValues,[0.00,0.14715,0.171675,0.14715]))
 
    
class Compute_parse_save_imls_damage(unittest.TestCase):   
         
    def setUp(self):   
        print 'test 16'
        self.accs_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/accelerograms/'
        self.imlsValues_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/imtvalues.txt'
        self.IMTs = ['PGA','PGV','Sa03','Sa10','Sd03','Saelastic'] 
    
    def test_parse_imlVales(self):
        imlValues = demand_calculations.parse_IMT_values(self.imlsValues_path)
        self.assertEqual(imlValues[0],['189042.AT2','0.0266941','1.39846','0.0445457799089','0.0169756639973'])
        self.assertEqual(imlValues[1],['189132.AT2','0.0338434','1.583016','0.052076062532','0.0441556915751'])
    
    def test_compute_save_imlVales(self):
        IMLs = demand_calculations.compute_imls_damage_states([1],self.accs_path,self.IMTs,self.imlsValues_path)
        self.assertTrue(numpy.allclose(IMLs[0],[0.0266941,1.39846,0.0445457799089,0.0169756639973]))
        self.assertTrue(numpy.allclose(IMLs[2],[0.1264644,0.06819,0.2304,0.0847],atol=0.001))
            
    def tearDown(self):
        out_file = open(self.imlsValues_path,"w")
        out_file.write('189042.AT2,0.0266941,1.39846,0.0445457799089,0.0169756639973\n189132.AT2,0.0338434,1.583016,0.052076062532,0.0441556915751')
        out_file.close()


class compute_demand_displacement(unittest.TestCase):   

    def setUp(self):
        print 'test 17' 
        self.accs_path = '/Users/vitorsilva/Documents/PhD/DBELA/tests/test_data/accelerograms/'
    
    def test_compute_demand_disp(self):
        disp = demand_calculations.compute_demand_displacement([1.5,2.0,3.0],[[0.5,1.5],[1.5,2.5],[2.5,3.5]],[1.5,2.5],0.05,self.accs_path,'Bare_Frame',[1,2,3])
        self.assertTrue(numpy.allclose(disp[0][0],0.5*1.8478728707195915))
        self.assertTrue(numpy.allclose(disp[2][2],0.0549817*1.7960957613183324,atol=0.001))             
        
class compute_damage_states_position(unittest.TestCase): 
    
    def test_DS1_DS2(self):   
        print 'test 18' 
        pos = damage_allocator.damage_state_position([1,2,3], [[0.5,1,4],[1.5,1.8,4]])
        self.assertTrue(numpy.allclose(pos,[[1,0,0,0],[0,1,0,0]]))
        
    def test_DS2(self):   
       pos = damage_allocator.damage_state_position([1,2,3], [[1.5,2.5,2.8],[1.5,2.5,4]])
       self.assertTrue(numpy.allclose(pos,[[0,0,1,0],[0,0,0,1]])) 
 
class compute_truncated_random_values(unittest.TestCase):
    
    def setUp(self):
        print 'test 18' 
        self.par_normal = [0.6, 25, 0.5, 0.7]
        self.dist_normal ='normal'
        self.par_lognormal = [0.6, 25, 0.5, 0.7]
        self.dist_lognormal ='lognormal'
        self.par_gamma = [0.6, 25, 0.5, 0.7]
        self.dist_gamma ='gamma'
    
    def test_compute_random_value(self):
        normal = 'true'
        lognormal = 'true'
        gamma = 'true'
        
        for i in range(10):
            normal_result=portfolio_builder.compute_continuous_prob_value(self.par_normal, self.dist_normal, None)
            lognormal_result=portfolio_builder.compute_continuous_prob_value(self.par_lognormal, self.dist_lognormal, None)
            gamma_result=portfolio_builder.compute_continuous_prob_value(self.par_gamma, self.dist_gamma, None)
            
            if normal_result > self.par_normal[3] or normal_result < self.par_normal[2]:
                normal = 'false'

            if lognormal_result > self.par_lognormal[3] or lognormal_result < self.par_lognormal[2]:
                lognormal = 'false'
                
            if gamma_result > self.par_gamma[3] or gamma_result < self.par_gamma[2]:
                gamma = 'false'

        self.assertEqual(normal,'true')
        self.assertEqual(lognormal,'true')
        self.assertEqual(gamma,'true')


class Process_results(unittest.TestCase):

    def setUp(self):
        print 'test 20'
        self.damageStates = numpy.array([[7 , 0 , 0 ,0],[2 , 2, 3, 0],[0, 0, 5, 2],[1, 1, 1, 4]], dtype=float)
        self.imlDamageStates = numpy.array([[0.026, 1.398, 0.044, 0.016], [0.034, 1.583, 0.052, 0.044], [0.088, 2.672, 0.179, 0.155], [0.075, 2.465, 0.243, 0.124]], dtype=float)
        self.PEs = [0.0, 0.0, 0.0, 0.0, 0.014, 0.088, 0.253, 0.471, 0.671, 0.816, 0.905, 0.954, 0.979, 0.990, 0.996, 0.998, 1.0, 1.0, 1.0, 1.0]
        self.IMLs = [0.010,	0.036,	0.062,	0.087,	0.113,	0.139,	0.165,	0.191,	0.216,	0.242,	0.268,	0.294,	0.319,	0.345,	0.371,	0.397,	0.423,	0.448,	0.474,	0.500]
        
    def test_extract_PO_first_DS(self): 
        POs_first = fit_curve.extract_POs(self.damageStates,0)
        self.assertEqual(POs_first,[1.0, 0.2857142857142857, 0.0, 0.14285714285714285])
        
    def test_extract_PO_last_DS(self): 
        POs_last = fit_curve.extract_POs(self.damageStates,3)
        self.assertEqual(POs_last,[0.0, 0.0, 0.2857142857142857, 0.5714285714285714])
        
    def test_extract_PE_first_LS(self):
        PEs_first = fit_curve.extract_PEs(self.damageStates,0)
        print PEs_first
        self.assertEqual(PEs_first,[0.0, 0.71428571428571419, 1.0, 0.8571428571428571]) 
          
    def test_extract_SaElastic(self): 
        IMLs=fit_curve.extract_IMLs(self.imlDamageStates,'Saelastic')
        self.assertEqual(IMLs,[0.016, 0.044, 0.155, 0.124])        

    def test_compute_first_solution(self):
        parameters=fit_curve.compute_first_approach(self.PEs,self.IMLs)
        print parameters[0]
        print parameters[1]
        self.assertTrue(numpy.allclose(parameters[0],-1.7028,atol=0.0001)) 
        self.assertTrue(numpy.allclose(parameters[1], 0.2388,atol=0.0001)) 


class compute_truncated_random_values(unittest.TestCase):

    def setUp(self):
        print 'test 19' 
        self.par_discrete = ['0.30-0.36-0.42-0.48-0.54-0.60', '0.596-0.242-0.099-0.040-0.016-0.007', '0', '0']
        self.dist_discrete ='discrete'
        
    def test_compute_random_value(self):
        discrete_result=portfolio_builder.compute_discrete_prob_value(self.par_discrete)
        
        
if __name__ == "__main__":
    unittest.main()

