#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 00:48:14 2019

@author: olya
"""

import numpy as np
import matplotlib.pyplot as plt
import os
path=os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
os.chdir(path)# move to the base directory of  the code
path1=os.path.abspath(os.path.join(path, os.pardir)) # this is the main directory where all the folders are
from utils.utils import load_params, get_data
from utils.calculations import calc_rates
from analysis.plot_utils import axis_default,set_aspect
import pandas as pd
from pylab import rcParams
colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
m=-1
IDs=['08-01_01:42:56','08-01_22:50:10']
for nn in range(5):
    fig,ax=plt.subplots(1,1)
    for ind, simID in enumerate(IDs):
        if ind==0:
            noise=1
        else:
            noise=nn
        params=load_params(simID,path1)
        dir_path=params.path+'/Data/'+simID+'/'
        filenames=sorted(item for item in os.listdir(dir_path))
        for file in filenames: 
            subfiles=sorted([item for item in os.listdir(dir_path+file) if item[-3:]=='pkl'])
            data=[pd.read_pickle(dir_path+file+'/'+item) for item in subfiles]
            targets=get_data(data[m],'target',params.offset[0],params.noise[noise])
            lures=get_data(data[m],'lure',params.offset[0],params.noise[noise])
            hit=calc_rates(targets,params.N_t)
            fa=calc_rates(lures,params.N_t)
            ax.plot(fa,hit,'o-',label=file)
    axis_default(ax,'False alarm rate','Hit rate',limit=[[0,1],[0,1]],aspect=True,legend=True)
    ax.plot([0,1],[0,1],'k--')
