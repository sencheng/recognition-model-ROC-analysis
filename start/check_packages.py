#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 11:06:59 2019

@author: hakobovg
"""
import os

local=[text for text in open(os.getcwd()+'/local_packages.txt', "r")]
project=[text for text in open(os.getcwd()+'/requirements.txt', "r")]
uninstalled=[]
for item in project:
  if item not in local:
    uninstalled.append(item)
with open('uninstalled.txt', 'w') as f:
    for item in uninstalled:
        f.write(item)