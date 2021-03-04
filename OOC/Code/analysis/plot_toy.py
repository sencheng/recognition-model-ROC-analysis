#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 12:37:16 2019

@author: hakobovg
"""
import os
import pandas as pd
#path=os.path.abspath(os.path.join(os.path.dirname( __file__ )))
#os.chdir(path)# move to the base directory of  the code
from utils.utils import check_directory
from utils.data import get_data
from utils.save_load import load_params
from utils.calculations import calc_rates
import matplotlib.pyplot as plt
from analysis.plot_utils import axis_default
from pylab import rcParams
import numpy as np

class plot:
  # Plot the results of a certain simulation. This is written in a way that you can plot the values of a simulation anytime you want by reloading the data.
  # You can modify it to plot the graphs while the simulation is running. 
  def __init__(self,simID):
    self.simID=simID
    self.params=load_params(simID,os.path.abspath('..'))
    self.data=pd.read_pickle(self.params.data_dir+'data.pkl')
    self.output_dir=self.params.path+'/Figures/'
    check_directory(self.output_dir)
    
  def roc_hist(self,noise,row=9,figsize=(8,8),save=False):
      rcParams["figure.figsize"]=figsize
      #plot the ROCs
      target_yes=get_data(self.data,'target',row,noise)
      lure_yes=get_data(self.data,'lure',row,noise)
      hit=calc_rates(target_yes,self.params.N_t)
      fa=calc_rates(lure_yes,self.params.N_t)
      fig,axes=plt.subplots(1,2)
      ax=axes[0]
      ax.plot(fa,hit,'o-')
      ax.plot([0,1],[0,1],'k--')
      axis_default(ax,'False alarm rate','Hit rate', limit=[[0,1],[0,1]],aspect=True)
      
      ax1=axes[1]
      target_dist=get_data(self.data,'min-dist-target',row,noise)
      lure_dist=get_data(self.data,'min-dist-lure',row,noise)
      thr_range=get_data(self.data,'threshold_range',row,noise)[:-1]
      ax1.hist(np.ravel(target_dist),color='green',bins=self.params.n_bins,alpha=0.7,label='Target')
      ax1.hist(np.ravel(lure_dist),color='red',bins=self.params.n_bins,alpha=0.7,label='Lure')
      y=ax1.get_ylim()
      [ax1.plot([item]*2,y,'k--') for item in thr_range]
      axis_default(ax1,'Distance','Count',aspect=True,legend=True)
      fig.tight_layout()
      fig.suptitle('Noise=%s' %noise,fontsize=16,y=0.75)
      if save:
        fig.savefig(self.output_dir+'ROC_hist-'+str(noise)+'-'+self.params.simID+'.png')