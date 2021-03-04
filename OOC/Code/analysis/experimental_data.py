#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 23:42:10 2020

@author: olya
"""
import numpy as np
import sys
sys.path.insert(1, '../')
from utils.calculations import normalize_F

def retrieve_experimental_data(study):
    if study == 'Aly et al.  2011':
        fa_control = np.array([.3,1.1,2.3,4,7.1])/14
        hit_control = np.array([6.8,8.5,9.5,10.2,11.1])/12.3
    
        fa_patient = np.array([0.7,1.5,2.9,5.5,8.4])/14
        hit_patient = np.array([6.1,7.8,9,10,11])/12.3
        R = -0.04033613445378159
        F  = -0.09227957678311655
    elif study =='MacPherson et al. 2008':
        targets_mc_patient = np.array([32.33,11.22,3.74,4.17,4.96,3.46])
        hit_patient = np.cumsum(targets_mc_patient)/np.sum(targets_mc_patient)
        lures_mc_patient = np.array([2.25,6.04,5.75,8.54,18.75,18.67])
        fa_patient = np.cumsum(lures_mc_patient)/np.sum(lures_mc_patient)
        targets_mc_control = np.array([35.79,12.33,4.18,2.12,3.70,1.88])
        hit_control = np.cumsum(targets_mc_control)/np.sum(targets_mc_control)
        lures_mc_control = np.array([1.85,3.7,4.87,7.48,18.18,23.91])
        fa_control = np.cumsum(lures_mc_control)/np.sum(lures_mc_control)
        R  = -0.06
        F = -0.21648443
    elif study == 'Farovik et al. 2008':
        fa_control = np.array([1.8,3,4.6,7,9.7])/12.1
        hit_control = np.array([7,7.7,9.3,10.5,11.2])/12.1
        fa_patient = np.array([3.9,4.6,6,7.9,10.4])/12.1
        hit_patient = np.array([6.6,7.6,9.3,10.1,11.1])/12.1
        R = -0.265
        F = 0
    elif study == 'Bowles et al. 2007':
        fa_control = np.array([0.1,0.7,2.5,5.7,10.5])/13.5
        hit_control = np.array([7.1,9.6,11,11.8,12.5])/12.5
        fa_patient = np.array([0.1,0.5,1.1,2.1,6.2])/13.5
        hit_patient = np.array([8.4,9.5,9.8,10.3,11.6])/12.5
        R_patient = 9.3/12.5
        F_patient = normalize_F([2.9*0.13+0.8-2.2*0.13])
        R_control = 7.9/12.5
        F_control = normalize_F([7.6*0.13+0.8-2.2*0.13])
        R = R_patient-R_control
        F = F_patient-F_control
        F = F[0]
    return fa_control, hit_control,fa_patient,hit_patient,R,F
