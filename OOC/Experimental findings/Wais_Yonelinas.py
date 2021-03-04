#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 17:43:01 2020

@author: olya
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(1, '../Code/')
from analysis.plot_utils import *
from utils.calculations import normalize_F


fa_yonelinas_control = np.array([.5,1.6,3.1,5.8,9.])/14
hit_yonelinas_control = np.array([6.35,8.35,9.8,11.3,12.5])/13.5

fa_yonelinas_patient = np.array([.3,1.5,4.35,7,11.6])/14
hit_yonelinas_patient = np.array([2,5.3,8.1,10.5,13])/13.5

fa_wais_control = np.array([.75,1.25,1.85,2.6,5.7])/14.65
hit_wais_control = np.array([9.1,11.05,11.6,12,13.05])/14.65

fa_wais_matched = np.array([.65,2.1,3.8,6,8.4])/14.65
hit_wais_matched = np.array([7,10,11.4,12.7,13.7])/14.65

fa_wais_patient = np.array([2.25,3.7,5.4,7.5,10.2])/14.65
hit_wais_patient = np.array([5.35,8.55,10.45,12.4,13.5])/14.65

F_wais_control = normalize_F([1.64])[0]
F_wais_matched = normalize_F([1.21])[0]
F_wais_patient = normalize_F([0.83])[0]

R_wais_control = 0.23
R_wais_matched = 0.22
R_wais_patient = 0

F_yonelinas_control = 0.33
F_yonelinas_patient = 0.19

R_yonelinas_control = 0.33
R_yonelinas_patient = 0.12


fig, axes = plt.subplots(1,2, figsize=(7,7))

axes[0].plot(fa_wais_control,hit_wais_control,color='gray',marker=markers[0],alpha=.7,label='1: Wais 2006, C')
axes[0].plot(fa_wais_patient,hit_wais_patient,color='gray',marker=markers[2],alpha=.7,label='2: Wais 2006, H')
axes[0].plot(fa_wais_matched,hit_wais_matched,color='gray',marker=markers[1],alpha=.7,label='3: Wais 2006, H-matched')

axes[0].plot(fa_yonelinas_control, hit_yonelinas_control,marker=markers[0],color='k',alpha=.7,label='4: Yonelinas 2002, C')
axes[0].plot(fa_yonelinas_patient, hit_yonelinas_patient,marker=markers[2],color='k',alpha=.7,label='5: Yonelinas 2002, H')
axes[0].plot([0,1],[0,1],'k--')

custom_axis(axes[0],{'xlabel':{'text':'False alarm rate'},
                                'ylabel':{'text':'Hit rate'}, 'ylim':{'ylimit':[0,1.05]},'xlim':{'xlimit':[0,1]}})


width=0.8


R_centers=np.linspace(0,5*width*1.2,3)
F_centers=R_centers[-1]*2+R_centers

axes[1].bar(R_centers,[R_wais_control,R_wais_patient,R_wais_matched],width=width,color=['gray','gray','gray'],alpha=0.7)
axes[1].bar(F_centers,[F_wais_control,F_wais_patient,F_wais_matched],width=width,color=['gray','gray','gray'],alpha=0.7)

custom_axis(axes[1],{'yticks':{'round':2}})
axes[1].set_xticks(np.concatenate((R_centers,F_centers)))
axes[1].set_xticklabels([1,2,3]+[1,2,3])
axes[1].text(R_centers[2],-0.12,'R',fontsize=15)
axes[1].text(F_centers[2],-0.12,'F',fontsize=15)

fig.tight_layout()
axes[0].legend(ncol=3,bbox_to_anchor=(2.7, -.3),prop={'size':12})

fig.savefig('wais_yonelinas.svg')
