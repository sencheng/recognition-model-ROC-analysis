# import necessary packages
from utils.set_params import sim_params
from memory import mem 
from Input import patterns as inp
from memory.run_tests import memory_test_basic
from utils.save_load import save_data
import numpy as np

# Specify desired parameters
params=sim_params()
params_change={'noise':[0.3],
               'trials':5, 'list_length':30,
               'N_thr':6,'notes':
               'awesome simulation, the params of which should be remembered'}

params.update_params(params_change)

# this is needed so that data is stored in the correct file, more relevant for the main code
params.cond = str(params.N_test)
params.data_dir = params.data_dir+params.cond+'/'

# initialize the class of inputs
input_patterns = inp.probes(params)
# load the face stimuli
probes = input_patterns.probe_faces()
# assign the stimuli to targets and lures
input_patterns.probe_assignment([-1]) 

# set the memory sysem
mem_system=mem.memory_system(params,1)
print('Memory system initialized')

mem_system.perform_scaling(input_patterns.study_all, 'study') 
mem_system.perform_scaling(input_patterns.test, 'test')

# perform the memory test for different noise levels
print('Performing recognition memory task...')
for nn in params.noise:
    memory_test_basic(params,mem_system,params.offset[0],nn)    

if params.save_metadata:
       save_data(params,'metadata_'+params.simID,file_format='pkl',folder=params.path+'/Log')
print('Done!')
