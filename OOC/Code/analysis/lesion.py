#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:52:13 2019

@author: olya
"""
import numpy as np
import os
import matplotlib.pyplot as plt

path=os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
os.chdir(path)# move to the base directory of  the code
path1=os.path.abspath(os.path.join(path, os.pardir)) # this is the main directory where all the folders are
from analysis.plot_utils import *
#info_update={'IDs':['01-02_21:48:15','01-02_21:48:15','01-02_21:48:15'],'cond':['0.006','0.006','0.006'],'line':['-','-','--'],
#      'pat_sep':[4,1,1],'noise':[2,2,0],'color':['tab:green','tab:purple','tab:purple'],'barcolor':['tab:green','tab:purple','white'],'edgecolor':[None,None,'tab:purple']}
info_update={'IDs':['01-02_21:48:15']*6,'cond':['0.006']+['0.01']*5,
      'pat_sep':[4]*6,'noise':[2]+[2,3,4,5,6,7]}

def compare_rocs(info_update,path,labeling='pat_sep',barplot=False,change=False,figsize=(7,7),save=False,filename='ROC_comparison'):
    # Update the dictionary 
    import copy
    from pylab import rcParams
#    from analysis.plot_utils import axis_default
    from utils.matlab import matlab
    from utils.save_load import load_params
    

    rcParams["figure.figsize"]=figsize
#    colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
    colors=['tab:green','tab:purple','steelblue','tab:gray','tab:orange','tab:red']
    info_default={'color':colors,'barcolor':colors,
              'edgecolor':None,'line':'-','offset':-1}
    data=copy.copy(info_default)
    data.update(info_update)
    # adjust the defaults to the current datasize
    default_keys=info_default.keys()
    update_keys=info_update.keys()
    defaults=list(set(default_keys).difference(set(update_keys))) 
    N=len(data['IDs'])
    for item in defaults:
        if item not in ['color','barcolor']:
            data[item]=[data[item]]*N 
    if barplot or change:
            fig,axes=plt.subplots(1,2)
            ax=axes[0]
            if change:
                F_all=[]
                R_all=[]
                X=[]
            if barplot:
                width=0.8
                center=0
    else:
            fig,ax=plt.subplots(1,1)
    Rticks=[]
    Fticks=[]
    for ind, simID in enumerate(data['IDs']):
        params=load_params(simID,path)
        mat = matlab(params)
        all_data=mat.load_dpsd()
        index=all_data[-1].index(data['cond'][ind])
        plot_data=all_data[0][index][data['pat_sep'][ind]]
        hit_model=plot_data['roc_hit'][data['offset'][ind]][:,data['noise'][ind]]
        fa_model=plot_data['roc_fa'][data['offset'][ind]][:,data['noise'][ind]]
        hit_obs=plot_data['hits'][data['offset'][ind]][data['noise'][ind]]
        fa_obs=plot_data['fa'][data['offset'][ind]][data['noise'][ind]]
        
        if labeling=='pat_sep':
            
            label=str(ind+1)+': p=%s'%params.pat_sep[info_update['pat_sep'][ind]]+',\u03C9=%s'%params.noise[data['noise'][ind]]
#            label='p=%s'%params.pat_sep[data['pat_sep'][ind]]+',\u03C9=%s'%params.noise[data['noise'][ind]]
        elif labeling=='cond':
            label=str(ind+1)+': \u03BB=%s'%data['cond'][ind]+',\u03C9=%s'%params.noise[data['noise'][ind]]
        ax.plot(fa_model,hit_model,color=data['color'][ind],linestyle=data['line'][ind])
        ax.plot(fa_obs,hit_obs,'o',color=data['color'][ind],label=label,alpha=0.7)
        ax.plot([0,1],[0,1],'k--')
        F=plot_data['F'][data['offset'][ind]][data['noise'][ind]]
        R=plot_data['R'][data['offset'][ind]][data['noise'][ind]]

        F_all.append(F)
        R_all.append(R)
    

#        if barplot or change:
#            ax1=axes[1]
#            F=plot_data['F'][data['offset'][ind]][data['noise'][ind]]
#            R=plot_data['R'][data['offset'][ind]][data['noise'][ind]]
#            if barplot:
#                ax1.bar(center,R,width=width,color=data['barcolor'][ind],edgecolor=data['edgecolor'][ind],linestyle=data['line'][ind])
#                ax1.bar(center+len(data)*width*1.2,F,width=width,color=data['barcolor'][ind],edgecolor=data['edgecolor'][ind],linestyle=data['line'][ind])
#                Rticks.append(center)
#                Fticks.append(center+len(data)*width*1.2)
#                center+=width*1.5



#            if change:
#                X_ind=data['pat_sep'][ind]
#                X.append(params.pat_sep[X_ind])
                
#    ax.legend()
#    custom_axis(ax,{'xlabel':{'text':'False alarm rate'},
#                        'ylabel':{'text':'Hit rate'}})
#    ax.legend(ncol=2,bbox_to_anchor=(1.1, -0.3),prop={'size':14})


#    axis_default(ax,'False alarm rate','Hit rate', limit=[[-0.01,1.01],[0,1.01]],legend=True,leg_size=12,aspect=True,labelsize=16,ticksize=14)
    if barplot:
       ax1 = axes[1]
       width = 0.8
       R_centers = np.linspace(0,5*width*1.2,len(F_all)-1)
       F_centers = R_centers[-1]*2+R_centers

       F = F_all[0]-F_all[1:]
       R = R_all[0]-R_all[1:]
       ax1.bar(R_centers,R,width=width)
       ax1.bar(F_centers,F,width=width)
       Rticks.append(center)
       Fticks.append(center+len(data)*width*1.2)
       print(R)
       print(F)
    fig.tight_layout()
    if save:
        plt.savefig(params.path+'/Figures/'+filename+".pdf", format='pdf', dpi=300)
#compare_rocs(info_update,path1,figsize=(8,8),barplot=True,change=True,labeling='pat_sep',save=True)
compare_rocs(info_update,path1,figsize=(10,10),barplot=True,change=True,labeling='cond',save=True)
