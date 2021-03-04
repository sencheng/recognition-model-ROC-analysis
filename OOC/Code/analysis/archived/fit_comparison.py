#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 19:36:21 2019

@author: olya
"""
import pickle
import sys
sys.path.append('../')
from utils.matlab import load_dpsd
from utils.utils import update_path
import numpy as np
import matplotlib.pyplot as plt
from analysis.plot_utils import set_aspect
from pylab import rcParams

import os
path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
path=path.split('/')[:-1]
path='/'.join(path+[''])

rcParams["figure.figsize"]=(8,8)

simID='06-22_01:18:58'#'05-09_20:33:13'#'05-08_21:51:32'#input('Please enter the desired simulation ID ')
params=pickle.load( open(path+'/Log/metadata_'+simID+'.pkl', "rb" ))
params.data_dir=update_path(path,params.data_dir)
params.path=update_path(path,params.path)

for params.fit in ['Rn:0']:

    data=load_dpsd(30,params.data_dir,N_o=len(params.offset),fit=params.fit)
    c=0
    c1=1
    F_comb=[np.subtract(comb['F'],data[c]['F'])[0] for comb in data[params.hip+1:]]
    F_comb1=[np.subtract(comb['F'],data[c1]['F'])[0] for comb in data[params.hip+1:]]
    
    R_comb=[np.subtract(comb['R'],data[c]['R'])[0] for comb in data[params.hip+1:]]
    R_comb1=[np.subtract(comb['R'],data[c1]['R'])[0] for comb in data[params.hip+1:]]
    
    
    F_hip=[np.subtract(hip['F'],data[c]['F'])[0] for hip in data[1:params.hip+1]]
    F_hip1=[np.subtract(hip['F'],data[c1]['F'])[0] for hip in data[1:params.hip+1]]
    
    R_hip=[np.subtract(hip['R'],data[c]['R'])[0] for hip in data[1:params.hip+1]]
    R_hip1=[np.subtract(hip['R'],data[c1]['R'])[0] for hip in data[1:params.hip+1]]
    
    fig,axes=plt.subplots(1,len(F_comb))
    fig1,axes1=plt.subplots(1,len(F_hip))
    
    for i,comb in enumerate(params.pat_sep[1:]):
        ax=axes[i]
        ax1=axes1[i]
        ax.plot(F_comb[i][1:],'go-',label='F')
        ax.plot(R_comb[i][1:],'bo-',label='R')
        
        ax.plot(F_comb1[i][1:],'go--',label='F1')
        ax.plot(R_comb1[i][1:],'bo--',label='R1')
    
        ax1.plot(F_hip[i][1:],'go-',label='F')
        ax1.plot(R_hip[i][1:],'bo-',label='R')
        ax1.plot(F_hip1[i][1:],'go--',label='F1',alpha=.5)
        ax1.plot(R_hip1[i][1:],'bo--',label='R1',alpha=.5)
    
        ax.set_ylim(0,0.3)
        ax1.set_ylim(0.,0.3)
        set_aspect(ax1)
        set_aspect(ax)
        ax.set_title(comb)
        ax1.set_title(comb)
        if i==0:
           ax.legend()
    fig.tight_layout()
    fig1.tight_layout()
    fig.suptitle(params.fit+': Comb',fontsize=16,y=.7)
    fig1.suptitle(params.fit+': Hip',fontsize=16,y=.7)
