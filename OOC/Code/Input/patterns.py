"""
This module loads the stimuli and assigns them to targets and lures

"""
import numpy as np
import os
path= os.path.dirname(os.path.realpath(__file__))

class probes:

    def __init__(self, params):
        
      """
      params: class object
        simulation parameters
      """
      self.params = params
      self.cond = params.cond
      
     
    def probe_faces(self, seed=1):
      
      """
      Load PCA-reduced input patterns
      
      Parameters
      -----------
      
      seed: int
             random seed for shuffling the input, updates in each trial to have 
             different input arrangements
      
      Returns
      -------
      probes : array_like
  
      """
      # load  the reduced dataset with the shape (85,11,8)-(items, morphs, features)
     
      dataset_reduced = np.load(path+'/dataset_faces.npy') 
      
      # shuffle to have different stimuli for different runs
      shuffled = np.random.RandomState(seed=seed).permutation(
                                      range(len(dataset_reduced))) 
      ID = shuffled[:self.params.list_length]
      
      # select the morph images defined in simulation
      morph_indices = self.params.target_morphs+self.params.offset
      probes = list(range(len(morph_indices))) 
      for o in range(len(morph_indices)):
          probes[o] = [dataset_reduced[j][morph_indices[o]][:self.params.d_item]  
                      for j in ID]
      self.probes = np.asarray(probes)

      
  
    def probe_assignment(self,lure_morph=[-1]):
        
      """
      Assign the probes to targets and lures      
      
      Parameters
      -----------
      
      lure morph: list
                  contains the morph level for lure items
      Returns
      -------
      study and test items : array_like
  
      """
      self.study_all = np.vstack(self.probes[self.params.target_morphs,:])
      lures = np.vstack(self.probes[lure_morph,:])
      self.test = np.vstack((self.study_all,lures)) 


