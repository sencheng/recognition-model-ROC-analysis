#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 16:12:52 2019

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

simID='07-30_13:58:12'#'05-09_20:33:13'#'05-08_21:51:32'#input('Please enter the desired simulation ID ')
fit='Rn:0'
params=pickle.load( open(path+'/Log/metadata_'+simID+'.pkl', "rb" ))
params.data_dir=update_path(path,params.data_dir)
params.path=update_path(path,params.path)
path_to=params.path+'/Data/'+simID+'/'

data=load_dpsd(params)[0]
for dat in data:
    R=[item['R'][0] for item in dat[:params.hip+1]]
    F=[item['F'][0]for item in dat[:params.hip+1]]
    fig,ax=plt.subplots(1,1)
    colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
    alphas=np.linspace(0.2,1,len(R[0]))
    #for i in range(len(R)):
    #    for ii in range(len(R[i])):
    #        ax.plot(F[i][ii],R[i][ii],'o',color=colors[i],alpha=alphas[ii])
    ax.scatter(F,R)
    
    #[ax.scatter(F[item],R[item]) for item in range(len(R))]
    ax.set_xlabel('F', fontsize=14)
    ax.set_ylabel('R', fontsize=14)
    ax.set_title('F and R: Aggregated across conditions'+' '+fit, fontsize=16,y=1.06)

