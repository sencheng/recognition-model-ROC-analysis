#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 19:32:26 2019

@author: olya
"""

import os
path=os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
os.chdir(path)# move to the base directory of  the code
path1=os.path.abspath(os.path.join(path, os.pardir)) # this is the main directory where all the folders are
from utils.save_load import load_params
import matplotlib.pyplot as plt
import sys

cond='general'
if cond=='general':
    import analysis.plot_general as plot
elif cond=='dpsd':
    from utils.matlab import load_dpsd
    from analysis.plot_dpsd import plot
        
simID='09-04_19:47:48'#'07-16_18:47:23'

params=load_params(simID,path1)
#from utils.utils import get_data
#from utils.calculations import round_for_fit,calc_rates
#from analysis.plot_general import plot
#plots=plot(params)
#data=plots.data
#targets=get_data(data,'target',9,params.noise[0])[0]
#lure=get_data(data,'lure',9,params.noise[0])[0]
#hits=calc_rates(round_for_fit(targets,params.N_t),params.N_t)
#fa=calc_rates(round_for_fit(lure,params.N_t),params.N_t)
#sys.exit()
if 'length' in params.effect:
    for nn in range(len(params.noise)):
        plot.list_length(params,-1,nn=nn,confounds='equal')
        
elif 'strength' in params.effect:
    for nn in range(len(params.noise)):
        plot.list_strength(params,-1,nn=nn)
elif 'decision' in params.effect or 'bias' in params.effect:
    for nn in range(len(params.noise)):
        plot.decision_noise(params,nn=nn,m=0)
elif 'item' in params.effect:
    from analysis.plot_general import plot
    params.show_fig=['roc_curves','distance_histograms_memory1','correct_retrieval','false_alarms']
    plots=plot(params) 
    for nn in params.noise:
#        plots.false_alarms(nn,info='lure')
#        plots.roc_curves(nn)
      plots.distance_histograms(nn)
#      run_plots(params,params.effect)

     
    


