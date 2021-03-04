#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 23:45:35 2019

@author: olya
"""

import numpy as np

def set_aspect(ax):

    x0,x1 = ax.get_xlim()
    y0,y1 = ax.get_ylim()
    ax.set_aspect(abs(x1-x0)/abs(y1-y0))


linestyles = [
     ('loosely dotted',        (0, (1, 10))),
     ('densely dotted',        (0, (1, 1))),

     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('densely dashed',        (0, (5, 1))),

     
     ('densely dashdotted',    (0, (3, 1, 1, 1))),
     ('loosely dashdotted',    (0, (3, 10, 1, 10))),

     ('loosely dashed',        (0, (5, 10))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))]

markers=['o','v','s','X','d','|','*','3','1','2']
colors=['tab:green','tab:purple','steelblue','tab:gray','tab:orange','tab:red','tab:cyan','tab:pink','tab:brown','tab:olive']
Lambda='\u03BB'
omega='\u03C9'

class custom_axis:
    def __init__(self,ax,new_params):
        axis_params={'aspect':{True},'xlabel':{'text':'','labelsize':16},
                     'ylabel':{'text':'','labelsize':16},
                     'xlim':{},'ylim':{},
                     'xticks':{'round':1,'ticksize':14, 'spacing':3},'yticks':{'round':1,'ticksize':14,'spacing':3},
                     'legend':{},
                     'set_title': {'text':'','titlesize':18,'offset':3}}
        for key in new_params.keys():
            if new_params[key]: # update if not empty
                axis_params[key].update(new_params[key])
            else: # replace if empty
                axis_params[key]=new_params[key]
        
        ax.set_xlabel(axis_params['xlabel']['text'],
                      fontsize=axis_params['xlabel']['labelsize'])
        ax.set_ylabel(axis_params['ylabel']['text'],
                      fontsize=axis_params['ylabel']['labelsize'])
        
        if axis_params['xlim']:
            ax.set_xlim(axis_params['xlim']['xlimit'])
        if axis_params['ylim']:
            ax.set_ylim(axis_params['ylim']['ylimit'])
        if axis_params['xticks']:
            if axis_params['xticks']['spacing']:
                xtick_loc = np.linspace((ax.axis()[0]),(ax.axis()[1]),axis_params['xticks']['spacing'])
            if axis_params['xticks']['round']:
                ax.set_xticks(np.round(xtick_loc,axis_params['xticks']['round']))
            ax.tick_params(axis='x', which='major', labelsize=axis_params['xticks']['ticksize'])

        if axis_params['yticks']:
            if axis_params['yticks']['spacing']:
                ytick_loc=np.linspace((ax.axis()[2]),(ax.axis()[3]),axis_params['yticks']['spacing'])
            if axis_params['yticks']['round']:
                ax.set_yticks(np.round(ytick_loc,axis_params['yticks']['round']))
            ax.tick_params(axis='y', which='major', labelsize=axis_params['yticks']['ticksize'])  

        if axis_params['legend']:
            if axis_params['legend']['bbox_to_anchor']:
                ax.legend(bbox_to_anchor=axis_params['legend']['bbox_to_anchor'],numpoints=1,prop={'size':axis_params['legend']['size']})
            else:
                ax.legend(loc='best',numpoints=1,prop={'size':axis_params['legend']['size']})

        if axis_params['aspect']:
                x0,x1 = ax.get_xlim()
                y0,y1 = ax.get_ylim()
                ax.set_aspect(abs(x1-x0)/abs(y1-y0))
#                
        if axis_params['set_title']:
            ax.set_title(axis_params['set_title']['text'],
                         fontsize=axis_params['set_title']['titlesize'],pad=axis_params['set_title']['offset'])

