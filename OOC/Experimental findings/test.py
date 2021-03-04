#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 18:09:32 2019

@author: olya
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from experiments import plot_findings

Aggleton=plot_findings('Aggleton2005')
Aggleton.criteria(fa=True,hit=True)
Yonelinas=plot_findings('Yonelinas1998')
Yonelinas.criteria(fa=True,hit=True)
#Wais=plot_findings('Wais2006')
#Wais.F_and_R()
