#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 22:49:11 2019

@author: olya
"""

import pickle
import os
import sys
import pandas as pd
path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
os.chdir(path)
path1=os.path.abspath(os.path.join(path, os.pardir))
m=-1 # which hippocampal system to access
from utils.utils import update_path, get_data, round_for_fit,calc_rates
import matplotlib.pyplot as plt
from analysis.plot_utils import set_aspect
fig,ax=plt.subplots(1,1)
nn=0.3
o=9
#IDs=['06-21_23:09:58','06-21_23:13:21','06-21_23:15:13','06-21_23:21:12','06-21_23:23:21','06-21_23:25:08','06-23_15:44:24']
#labels=['control','PFC lesion:0.015','PFC lesion:0.0.02','PFC lesion:0.0.025','PFC lesion:0.0.03','PFC lesion:0.0.035','testing']

#noise added to the threshold
IDs=['07-05_15:32:17']
labels=['last']

for i,simID in enumerate(IDs):
    params=pickle.load( open(path1+'/Log/metadata_'+simID+'.pkl', "rb" ))
    params.data_dir=update_path(path1,params.data_dir)
    params.data_dir="/".join(params.data_dir.split(os.sep)[:9])+'/'
    params.path=update_path(path1,params.path)
    for dn_ind,dn in enumerate(sorted(os.listdir(params.data_dir))):
        
        try:
          input_dir=params.data_dir+dn+'/'
          filenames=sorted([item for item in os.listdir(input_dir) if item[-3:]=='pkl'])
        except:
          input_dir=params.data_dir
          filenames=sorted([item for item in os.listdir(input_dir) if item[-3:]=='pkl'])

        data=[pd.read_pickle(input_dir+file) for file in filenames]
        
        target=get_data(data,'target',o,nn)[0]
        lure=get_data(data,'lure',o,nn)[0]
        target=round_for_fit(target,params.N_t)
        lure=round_for_fit(lure,params.N_t)
        hit=calc_rates(target,params.N_t)
        fa=calc_rates(lure,params.N_t)
        ax.plot(fa,hit,'o-',label=dn)
        ax.plot([0,1],[0,1],'k--')
        ax.set_xlim(-0.01,1)
        ax.set_ylim(-0.01,1)
        ax.legend()
        set_aspect(ax)