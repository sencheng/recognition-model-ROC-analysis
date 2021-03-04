#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:17:49 2019

@author: olya
"""

import pickle
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
#sys.path.insert(0,path)
path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
os.chdir(path)
path1=os.path.abspath(os.path.join(path, os.pardir))

m=-1 # which hippocampal system to access
from utils import utils
from utils.utils import update_path
from analysis.plot_utils import set_aspect

simID='07-05_17:39:39'
params=pickle.load( open(path1+'/Log/metadata_'+simID+'.pkl', "rb" ))
params.data_dir=update_path(path1,params.data_dir,separator='Data')
params.data_dir="/".join(params.data_dir.split(os.sep)[:9])+'/'
params.path=update_path(path1,params.path)

# don't change these
o=params.offset[-1] # offset level to access
n=params.noise[0] # noise level to access

data_weak=[pd.read_pickle(params.data_dir+'weak/'+str(params.N_t)+'-'+str(params.pat_sep[ii])+'.pkl') for ii in [0,m]]
data_strong=[pd.read_pickle(params.data_dir+'strong/'+str(params.N_t)+'-'+str(params.pat_sep[ii])+'.pkl') for ii in [0,m]]
data_mixed= [pd.read_pickle(params.data_dir+'mixed/'+str(params.N_t)+'-'+str(params.pat_sep[ii])+'.pkl') for ii in [0,m]]   

#example of how to access the details of each dataset
data_weak_cort=data_weak[0].loc[o,n] # note this is a dictionary, so google how to handle these
data_weak_hip=data_weak[m].loc[o,n]
data_mixed_cort=data_mixed[0].loc[o,n] 
data_mixed_hip=data_mixed[m].loc[o,n]
data_strong_cort=data_strong[0].loc[o,n] 
data_strong_hip=data_strong[m].loc[o,n]

threshold=np.arange(1,len(data_weak_cort['threshold_range'])+1)

from utils.utils import calc_rates
cort_hit_rate=[calc_rates(data_weak_cort['target'],params.N_t),
               calc_rates(data_mixed_cort['target'],params.N_t),
               calc_rates(data_strong_cort['target'],params.N_t)]
cort_false_rate=[calc_rates(data_weak_cort['lure'],params.N_t),
               calc_rates(data_mixed_cort['lure'],params.N_t),
               calc_rates(data_strong_cort['lure'],params.N_t)]
hip_hit_rate=[calc_rates(data_weak_hip['target'],params.N_t),
               calc_rates(data_mixed_hip['target'],params.N_t),
               calc_rates(data_strong_hip['target'],params.N_t)]
hip_false_rate=[calc_rates(data_weak_hip['lure'],params.N_t),
               calc_rates(data_mixed_hip['lure'],params.N_t),
               calc_rates(data_strong_hip['lure'],params.N_t)]

labels=['weak','mixed','strong']
titles=['cort_hit_rate','cort_false_rate','hip_hit_rate','hip_false_rate']

data_all=[cort_hit_rate,cort_false_rate,hip_hit_rate,hip_false_rate]
fig1,axes=plt.subplots(2,2)
axes=axes.flatten()
for i, data in enumerate(data_all):
    ax=axes[i]
    [ax.plot(threshold[:-1],item[:-1],'o-',label=labels[ind]) 
    and ax.legend() 
    and ax.set_ylabel(titles[i]) 
    and ax.set_xlabel('threshold')
    and ax.set_ybound(0,1.1)
    and set_aspect(ax)
    for ind,item in enumerate(data)]
#    ax.set_aspect('equal')
fig1.tight_layout()

#fig2,axes=plt.subplots(2,2)
#axes=axes.flatten()
#for i, data in enumerate(data_all):
#    ax=axes[i]
#    ax.plot([1,2,3],[data[0][0],data[1][0],data[2][0]], 'o-', label='threshold 1')
#    ax.plot([1,2,3],[data[0][1],data[1][1],data[2][1]], 'o-', label='threshold 2')
#    ax.set_ylabel(titles[i])
#    ax.set_ybound(0,0.9)
#    ax.legend()
#    ax.set_xticks([1,2,3])
#    ax.set_xticklabels(labels)
#fig2.tight_layout()
#
#ROC Curves
list_strength=np.arange(1,len(labels)+1)
fig3,axes=plt.subplots(1,2)
axes=axes.flatten()
strengths=np.arange(len(labels))
for strength in strengths:
    ax=axes[0]
    ax.plot(cort_false_rate[strength],cort_hit_rate[strength],'o-',label=labels[strength])
    ax.set_xlabel('false alarm rate')
    ax.set_ylabel('hit rate')
    ax.set_title('cortex')
    ax.set_ybound(0,1.1)
    ax.legend()
    set_aspect(ax)
    ax=axes[1]
    ax.plot(hip_false_rate[strength],hip_hit_rate[strength],'o-',label=labels[strength])
    ax.set_xlabel('false alarm rate')
    ax.set_ylabel('hit rate')
    ax.set_title('hippocampus')
    ax.set_ybound(0,1.1)
    ax.legend()
    set_aspect(ax)
fig3.tight_layout()

cort_threshold=[data_weak_cort['threshold_range'], data_mixed_cort['threshold_range'],data_strong_cort['threshold_range']]
hip_threshold=[data_weak_hip['threshold_range'], data_mixed_hip['threshold_range'],data_strong_hip['threshold_range']]

colors=['b','orange','g']
fig,axes=plt.subplots(1,2)
data_threshold=[cort_threshold,hip_threshold]
for ind,ax in enumerate(axes):
    [ax.plot(item[:-1],'o-',color=colors[item_ind]) for item_ind,item in enumerate(data_threshold[ind])]
    set_aspect(ax)