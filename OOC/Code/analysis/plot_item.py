#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 16:22:26 2020

@author: olya
"""

import matplotlib.pyplot as plt
from utils.utils import check_directory,list_chronologically
from utils.calculations import calc_rates
from utils.data import get_data
from analysis.plot_utils import *
import os
import pandas as pd
import numpy as np


class plot_individual:
      def __init__(self,params,nn=2,cond = '30'):
          self.cond=cond
          self.input_dir = f'{params.path}/Data/{params.simID}/{cond}/'
          self.params = params
          self.output_dir = params.path+'/Figures/'
          check_directory(self.output_dir)
          self.fig_format='pdf'
          self.save=params.save_figs
          self.nn=nn
          self.o=-1
          self.fit='Rn:0'
          self.title = f'o={params.offset[self.o]}, {omega}={params.noise[self.nn]}, cond={cond}'

          
      def load_data(self):
          # load the general data
          filenames=sorted([item for item in os.listdir(self.input_dir) if item[-3:]=='pkl' and 'std' not in item])
          self.data=[pd.read_pickle(self.input_dir+file) for file in filenames]
          
      def load_dpsd_data(self):
          from utils.matlab import matlab
          mat = matlab(self.params)
          self.data_dpsd,conds = mat.load_dpsd(fit=self.fit,filenames=[self.cond])
          self.data_dpsd = self.data_dpsd[0]

  
          
      def run(self):
        params = self.params
        self.figs = [plt.subplots(self.plot_defaults[item]['nrows'],self.plot_defaults[item]['ncols'],figsize=self.plot_defaults[item]['figsize']) for item in self.plot_defaults.keys()]
        self.title = f'p={params.scale[self.p]}, o={params.offset[self.o]}, {omega}={params.noise[self.nn]}'

        for key in self.plot_defaults.keys():
             if self.plot_defaults[key]['run']:
                 plot = getattr(self, key)
                 plot()
   
      def empty_figure(self,name):
        fig_index = list(self.plot_defaults.keys()).index(name)
        fig = self.figs[fig_index][0]
        ax = self.figs[fig_index][1]
        return fig,ax

      def distance_histograms(self):
        params = self.params
        name = 'distance_histograms'
#        fig,axes = self.empty_figure(name)
        fig,axes=plt.subplots(1,3,figsize=(8,8))

        plot_data={'targ-hist-freq':[],'lure-hist-freq':[],'targ-hist-bins':[],'lure-hist-bins':[],'threshold_range':[]}

        for key in plot_data.keys():
            plot_data[key]=get_data(self.data[:params.hip+1],key,params.offset,params.noise[self.nn])

        for o in range(len(params.offset)): 
            count=0
            for m in params.scale[::2]:
                target_bins = plot_data['targ-hist-bins'][params.scale.index(m)][o]
                target_freq = plot_data['targ-hist-freq'][params.scale.index(m)][o]
                lure_bins = plot_data['lure-hist-bins'][params.scale.index(m)][o]
                lure_freq = plot_data['lure-hist-freq'][params.scale.index(m)][o]
                try:
                    ax = axes[count]
                except:
                    ax = axes
                count += 1
                ax.bar(target_bins[:-1],target_freq,width=np.diff(target_bins)[0],color='tab:green',alpha=.8,label="Target")
                ax.bar(lure_bins[:-1],lure_freq,width=np.diff(target_bins)[0],color='tab:purple',alpha=.8,label="Lure")
                [ax.plot([item]*2,[0,params.N_t*.7], 'k--') for item in plot_data['threshold_range'][params.scale.index(m)][o]]
                [ax.plot([item+0.02]*2,[0,params.N_t*.7], '--',color='gray',alpha=0.5) for item in plot_data['threshold_range'][params.scale.index(m)][o]]

                if m == params.scale[::2][-1]:
                    custom_axis(ax,{'xlabel':{'text':' '},
                        'ylabel':{'text':''},'xlim':{'xlimit':(-0.03,0.2)},'ylim':{'ylimit':(0,int(params.N_t*.6))},
                        'legend':{'size':14,'bbox_to_anchor':None}})
                elif count == 1:
                    custom_axis(ax,{'xlabel':{'text':''},
                        'ylabel':{'text':f'{omega}={params.noise[self.nn]}\nCount'},'xlim':{'xlimit':(-0.03,0.2)},'ylim':{'ylimit':(0,int(params.N_t*.6))}})  
                else:
                    custom_axis(ax,{'xlabel':{'text':'Distance'},
                        'ylabel':{'text':''},'xlim':{'xlimit':(-0.03,0.2)},'ylim':{'ylimit':(0,int(params.N_t*.6))}})

                ax.set_title(f'p={m}',loc='center', fontsize=16)

            fig.tight_layout()
            fig.suptitle(self.title,fontsize=14,y=.7)
            if params.save_figs:
                fig.savefig(f"{self.output_dir}/{name}-{params.noise[self.nn]}-{params.simID}.pdf")

      def correct_retrieval(self,info='targ-match'):
        params = self.params
        name = 'correct-retrieval'
#        fig,axes = self.empty_figure(name)
        fig = plt.figure(figsize=(6,6))
        if np.mod(len(params.offset),2) == 0:
          loop = len(params.offset)
        elif len(params.offset) == 1:
            loop = 1
        else:
          loop = len(params.offset)-1
        
        for o in range(loop):
           ax = fig.add_subplot(2,int(np.ceil(loop/2)),o+1) 
           plot_data = {info:[]}
           for key in plot_data.keys():
               plot_data[key] = get_data(self.data[:params.hip+1],key,params.offset[o],params.noise)
           [ax.plot(params.noise,plot_data[key][params.scale.index(item)],'o-',color='k',alpha=0.7,marker=markers[ind],label='p=%s'%item) for ind,item in enumerate(params.scale[:params.hip+1])]
           custom_axis(ax,{'xlabel':{'text': omega},
                        'ylabel':{'text':'Correct retrieval'},'xlim':{'xlimit':(min(params.noise),max(params.noise))},'ylim':{'ylimit':(0.3,1)},'xticks':{'round':2},
                        'legend':{'size':14,'bbox_to_anchor':None}})

        fig.tight_layout()
        fig.suptitle(self.title,fontsize=14,y=1.1)
        if params.save_figs:
           fig.savefig(f"{self.output_dir}/{name}-{self.params.noise[self.nn]}-{params.simID}.pdf")
    
      def features_heatmap(self):
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        from utils.calculations import zscore

        params = self.params
        name = 'features-heatmap'
        data = self.data_dpsd
        fig,axes = plt.subplots(1,3, figsize=(8,8))
        keys=['R','F','auc']
        
        for ind,key in enumerate(keys):
            keyName = ''.join([item.capitalize() for item in key])

            par = [item[key][self.o] for item in data]
            noise = params.noise
            par = zscore(par)
            x_min = np.min(par)
            x_max = np.max(par)
            ind = keys.index(key)
            im = axes[ind].imshow(par,origin='lower')
            divider = make_axes_locatable(axes[ind])
            cax = divider.new_vertical(size="5%",pad=0.7,pack_start=True)
    
            fig.add_axes(cax)
            ticks = np.linspace(x_min,x_max,3)
            colorbar = fig.colorbar(im, cax=cax,orientation="horizontal")
            tick_lab = [str(np.round(t,1)) for t in ticks]
            colorbar.set_ticks(ticks)
            colorbar.set_ticklabels(tick_lab) 
            colorbar.ax.tick_params(labelsize=14)             
            if ind == 0:
                custom_axis(axes[ind],{
                            'ylabel':{'text':'p'},'set_title':{'text':f'z{keyName}','titlesize':16,'offset':3}})
            elif ind == 1:
                custom_axis(axes[ind],{'xlabel':{'text':omega},
                            'set_title':{'text':f'z{keyName}','titlesize':16,'offset':3}})
            else:
                custom_axis(axes[ind],{
                            'set_title':{'text':f'z{keyName}','titlesize':16,'offset':3}})
            axes[ind].set_xticklabels(np.round(np.linspace(noise[0],noise[-1],3),2))
            axes[ind].set_yticklabels(np.linspace(params.scale[0],params.scale[-1],3))

        fig.tight_layout()
        fig.suptitle(self.title,fontsize=14,y=.7)
        if params.save_figs:
           fig.savefig(f"{self.output_dir}/{name}-{self.cond}-{params.simID}.pdf")

      def noise_effect(self,m=-1):
        params = self.params
        name = 'noise-effect'
        data = self.data_dpsd
        fig,axes = plt.subplots(1,2, figsize=(7,7))
        keys = ['R','F','auc']
        noise_ind = [params.noise.index(item) for item in params.noise]
        
        for ind, key in enumerate(keys):
            keyName = ''.join([item.capitalize() for item in key])
            par = [data[m][key][self.o][nn] for nn in noise_ind]
            axes[1].plot(params.noise,par,color='k',alpha=0.7,marker=markers[ind],label=keyName)
        
        custom_axis(axes[1],{'xlabel':{'text': omega},
                    'ylabel':{'text':'Estimate'},'xlim':{'xlimit':(min(params.noise),max(params.noise))},'ylim':{'ylimit':(0,1)},'xticks':{'round':2},
                    'legend':{'size':12,'bbox_to_anchor':None}})
    

        for nn in noise_ind:
            fa_obs = data[m]['fa'][self.o][nn]
            hit_obs = data[m]['hits'][self.o][nn]
            axes[0].plot(fa_obs,hit_obs,'o', color='k',alpha=0.7,marker=markers[noise_ind.index(nn)],label='\u03C9=%s'%np.round(params.noise[nn],2)) 
            axes[0].plot(data[m]['roc_fa'][self.o][:,nn],data[m]['roc_hit'][self.o][:,nn],color='k',alpha=0.8,)
        axes[0].plot([0,1],[0,1.01],'k--')
        
        if nn == noise_ind[-1]:
            custom_axis(axes[0],{'xlabel':{'text': 'False alarm rate'},
                            'ylabel':{'text':'Hit rate'},'xlim':{'xlimit':(-0.03,1.03)},'ylim':{'ylimit':(-0.03,1.03)},
                            'legend':{'size':12,'bbox_to_anchor':None}})
       
        fig.tight_layout()
        fig.suptitle(self.title,fontsize=14,y=.75)
        if params.save_figs:
           fig.savefig(f"{self.output_dir}/{name}-{self.cond}-{params.simID}.pdf")

    
      def roc_curves(self):

        params = self.params
        name = 'roc-curves'
        try:
            data = self.data_dpsd
        except:
            data = self.data
        fig,ax= plt.subplots(1,1, figsize=(3.2,3.2))
        
        scale=list(range(len(params.scale)))[::2]

        for ind, item in enumerate(scale):
            try:
                ax.plot(data[item]['fa'][self.o][self.nn],data[item]['hits'][self.o][self.nn],markers[ind],label=f'p={params.scale[item]}',color='k',alpha=.8)
                ax.plot(data[item]['roc_fa'][self.o][:,self.nn],data[item]['roc_hit'][self.o][:,self.nn],color='k',alpha=.8)
            except:
#                from analysis.experimental_data import retrieve_experimental_data

#                fa_control, hit_control,fa_patient,hit_patient,R_exp,F_exp=retrieve_experimental_data('Farovik et al. 2008')
                target = get_data(data[item],'target',params.offset[self.o],params.noise[self.nn])
                lure = get_data(data[item],'lure',params.offset[self.o],params.noise[self.nn])
                hit = calc_rates(target,params.N_t)
                fa = calc_rates(lure,params.N_t)
                
                ax.plot(fa,hit,'o-',label=f'p={params.scale[item]}')
#                ax.plot(fa_control,hit_control,'ko-')

        ax.plot([0,1],[0,1],'k--')
        custom_axis(ax,{'xlabel':{'text': 'False alarm rate'},
                        'ylabel':{'text':'Hit rate'},'xlim':{'xlimit':(-0.03,1.03)},'ylim':{'ylimit':(-0.03,1.03)},
                        'legend':{'size':14,'bbox_to_anchor':None}})
       
        fig.tight_layout()
        fig.suptitle(self.title,fontsize=14,y=1.)
        if params.save_figs:
           fig.savefig(f"{self.output_dir}/{name}-{self.params.noise[self.nn]}-{self.cond}-{params.simID}.pdf")
      
      def overlap_rates(self):
           params=self.params
           name = 'overlap-rates'
           data=self.data
           scale_ind=np.arange(len(params.scale))[::2]
           scales=np.asarray(params.scale)[scale_ind]
           fig,axes=plt.subplots(1,len(scales),figsize=(10,10))
 

      def overlap_effect(self):
            params=self.params
            name = 'overlap-effect'
            data=self.data_dpsd
            scale_ind=np.arange(len(params.scale))[::2]
            scales=np.asarray(params.scale)[scale_ind]
            fig,axes=plt.subplots(1,len(scales),figsize=(10,10))
            
            off_ind=np.arange(len(params.offset))#[::2]
            off=np.asarray(params.offset)[off_ind]
            for ind, ax in enumerate(axes):
                m=scale_ind[ind]
                for o_ind,o in enumerate(off_ind):
                    lab=(10-off[o_ind])*10
                    hit=np.asarray(data[m]['roc_hit'])[o]
                    fa=np.asarray(data[m]['roc_fa'])[o]
                    fa_obs=data[m]['fa'][o]
                    hit_obs=data[m]['hits'][o]
                    ax.plot(fa[:,self.nn],hit[:,self.nn],color=colors[o_ind])
                    ax.plot(fa_obs[self.nn],hit_obs[self.nn],'o',color=colors[o_ind],label=f"{lab}%")
                    ax.plot([0,1],[0,1],'k--')
                if ind==len(axes)-1:
                    custom_axis(ax,{'xlabel':{'text':'False alarm rate'},
                                    'ylabel':{'text':'Hit rate'}})
                else:
                    custom_axis(ax,{'xlabel':{'text':'False alarm rate'},
                                    'ylabel':{'text':'Hit rate'}})
                ax.set_title(f"p= {scales[ind]}",fontsize=14)
    
            fig.tight_layout()
            ax.legend(ncol=len(params.offset),bbox_to_anchor=(.5, -0.3),prop={'size':14})
            fig.suptitle(self.title,fontsize=14,y=1.)
            if params.save_figs:
                fig.savefig(f"{self.output_dir}/{name}-{self.params.noise[self.nn]}-{self.cond}-{params.simID}.pdf")

      def overlap_hist(self):
        params=self.params
        data=self.data
        name='overlap-hist'
        
        plot_data={'targ-hist-freq':[],'lure-hist-freq':[],'targ-hist-bins':[],'lure-hist-bins':[],'threshold_range':[]}
        for key in plot_data.keys():
            plot_data[key]=get_data(data,key,params.offset,params.noise[self.nn])

        scale_ind=np.arange(len(params.scale))[::2]
        scales=np.asarray(params.scale)[scale_ind]
        
        fig,axes=plt.subplots(1,len(scales),figsize=(10,10))
        off_ind=np.arange(len(params.offset))[::2]#[::2]
        off=np.asarray(params.offset)[off_ind]
        colors=['tab:green','tab:blue','tab:red']
        for ind, ax in enumerate(axes):
            m=scale_ind[ind]
            for o_ind,o in enumerate(off_ind):
                lab=(10-off[o_ind])*10
                if o_ind==0:
                    target_bins=plot_data['targ-hist-bins'][m][o_ind]
                    target_freq=plot_data['targ-hist-freq'][m][o_ind]
                lure_bins=plot_data['lure-hist-bins'][m][o_ind]
                lure_freq=plot_data['lure-hist-freq'][m][o_ind]
                ax.bar(lure_bins[:-1],lure_freq,width=np.diff(target_bins)[0],color=colors[o_ind],alpha=.8,label=f"{lab}%")
                [ax.plot([item]*2,[0,params.N_t*.7], 'k--') for item in plot_data['threshold_range'][m][o][:-1]]

                if o_ind==len(off_ind)-1:
                    ax.bar(target_bins[:-1],target_freq,width=np.diff(target_bins)[0],
                           fc=(1, 1, 1, 0.0), linestyle='-',edgecolor=(0, 0, 0, 1),label="Target")

                custom_axis(ax,{'xlabel':{'text':'Distance'},
                                'ylabel':{'text':'Count'}, 'ylim':{'ylimit':[0,int(params.N_t*.6)]}})
        fig.tight_layout()
        ax.legend(ncol=len(off_ind)+1,bbox_to_anchor=(.2, -0.3),prop={'size':14})
        fig.suptitle(self.title,fontsize=14,y=.7)
        if params.save_figs:
                fig.savefig(f"{self.output_dir}/{name}-{self.params.noise[self.nn]}-{self.cond}-{params.simID}.pdf")

      def overlap_comparison(self):
            params=self.params
            name = 'overlap-comparison'
            data = self.data_dpsd
            fig,ax = plt.subplots()
            x = 100-np.asarray(params.offset)*10
            for ind, m in enumerate(params.scale):
                par = data[ind]['auc'][:,self.nn] 
                ax.plot(x,par,'o-',color='k',marker=markers[ind],alpha=.7,label=f'p={m}')
            custom_axis(ax,{'xlabel':{'text': 'Target-lure similarity'},
                        'ylabel':{'text':'AUC'}})
            ax.legend(prop={'size':14})


            

