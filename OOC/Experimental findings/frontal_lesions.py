#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 18:23:25 2020

@author: olya
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(1, '../Code/')
from analysis.plot_utils import *
from utils.calculations import normalize_F


fa_aly_control = np.array([.3,1.1,2.3,4,7.1])/14
hit_aly_control = np.array([6.8,8.5,9.5,10.2,11.1])/12.3

fa_aly_patient = np.array([0.7,1.5,2.9,5.5,8.4])/14
hit_aly_patient = np.array([6.1,7.8,9,10,11])/12.3

targets_mc_patient = np.array([32.33,11.22,3.74,4.17,4.96,3.46])
hit_mc_patient = np.cumsum(targets_mc_patient)/np.sum(targets_mc_patient)
lures_mc_patient = np.array([2.25,6.04,5.75,8.54,18.75,18.67])
fa_mc_patient = np.cumsum(lures_mc_patient)/np.sum(lures_mc_patient)

targets_mc_control = np.array([35.79,12.33,4.18,2.12,3.70,1.88])
hit_mc_control = np.cumsum(targets_mc_control)/np.sum(targets_mc_control)
lures_mc_control = np.array([1.85,3.7,4.87,7.48,18.18,23.91])
fa_mc_control = np.cumsum(lures_mc_control)/np.sum(lures_mc_control)

fa_F_control = np.array([1.8,3,4.6,7,9.7])/12.1
hit_F_control = np.array([7,7.7,9.3,10.5,11.2])/12.1

fa_F_patient = np.array([3.9,4.6,6,7.9,10.4])/12.1
hit_F_patient = np.array([6.6,7.6,9.3,10.1,11.1])/12.1

F_aly_control = normalize_F([11*1.2/11.9])[0]
F_aly_patient = normalize_F([8.6*1.2/11.9])[0]

R_aly_control = 4.7*1.2/11.9
R_aly_patient = 4.3*1.2/11.9

F_mc_control = normalize_F([1.60])
F_mc_patient = normalize_F([1.05])

R_mc_control = 0.51
R_mc_patient = 0.45

F_F_control = 0.49
F_F_patient = 0.49

R_F_control = 0.375
R_F_patient = 0.11

width = 0.8
R_centers = np.linspace(0,5*width*1.2,3)
F_centers = R_centers[-1]*2+R_centers

fig, axes = plt.subplots(1,2, figsize=(6.5,6.5))
axes[0].plot(fa_aly_control,hit_aly_control,color='gray',alpha=0.7,marker=markers[0],label='1: Aly 2011, C')
axes[0].plot(fa_aly_patient,hit_aly_patient,color='gray',alpha=0.7,marker=markers[1],label='2: Aly 2011, F')
axes[0].plot(fa_mc_control,hit_mc_control,color='k',alpha=0.7,marker=markers[0],label='3: MacPherson 2008, C')
axes[0].plot(fa_mc_patient,hit_mc_patient,color='k',alpha=0.7,marker=markers[1],label='4: MacPherson 2008, F')
axes[0].plot(fa_F_control,hit_F_control,color='tab:blue',alpha=0.7,marker=markers[0],label='5: Farovik 2008, C')
axes[0].plot(fa_F_patient,hit_F_patient,color='tab:blue',alpha=0.7,marker=markers[1],label='6: Farovik 2008, F')

axes[0].plot([0,1],[0,1],'k--')

custom_axis(axes[0],{'xlabel':{'text':'False alarm rate'},
                                'ylabel':{'text':'Hit rate'}, 'ylim':{'ylimit':[0,1.05]},'xlim':{'xlimit':[0,1]}})


axes[1].bar(R_centers,[R_aly_control-R_aly_patient,R_mc_control-R_mc_patient,R_F_control-R_F_patient],width=width,color=['gray','k','tab:blue'],alpha=0.7)
axes[1].bar(F_centers,[F_aly_control-F_aly_patient,F_mc_control-F_mc_patient,F_F_control-F_F_patient],width=width,color=['gray','k','tab:blue'],alpha=0.7)
#axes[1].plot([R_centers[0]-width*2,F_centers[-1]+width*2],[0,0],'k-')


custom_axis(axes[1],{'yticks':{'round':2}})
axes[1].set_xticks(np.concatenate((R_centers,F_centers)))
axes[1].set_xticklabels([1,2,3,]+[1,2,3])
axes[1].text(R_centers[2],-0.12,'R',fontsize=15)
axes[1].text(F_centers[2],-0.12,'F',fontsize=15)

fig.tight_layout()
axes[0].legend(ncol=3,bbox_to_anchor=(2.5, -.4),prop={'size':12})

fig.savefig('frontal_lesions.svg')

