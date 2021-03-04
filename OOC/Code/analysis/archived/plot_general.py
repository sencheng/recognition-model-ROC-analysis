#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:55:23 2019

@author: hakobovg
"""

import matplotlib.pyplot as plt
from utils.utils import check_directory,list_chronologically
from utils.calculations import calc_rates
from utils.data import get_data
import pandas as pd
import numpy as np
from pylab import rcParams
from analysis.plot_utils import *
import os
colors=plt.rcParams['axes.prop_cycle'].by_key()['color']

class plot:
    def __init__(self,params):
        self.params=params
        self.N=params.list_length
        self.input_dir=params.data_dir
        self.output_dir=params.path+'/Figures'
        self.fig_format='pdf'
        check_directory(self.output_dir)
        filenames=sorted([item for item in os.listdir(self.input_dir) if item[-3:]=='pkl' and 'std' not in item])
        self.data=[pd.read_pickle(self.input_dir+file) for file in filenames]
        self.save=params.save_figs
        
     
    def distance_histograms(self,nn,figsize=(8,8)):
        params=self.params
        data=self.data
        rcParams["figure.figsize"]=figsize
        
        plot_data={'targ-hist-freq':[],'lure-hist-freq':[],'targ-hist-bins':[],'lure-hist-bins':[],'threshold_range':[]}

        for key in plot_data.keys():
            plot_data[key]=get_data(data[:params.hip+1],key,params.offset,nn)
        for o in range(len(params.offset)): 
            fig,axes=plt.subplots(1,len(params.pat_sep[::2]))
            count=0
            for m in params.pat_sep[::2]:
                target_bins=plot_data['targ-hist-bins'][params.pat_sep.index(m)][o]
                target_freq=plot_data['targ-hist-freq'][params.pat_sep.index(m)][o]
                lure_bins=plot_data['lure-hist-bins'][params.pat_sep.index(m)][o]
                lure_freq=plot_data['lure-hist-freq'][params.pat_sep.index(m)][o]
                try:
                    ax=axes[count]
                except:
                    ax=axes
                count+=1
                ax.bar(target_bins[:-1],target_freq,width=np.diff(target_bins)[0],color='forestgreen',alpha=.8,label="Target")
                ax.bar(lure_bins[:-1],lure_freq,width=np.diff(target_bins)[0],color='purple',alpha=.8,label="Lure")
                
                if params.rec_test=='roc_item' or params.rec_test=='cue_target' :
                    [ax.plot([item]*2,[0,self.N*.7], 'k--') for item in plot_data['threshold_range'][params.pat_sep.index(m)][o]]
                
                elif params.rec_test=='YN_item':
                    ax.plot(plot_data['threshold_range'][params.pat_sep.index(m)][o]*2,[0,self.N*.7], 'k--')
                ax.set_title(m,loc='left', fontsize=14)
                if m==params.pat_sep[::2][-1]:
                    axis_default(ax,'Distance','Count',limit=[[-0.05,0.2],[0,int(self.N*.6)]],legend=True,leg_size=12,aspect=True,ticksize=14,labelsize=16)
                else:
                    axis_default(ax,'Distance','Count',limit=[[-0.05,0.2],[0,int(self.N*.6)]],aspect=True,ticksize=14,labelsize=16)
#                ax.set_ylim(0,90*self.N/100)
    
            fig.tight_layout()
            fig.suptitle('Noise: '+str(np.round(nn,2))+ ' Offset=%s' %str(params.offset[o]), fontsize=14, fontweight='bold',y=.7)
            if self.save:
               try:
                   [ax.set_rasterized(True) for ax in axes]
               except:
                   ax.set_rasterized(True)
#               fig.savefig(self.output_dir + '/DistMem'+"_"+params.cond+"_"+str(nn)+"_"+ params.simID + ".eps", format='eps', dpi=300)
                   
    def overlap_hist(self,nn=2,figsize=(10,10),save=True):
        params=self.params
        data=self.data
        
        plot_data={'targ-hist-freq':[],'lure-hist-freq':[],'targ-hist-bins':[],'lure-hist-bins':[],'threshold_range':[]}
        for key in plot_data.keys():
            plot_data[key]=get_data(data,key,params.offset,params.noise[nn])

        pat_sep_ind=np.arange(len(params.pat_sep))[::2]
        pat_seps=np.asarray(params.pat_sep)[pat_sep_ind]
        
        fig,axes=plt.subplots(1,len(pat_seps),figsize=figsize)
        off_ind=np.arange(len(params.offset))[::2]#[::2]
        off=np.asarray(params.offset)[off_ind]
        colors=['tab:green','tab:blue','tab:red']
        for ind, ax in enumerate(axes):
            m=pat_sep_ind[ind]
            for o_ind,o in enumerate(off_ind):
                lab=(10-off[o_ind])*10
                if o_ind==0:
                    target_bins=plot_data['targ-hist-bins'][m][o_ind]
                    target_freq=plot_data['targ-hist-freq'][m][o_ind]
                lure_bins=plot_data['lure-hist-bins'][m][o_ind]
                lure_freq=plot_data['lure-hist-freq'][m][o_ind]
                ax.bar(lure_bins[:-1],lure_freq,width=np.diff(target_bins)[0],color=colors[o_ind],alpha=.8,label=f"{lab}%")

                if o_ind==len(off_ind)-1:
                    ax.bar(target_bins[:-1],target_freq,width=np.diff(target_bins)[0],
                           fc=(1, 1, 1, 0.0), linestyle='-',edgecolor=(0, 0, 0, 1),label="Target")

                custom_axis(ax,{'xlabel':{'text':'Distance'},
                                'ylabel':{'text':'Count'}, 'ylim':{'ylimit':[0,int(self.N*.6)]}})
        fig.tight_layout()
        ax.legend(ncol=len(off_ind)+1,bbox_to_anchor=(.2, -0.3),prop={'size':12})
        fig.suptitle(f"{omega}={params.noise[nn]}",fontsize=14, fontweight='bold',y=0.7)
        if save==True:
           fig.savefig(self.output_dir + '/overlap_hist'+"_"+str(self.N)+"_"+str(params.pat_sep[m])+"_"+ params.simID +'.'+ self.fig_format, dpi=300)


    def roc_curves(self,nn,figsize=(8,8)):
        
        params=self.params
        data=self.data
        
        rcParams["figure.figsize"]=figsize
        
        plot_data={'target':[],'lure':[]}
        for key in plot_data.keys():
            plot_data[key]=get_data(data,key,params.offset,nn)
        
        fig,axes=plt.subplots(len(params.pat_sep[::2]),len(params.offset))
        x,y=0,0
        
        mem_range=params.pat_sep[1:][::2]+[params.pat_sep[-1]]
        for m in mem_range[::-1] :
            for o in params.offset:
                hip_ind=params.pat_sep.index(m)
                cortex_false=calc_rates(plot_data['lure'][0][params.offset.index(o)],params.N_t)
                cortex_hits=calc_rates(plot_data['target'][0][params.offset.index(o)],params.N_t)
                hip_false=calc_rates(plot_data['lure'][hip_ind][params.offset.index(o)],params.N_t)
                hip_hits=calc_rates(plot_data['target'][hip_ind][params.offset.index(o)],params.N_t)
                try:
                    comb_false=calc_rates(plot_data['lure'][hip_ind+params.hip][params.offset.index(o)],params.N_t)
                    comb_hits=calc_rates(plot_data['target'][hip_ind+params.hip][params.offset.index(o)],params.N_t)
                except:
                    pass

                if len(params.offset)>=2:
                   ax=axes[x][y]
                   y+=1
                else:
                    try:
                        ax=axes[x]
                    except:
                        ax=axes
                  
                ax.plot(cortex_false,cortex_hits,'ro-',label='Cort')
                ax.plot(hip_false,hip_hits,'bo-',label='Hip')
                try:
                    ax.plot(comb_false,comb_hits,'go-',label='Control')
                except:
                    pass
                ax.plot([0,1],[0,1],'k--')

                if y==1 or y==0 and len(params.offset)<2:
                    ax.set_title(m,loc='left')
                if x==0:
                    ax.set_title(o,loc='center')
                axis_default(ax,'False alarms','Hits',limit=[[0,1],[0,1.01]],legend=True,leg_size=10,aspect=True)
            x+=1
            y=0
            
        fig.tight_layout()
        fig.suptitle('Noise: '+str(nn), fontsize=14, fontweight='bold',y=1.05)
        if self.save:
            try:
                [ax.set_rasterized(True) for ax in axes]
            except:
                ax.set_rasterized(True)
            fig.savefig(self.output_dir + '/ROC'+"_"+params.cond+"_"+str(nn)+"_"+ params.simID + '.'+self.fig_format, format=self.fig_format, dpi=300)
    
    def false_alarms(self,nn,figsize=(6,6),c=0,m=4, info='lure'):
      
        params=self.params
        data=self.data
        
        rcParams["figure.figsize"]=figsize
        
        plot_data={info:[]}
        for key in plot_data.keys():
            plot_data[key]=get_data(data,key,params.offset,nn)
        
        if np.mod(len(params.offset),2)==0:
          loop=len(params.offset)
        elif len(params.offset)==1:
            loop=1
        else:
          loop=len(params.offset)-1

        fig=plt.figure()
        for o in range(loop):
          ax=fig.add_subplot(2,int(np.ceil(loop/2)),o+1) 
          cort=plot_data[info][c][o]
          hip=plot_data[info][m][o]
          
          try:
              comb=plot_data['lure'][m+params.hip][o]
          except:
              pass
          
          threshold=np.arange(1,params.N_thr+1)
          ax.plot(threshold,np.cumsum(cort),'ro-',label='Cort')
          ax.plot(threshold,np.cumsum(hip),'bo-',label='Hip')
          try:
              ax.plot(threshold,np.cumsum(comb),'go-',label='Comb')
          except:
              pass
          ax.set_title('Offset=%s' %params.offset[o])
          
          axis_default(ax,'Threshold','CumSum',limit=[[min(threshold), max(threshold)],[0,self.N]],legend=True,leg_size=10,aspect=True)

        fig.tight_layout()
        fig.suptitle('Noise: '+str(nn), fontsize=14, fontweight='bold',y=1.05)
        if self.save:
           fig.savefig(self.output_dir + '/Lures'+"_"+params.cond+"_"+str(nn)+"_"+ params.simID + '.'+self.fig_format, format=self.fig_format, dpi=300)

    def correct_retrieval(self,nn,info='targ-match', figsize=(6,6)):
        params=self.params
        data=self.data[:params.hip+1]
        
        rcParams["figure.figsize"]=figsize
                
        if np.mod(len(params.offset),2)==0:
          loop=len(params.offset)
        elif len(params.offset)==1:
            loop=1
        else:
          loop=len(params.offset)-1

        fig=plt.figure()
        alphas=np.linspace(0.4,1,len(params.pat_sep))
        linewidths=np.linspace(0.5,3,len(params.pat_sep))
        for o in range(loop):
           ax=fig.add_subplot(2,int(np.ceil(loop/2)),o+1) 
           plot_data={info:[]}
           for key in plot_data.keys():
               plot_data[key]=get_data(data,key,params.offset[o],nn)
           [ax.plot(nn,plot_data[key][params.pat_sep.index(item)],'o-',color='slategray',marker=markers[ind],label='p=%s'%item) for ind,item in enumerate(params.pat_sep[:params.hip+1])]
#           [ax.text(nn[-1]+0.025,plot_data[key][params.pat_sep.index(item)][-1]-0.01,'p=%s'%item,fontsize=14) for item in params.pat_sep[:params.hip+1]]
           ax.set_ylim(0.3,1)
#           ax.set_xlim(nn[0],nn[-1]+0.09)
           axis_default(ax,'Noise','Correct retrieval',labelsize=16,limit=[[min(nn),max(nn)],[0.3,1]],ticksize=14,r=2)
#           ax.set_xlim(nn[0],nn[-1]+0.11)

           ax.legend(loc='lower left',prop={'size':12})
           set_aspect(ax)
           ax.set_title('Offset=%s' %params.offset[o],fontsize=14)
        
        fig.tight_layout()
        fig.suptitle('Intended retrieval', fontsize=14, fontweight='bold',y=1.05)
        if self.save:
           fig.savefig(self.output_dir + '/Ret_accuracy'+"_"+params.cond+"_"+ params.simID +'.'+self.fig_format, format=self.fig_format, dpi=300)

    def fc_offset_performance(self,figsize=(8,8),ylabel='Correct', info=['target']):
        params=self.params
        data=self.data
        noise=params.noise
        
        rcParams["figure.figsize"]=figsize
        
        for i in range(len(info)):
            try:
                y_lab=ylabel[i]
            except:
                pass
            fig=plt.figure()
            for nn in range(len(noise)):
                ax=fig.add_subplot(1,len(noise),nn+1)
                plot_data={info[i]:[]}
                for key in plot_data.keys():
                   plot_data[key]=get_data(data,key,params.offset,noise[nn])
                ax.plot(params.offset,plot_data[info[i]][0], 'ro-',label='Cort')
                ax.plot(params.offset,plot_data[info[i]][-1], 'go-',label='Hip')
                axis_default(ax,'Offset', y_lab,limit=[[params.offset[0],params.offset[-1]],[0.5,1]],legend=True,aspect=True,r=1)
                ax.set_title('Noise=%s' %noise[nn],fontsize=14,fontweight='bold',y=1.05)
            fig.tight_layout()
            if self.save:
               fig.savefig(self.output_dir + '/fc-offset'+"_"+params.cond+"_"+ params.simID + '.'+self.fig_format, format=self.fig_format, dpi=300)

    def correct_retrieval_list(self,info='targ-match',figsize=(8,8)):
        params=self.params
        noise=params.noise
         
        data_lists=[{info:[]} for i in range(len(params.list_length))]
        data_all=list(range(len(params.list_length)))
        # load the data for all list lengths
        for j in range(len(params.list_length)):
          data_all[j]=[pd.read_pickle(self.input_dir+str(params.list_length[j])+'-'+str(params.pat_sep[jj])+'.pkl') for jj in range(len(params.pat_sep))]
        # loda the required info for all list lengths
        for dic,dat in zip(data_lists,data_all):
          for key in  dic.keys():
              dic[key]=get_data(dat,key,params.offset[-1],params.noise)
              
        fig,axes=plt.subplots(1,len(params.pat_sep[::2]))
        
        for i in range(len(params.pat_sep[::2])):
            ind=params.pat_sep.index(params.pat_sep[::2][i])
            ax=axes[i]
            for nn in range(len(params.noise)):
              plot_data=[item[info][ind][nn] for item in data_lists]
              ax.plot(params.list_length,plot_data,'o-',label=np.round(noise[nn],2))
              if ind==len(params.pat_sep)-1:
                axis_default(ax,'List length', info,limit=[[params.list_length[0],params.list_length[-1]],[0.3,1]],legend=True,leg_size=10,aspect=True,r=1)
              else:
                axis_default(ax,'List length', info,limit=[[params.list_length[0],params.list_length[-1]],[0.3,1]],legend=False,aspect=True,r=1)
              ax.set_title('Pat Sep=%s' %params.pat_sep[::2][i],fontsize=14,fontweight='bold',y=1.05)
        fig.tight_layout()
        if self.save:
          fig.savefig(self.output_dir + '/Rec_accuracy_list'+"_"+ params.simID + '.'+self.fig_format, format=self.fig_format, dpi=300)
                
    def bps_distances(self,nn,figsize=(8,8),save=True):
        params=self.params
        data=self.data
        rcParams["figure.figsize"]=figsize
        fig,axes=plt.subplots(1,2)
        for m in range(len([0,params.hip])):
            dat1=data[m]
            ax=axes[m]
            plot_data={'targ-hist-freq':[],'lure-hist-freq':[],'targ-hist-bins':[],'lure-hist-bins':[],'threshold_range':[],'min-distances':[],'target':[],'lure':[]}
            for key in plot_data.keys():
                plot_data[key]=get_data(dat1,key,params.offset,nn) 
            width=np.diff(plot_data['targ-hist-bins'][0])[0]
            ax.bar(plot_data['targ-hist-bins'][0][:-1],plot_data['targ-hist-freq'][0],width=width,color='g',alpha=0.7)
            ax.bar(plot_data['lure-hist-bins'][0][:-1],plot_data['lure-hist-freq'][0],width=width,color='orange',alpha=0.7)
            ax.bar(plot_data['lure-hist-bins'][-1][:-1],plot_data['lure-hist-freq'][-1],width=width,color='r',alpha=0.7)
            y=ax.get_ylim()
            [ax.plot([item]*2,y, 'k-') for item in plot_data['threshold_range'][0]]
            ax.set_title('Pat_sep=%s'%params.pat_sep[m],fontsize=16)
#            ax.set_xlim(0,0.1)
            set_aspect(ax)
        fig.suptitle('Noise: '+str(nn), fontsize=14, fontweight='bold',y=0.8)
        if save:
           ax.set_rasterized(True) 
           fig.savefig(self.output_dir + '/bps_hist'+"_"+params.cond+"_"+str(nn)+"_"+ params.simID + '.'+self.fig_format, format=self.fig_format, dpi=300)
        
            
    def bps_performance(self,nn,figsize=(8,8),save=True):
        params=self.params
        data=self.data#[:params.hip+1]
        rcParams["figure.figsize"]=figsize
        fig,axes=plt.subplots(1,3)
        plot_data={'target':[],'lure':[]}
        for key in plot_data.keys():
            plot_data[key]=get_data(data,key,params.offset,nn)
            
        targ=[plot_data['target'][item][0]/self.N for item in range(len(plot_data['target']))][::-1]
        RL=[plot_data['lure'][item][0]/self.N for item in range(len(plot_data['lure']))][::-1]
        L=[plot_data['lure'][item][-1]/self.N for item in range(len(plot_data['lure']))][::-1]
        
        all_resp=[targ,RL,L]
        colors=['g','orange','crimson']
        labels=['T', 'RL','L']
        [axes[0].plot(np.asarray(all_resp[item])[:,0],'o-',color=colors[item]) for item in range(len(all_resp))]
        [axes[1].plot(np.asarray(all_resp[item])[:,1],'o-',color=colors[item]) for item in range(len(all_resp))]
        [axes[2].plot(1-(np.asarray(all_resp[item])[:,-1]+np.asarray(all_resp[item])[:,0]),'o-',color=colors[item],label=labels[item]) for item in range(len(all_resp))]
        [axis_default(ax,'Pat_sep','Positive response',aspect=True) for ax in axes[:-1]]
        [ax.set_xticklabels(params.pat_sep[::-2]) for ax in axes]
        axis_default(axes[-1],'Pat_sep','Positive response',legend=True,aspect=True)
        
        fig.tight_layout()
        fig.suptitle('Noise: '+str(nn), fontsize=14, fontweight='bold',y=0.7)
        if save==True:
           [ax.set_rasterized(True) for ax in axes]
           fig.savefig(self.output_dir + '/bps_performance'+"_"+params.cond+"_"+str(nn)+"_"+ params.simID + '.'+self.fig_format, format=self.fig_format, dpi=300)
        
        rcParams["figure.figsize"]=(6,6)

        fig,ax=plt.subplots(1,1)
        width=.5
        ax.bar(1,RL[-1][1]-L[-1][1],width=width,color='white',edgecolor='k')
        ax.bar(2,RL[0][1]-L[0][1],width=width,color='gray',edgecolor='k')
        axis_default(ax,' ','BPS',aspect=True)
        ax.set_xticks([1,2])
        ax.set_xticklabels(["Amnesia","Control"],fontsize=14)
        fig.suptitle('Noise: '+str(nn), fontsize=14, fontweight='bold',y=1.05)

        if save:
           fig.savefig(self.output_dir + '/bps_index'+"_"+str(self.N)+"_"+str(nn)+"_"+ params.simID + '.'+self.fig_format, format=self.fig_format, dpi=300)

    

def run_plots(params,cond):
    if cond in ['item','bps']:
       plots = plot(params) 
       all_noise = ['correct_retrieval']
       individual_noise = ['distance_histograms','roc_curves','false_alarms','bps_distances','bps_performance']
       for fig in params.show_fig: 
           if fig in individual_noise:
               for nn in params.noise:
                   getattr(plots, fig)(nn)
           elif fig in all_noise:
                 if params.noise[0] == 0.2:
                     noise = params.noise[1:]
                 else:
                     noise = params.noise
                 getattr(plots, fig)(noise)
           else:
                 getattr(plots,fig)()                
    elif 'length' in cond:
          list_length(params,-1)
    elif 'strength' in cond:
         print(params.noise)
         for ind,noise in enumerate(params.noise):
             
             print(ind)
             list_strength(params,-1,nn=ind)
    elif 'decision' in cond or 'liberal_bias' in cond:
        for nn in range(len(params.noise)):
            decision_noise(params,nn=nn)
