#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 02:00:45 2021

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
          self.p=-1
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
        self.title = f'p={params.pat_sep[self.p]}, o={params.offset[self.o]}, {omega}={params.noise[self.nn]}'

        for key in self.plot_defaults.keys():
             if self.plot_defaults[key]['run']:
                 plot = getattr(self, key)
                 plot()
   
      def empty_figure(self,name):
        print(self.plot_defaults.keys())
        fig_index = list(self.plot_defaults.keys()).index(name)
        fig = self.figs[fig_index][0]
        ax = self.figs[fig_index][1]
        return fig,ax

      def distance_histograms(self, param=''):
        params = self.params
        name = 'distance_histograms'
#        fig,axes = self.empty_figure(name)
        fig,axes=plt.subplots(1,3,figsize=(8,8))
        plot_data={'targ-hist-freq'+param:[],'lure-hist-freq'+param:[],'targ-hist-bins'+param:[],'lure-hist-bins'+param:[],'threshold_range'+param:[]}
        print(plot_data.keys())
        for key in plot_data.keys():
            plot_data[key]=get_data(self.data[:params.hip+1],key,params.offset,params.noise[self.nn])
        for o in range(len(params.offset)): 
            count=0
            for m in params.pat_sep[::2]:
                target_bins = plot_data['targ-hist-bins'+param][params.pat_sep.index(m)][o]
                target_freq = plot_data['targ-hist-freq'+param][params.pat_sep.index(m)][o]
                lure_bins = plot_data['lure-hist-bins'+param][params.pat_sep.index(m)][o]
                lure_freq = plot_data['lure-hist-freq'+param][params.pat_sep.index(m)][o]
                try:
                    ax = axes[count]
                except:
                    ax = axes
                count += 1
                ax.bar(target_bins[:-1],target_freq,width=np.diff(target_bins)[0],color='tab:green',alpha=.8,label="Target")
                ax.bar(lure_bins[:-1],lure_freq,width=np.diff(target_bins)[0],color='tab:purple',alpha=.8,label="Lure")
                [ax.plot([item]*2,[0,params.N_t*.7], 'k--') for item in plot_data['threshold_range'+param][params.pat_sep.index(m)][o]]
                [ax.plot([item+0.02]*2,[0,params.N_t*.7], '--',color='gray',alpha=0.5) for item in plot_data['threshold_range'+param][params.pat_sep.index(m)][o]]

                if m == params.pat_sep[::2][-1]:
                    custom_axis(ax,{'xlabel':{'text':' '},
                        'ylabel':{'text':''},'xlim':{'xlimit':(-0.03,1)},'ylim':{'ylimit':(0,int(params.N_t*.6))},
                        'legend':{'size':14,'bbox_to_anchor':None}})
                elif count == 1:
                    custom_axis(ax,{'xlabel':{'text':''},
                        'ylabel':{'text':f'{omega}={params.noise[self.nn]}\nCount'},'xlim':{'xlimit':(-0.03,1)},'ylim':{'ylimit':(0,int(params.N_t*.6))}})  
                else:
                    custom_axis(ax,{'xlabel':{'text':'Distance'},
                        'ylabel':{'text':''},'xlim':{'xlimit':(-0.03,1)},'ylim':{'ylimit':(0,int(params.N_t*.6))}})

                ax.set_title(f'p={m}',loc='center', fontsize=16)

            fig.tight_layout()
            fig.suptitle(self.title,fontsize=14,y=.7)
            if params.save_figs:
                fig.savefig(f"{self.output_dir}/{name}-{params.noise[self.nn]}-{params.simID}.pdf")
    
      def rates(self):
        name = 'rates'
        fig,axes=plt.subplots(1,2,figsize=(8,8))

        params = self.params

        for ind,item in enumerate(self.data):
            N=params.N_t
            target = get_data(item[self.p],'target',params.offset[self.o],params.noise[self.nn])
            lure = get_data(item[self.p],'lure',params.offset[self.o],params.noise[self.nn])
            hit = calc_rates(target,N)[:-1]
            fa = calc_rates(lure,N)[:-1]
            x_values=np.arange(1,len(fa)+1)

            ax[0].plot(x_values,hit,'o-',color=self.colors[ind],alpha=self.alphas[ind],marker=self.markers[ind],label=f"{self.aux}= {self.labels[ind]}")
            ax[1].plot(x_values,fa,'o-',color=self.colors[ind],alpha=self.alphas[ind],marker=self.markers[ind],label=f"{self.aux}= {self.labels[ind]}")
            
        custom_axis(ax[0],{'xlabel':{'text':'#Threshold'},
                        'ylabel':{'text':'Hit rate'},'xlim':{'xlimit':(min(x_values),max(x_values))}})
        
        custom_axis(ax[1],{'xlabel':{'text':'#Threshold'},
                        'ylabel':{'text':'False alarm rate'},'xlim':{'xlimit':(min(x_values),max(x_values))},
                        'legend':{'size':14,'bbox_to_anchor':(1.03, 1.03)}})
        fig.tight_layout()
        fig.suptitle(self.title,fontsize=14,y=.7)
        if params.save_figs:
            fig.savefig(f"{self.output_dir}{self.effect}-{name}-{self.params.noise[self.nn]}-{params.simID}.pdf")
