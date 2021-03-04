#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:38:07 2019

@author: cdanhong
"""

import os
import shutil
import pandas as pd
from datetime import date,datetime
import re
import sys
import mdp
path= os.path.abspath(os.path.join(os.getcwd(), os.pardir,os.pardir))
path=path+'/'
directories=[item for item in os.listdir(path) if os.path.isdir(f'{path}{item}') and item!='.git'] #list comprehension 
passed_days=10
today=datetime.now()


dataset=pd.read_csv(path+'/Log/notes.csv',error_bad_lines=False)
df2=dataset[dataset.columns[0]]


for directory in directories:
    if directory=='Data':
        directory=directory
    filenames=os.listdir(f'{path}{directory}')
    for file in filenames:
        match=[item in file for item in df2]
        try:
            sim_date=re.findall(r'[\d\.-]+-[\d\.-]+',file)[0]
            sim_month=int(sim_date[:2])
            sim_day=int(sim_date[-2:])
            
            delta_time= date(today.year,today.month,today.day)-date(today.year,sim_month,sim_day)
            delta_time=delta_time.days
            if delta_time>passed_days:
                try:
                    os.remove(path+directory+'/'+file)
                    print(file+' removed')
                except:
                    try:
                        shutil.rmtree(path+directory+'/'+file)
                        print(file+' removed')
                    except:
                        print('Something went wrong')
        except:
            pass



#for root, directories, filenames in os.walk('/home/cdanhong/dan-internship (copy)'):
#    for file in directories:
#            match=[fnmatch.fnmatch(file,item) for item in df2]
#            if True in match:
#                print(file)
#                pass
#            else:
#                x=datetime.datetime.now()
#                #print(x.day)
#                date0=re.findall(r'[\d\.-]+-[\d\.-]+',file)[0]
#                sim_month=int(date0[:2])
#                sim_day=int(date0[-2:])
#                
#                delta_time= date(today.year,today.month,today.day)-date(today.year,sim_month,sim_day).days
#                if delta_time>passed_days:
#                    
#
#                try:
#                    date=[int(s) for s in re.findall(r"\d+",date0[0])]
#                    if len(date)==0:
#                        pass
#                    else:
#                        if date[1]>(x.day-3):
#                            print("newdir"+file)
#                        else:
#                            try:
#                                os.remove(file)
#                                print(file+' removed')
#                            except:
#                                try:
#                                    shutil.rmtree(file)
#                                except:
#                                    print ("keep"+file)
#                                    pass
#                except:
#                    print("keep"+file)
#                    pass
#                
#    for file in filenames: 
#        match=[fnmatch.fnmatch(file,item) for item in df2]
#        if True in match:
#            print(file)
#            pass
#        else:
#            x=datetime.datetime.now()
#            #print(x.day)
#            date0=re.findall(r'[\d\.-]+-[\d\.-]+',file)
#            try:
#                date=[int(s) for s in re.findall(r"\d+",date0[0])]
#                if len(date)==0:
#                    pass
#                else:
#                    if date[1]>(x.day-3):
#                        print("newfile"+file)
#                    else:
#                        try:
#                            os.remove(file)
#                            print(file+' removed')
#                        except:
#                            try:
#                                shutil.rmtree(file)
#                            except:
#                                print ("keep"+file)
#                                pass
#            except:
#                print("keep"+file)
#                pass
#    
