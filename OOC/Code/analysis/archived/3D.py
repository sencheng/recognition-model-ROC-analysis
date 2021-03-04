#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 00:01:47 2019

@author: olya
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib import cm
path=os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
os.chdir(path)# move to the base directory of  the code
path1=os.path.abspath(os.path.join(path, os.pardir)) # this is the main directory where all the folders are
from utils.utils import load_params
from utils.matlab import load_dpsd
from analysis.plot_utils import set_aspect,axis_default
from pylab import rcParams
import sys
from utils.calculations import zscore
from pylab import rcParams
rcParams["figure.figsize"]=(8,8)
simID='07-30_13:58:12'
params=load_params(simID,path1)
data=load_dpsd(params)
R=[]
F=[]
AUC=[]
delta=[]
for ind, dat in enumerate(data[0]):
    Rs=[item['R'][0]for item in dat[:len(params.pat_sep)]]
    Fs=[item['F'][0] for item in dat[:len(params.pat_sep)]]
    aucs=[item['auc'][0]for item in dat[:len(params.pat_sep)]]       
    for item in dat[:len(params.pat_sep)]:
        item_R=item['R'][0]
        for item_ind,item1 in enumerate(item_R):
            if item1>0.2:   
                diff_R=item1-dat[1]['R'][0][item_ind]
                diff_F=item['F'][0][item_ind]-dat[1]['F'][0][item_ind]
                diff=np.subtract(diff_R,diff_F)
                delta.append(diff)
    R.append(Rs)
    F.append(Fs)
    AUC.append(aucs)
    delta.append(diff)
labels=['R','F','AUC']
for ind,param in enumerate([R,F,AUC]):
    dat=np.ravel(param)
#    if labels[ind]=='AUC':
#        dat=zscore(dat)
    decisions=[float(item) for item in data[-1]]
    dec=[[item]*len(params.pat_sep)*len(params.noise) for item in decisions]
    dec=[item for sublist in dec for  item in sublist]
    pat=[[item]*len(params.noise) for item in params.pat_sep]
    pat=[item for sublist in pat for  item in sublist]
    pat=pat*len(decisions)
    noise=params.noise*int(len(dat)/len(params.noise))
    fig=plt.figure()
    ax = fig.gca(projection='3d')
    plot=ax.scatter3D(dec,pat,noise,c=dat, cmap='Blues',vmin=min(dat),vmax=max(dat))
    ax.set_ylabel('Pattern separation',fontsize=16)
    ax.set_xlabel('Liberal offset',fontsize=16,labelpad=20)
    ax.set_zlabel('Noise',fontsize=16,labelpad=20)
    ax.set_yticks(np.linspace(pat[0],pat[-1],len(params.pat_sep)))
    ax.set_xticks(np.linspace(dec[0],dec[-1],len(decisions)))
    ax.set_zticks(np.linspace(noise[0],noise[-1],len(params.noise)))
    ax.set_zticklabels(params.noise)
    ax.set_title(labels[ind])
    ax.view_init(azim=80)
    fig.colorbar(plot,shrink=0.5)
    set_aspect(ax)
        
#x_scale=1
#y_scale=.7
#z_scale=1
#
#scale=np.diag([x_scale, y_scale, z_scale, 1.0])
#scale=scale*(1.0/scale.max())
#scale[3,3]=1.0
#
#def short_proj():
#  return np.dot(Axes3D.get_proj(ax), scale)
#
#ax.get_proj=short_proj
