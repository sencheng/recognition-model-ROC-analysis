#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 18:02:54 2020

@author: olya
"""
import matplotlib.pyplot as plt
from utils.utils import check_directory,list_chronologically
from utils.calculations import calc_rates
from utils.data import get_data
from analysis.plot_utils import *
from analysis.experimental_data import retrieve_experimental_data

import os
import pandas as pd
import numpy as np

class plot_multiple:
    def __init__(self,params,effect,p=-1,o=-1,nn=2):
        self.input_dir = params.path+'/Data/'+params.simID+'/' # simulation directory, e.g. '../OOC/Data/12-19_16:03:35/''
        self.folders = list_chronologically(self.input_dir) # subfolders such as '30' etc
        try:
            self.labels = [float(item) for item in self.folders]
        except:
            self.labels = self.folders
            pass
        self.params = params
        self.output_dir = params.path+'/Figures/'
        check_directory(self.output_dir)
        self.colors = ['tab:green','tab:purple','steelblue','tab:gray','tab:orange','tab:red']
        self.alphas = [1]*len(self.labels)
        self.p = p
        self.o = o       
        self.nn = nn
        self.effect = effect
        self.fit='Rn:0'
        
    def load_data(self):
        self.data = []
        for ind,folder in enumerate(self.folders):
            full_path = self.input_dir+folder+'/'
            filenames = sorted([item for item in os.listdir(full_path) if item[-3:]=='pkl' and 'std' not in item])
            self.data.append([pd.read_pickle(full_path+file) for file in filenames])
            
    def load_dpsd(self):
        self.data_dpsd = []
        from utils.matlab import matlab
        mat = matlab(self.params)
        self.data_dpsd,conds = mat.load_dpsd(fit=self.fit)


    def run(self):
        params = self.params
        self.figs = [plt.subplots(self.plot_defaults[item]['nrows'],self.plot_defaults[item]['ncols'],figsize=self.plot_defaults[item]['figsize']) for item in self.plot_defaults.keys()]
        self.title = f'p={params.pat_sep[self.p]}, o={params.offset[self.o]}, {omega}={params.noise[self.nn]}'

        for key in self.plot_defaults.keys():
             if self.plot_defaults[key]['run']:
                 plot = getattr(self, key)
                 plot()
                 
                 
    def empty_figure(self,name):
        fig_index = list(self.plot_defaults.keys()).index(name)
        fig = self.figs[fig_index][0]
        ax = self.figs[fig_index][1]
        return fig,ax
    
    
    def N_test(self,label):
        if 'match' in self.params.effect:
            N = label
#        elif 'length' in self.params.effect:
#            N = self.params.N_t
        elif label =='MW' or label =='MS':
             N = 15#int(self.params.N_t/2)
        else:
            N = 30
        return N

        
    def interference(self):
        name = 'interference'
        params = self.params
        fig,ax = self.empty_figure(name)
#        alphas=np.linspace(0.1,1,len(params.noise))
        
        for ind,item in enumerate(params.noise):
            target_match = [get_data(dat[-1],'targ-match',params.offset[-1],
                                 params.noise[ind]) for dat in self.data]
            ax.plot(self.labels,target_match,label=f"{omega}={params.noise[ind]}",
                    marker = markers[ind],color='k',alpha=.7)
        
        custom_axis(ax,{'xlabel':{'text':self.effect},
                        'ylabel':{'text':'Correct retrieval'},'xlim':{'xlimit':(min(self.labels),max(self.labels))},
                       })
        fig.suptitle(self.title,fontsize=14,y=.95)
        if params.save_figs:
            fig.savefig(f"{self.output_dir}{self.effect}-{name}-{params.simID}.pdf")

    def mean_distance(self):
        params = self.params
        name = 'mean_distance'
        fig,ax = self.empty_figure(name)

        for ind,item in enumerate(params.noise):
            target_mean = [np.mean(get_data(dat[self.p],'min-dist-target',params.offset[self.o],item)) for dat in self.data]
            lure_mean = [np.mean(get_data(dat[self.p],'min-dist-lure',params.offset[self.o],item)) for dat in self.data]
            ax[0].plot(self.labels,target_mean,marker=markers[ind],color='k',alpha=0.7,label=f"{omega}={params.noise[ind]}")
            ax[1].plot(self.labels,lure_mean,marker=markers[ind],color='k',alpha=0.7,label=f"{omega}={params.noise[ind]}")
        
        custom_axis(ax[0],{'xlabel':{'text':self.effect},
                        'ylabel':{'text':'Mean d (targets)'},'xlim':{'xlimit':(min(self.labels),max(self.labels))}})
        
        custom_axis(ax[1],{'xlabel':{'text':self.effect},
                        'ylabel':{'text':'Mean d (lures)'},'xlim':{'xlimit':(min(self.labels),max(self.labels))},
                        'legend':{'size':12,'bbox_to_anchor':(1.03, 1.03)}})
        
        fig.tight_layout()
        fig.suptitle(self.title,fontsize=14,y=.7)

        if params.save_figs:
            fig.savefig(f"{self.output_dir}{self.effect}-{name}-{self.params.noise[self.nn]}-{params.simID}.pdf")
    
    def rates(self):
        name = 'rates'
        fig,ax = self.empty_figure(name)
        params = self.params
        for ind,item in enumerate(self.data):
            N=self.N_test(self.labels[ind])
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
            
    def roc_barplot(self):
        name='roc_barplot'
        fig,axes=self.empty_figure(name)
        params=self.params
        
        for ind, item in enumerate(self.data_dpsd):
            axes[0].plot(item[self.p]['roc_fa'][self.o][:,self.nn],item[self.p]['roc_hit'][self.o][:,self.nn],
              color=self.colors[ind],alpha=self.alphas[ind])
            axes[0].plot(item[self.p]['fa'][self.o][self.nn],item[self.p]['hits'][self.o][self.nn],
              'o',color=self.colors[ind],alpha=self.alphas[ind],label=f'{self.aux}= {self.labels[ind]}')
            axes[0].plot([0,1],[0,1],'k--')
            
        for ind,feature in enumerate(self.features):
            ax=axes[ind+1]
            data_relevant=[item[self.p][feature][self.o][self.nn] for item in self.data_dpsd]
            x_values=range(len(self.labels))
            [ax.bar(x_values[index],item,color=self.colors[index],alpha=self.alphas[index]) 
                    for index,item in enumerate(data_relevant)]
            ax.set_xticks(x_values)
            ax.set_xticklabels(self.labels)
            ax.tick_params(axis='x', which='major', labelsize=14)  

            custom_axis(ax,{'xlabel':{'text':self.effect},
                    'ylabel':{'text':feature.upper()},'ylim':{'ylimit':[0,1]},'xticks':{}})
        custom_axis(axes[0],{'xlabel':{'text':'False alarm rate'},'xlim':{'xlimit':[0,1]},
                    'ylabel':{'text':'Hit rate'},'ylim':{'ylimit':[0,1]}})
        
        fig.tight_layout()
        fig.suptitle(self.title,fontsize=14,y=.7)
        if params.save_figs:
            fig.savefig(f"{self.output_dir}{self.effect}-{name}-{self.params.noise[self.nn]}-{params.simID}.pdf")
   
    def roc_curves(self):
        name='roc_curves'
        fig,axes=self.empty_figure(name)
        params=self.params
        
        for ind, item in enumerate(self.data_dpsd):
            axes[0].plot(item[self.p]['roc_fa'][self.o][:,self.nn],item[self.p]['roc_hit'][self.o][:,self.nn],
              color=self.colors[ind],alpha=.3)
            axes[0].plot(item[self.p]['fa'][self.o][self.nn],item[self.p]['hits'][self.o][self.nn],
              marker=markers[ind],linestyle='None',color=self.colors[ind],alpha=0.5,label=f'{self.aux}= {self.labels[ind]}')
            axes[0].plot([0,1],[0,1],'k--')
        for ind,feature in enumerate(self.features):
            ax=axes[1]
            data_relevant=[item[self.p][feature][self.o][self.nn] for item in self.data_dpsd]
            ax.plot(self.labels,data_relevant, marker=markers[ind],color='k',alpha=0.7,label=feature.upper())

        custom_axis(ax,{'xlabel':{'text':self.aux},
                'ylabel':{'text':'Parameter'},'ylim':{'ylimit':[-0.05,1.09]},'xticks':{'round':3},'legend':{'size':12,'bbox_to_anchor':False}})
        custom_axis(axes[0],{'xlabel':{'text':'False alarm rate'},'xlim':{'xlimit':[-0.05,1.05]},
                    'ylabel':{'text':'Hit rate'},'ylim':{'ylimit':[0,1]}})
        fig.tight_layout()

        axes[0].legend(ncol=4,bbox_to_anchor=(2.5, -.3),prop={'size':14})
        fig.suptitle(self.title,fontsize=14,y=.8)
        if params.save_figs:
            fig.savefig(f"{self.output_dir}{self.effect}-{name}-{self.params.noise[self.nn]}-{params.simID}.pdf")
    
    def frontal_lesion(self,control='0.006',patient='0.01',noise_diff=1,comparison='Bowles et al. 2007'):
        name = 'frontal_lesion'
        print(name)
        fig,axes = self.empty_figure(name)
        params = self.params
        noise = [self.nn]+[self.nn+noise_diff]
        control_index = self.labels.index(float(control))
        patient_index = self.labels.index(float(patient))
        colors = ['k','gray']
        F_all, R_all = [],[]
        if comparison:
            fa_control, hit_control,fa_patient,hit_patient,R_exp,F_exp=retrieve_experimental_data(comparison)

        for ind, item in enumerate([control_index,patient_index]):
            data = self.data_dpsd[item]
            axes[0].plot(data[self.p]['roc_fa'][self.o][:,noise[ind]],data[self.p]['roc_hit'][self.o][:,noise[ind]],
                      color=colors[0],alpha=.7)
            axes[0].plot(data[self.p]['fa'][self.o][noise[ind]],data[self.p]['hits'][self.o][noise[ind]],
                  markers[ind],color=colors[0],alpha=0.7,label=f'{omega}={params.noise[noise[ind]]}, {Lambda}={self.labels[item]}')
            F_all.append(data[self.p]['F'][self.o][noise[ind]])
            R_all.append(data[self.p]['R'][self.o][noise[ind]])
            if comparison and ind == 0:
                axes[0].plot(fa_control,hit_control,color=colors[1],marker=markers[ind],alpha=.7,label=f'exp-C')
            elif comparison and ind == 1:
                axes[0].plot(fa_patient,hit_patient,color=colors[1],alpha=.7,marker=markers[ind],label=f'exp-F')
            

        axes[0].plot([0,1],[0,1],'k--')
        custom_axis(axes[0],{'xlabel':{'text':'False alarm rate'},'xlim':{'xlimit':[-0.05,1.05]},
                    'ylabel':{'text':'Hit rate'},'ylim':{'ylimit':[0,1.05]}})
        
        width = 0.4
        print(R_all)
        R_centers = np.array([.5,1])
        F_centers =R_centers[-1]*1.5+R_centers
        F = np.subtract(F_all[-1],F_all[0])
        R = np.subtract(R_all[-1],R_all[0])
        R = R.tolist()
        F = F.tolist()
        axes[1].bar(R_centers[0],R,width=width,color='k')
        axes[1].bar(F_centers[0],F,width=width,color='k')
        axes[1].plot([R_centers-width*2,F_centers+width*2],[0,0],'k-')

        axes[1].bar(R_centers[1],[R_exp],width=width,color='gray')
        axes[1].bar(F_centers[1],[F_exp],width=width,color='gray')
#        axes[1].plot([R_centers-width*2,F_centers+width*2],[0,0],'k-')

        custom_axis(axes[1],{'xlabel':{'text':''},
                    'ylabel':{'text':'Estimate'},'ylim':{'ylimit':[-0.4,0.4]}
                    ,'xlim':{'xlimit':[0,3]}})
        custom_axis(axes[-1],{'xlabel':{'text':''},
                    'ylabel':{'text':'Estimate'},'ylim':{'ylimit':[-0.4,0.4]},'xlim':{'xlimit':[0,3]}})

        fig.tight_layout()
        axes[0].legend(ncol=2,bbox_to_anchor=(2.5, -.4),prop={'size':14})
        axes[-1].text(R_centers[1]-.4,-0.5,'ΔR',fontsize=15)
        axes[-1].text(F_centers[1]-.4,-0.5,'ΔF',fontsize=15)
        axes[-1].set_xticks(())
        fig.suptitle(comparison,fontsize=16,y=0.8)
        if params.save_figs:
            fig.savefig(f"{self.output_dir}{self.effect}-{name}-{comparison}-{self.params.noise[self.nn]}-{params.simID}.pdf")

    
    def bias_overview(self,par_value=['0.006']+['0.01']*5,barplot=False,lineplot=True):
        name = 'bias_overview'
        print(name)

        fig,axes = self.empty_figure(name)
        params = self.params
        noise = [self.nn]+np.arange(self.nn,len(par_value)-1+self.nn).tolist()
        F_all = []
        R_all = []
        for ind, par in enumerate(par_value):
            index = self.labels.index(float(par))
            data = self.data_dpsd[index]
            F_all.append(data[self.p]['F'][self.o][noise[ind]])
            R_all.append(data[self.p]['R'][self.o][noise[ind]])
            axes[0].plot(data[self.p]['roc_fa'][self.o][:,noise[ind]],data[self.p]['roc_hit'][self.o][:,noise[ind]],
                  color=colors[ind],alpha=.7)
            axes[0].plot(data[self.p]['fa'][self.o][noise[ind]],data[self.p]['hits'][self.o][noise[ind]],
                  marker='o',linestyle='None',color=colors[ind],alpha=0.7,label=f'{ind+1}: {omega}={params.noise[noise[ind]]}, {Lambda}={par}')
            axes[0].plot([0,1],[0,1],'k--')
            
        custom_axis(axes[0],{'xlabel':{'text':'False alarm rate'},'xlim':{'xlimit':[-0.05,1.05]},
                    'ylabel':{'text':'Hit rate'},'ylim':{'ylimit':[0,1.05]}})
        F = np.subtract(F_all[1:],F_all[0])
        R = np.subtract(R_all[1:],R_all[0])
        R = R.tolist()
        F = F.tolist()

        if barplot:
            width = 0.8
            R_centers = np.linspace(0,len(par_value)*width*1.2,len(par_value)-1)
            F_centers = R_centers[-1]*2+R_centers
            axes[-1].bar(R_centers,R,width=width,color=colors[1:])
            axes[-1].bar(F_centers,F,width=width,color=colors[1:])
            axes[-1].plot([R_centers[0]-width*2,F_centers[-1]+width*2],[0,0],'k-')
            
            custom_axis(axes[-1],{'xlabel':{'text':''},
                        'ylabel':{'text':'Estimate'}, 'ylim':{'ylimit':[-0.4,0.4]}})
        elif lineplot:
            x = [params.noise[item] for item in noise[1:]]
#            x = np.arange(2,len(par_value)+1)
            axes[-1].plot(x,R,color='k',alpha=0.5,marker=markers[0],label='ΔR')
            axes[-1].plot(x,F,color='k',alpha=0.5,marker=markers[1],label='ΔF')
            axes[-1].plot(x,[0]*len(x),'k--',alpha=.2)
            custom_axis(axes[-1],{'xlabel':{'text':f'{omega}'},
                        'ylabel':{'text':'Estimate'},'legend':{'size':14,'bbox_to_anchor':False},'xticks':{'spacing':5, 'round':2},'ylim':{'ylimit':[-0.5,0.5]}})
            axes[-1].set_xticks(x)

        fig.tight_layout()
        axes[0].legend(ncol=2,bbox_to_anchor=(2.3, -.3),prop={'size':14})
        if barplot:
            axes[-1].set_xticks(())
            axes[-1].text(R_centers[3],-0.5,'ΔR',fontsize=15)
            axes[-1].text(F_centers[3],-0.5,'ΔF',fontsize=15)

        if params.save_figs:
            fig.savefig(f"{self.output_dir}{self.effect}-{name}-{self.params.noise[self.nn]}-{params.simID}.pdf")



    def noise_effect(self):
        name='noise_effect'
        fig,axes=self.empty_figure(name)
        params=self.params
        for ind, feature in enumerate(self.features):
            ax=axes[ind]
            x_values=range(len(self.labels))
            for n_ind,nn in enumerate(self.params.noise):
                data_relevant=[item[self.p][feature][self.o][n_ind] for item in self.data_dpsd]
                ax.plot(x_values,data_relevant,color='k',alpha=0.7,marker=markers[n_ind],label=f'{omega}={nn}')
            if ind==len(axes)-1:
                legend={'size':14,'bbox_to_anchor':(1.03, 1.03)}
            else:
                legend={}
            custom_axis(ax,{'xlabel':{'text':self.effect},
                    'ylabel':{'text':feature.upper()},'xticks':{},'ylim':{'ylimit':[0,1]},'legend':legend})
            ax.set_xticks(x_values)
            ax.set_xticklabels(self.labels)
            ax.tick_params(axis='x', which='major', labelsize=14)  

        fig.tight_layout()
        fig.suptitle(self.title,fontsize=14,y=.7)
        if params.save_figs:
            fig.savefig(f"{self.output_dir}{self.effect}-{name}-{params.simID}.pdf")

            
    def criteria(self):
        name = 'criteria'
        fig,ax = self.empty_figure(name)
        params = self.params
        for ind,item in enumerate(self.data):
            threshold = get_data(item[self.p],'threshold_range',params.offset[self.o],params.noise[self.nn])
            x_values=np.arange(1,len(threshold))
            ax.plot(x_values,threshold[:-1],'o-',color=self.colors[ind],alpha=self.alphas[ind],marker=self.markers[ind],label=f"{self.labels[ind]}")
        
        custom_axis(ax,{'xlabel':{'text':'#Threshold'},
                        'ylabel':{'text':'Value'},'xlim':{'xlimit':(min(x_values),max(x_values))},'legend':{'size':12,'bbox_to_anchor':(1.03, 1.03)}})
    
        fig.suptitle(self.title,fontsize=14,y=.95)
        if params.save_figs:
            fig.savefig(f"{self.output_dir}{self.effect}-{name}-{self.params.noise[self.nn]}-{params.simID}.pdf")
            
    def overlap_ROCs(self):
        name = 'overlap_ROCs'
        fig,axes = self.empty_figure(name)
        params = self.params
        if params.offset[0] == 1: 
            fa_rotello_cons = np.array([2.2,3.8,5.3,6.7,9.1])/15
            fa_rotello_lib = np.array([2.9,4.8,6.9,8.8,11.5])/14.9
        else:
            fa_rotello_cons =  np.array([0.7,2,3.7,6.2,10.7])/15
            fa_rotello_lib = np.array([0.5,1.5,2.7,5,9.6])/15

        hit_rotello_cons = np.array([7,9,10.5,11.8,13.8])/15
        hit_rotello_lib = np.array([7.3,8.9,10.3,11.7,13.7])/14.9
        
        
        for ind, item in enumerate(self.data_dpsd):
            ax=axes[ind]
            if params.offset[0] != 1:
                for nn in [self.nn,self.nn+1]:
                    ax.plot(item[self.p]['roc_fa'][self.o][:,nn],item[self.p]['roc_hit'][self.o][:,nn],
                      color='k',alpha=0.7)
            ax.plot(item[self.p]['fa'][self.o][self.nn][:-1],item[self.p]['hits'][self.o][self.nn][:-1],markers[0],alpha=0.7,
              color='k',label=f'{omega}={params.noise[self.nn]}')
            ax.plot(item[self.p]['fa'][self.o][self.nn+1][:-1],item[self.p]['hits'][self.o][self.nn+1][:-1],markers[1],alpha=0.7,
              color='k',label=f'{omega}={params.noise[self.nn+1]}')

            ax.plot([0,1],[0,1],'k--')
            if params.offset[0] == 1:
                for nn in [self.nn, self.nn+1]:
                    coef = np.polyfit(item[self.p]['fa'][self.o][nn][:-1],item[self.p]['hits'][self.o][nn][:-1],1)
                    poly1d_fn = np.poly1d(coef) 
                    ax.plot(item[self.p]['fa'][self.o][nn][:-1], poly1d_fn(item[self.p]['fa'][self.o][nn][:-1]),color='k',alpha=0.7)
            custom_axis(ax,{'xlabel':{'text':'False alarm rate'},
                        'ylabel':{'text':'Hit rate'},'set_title': {'text':f'{self.aux}={self.labels[ind]}'}})
            ax.plot(fa_rotello_lib,hit_rotello_lib,color='gray', marker=markers[3],label='Rotello 2000, exp.1',alpha=0.4)
            ax.plot(fa_rotello_cons,hit_rotello_cons,color='gray', marker=markers[2],label='Rotello 2000, exp.2',alpha=0.4)

        fig.tight_layout()
        ax.legend(ncol=4,bbox_to_anchor=(0, -.3),prop={'size':14})

        fig.suptitle(self.title,fontsize=14,y=1.)
        if params.save_figs:
            fig.savefig(f"{self.output_dir}overlap_bias-{name}-{self.params.noise[self.nn]}-{params.simID}.pdf")
        




  
class length(plot_multiple):
    def __init__(self,params,plot_params=False,plot_cond='general',data_dpsd=[]):
        super().__init__(params,'List length')
        self.load_data()
        self.load_dpsd()

        try:
            self.labels=[int(label) for label in self.labels]
        except:
            self.labels=[int(label[-2]) for label in self.labels]
        if plot_cond == 'general':
            self.plot_defaults = {'interference':{'run':True,'figsize':(2.5,2.5),'nrows':1,'ncols':1},
                                  'rates':{'run':True,'figsize':(7,7),'nrows':1,'ncols':2}, 
                                  'mean_distance':{'run':True,'figsize':(7,7),'nrows':1,'ncols':2},
                                  'criteria':{'run':True,'figsize':(3.2,3.2),'nrows':1,'ncols':1}}
        elif plot_cond == 'dpsd':
#            self.data_all=data_all
            self.features=['R','F','auc']
            self.plot_defaults = {'roc_barplot':{'run':True,'figsize':(3.2+(2.5*len(self.features)+1),(3.2+(2.5*len(self.features)+1))),'nrows':1,'ncols':len(self.features)+1},
                                  'noise_effect':{'run':True,'figsize':(3+(2.5*len(self.features)),(3+(2.5*len(self.features)))),'nrows':1,'ncols':len(self.features)}}
        
        self.aux='N'
        self.markers=['o']*len(self.labels)
        # change the plot specifics if given
        if plot_params:
            for key in plot_params.keys():
                self.plot_defaults[key].update(plot_params[key])


class strength(plot_multiple):
        def __init__(self,params,plot_params=False,data_all=[],plot_cond='general'):
            super().__init__(params,'List strength',nn=-1)
            self.load_data()
            self.load_dpsd()

            if plot_cond == 'general':
                self.plot_defaults = {'rates':{'run':True,'figsize':(8,8),'nrows':1,'ncols':2}, 
                                  'criteria':{'run':True,'figsize':(3.2,3.2),'nrows':1,'ncols':1}}
            # change the plot specifics if given
            elif plot_cond == 'dpsd':
#                self.data_all = data_all
                self.features = ['F','auc']
                self.plot_defaults = {'roc_barplot':{'run':True,'figsize':(3+(2.5*len(self.features)+1),(3+(2.5*len(self.features)+1))),'nrows':1,'ncols':len(self.features)+1}}
            self.colors = ['tab:green','tab:green','tab:purple','tab:purple']
            self.alphas = [1,.5,1,.5]
            self.markers = ['o']*len(self.labels)
            self.aux = ''
            if plot_params:
                for key in plot_params.keys():
                    self.plot_defaults[key].update(plot_params[key])


class liberal_bias(plot_multiple):
    def __init__(self,params,plot_params=False,data_all=[],plot_cond='general'):
        super().__init__(params,'lambda',nn=2)
        self.load_data()
        try: 
          self.load_dpsd()
        except:
          pass
        if  plot_cond == 'general':
            self.plot_defaults={'rates':{'run':True,'figsize':(7,7),'nrows':1,'ncols':2}}
            
        
        elif plot_cond == 'dpsd':
#            self.data_all = data_all
            self.features = ['R','F','auc']
            self.plot_defaults = {'roc_curves':{'run':False,'figsize':(7,7),'nrows':1,'ncols':2},
                                                'overlap_ROCs': {'run':False,'figsize':(3+(2.5*len(self.data_dpsd)+1),(3+(2.5*len(data_all)+1))),'nrows':1,'ncols':len(self.data_dpsd)},
                                               'frontal_lesion':{'run':False,'figsize':(7,7),'nrows':1,'ncols':2},
                                               'bias_overview':{'run':False, 'figsize':(7,7),'nrows':1,'ncols':2}}
        if plot_params:
                for key in plot_params.keys():
                    self.plot_defaults[key].update(plot_params[key])

        self.colors = ['k']*len(self.labels)
        self.alphas = [.3]*len(self.labels)
        self.markers = markers
        self.aux = Lambda

        
    
