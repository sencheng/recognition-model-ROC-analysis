"""
This method provides routines for performing memory tests and saving the results
"""
import numpy as np
import copy
from utils.save_load import save_average,save_data

def memory_test(params,mem_systems,row,col):
    
     """
     Run memory test for a given number of trials and average the results
   
     Parameters
     --------------------------
    
     params : class instance
            contains simulation parameters
    
     mem_systems : list of class instances
                 contains memory systems with different pattern separation values
                 
     comb : list of class instances
          contains memory systems combining the system with no pattern separation with the ones having different pattern separation values
     
     row,col : int 
         the row and column of the dataframe to store data to. Typically, row represents offset and col the noise level
     
     """
     
     import memory.test_types as test
     import Input.patterns as inp
     
     data = np.zeros(((params.hip+1),params.trials)).tolist()
         
     for t in range(params.trials):
         # load the stimuli
         input_patterns = inp.probes(params)
         input_patterns.probe_faces(seed=t)
         input_patterns.probe_assignment() 
         params.d_pattern = np.shape(input_patterns.test)[-1] # ignore

         # perform scaling
         [mem_sys.perform_scaling(input_patterns.study_all, 'study') for mem_sys in mem_systems]
         [mem_sys.perform_scaling(input_patterns.test, 'test') for mem_sys in mem_systems]

         for m,mem in enumerate(mem_systems):
             mem.target_memory = []
             mem.item_retrieval(col)
             test.roc_test(mem)
             data[m][t] = [copy.deepcopy(mem.retrieved), copy.deepcopy(mem.performance)]
                                 
     for m,mem in enumerate(mem_systems):  
        save_average(mem.dataFrame,data[m],row,col) # average the data over all trials
        if row == params.offset[-1] and col == params.noise[-1]:
           save_data(mem.dataFrame,str(params.list_length)+'-'+str(mem.scale),'pkl', folder=params.data_dir)
           
     return data    

def memory_test_basic(params,mem_system,row,col):
    
    """
     Run memory test for a given number of trials and average the results, a simplified version of memory_test
   
     Parameters
     --------------------------
    
     params : class instance
            contains simulation parameters
    
     mem_systems : list of class instances
                 contains memory systems with different pattern separation values
                      
     row,col : int 
         the row and column of the dataframe to store data to. Typically, row represents offset and col the noise level
     
    
     """

    import memory.test_types as test
    data = np.zeros((1,params.trials)).tolist()[0]
    for t in range(params.trials):
        mem_system.item_retrieval(col)
        test.roc_test(mem_system)
        data[t] = [copy.deepcopy(mem_system.retrieved), copy.deepcopy(mem_system.performance)]
    save_average(mem_system.dataFrame,data,row,col) # average the data over all trials
    if col == params.noise[-1]:
        save_data(mem_system.dataFrame,str(params.list_length)+'-'+str(mem_system.scale),'pkl', folder=params.data_dir)
