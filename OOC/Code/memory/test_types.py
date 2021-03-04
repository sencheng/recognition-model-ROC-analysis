"""
This module contains simlations of different recognition memory tests 
"""
import numpy as np
from memory import distance


def roc_test(memory):
    
    """
    Recognition test with "confidence ratings"
    The distance value between the cue and the retrieved item is mapped
    to the next threshold (=confidence rating) larger than the distance
     
    Parameters
    ------------
    
    memory: class object
         contains information about the given memory system
    """

    from utils.calculations import get_histograms
    params = memory.params

    # place the criteria based on the target strength distribution
    if params.strength in ['MS', 'MW'] and params.strong_excluded:
        thr_range = distance.set_threshold(params,np.asarray(memory.retrieved['min-distances'])[memory.test_ID]) 
    else:
        thr_range = distance.set_threshold(params,memory.retrieved['min-distances'][:memory.N]) 
   
    # test only the first half of the items for mixed conditions of the strength manipulation
    if params.strength in ['MS', 'MW']:
      test,distances_test = adjust_number(memory)
    else:
      distances_test = memory.retrieved['min-distances']
      test = memory.test
    
    # memory.test1 = test
    target,lure = np.zeros((params.N_thr)),np.zeros((params.N_thr)) # allocated for storing positive responses for each threshold

    for ind,probe in enumerate(distances_test):
      thr_ind = np.argmin([item if item>0  else np.inf for item in thr_range-probe]) # find the first threshold that the is bigger than the distance
      if ind<len(test)/2:
        target[thr_ind] += 1
      else:
        lure[thr_ind] += 1   


    memory.performance['target'] = target
    memory.performance['lure'] = lure
    
    
    # histogram the distibution for a fixed range to average the bins later. Otherwise, if the distances were stored for histogramming at the end, a lot of memory would be used
    memory.retrieved['lure-hist-freq'],memory.retrieved['lure-hist-bins'] = get_histograms(memory.retrieved['min-distances'][memory.N:],params.n_bins,0.2)
    memory.retrieved['targ-hist-freq'],memory.retrieved['targ-hist-bins'] = get_histograms(memory.retrieved['min-distances'][:memory.N],params.n_bins,0.2)
    memory.retrieved['threshold_range'] = thr_range

def adjust_number(memory):
  
    """
    Adjusts the number of targets and lures to be used at test. 
    If applied, only the first half of targets and lures are going to be used
    
    Parameters
    ------------
    
    memory: class object
         contains information about the given memory system
    
    Returns    
    ------------

    adjusted test probes and distances : array_like
                          
    """
    
    distances_targ = np.asarray(memory.retrieved['min-distances'])[memory.test_ID]
    distances_lure = np.asarray(memory.retrieved['min-distances'])[memory.N+memory.test_ID]
    distances_test = np.hstack((distances_targ,distances_lure))
    test_target = memory.test[:int(memory.N/2)]
    test_lure = memory.test[memory.N:memory.N+int(memory.N/2)]
    test = np.vstack((test_target,test_lure))
    
    return test, distances_test

     
