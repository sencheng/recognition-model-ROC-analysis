from utils.save_load import save_data
from utils.matlab import matlab
import memory.mem as memory
from memory.run_tests import memory_test


def run_routine(params):    
    
    """
    Runs the routine simulation
    
    Parameters
    ---------
    params : class instance
        simulation parameters
        
    """
    
    #Initialize the memory systems
    mem_systems = [memory.memory_system(params,params.scale[i]) for i in range(len(params.scale))]
    
        
    for o in range(len(params.offset)): 
        mems = []
        
        #make and store the memory modules  
        for m in range(len(params.scale)): 
            mem_sys = mem_systems[m]
            mems.append(mem_sys)
            
        #perform the memory test for different levels of memory noise
        print('Stimuli loaded, memory systems initialized')
        print('Performing the memory tests for %s trials...' %params.trials)
        for nn in params.noise:
            data = memory_test(params,mems,params.offset[o],nn)

    if  params.strength in ['MS','MW']:
        params.N_test = int(params.N_test/2)
        
    #save the information if required
    if params.matlab: # to fit the data by the Yonelinas model
       mat = matlab(params)
       mat.prepare_data()
       
    if params.save_metadata:
       folder = params.path+'/Log'
       save_data(params,'metadata_'+params.simID,file_format='pkl',folder=folder)
    return mems,data


    


