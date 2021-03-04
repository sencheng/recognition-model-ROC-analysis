#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 23:47:28 2019

@author: olya
"""

import matplotlib.pyplot as plt
from analysis.plot_utils import *
from utils.utils import check_directory
from utils.utils import list_chronologically

from pylab import rcParams
import numpy as np
import pandas as pd
import os

class plot:
    
    def __init__(self,params,data):
        self.params=params
        self.N=params.list_length
        self.input_dir=params.data_dir
        self.output_dir=params.path+'/Figures/'
        check_directory(self.output_dir)
        self.data=data
        self.fig_format='.pdf'
        filenames=sorted([item for item in os.listdir(self.input_dir) if item[-3:]=='pkl'])
        self.data_observed=[pd.read_pickle(self.input_dir+file) for file in filenames]

    
    def features_line(self,nn,o,figsize=(8,8),save=True):
        from scipy.stats import linregress

        pat_sep=self.params.pat_sep
        params=self.params
        data=self.data[:len(pat_sep)]
        rcParams["figure.figsize"]=figsize
        fig,axes=plt.subplots(1,2)
        F=[item['F'][o][nn] for item in data]
        R=[item['R'][o][nn] for item in data]
        slope_R=np.round(linregress(pat_sep,R)[0],1)
        slope_F=np.round(linregress(pat_sep,F)[0],1)

        axes[0].plot(pat_sep,F,'go-',label='F, slope=%s' %slope_F)
        axes[0].plot(pat_sep,R,'bo-',label='R, slope=%s' %slope_R)
        axis_default(axes[0],'Pattern separation','Parameter',limit=[[min(pat_sep),max(pat_sep)],[0,0.8]],legend=True,leg_size=10,aspect=True)
        axes[0].set_title('Noise=%s' %params.noise[nn],fontsize=16, fontweight='bold')

        slope=np.round(linregress(F,R)[0],1)
        axes[1].plot(F,R,'bo-',label=slope)
        axis_default(axes[1],'F','R',legend=True,leg_size=10,aspect=True)
        fig.tight_layout()
    
    def features_heatmap(self,o,figsize=(10,10),save=True):
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        from utils.calculations import zscore
        data=self.data[:len(self.params.pat_sep)]
        params=self.params
        rcParams["figure.figsize"]=figsize
#        print(np.shape(data))

        fig,axes=plt.subplots(1,3)        
        keys=['R','F','auc']
        
        for key in keys:
            par=[item[key][o] for item in data]
            noise=params.noise
            par=zscore(par)
            x_min=np.min(par)
            x_max=np.max(par)
            ind=keys.index(key)
            im=axes[ind].imshow(par,origin='lower')
            axis_default(axes[ind],omega,'p',aspect=True,labelsize=16,ticksize=14)
            
            axes[ind].set_xticklabels(np.round(np.linspace(noise[0],noise[-1],3),2))
            axes[ind].set_yticklabels(np.linspace(params.pat_sep[0],params.pat_sep[-1],3))
            
            name=''.join([item.capitalize() for item in key])
            axes[ind].set_title('z'+name,fontsize=16)
            divider = make_axes_locatable(axes[ind])
            cax = divider.new_vertical(size="5%",pad=0.7,pack_start=True)
    
            fig.add_axes(cax)
            ticks=np.linspace(x_min,x_max,3)
            colorbar=fig.colorbar(im, cax=cax,orientation="horizontal")
            tick_lab=[str(np.round(t,1)) for t in ticks]
            colorbar.set_ticks(ticks)
            colorbar.set_ticklabels(tick_lab) 

        fig.tight_layout()
        if save==True:
           fig.savefig(self.output_dir + 'Heatmap'+"_"+str(self.N)+"_"+ params.simID + self.fig_format,dpi=300)

        
    def noise_effect(self,o,m,figsize=(10,8),save=True,title=''):
        from scipy.stats import linregress
        params=self.params
        noise=params.noise
        data=self.data
        rcParams["figure.figsize"]=figsize
        fig,axes=plt.subplots(1,2)    
        keys=['R','F','auc']            
        noise_ind=[params.noise.index(item) for item in noise]
        
        colors= plt.rcParams['axes.prop_cycle'].by_key()['color']
        cols=['slategray','slategray','slategray']
        alphas=np.linspace(0.3,1,len(noise)+1)[::-1]
        colors=['slategray']*len(noise)
        color='slategray'
        for ind,key in enumerate(keys):
            par=[data[m][key][o][nn] for nn in noise_ind]
            axes[1].plot(noise,par,color=cols[keys.index(key)],marker=markers[ind],label=key)
        axis_default(axes[1],omega,'Parameter',limit=[[noise[0],noise[-1]],[0,1]],legend=True,aspect=True,r=2)
        [axes[0].plot(data[m]['roc_fa'][o][:,nn],data[m]['roc_hit'][o][:,nn],color=color) for nn in noise_ind]
        
        for nn in noise_ind:
            fa_obs=data[m]['fa'][o][nn] 
            hit_obs=data[m]['hits'][o][nn] 
            axes[0].plot(fa_obs,hit_obs,'o', color=color,marker=markers[noise_ind.index(nn)],label='\u03C9=%s'%np.round(params.noise[nn],2)) 
        axes[0].plot([0,1],[0,1.01],'k--')
        axis_default(axes[0],'False alarm rate','Hit rate',limit=[[0,1],[0,1]],legend=True,aspect=True,labelsize=16)
        fig.suptitle('p='+title,fontsize=14, fontweight='bold',y=0.85)
        fig.tight_layout()
        if save==True:
           fig.savefig(self.output_dir + 'Noise_effect'+"_"+str(self.N)+"_"+str(params.pat_sep[m])+"_"+ params.simID + self.fig_format, dpi=300)


    def cue_target(self,nn,m=-1,figsize=(8,8),save=True):
        params=self.params
        data=self.data
        data_observed=self.data_observed
        fig,axes=plt.subplots(1,2)
        colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
        
        for o in range(len(params.offset)):
            hit=np.asarray(data[m]['roc_hit'])[o]
            fa=np.asarray(data[m]['roc_fa'])[o]
            fa_obs=data[m]['fa'][o]
            hit_obs=data[m]['hits'][o]
#            fa_obs,hit_obs=calc_rates(data_observed[m].loc[params.offset[o]][params.noise[nn]]['lure'],params.N_t),calc_rates(data_observed[m].loc[params.offset[o]][params.noise[nn]]['target'],params.N_t)
            axes[0].plot(fa[:,nn],hit[:,nn],label=params.offset[o],color=colors[o])
            axes[0].plot(fa_obs[nn],hit_obs[nn],'o',color=colors[o])
            axes[0].plot([0,1],[0,1],'k--')
            axis_default(axes[0],'False alarm rate','Hit rate',legend=True,leg_size=12,aspect=True)
        
        R=np.asarray(data[m]['R'])[:,nn]
        F=np.asarray(data[m]['F'])[:,nn]
        axes[1].plot(params.offset[:],R,'bo-',label='R')
        axes[1].plot(params.offset[:],F,'go-',label='F')
        axis_default(axes[1],'Offset','Parameter',legend=True,leg_size=12,aspect=True)
        fig.tight_layout()
        
    def overlap_effect(self,nn=2,figsize=(10,10),save=True):
        params=self.params
        data=self.data
        pat_sep_ind=np.arange(len(params.pat_sep))[::2]
        pat_seps=np.asarray(params.pat_sep)[pat_sep_ind]
        fig,axes=plt.subplots(1,len(pat_seps),figsize=figsize)
        off_ind=np.arange(len(params.offset))#[::2]
        off=np.asarray(params.offset)[off_ind]
        for ind, ax in enumerate(axes):
            m=pat_sep_ind[ind]
            for o_ind,o in enumerate(off_ind):
                lab=(10-off[o_ind])*10
                hit=np.asarray(data[m]['roc_hit'])[o]
                fa=np.asarray(data[m]['roc_fa'])[o]
                fa_obs=data[m]['fa'][o]
                hit_obs=data[m]['hits'][o]
                ax.plot(fa[:,nn],hit[:,nn],color=colors[o_ind])
                ax.plot(fa_obs[nn],hit_obs[nn],'o',color=colors[o_ind],label=f"{lab}%")
                ax.plot([0,1],[0,1],'k--')
            if ind==len(axes)-1:
                custom_axis(ax,{'xlabel':{'text':'False alarm rate'},
                                'ylabel':{'text':'Hit rate'}})
            else:
                custom_axis(ax,{'xlabel':{'text':'False alarm rate'},
                                'ylabel':{'text':'Hit rate'}})
            ax.set_title(f"p= {pat_seps[ind]}",fontsize=14)

        fig.tight_layout()
        ax.legend(ncol=len(params.offset),bbox_to_anchor=(.5, -0.3),prop={'size':12})
        fig.suptitle(f"{omega}={params.noise[nn]}",fontsize=14, fontweight='bold',y=0.7)
        if save==True:
           fig.savefig(self.output_dir + 'overlap_effect'+"_"+str(self.N)+"_"+str(params.pat_sep[m])+"_"+ params.simID + self.fig_format, dpi=300)

        
                



        


            
            
        
        
        

