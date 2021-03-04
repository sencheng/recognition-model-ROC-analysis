#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 22:06:38 2019

@author: olya
"""
import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
os.chdir(path)
path1=os.path.abspath(os.path.join(path, os.pardir))
from utils.utils import get_data,calc_rates, update_path
from analysis.plot_utils import set_aspect
#figure,ax=plt.subplots(1,1)

#IDs=['07-04_15:39:53','07-04_15:44:04','07-04_15:48:34','07-05_10:55:31']
#n_ind=0
#for simID in IDs:
#    params=pickle.load( open(path1+'/Log/metadata_'+simID+'.pkl', "rb" ))
#    params.data_dir=update_path(path1,params.data_dir)
#    params.data_dir="/".join(params.data_dir.split(os.sep)[:9])+'/'
#    params.path=update_path(path1,params.path)
#    
#    input_dir=params.data_dir
#    data=list(range(len(os.listdir(input_dir))))
#
#    o=params.offset[-1]
#    m=-1
#    nn=params.noise[n_ind]
#    folders=sorted(os.listdir(input_dir))
#    if os.path.isdir(folders[0]):
#        folders=[input_dir+folder+'/' for folder in folders]
#        
#    targs=[]
#    lures=[]
#    for ind, directory in enumerate(folders):
#        filenames=sorted([item for item in os.listdir(directory) if item[-3:]=='pkl'])
#        data=[pd.read_pickle(directory+file) for file in filenames]
#        targ=get_data(data[m],'target',o,nn)
#        lure=get_data(data[m],'lure',o,nn)
#        targs.append(targ)
#        lures.append(lure)
#        hit=calc_rates(targ,params.N_t)
#        fa=calc_rates(lure,params.N_t)
#        ax.plot(fa,hit,'o-',label=folder)
#    ax.set_xlim(0,1)
#    ax.set_ylim(0,1)
#    ax.legend()
#    set_aspect(ax)
#sys.exit()
simID='07-05_13:34:41'
params=pickle.load( open(path1+'/Log/metadata_'+simID+'.pkl', "rb" ))
params.data_dir=update_path(path1,params.data_dir)
params.data_dir="/".join(params.data_dir.split(os.sep)[:9])+'/'
params.path=update_path(path1,params.path)

input_dir=params.data_dir
data=list(range(len(os.listdir(input_dir))))

o=params.offset[-1]
m=-1
figure,axis=plt.subplots(1,1)
for noise_ind in range(len(params.noise)):
    nn=params.noise[noise_ind]

    colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
    
    fig,ax=plt.subplots(1,1)
    folders=sorted(os.listdir(input_dir))
    targs=[]
    lures=[]
    for ind, folder in enumerate(folders):
        directory=input_dir+folder+'/'
        filenames=sorted([item for item in os.listdir(directory) if item[-3:]=='pkl'])
        data=[pd.read_pickle(directory+file) for file in filenames]
        targ=get_data(data[m],'target',o,nn)
        lure=get_data(data[m],'lure',o,nn)
        targs.append(targ)
        lures.append(lure)
        hit=calc_rates(targ,params.N_t)
        fa=calc_rates(lure,params.N_t)
        ax.plot(fa,hit,'o-',label=folder)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.legend()
    set_aspect(ax)
    
    targs_average=np.mean(targs[:10],axis=0)
    lure_average=np.mean(lures[:10],axis=0)
    hit_average=calc_rates(targs_average,params.N_t)
    fa_average=calc_rates(lure_average,params.N_t)
    axis.plot(fa_average,hit_average,'o-')
    axis.plot([0,1],[0,1],'k--')
    axis.set_xlim(0,1)
    axis.set_ylim(0,1)
    set_aspect(axis)
sys.exit()
   
    
#figure,axis=plt.subplots(1,1)
#for noise_ind in range(len(params.noise)):
#    nn=params.noise[noise_ind]    folders=sorted(os.listdir(input_dir))
#    targs=[]
#    lures=[]
#    for ind, folder in enumerate(folders):
#        directory=input_dir+folder+'/'
#        filenames=sorted([item for item in os.listdir(directory) if item[-3:]=='pkl'])
#        data=[pd.read_pickle(directory+file) for file in filenames]
#        targ=get_data(data[m],'target',o,nn)
#        lure=get_data(data[m],'lure',o,nn)
#        targs.append(targ)
#        lures.append(lure)
#        hit=calc_rates(targ,params.N_t)
#        fa=calc_rates(lure,params.N_t)
#        ax.plot(fa,hit,'o-',label=folder)
#    ax.set_xlim(0,1)
#    ax.set_ylim(0,1)
#    ax.legend()
#    set_aspect(ax)
#
#
#    colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
#    
#    fig,ax=plt.subplots(1,1)
#    
#    targs_average=np.mean(targs[:10],axis=0)
#    lure_average=np.mean(lures[:10],axis=0)
#    hit_average=calc_rates(targs_average,params.N_t)
#    fa_average=calc_rates(lure_average,params.N_t)
#    axis.plot(fa_average,hit_average,'o-')
#    axis.plot([0,1],[0,1],'k--')
#    axis.set_xlim(0,1)
#    axis.set_ylim(0,1)
#    set_aspect(axis)
#    
#sys.exit()
#
F=[]
R=[]
fig1,ax1=plt.subplots(1,1)
fit='Rn:0'
from utils.matlab import load_dpsd
folders=sorted(os.listdir(input_dir))
for ind, folder in enumerate(folders):
    directory=input_dir+folder+'/'
    data=load_dpsd(params.N_t,directory,N_o=len(params.offset),fit=fit)
    data=data[m]
    ax1.scatter(data['F'][0][noise_ind],data['R'][0][noise_ind],color=colors[ind],label=folder)
    R.append(data['R'][0][noise_ind])
    F.append(data['F'][0][noise_ind])
#
#
ax1.legend(numpoints=1)
ax1.set_ylabel('R',fontsize=16)
ax1.set_xlabel('F',fontsize=16)

#control='0.7778'
#pfc='0.0'
#fig3,axes3=plt.subplots(1,2)
#folders=sorted(os.listdir(input_dir))
#centers=[0,0.5]
#offset=0
#width=0.1
#labels=['Control','PFC']
#for ind, folder in enumerate([control,pfc]):
#    color_ind=folders.index(folder)
#    directory=input_dir+folder+'/'
#    data=load_dpsd(params.N_t,directory,N_o=len(params.offset),fit=fit)
#    data=data[m]
#    hits_observed=data['hits'][0][noise_ind]
#    fa_observed=data['fa'][0][noise_ind]
#    
#    roc_hit=data['roc_hit'][0][:,noise_ind]
#    roc_fa=data['roc_fa'][0][:,noise_ind]
#    axes3[0].plot(roc_fa,roc_hit, color=colors[color_ind],label=labels[ind])
#    axes3[0].plot(fa_observed,hits_observed,'o', color=colors[color_ind])
#    axes3[0].set_xlim(-0.0,1)
#    axes3[0].set_ylim(0,1)
#    axes3[0].legend()
#    set_aspect(axes3[0])
#    axes3[1].bar(centers[0]+offset,data['R'][0][noise_ind], width,color=colors[color_ind])
#    axes3[1].bar(centers[1]+offset,data['F'][0][noise_ind],width, color=colors[color_ind])
#    axes3[1].set_xticks(np.add(centers,width))
#    axes3[1].set_xticklabels(["R","F"],fontsize=14)
#    set_aspect(axes3[1])
#    offset+=0.15
