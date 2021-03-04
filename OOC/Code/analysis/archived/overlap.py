#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 19:34:57 2019

@author: olya
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../')

from utils.data import get_data
from utils.utils import update_path
from utils.calculations import calc_rates
from analysis.plot_utils import set_aspect,axis_default
#from utils.save_load import load_dpsd
from utils.matlab import matlab

import os
import pandas as pd
import pickle

path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
#os.chdir(path)
path1=os.path.abspath(os.path.join(path, os.pardir))
#simID='08-01_21:56:01'#'07-01_21:20:36'
#params=pickle.load( open(path1+'/Log/metadata_'+simID+'.pkl', "rb" ))
#params.data_dir=update_path(path1,params.data_dir)
#params.data_dir="/".join(params.data_dir.split(os.sep)[:9])+'/'
#params.path=update_path(path1,params.path)
#input_dir=params.data_dir
#fig=[plt.subplots(1,1) for i in range(len(params.noise))]
IDs=['10-13_15:40:44','10-13_15:40:51']
#IDs=['10-13_18:13:22','10-13_18:13:14','10-13_18:41:30','10-13_19:23:53']
#labels=['Related lures','Unrelated lures']
labels=['1','2','3','4']
colors=['r','g','b','orange']
markers=['-','-','-','-']
#fits=['Rn:0','Rn:0','Rn:0','Rn:0']
fits=['Full','Rn:0','Full','Full']
fig,ax=plt.subplots(1,1)
m=-1
o=0
nn=0
for index,simID in enumerate(IDs):
    params=pickle.load( open(path1+'/Log/metadata_'+simID+'.pkl', "rb" ))
    params.data_dir=update_path(path1,params.data_dir)
    params.data_dir="/".join(params.data_dir.split(os.sep)[:9])+'/'
    params.path=update_path(path1,params.path)
    mat=matlab(params)
    data,conds=mat.load_dpsd(fit=fits[index])
    ax.plot(data[o][m]['fa'][0][nn],data[o][m]['hits'][0][nn],'o',color=colors[index],alpha=0.6)
#    ax.plot(data[o][0]['fa'][nn][0],data[o][0]['hits'][nn][0],'ro')
    ax.plot(data[o][m]['roc_fa'][m][:,nn],data[o][m]['roc_hit'][0][:,nn],'b',color=colors[index],linestyle=markers[index],label='Set '+labels[index])
#    ax.plot(data[o][0]['roc_fa'][0][:,nn],data[o][0]['roc_hit'][0][:,nn],'r',linestyle=markers[index])
    ax.plot([0,1],[0,1],'k--')
    set_aspect(ax)
    axis_default(ax,'False alarm rate','Hit rate',legend=True)
fig.savefig('related_unrelated.eps')
