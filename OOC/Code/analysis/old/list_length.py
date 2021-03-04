#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:04:16 2019

@author: olya
"""

import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
os.chdir(path)
path1=os.path.abspath(os.path.join(path, os.pardir))
m=-1 # which hippocampal system to access
from utils.utils import update_path
import numpy as np
from analysis.plot_utils import axis_default
from pylab import rcParams
rcParams["figure.figsize"]=(8,8)
o=-1
m=-1


simID='06-27_19:35:12'
params=pickle.load( open(path1+'/Log/metadata_'+simID+'.pkl', "rb" ))
params.data_dir=update_path(path1,params.data_dir)
params.data_dir="/".join(params.data_dir.split(os.sep)[:9])+'/'
params.path=update_path(path1,params.path)
input_dir=params.data_dir

import copy
from utils.utils import get_data
infos=['target','lure','targ-match', 'threshold_range']
fig,axes=plt.subplots(1,2)
fig1,axes1=plt.subplots(1,len(infos)-1)
fig2,ax2=plt.subplots(1,1)
nn=-1
noise_cond='diff'
colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
for info in infos:
    data_lists=[{info:[]} for i in range(len(params.list_length))]
    data_all=list(range(len(params.list_length)))
    # load the data for all list lengths
    for j in range(len(params.list_length)):
      data_all[j]=[pd.read_pickle(input_dir+str(params.list_length[j])+'-'+str(params.pat_sep[jj])+'.pkl') for jj in range(len(params.pat_sep))]
    # loda the required info for all list lengths
    for dic,dat in zip(data_lists,data_all):
      for key in  dic.keys():
          dic[key]=get_data(dat,key,params.offset[-1],params.noise)
    if noise_cond=='same':
        noises=[nn]*len(params.list_length)
    else:
        noises=np.arange(len(params.list_length))
    if info!='targ-match':
      data_know=[]
      data_remember=[]
    data_match=[]
    data_threshold=[]
    data_ALL=copy.deepcopy(data_all)
    for i in range(len(data_all)):
        if params.rec_test=='roc_item_LL':
            N_targ=params.list_length[i]
        else:
            N_targ=params.N_t
            
        if info in 'target' or info in 'lure':
            data=np.cumsum(get_data(data_ALL[i][m],info,params.offset[o],params.noise[noises[i]]))/N_targ
        elif info in 'targ-match':
            data_match.append(get_data(data_ALL[i][m],info,params.offset[o],params.noise[noises[i]]))
        elif info in 'threshold_range':
             data_threshold.append(get_data(data_ALL[i][m],info,params.offset[o],params.noise[noises[i]]))
          
        if info in ['target','lure']:
           data_know.append(get_data(data_ALL[i][m],info,params.offset[o],params.noise[noises[i]])[1]/N_targ)
           data_remember.append(get_data(data_ALL[i][m],info,params.offset[o],params.noise[noises[i]])[0]/N_targ)
           
           ax=axes[infos.index(info)]
           ax.plot(data,'o-',label=str(params.list_length[i])+' :' +str(params.noise[noises[i]]),color=colors[i]) 
           if info=='target':
               ax.set_ylim(0.,1)
           else:
               ax.set_ylim(0.,1)
           axis_default(ax,'Threshold','Positive response ',legend=True, leg_size=10,aspect=True)
           ax.set_title(info)
    if info!='threshold_range':   
      ax1=axes1[infos.index(info)]
      if info in ['target','lure']:
          ax1.plot(params.list_length,data_remember,'bo-',label='Remember')
          ax1.plot(params.list_length,data_know,'go-',label='Know')
      else:
          ax1.plot(params.list_length,data_match, 'o-')
      ax1.set_title(info)
      if info in infos[:-1]:
          ax1.set_ylim(0,1)
          axis_default(ax1,'List length','Response',legend=True, leg_size=10,aspect=True)
      else:
          ax1.set_ylim(.5,1)
          axis_default(ax1,'List length','Correct retrieval',aspect=True)
[ax2.plot(np.arange(params.N_thr-1),threshold[:-1],'o-',label=params.list_length[ind]) for ind,threshold in enumerate(data_threshold)]
ax2.legend()
ax2.set_xlabel('Threshold N',fontsize=16)
ax2.set_ylabel('Value',fontsize=16)
fig.tight_layout()
fig1.tight_layout()

