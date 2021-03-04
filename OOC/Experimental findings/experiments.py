#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 16:44:25 2019

@author: olya
"""
import sys
sys.path.append('../Code/')
from utils.calculations import normalize_F
from analysis.plot_utils import set_aspect,custom_axis
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pylab import rcParams
#
class plot_findings:
    def __init__(self,name, figsize=(4,4)):
        self.name=name
        self.data=pd.read_csv(name)
        rcParams["figure.figsize"]=figsize

    def F_and_R(self):
        data=self.data
        F_time=normalize_F(data.iloc[:5][:]['F'])
        R_time=data.iloc[:5][:]['R']
        cond=data.iloc[:5][:]['Condition']
        fig,ax=plt.subplots(1,1)
        ax.plot(F_time,'go-',label='F')
        ax.plot(R_time,'bo-',label='R')
        plt.xticks(range(len(cond)), cond, fontsize=14)
        ax.legend(prop={'size':15})
        ax.set_title(self.name,fontsize=15)
        set_aspect(ax)
 
    def criteria(self,hit=False,fa=False):
        data=self.data
        amnesic_fa=data.iloc[0][::-1]
        control_fa=data.iloc[3][::-1]
        amnesic_fa=amnesic_fa[:-1]
        control_fa=control_fa[:-1]
        
        amnesic_hit=data.iloc[1][::-1]
        control_hit=data.iloc[4][::-1]
        amnesic_hit=amnesic_hit[:-1]
        control_hit=control_hit[:-1]
        
        if fa:
            fig,ax=plt.subplots(1,1)
            ax.plot(np.arange(1,7,1),np.cumsum(amnesic_fa),'ro-')
            ax.plot(np.arange(1,7,1),np.cumsum(control_fa),'go-')
            ax.plot()
            ax.set_title(self.name, fontsize=16)
            ax.set_ylabel('False alarms',fontsize=16)
            ax.set_xlabel('Threshold',fontsize=16)
            set_aspect(ax)
            
        if hit:
            fig,ax=plt.subplots(1,1)
            ax.plot(np.arange(1,7,1),np.cumsum(amnesic_hit),'ro-')
            ax.plot(np.arange(1,7,1),np.cumsum(control_hit),'go-')
            ax.set_title(self.name, fontsize=16)
            ax.set_ylabel('Hits',fontsize=16)
            ax.set_xlabel('Threshold',fontsize=16)
            set_aspect(ax)
#        
#            
            
class ratcliff:
    def __init__(self):
        self.data={'experiment1':{'hits':{},'fa':{}},'experiment2':{'hits':{},'fa':{}}}
        self.keys=['strong_mixed','weak_mixed','hits_strong','hits_weak']
        hit_values1=[[0.595, 0.68, 0.788, 0.828, 0.928],[.419, 0.498, 0.636, 0.691, 0.817],
            [0.554, 0.694, 0.757, 0.82, 0.907],[0.446, 0.561, 0.685, 0.751, 0.849]]
        
        fa_values1=[[0.096, 0.196, 0.27, 0.405, 0.51],[0.096, 0.196, 0.27, 0.405, 0.51],
                    [0.083, 0.179, 0.27, 0.363, 0.505],[0.111, 0.224, 0.313, 0.402, 0.586]]
        
        hit_values2=[[0.829, 0.87, 0.937, 0.967, 0.985], [0.56, 0.675, 0.77, 0.803, 0.921],
             [0.734, 0.843, 0.93, 0.924, 0.978],[0.621, 0.732, 0.794, 0.848, 0.935]]
        
        fa_values2=[[0.034, 0.093, 0.144, 0.19, 0.427],[0.034, 0.093, 0.144, 0.19, 0.427],
                    [0.026, 0.084, 0.134, 0.202, 0.334],[0.034, 0.109, 0.199, 0.275, 0.421]]
        
        self.data['experiment1']['hits']=dict(zip(self.keys, hit_values1))
        self.data['experiment2']['hits']=dict(zip(self.keys,hit_values2))
        self.data['experiment1']['fa']=dict(zip(self.keys, fa_values1))
        self.data['experiment2']['fa']=dict(zip(self.keys,fa_values2))
        self.data['experiment1']['notes']={'strenghtening':'longer study time','N of participants':4,'material':'words'}
        self.data['experiment2']['notes']={'strenghtening':'repetition','N of participants':7,'material':'words'}

    def plot_results(self,experiment):
        fig,axes=plt.subplots(1,3,figsize=(10,10))
        hits=self.data[experiment]['hits']
        fa=self.data[experiment]['fa']
        markers=['go--','ro--','go-','ro-']
        for ind, item in enumerate(self.keys):
            axes[0].plot(hits[item],markers[ind],label=item)
            axes[1].plot(fa[item],markers[ind],label=item)
            axes[2].plot(fa[item],hits[item],markers[ind],label=item)

#        axis_default(axes[0],'Criterion','Hit rate',legend=True,limit=[[0,len(hits[item])],[0,1]])
#        axis_default(axes[1],'Criterion','False alarm rate',limit=[[0,len(fa[item])],[0,1]],legend=False)
#        axis_default(axes[2],'False alarm rate','Hit rate',limit=[[0,1],[0,1]],legend=False)
        [set_aspect(ax) for ax in axes]
        fig.tight_layout()
        fig.suptitle('Ratcliff et al. 1992 '+experiment,fontsize=15,y=.75)

class list_strength:
    def __init__(self,filename):
        self.data = pd.read_csv(filename,sep=';',index_col=False)
        self.name = filename
        self.experiments = self.data['experiment']
        self.notes=self.data['notes']
#        self.hit_keys = [item for item in self.data.columns if 'hit' in item]
#        self.fa_keys = [item  for item in self.data.columns if 'fa' in item]
        self.hit_keys = ['hit S','hit MS','hit W','hit MW']
        self.fa_keys = ['fa S', 'fa MS','fa W','fa MW']

    def plot_experiment(self,experiment):
        experiment -= 1
        exp = self.experiments[experiment]
        fig,axes = plt.subplots(1,2,figsize=(8,8))
        hit = self.data.loc[experiment,self.hit_keys]
        fa = self.data.loc[experiment,self.fa_keys]
        hit.plot.bar(ax=axes[0],x='lab',y='val',rot=0,colors=['g','g','crimson','crimson'])
        fa.plot.bar(ax=axes[1],x='lab', y='val', rot=0,colors=['g','g','crimson','crimson'])
#        axis_default(axes[0],' ','Hit rate',legend=False,limit=[[None,None],[0,1]],ticks=False)
#        axis_default(axes[1],' ','False alarm rate',legend=False,limit=[[None,None],[0,1]],ticks=False)
        [set_aspect(ax) for ax in axes]
        fig.tight_layout()
        fig.suptitle(self.name+': experiment '+str(exp)+'*',fontsize=15,y=.75)
        plt.gcf().text(0.1, .2, '*'+self.notes[experiment], fontsize=14)
        
        
rat = ratcliff()
rat.plot_results('experiment1')
rat.plot_results('experiment2')
import sys
hirschmann = list_strength('Hirschmann')
hirschmann.plot_experiment(1)
hirschmann.plot_experiment(2)
hirschmann.plot_experiment(3)
hirschmann.plot_experiment(4)
#
murnane = list_strength('Murnane&Shiffrin91')
murnane.plot_experiment(1)
murnane.plot_experiment(2)
sys.exit()
#

weak_hits=[.55,.73,.77,.82,.92]
weak_sp=[.24,.40,.45,.52,.72]
weak_ur=[.05,.13,.18,.33,.65]

strong_hits=[.38,.60,.64,.70,.82]
strong_sp=[.14,.30,.36,.43,.64]
strong_ur=[.02,.06,.09,.19,.41]


fig,axes=plt.subplots(1,3)    
axes[0].plot(weak_hits,'ro-')
axes[0].plot(strong_hits,'go-')
axes[1].plot(weak_sp,'ro-')
axes[1].plot(strong_sp,'go-')
axes[2].plot(weak_ur,'ro-')
axes[2].plot(strong_ur,'go-')
axes[0].set_title('Hit rates')
axes[1].set_title('SP false alarms')
axes[2].set_title('UL false alarms')

[set_aspect(ax) for ax in axes]
fig.tight_layout()


fig1,axes1=plt.subplots(1,3)
axes1[0].plot(weak_ur,weak_hits,'ro-')
axes1[0].plot(strong_ur,strong_hits,'go-')
axes1[1].plot(weak_sp,weak_hits,'ro-')
axes1[1].plot(strong_sp,strong_hits,'go-')
axes1[2].plot(weak_ur,weak_sp,'ro-')
axes1[2].plot(strong_ur,strong_sp,'go-')
axes1[0].set_title('ROC for UL')
axes1[1].set_title('ROC for SP**')
axes1[2].set_title('ROC UL vs SP**')

[set_aspect(ax) for ax in axes1]
fig1.tight_layout()


