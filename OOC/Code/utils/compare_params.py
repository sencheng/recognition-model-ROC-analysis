"""
@author: cdanhong
Compare the parameters form different simulations

"""

import pickle
import os
import numpy as np
path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
os.chdir(path)
path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))

def load_param_dir(simID):
    params=pickle.load( open(path+'/Log/metadata_'+simID+'.pkl', "rb" ))
    load_data=dir(params)
    return load_data

def load_param_data(simID,param_dir):
    params=pickle.load( open(path+'/Log/metadata_'+simID+'.pkl', "rb" ))
    data=[]
    for item in param_dir:
        data.append(params.__getattribute__(item))
    return data

def load_attr(simID):
    param_dir=load_param_dir(simID)
    param_data=load_param_data(simID,param_dir)
    return [param_dir,param_data]


simID1='01-15_15:31:19'
simID2='01-02_21:48:15'

attr1=load_attr(simID1)
attr2=load_attr(simID2)

attr1_names=[item for item in attr1[0]  if item[0]!='_']
attr2_names=[item for item in attr2[0]  if item[0]!='_']
attr_all=np.unique(attr1_names+attr2_names)


ignore=['notes','update_params','simID','show_fig','save_metadata','save_figs',
        'save_metadata','path','notes','matlab',
        'data_dir','count','cond']

print(simID1+'-->'+simID2)
for items in attr_all:
    if items not in ignore:
        try:
            ind1=attr1[0].index(items)
        except: 
            ind2=attr2[0].index(items)
            print(items+' '+str(attr2[1][ind2])+'--> ')
            ind1=None
        try:
            ind2=attr2[0].index(items)
        except:
            ind1=attr1[0].index(items)
            print(items+' -->'+str(attr1[1][ind1]))
            ind2=None
        if None not in [ind1,ind2]:
            if attr1[1][ind1]!=attr2[1][ind2]:
                print(items+': '+str(attr1[1][ind1])+'-->'+str(attr2[1][ind2]))
