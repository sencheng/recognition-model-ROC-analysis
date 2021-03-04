
"""
Contains the class for generating memory systems
"""

import numpy as np
import os
path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from utils import data
from memory import distance
    
class memory_system:

    """
    Represents a memory system with its parameters 
    and memory operations, such as memory storage and retrieval
    
    Attributes
    ----------
        
    params: class object
        simulation parameters
                
    scale: float
        the scaling value
            

    """

    def __init__(self,params,scale):
        
        self.params = params
        self.N = params.N_test
        self.scale = scale
        self.retrieved = {} # allocated for storing retrieval measures
        self.performance = {} # allocated for storing performance measures
        self.test = [] 
        self.study = []
        self.dataFrame = data.create_dataFrame(params.offset,params.noise) # empty dataframe for storage
        self.dataFrame1 = data.create_dataFrame(params.offset,params.noise) # empty dataframe for storage
        
    def perform_scaling(self,probes,probe_type):
        
        """
        Performs scaling by multiplying each item vector by a scalar        
        
        Parameters
        -----------
        
        probes: array_like
             contains all probes: targets and lures
             
        probe_type: string
             indicates whether the items are for test or study
             
        """

        if probe_type == 'test':
            self.test = np.multiply(probes,self.scale)
        elif probe_type == 'study':
            self.study = np.multiply(probes,self.scale)
    
    def strengthening(self,noise):
        params = self.params
        
        N = int(self.N/2)
        noise_strong = noise/params.strength_noise # 1 if the strengthening by repetition
                
        # shuffle the items
        indices = np.arange(params.list_length)
        shuffled = np.arange(params.list_length)
        shuffled = np.random.permutation(params.list_length)
        
        # assign the first and second halfs to certain condition
        if params.strength == 'MS':
            ID_strong = indices[shuffled][:N]
            ID_weak = indices[shuffled][N:]
            self.test_ID = ID_strong
        elif params.strength == 'MW':
            ID_strong = indices[shuffled][N:]
            ID_weak = indices[shuffled][:N]
            self.test_ID = ID_weak
            
        # store the given number of memory traces for items to be strengthened
        for trace in range(params.mem_traces):
              memory_noise_strong = np.asarray([np.random.normal(0,noise_strong,
                                    params.d_pattern) for i in range(len(self.study[ID_strong]))]) 
              self.target_memory.append(np.add(memory_noise_strong,self.study[ID_strong])) 
        memory_noise_weak = np.asarray([np.random.normal(0,noise,params.d_pattern) for i in range(len(self.study[ID_weak]))]) 
        self.target_memory.append(np.add(memory_noise_weak,self.study[ID_weak]))
        self.target_memory = np.vstack((self.target_memory)) # correct shape 

            
    def add_memory_noise(self,noise):
        
        """
        Adds noise to the stored memory items        
        
        Parameters
        ----------
        
        noise: float
             the variance of the noise distribution
             
        Note
        -----
        In the simulations of list strength, if mixed lists are tested, 
        the first half of the target items is stored n times (params.mem_traces) or given smaller noise level, 
        while the second half is only stored once or given the normal noise level. Otherwise, the number of the
        memory traces is given by params.mem_traces
             
        """

        params = self.params
        
        if params.strength in ['MS','MW']: 
            self.strengthening(noise)
        else:
            noise = noise/params.strength_noise # 1 if no strengthening
            for trace in range(params.mem_traces):
                # create noise vectors
                memory_noise = np.asarray([np.random.normal(0,noise,
                               params.d_pattern) for i in range(len(self.study))]) 
                # store noisy traces
                self.target_memory.append(np.add(memory_noise,self.study)) 
        self.target_memory = np.vstack((self.target_memory)) # for correct shape 

       
    def item_retrieval(self,noise):
      
        """
        Performs the retrieval of the items from memory        
        
        Parameters
        ----------
        
        noise: float
             the variance of the noise distribution
        """
        self.target_memory = [] # allocated for storing noisy memory traces

        params = self.params
        test = self.test
        match = np.zeros((self.N*2,1))  # allocated for saving accurate instances

        #set the distance measure
        distance_calculator = distance.set_metric(params.dist_metric)
        distances = list(range(len(test))) # allocated for saving distances
        
        
        #add noise to the original items to mimic memory storage
        self.add_memory_noise(noise)
        
            
        # perform retrieval for each test item
        for ind,cue in enumerate(test): 
             if params.dist_metric == 'corr':
                 dist = [1-distance_calculator(cue,item)[0] 
                         for item in self.target_memory]
             else:
                 
                dist = [distance_calculator(cue,item) 
                        for item in self.target_memory]
                
            # check if the retrieved item corresponds to the stored item or its intended morph
             ret_ind = dist.index(min(dist)) 
             if ret_ind == ind or ret_ind == ind-self.N:
                match[ind] = 1 
             distances[ind] = min(dist)
             
        self.retrieved['min-distances'] = distances
        self.retrieved['targ-match'] = np.sum(match[:self.N])/self.N 
        self.retrieved['lure-match'] = np.sum(match[self.N:])/self.N # relevant if similar lures are used
        # self.retrieved['min-dist-target'] = distances[:self.N]
        # self.retrieved['min-dist-lure'] = distances[self.N:]
        # import matplotlib.pyplot as plt
        # fig,ax=plt.subplots()
        # ax.hist(distances[:self.N],bins=10,color='g',alpha=0.5)
        # ax.hist(distances[self.N:],bins=10,color='r',alpha=0.5)
