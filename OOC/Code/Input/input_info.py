"""
This module analyses input properties and their representations in memory
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams

path=os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
from analysis.plot_utils import set_aspect
colors=plt.rcParams['axes.prop_cycle'].by_key()['color']

class sensory_input:
    def __init__(self):
        self.layer = 7
        self.faces=[3,5,7,8,10,11,12,13,14,16,17,18,19,20,23,24,26,28,29,30,31,32,33,34,35,36,37,38,43,44,46,47,48,49,51,52,53,54,55,57,58,59,60,61,63,64,66,68,69,70,71,74,77,79,80,82,83,84,85,87,88,90,91,95,96,97,99,100,102,103,104,105,107,108,109,111,112,113,114,115,116,117,118,119,120]
        self.faceVars=[1,2,3,4,5,6,7,8,9,10,11]
        self.filt=4
        self.input_path='/media/olya/Acer'
        self.pca_dataset=np.load('dataset_faces.npy')
        self.targets=self.pca_dataset[:,0]
        self.lures=self.pca_dataset[:,-1]
        self.pat_sep=1.8
#        self.load_network_output()
    
    def load_network_output(self):
        
        """
        Loads the output of the specified layer and filter of the hiearchical network. 
        
        """
        import scipy.io 
        dataset=[list(range(len(self.faceVars))) for _ in range(len(self.faces))]
        imageSourceDirectory= path+'/Nat Input'
        for i in range(len(self.faces)):
            for ii in range(len(self.faceVars)):
                mat = scipy.io.loadmat('{}/Model_Resp/Full/{}F/Layer{}/r_i{:0>2}'.format(imageSourceDirectory, self.faces[i], self.layer, self.faceVars[ii]))
                data = mat['r']
                dataset[i][ii]=data['s%s'%self.filt][0][0]
        self.raw_dataset=dataset
    
    def add_noise(self,noise,N,noise_same=True):
        
        """
        Adds noise to the input patterns 
        
        Parameters
        ----------
        
        noise: float
               the variance of the noise distribution
        N: int
           number of items to be chosen
          
        noise_same: bool
          if True, the input noise value is added to all features of all items
         
        Returns
        -------
        data : array_like
        """
        
        patterns=self.targets
        import random as rd
        IDs=rd.sample(list(range(len(patterns))),N)
        patterns=patterns[IDs]
        patterns_separated=patterns*self.pat_sep
        if noise_same:
            noisy=[np.add(item,noise) for item in patterns]
            noisy_separated=[np.add(item,noise) for item in patterns_separated]
        else:
            noisy=[np.add(item,np.random.normal(0,noise,len(item))) for item in patterns]
            noisy_separated=[np.add(item,np.random.normal(0,noise,len(item))) for item in patterns_separated]
        data=[{'patterns':patterns,'noisy':noisy,'label':'p=1'},{'patterns':patterns_separated,'noisy':noisy_separated,'label':'p=%s'%self.pat_sep}]
        return data
    
    def system_difference(self,N,noise=0.7,save=True):   
        
        """
        Visualizes the systems with different values of pattern separation
        
        Parameters
        ----------
        
        N: int
           number of items to show
           
        noise: float
            the variance of the noise distribution
            
        save: bool
            if True, save the figure
        """
        data=self.add_noise(noise,N)
        fig,axes=plt.subplots(1,2,figsize=(6,6))
        for index,ax in enumerate(axes):
            [ax.plot(item[0],item[1],'o',color=colors[ind]) for ind,item in enumerate(data[index]['patterns'])]
            [ax.plot(item[0],item[1],'go',alpha=0.5,color=colors[ind]) for ind,item in enumerate(data[index]['noisy'])]
            [ax.plot([data[index]['patterns'][ind][0],data[index]['noisy'][ind][0]],[data[index]['patterns'][ind][1],data[index]['noisy'][ind][1]],color=colors[ind]) for ind in range(N)]
            ax.set_title(data[index]['label'],fontsize=16)
            # axis_default(ax,'PCA1','PCA2',limit=[[-4,4],[-4,4]],aspect=True)
        fig.tight_layout()
        if save:
            fig.savefig('PCA-noise.pdf',dpi=500)
            
    def compare_dist_metrics(self,noise=0.7,save=True,metrics=['euclidean','corr','cosine'],labels=['Euclidean','Correlation','Cosine'],figsize=(10,10)):
        
       """
       Compares different distance metrics by drawing histograms of distance distributions
       
       Parameters
       ----------
       noise: float
              the variance of the noise distribution
              
       save: bool
             if True, save the figure
             
       metrics: list
                contains the names of the distance measures to compare
                
       figsize: tuple
               the figure size
       """
       from memory.distance import set_metric
       rcParams["figure.figsize"]=figsize
       data=self.add_noise(noise,80,noise_same=False)
       cols=['purple','green']
       fig,axes=plt.subplots(1,len(metrics))

       for metric_ind,metric in enumerate(metrics):
           distance_calculator=set_metric(metric)
           ax=axes[metric_ind]
           for index,dat in enumerate(data):
                distance=[distance_calculator(dat['patterns'][ind],dat['noisy'][ind]) for ind in range(len(dat['patterns']))]
                if metric=='corr':
                    distance=[1-distance_calculator(dat['patterns'][ind],dat['noisy'][ind])[0] for ind in range(len(dat['patterns']))]
                ax.hist(distance,color=cols[index],alpha=.7,label=dat['label'])
                ax.set_title(labels[metric_ind],fontsize=16)
                # axis_default(ax,'Distance','Count',aspect=True,legend=True)
       fig.tight_layout()
       if save:
            fig.savefig('dist-compare.pdf',dpi=500)
   
    def plot_sep(self,noise=0.3,metric='corr',pat_sep=[1,1.8],figsize=(3,3),trials=100):
       
        """
        Plots the distances in the memory space against the distances in the input space for different
        values of pattern separation. 
        
        Parameters
        ----------
        noise: float
               the variance of noise distribution
               
        metric: string
            the distance metric to use, default='corr'
            
        
        pat_sep: list
            pattern separation values
            
        figsize: tuple
                 the figure size
                 
        trials: int
                how many trials to run before averaging
        """
        from memory.distance import set_metric
        distance_calculator=set_metric(metric)
        rcParams["figure.figsize"]=figsize
        colors=['purple','green']
        delta_in=[]
        delta_out=[]
        fig,ax=plt.subplots(1,1)
        for ind,p in enumerate(pat_sep):
            for t in range(trials):
                for data in self.pca_dataset:
                    if metric=='corr':
                        delta_in.append([1-distance_calculator(data[0]*p,item*p)[0] for item in data])
                        delta_out.append([1-distance_calculator(np.add(data[0]*p,np.random.normal(0,noise,len(item))),np.add(item*p,np.random.normal(0,noise,len(item))))[0] for item in data])
                delta_in_mean=np.mean(delta_in,axis=0)
                delta_out_mean=np.mean(delta_out,axis=0)
            ax.plot(delta_in_mean,delta_out_mean,'o',label='p=%s'%p,color=colors[ind])
            fit = np.polyfit(delta_in_mean,delta_out_mean,1)
            fit_fn = np.poly1d(fit) 
            ax.plot(delta_in_mean,delta_out_mean, 'o', delta_in_mean, fit_fn(delta_in_mean), '--',color=colors[ind])

        # axis_default(ax,'Input','Memory',limit=[[0,1],[0,1]],legend=True,aspect=True)
        
    
sens=sensory_input()
sens.system_difference(10,0.7)
sens.compare_dist_metrics(noise=1)
#for nn in np.linspace(0,1,5):
#    sens.plot_sep(noise=nn)
