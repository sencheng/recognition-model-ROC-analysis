#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 15:50:52 2019

@author: olya
"""

import numpy as np
import matplotlib.pyplot as plt
import os
path=os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
os.chdir(path)# move to the base directory of  the code
path1=os.path.abspath(os.path.join(path, os.pardir)) # this is the main directory where all the folders are
from utils.utils import load_params
from utils.matlab import load_dpsd
from analysis.plot_utils import axis_default,set_aspect
from pylab import rcParams
colors=plt.rcParams['axes.prop_cycle'].by_key()['color']

simID='07-18_16:51:25'
params=load_params(simID,path1)
data, conds=load_dpsd(params,fit='Rn:0')
data1,conds1=load_dpsd(params,fit='Full')
mem=[0,-1]
alphas=[.5,1]
nn=2
o=-1
rcParams["figure.figsize"]=(6,6)

fig,ax=plt.subplots(1,1)
for ind,m in enumerate(mem):
    F=[item[m]['F'][o][nn] for item in data]
    R=[item[m]['R'][o][nn] for item in data]
    F1=[item[m]['F'][o][nn] for item in data1]
    R1=[item[m]['R'][o][nn] for item in data1]
    auc=[item[m]['auc'][o][nn] for item in data]
    ax.plot(conds,F,'go-',label='F',alpha=alphas[ind])
    ax.plot(conds,R,'ro-',label='R',alpha=alphas[ind])
    ax.plot(conds,auc,'o-',color='orange',label='auc',alpha=alphas[ind])
axis_default(ax,'Threshold offset','Paramter',legend=True,aspect=True)

rcParams["figure.figsize"]=(12,12)

fig,axes=plt.subplots(1,len(conds))
m=-1
for ind, sample in enumerate(data):
    hit_fit=sample[m]['roc_hit'][o][:,nn][:-1]
    fa_fit=sample[m]['roc_fa'][o][:,nn][:-1]
    hit_fit1=data1[ind][m]['roc_hit'][o][:,nn][:-1]
    fa_fit1=data1[ind][m]['roc_fa'][o][:,nn][:-1]
    hit_obs=sample[m]['hits'][o][nn][:-1]
    fa_obs=sample[m]['fa'][o][nn][:-1]
#    fit = np.polyfit(fa_obs,hit_obs,1)
#    fit_fn = np.poly1d(fit) 
    ax=axes[ind]
#    ax1=axes[1][ind]
    ax.plot(fa_fit,hit_fit,'b-')
    ax.plot(fa_obs,hit_obs,'bo')
    ax.plot(fa_fit1, hit_fit1, 'r--')
#    ax1.plot(fa_obs,hit_obs,'bo')
    ax.plot([0,1],[0,1],'k--')
#    ax1.plot([0,1],[0,1],'k--')
    if ind==0:
        axis_default(ax,'Fa','Hit',aspect=True)
#        axis_default(ax1,'Fa','Hit',aspect=True)
    else:
        axis_default(ax,'Fa',' ',aspect=True)
#        axis_default(ax1,'Fa',' ',aspect=True)
    ax.set_title(conds[ind],fontsize=16)
fig.tight_layout()
    