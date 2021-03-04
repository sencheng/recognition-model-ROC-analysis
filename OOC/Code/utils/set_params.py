#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from utils import utils
from utils.save_load import save_notes
import os 



class sim_params:
    
    """
    Initializes the default parameters of the simulation 
    
    """

    def __init__(self):
        
        self.path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        
        self.rec_test = 'roc_item' # the recognition test to be used
        self.dist_metric = 'corr' # distance metric to be used
        self.simID = utils.simID() # simulation ID
        self.d_item = 6 # the dimensonality of the patterns
        self.d_pattern = self.d_item # ignore for current purposes
        self.pairing = ''
        
        self.hip = 4 # the number of hippocamal systems
        self.scale = np.round(np.linspace(1.0,1.8,self.hip+1),1).tolist() #pattern separation values
        
        self.noise = None
        self.offset = [9] # the morph level to be used for lures
        self.target_morphs = [0] # morph level to be used for targets
        self.list_length = 30 # the number of studied items
        self.N_test = self.list_length # number of targets = number of lures at test

        self.trials = [5]# number of trials=simulations for each condition
        self.mem_traces = 1 # number of memory traces to be stored
        self.strength = 'weak' # the list strength condition, could be weak, strong or mixed
       
        self.strength_noise = 1
        self.threshold_range = None # threshold range
        self.n_bins = 10 # number of bins for histograming
        self.bias_offset = 0 #shift of criteria
        
        self.matlab = False # if True, save the data to fit by Yonelinas model using the matlab Code
        self.save_data = True # whether or not to save the dara
        self.save_metadata = True # whether or not to save simulation parameters
        self.show_fig = ['roc_curves','distance_histograms','correct_retrieval'] # which figures to plot
        self.save_figs = False  #whether or not to save the plots
         
        self.data_dir = self.path+'/Data/' # the directory to save the data
        self.N_thr = 6 # the number of  decision thresholds
        self.notes = [] # notes about the simulation that are saved
        
        self.decision = 'threshold' # threshold or closest
        self.combined = False # if True, combine the responses of hippocampal and cortical systems
    
    def update_params(self,new_params):
        
        """
        Change and modify the parameters based on the input dictionary
        
        Parameters
        ----------
        new_params: dict
                    the parameters to be changed
        
        """
        
        keys = list(new_params.keys())
        values = list(new_params.values())
        for i in range(len(keys)):
              setattr(self,keys[i],values[i])
        
        # turn into list  
        self.noise = [np.round(item,2) for item in self.noise]
        try:
            self.pat_sep = self.pat_sep.tolist()
        except:
            pass
        
        if self.save_data == True:
            self.save_metadata = True
            self.data_dir = self.path+'/Data/'+self.simID+'/'
            
        if len(self.notes) > 0:
            save_notes(self.notes,self.simID,self.path)
            
        if self.rec_test == 'fc' or self.rec_test=='YN_item':
            self.show_fig = ['fc_performance']
        elif self.rec_test == 'cue_target':
            self.show_fig = ['cue_target_roc','distance_histograms']
        elif self.rec_test == 'bps':
             self.show_fig = ['bps_distances','bps_performance']
             self.offset = [1,9]
         
def meta_params(condition):
    
    """
    Define the metaparameters for the given condition
    Allows to run multiple meta-conditions with the same simID

    Parameters
    ---------
    condition: string
        Experimental manipulation
    """
    # the default condition of item recognition
    if condition == 'item':
        cond_params = ['N_t']
        cond_values = [[30]]
    
    # list length simulations
    elif condition == 'length':
        cond_params = ['list_length','hip','pat_sep']
        cond_values = [[30,40,50,60,70],[1]*5,[[1.8]]*5]
        
    # list length simulation where the number of tested targets matches the number in the study phase
    elif condition == 'length_match':
        cond_params = ['list_length','N_t','hip','pat_sep']
        cond_values = [[30,40,50,60,70],[30,40,50,60,70],[1]*5,[[1.8]]*5]
   
    # list length simulation where the similarity between targets is manipulated
    elif condition == 'length_reverse':
        cond_params = ['target_morphs']
        cond_values = [[[0],[0,1],[0,1,2],[0,1,2,3],[0,1,2,3,4]]]
        
    # list strength simulation
    elif condition == 'strength':
        cond_params = ['strength','mem_traces', 'strength_noise','list_length','N_t','hip','pat_sep','strong_excluded']
#        cond_values = [['S','MS','W','MW'],[5,5,1,5],[1,1,1,1],[30,30,30,30],[30,30,30,30],[1]*4,[[1.8]]*4,[False,False,False,False]]
#        cond_values=[['W','MW'],[1,5],[1,1],[60,30],[30,30],[1]*2,[[1.8]]*2,[True,True],[0.006,0.002]]
        cond_values=[['S','MS','W','MW'],[1,1,1,1],[3,3,1,3],[30,30,30,30],[30,30,30,30],[1]*4,[[1.8]]*4,[False,False,False,False]]

    # manipulating the decision noise

    elif condition == 'decision':
        cond_params = ['decision_noise']
        cond_values = [np.linspace(0.0,0.015,10)[::2]]
        
    # manipulating the decision criteria
    elif condition == 'liberal_bias':
        cond_params = ['bias_offset']
#        cond_values = [np.array([0.002,0.004,0.006,0.008])]
#        cond_values=[np.linspace(0.006,0.02,8)]
        cond_values=[np.linspace(0.002,0.008,10)]

    conditions = cond_values[0]
    return cond_params,cond_values,conditions

    
            

             



