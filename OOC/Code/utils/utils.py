#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains handy functions to facilitate some trivial steps 
"""
import os
#path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))

def print_statement(text):
    
    """
    Enables printing in the same line
    
    Parameters
    ----------
    
    text: string
        the text to print
    """
    
    print(text, end="", flush=False)
  
            
def simID():
    
    """
    Create a simulation ID based on datetime 
    
    Returns
    -------
    simulation ID : string
    """
    from  datetime import datetime
    simID=str(datetime.now())[5:-7]
    simID=simID[:5]+"_"+simID[6:]
    path=os.path.dirname(os.path.realpath(__file__))
    text_file = open(path+'/simID.txt', "w")
    text_file.write(simID)
    text_file.close()
    return simID


def update_path(path_current,path_old, separator='recognition-memory'):
    
    """
    Update the absolute path to be able to run on different machines
    
    Parameters
    ----------
    
    path_current : string 
      the current path of the file
    path_old : string
        the saved path
    separator : string
        the main project directory
    Returns
    -------
    the updated path: string
    
    """

    ind=path_old.split(os.sep).index(separator)
    home_dir="/".join(path_current.split(os.sep)[:ind])
    base="/".join(path_old.split(os.sep)[ind:])
    return home_dir+'/'+base

def check_directory(path):
    
    """
    Check whether a given directory exist and create it otherwise
    
    Parameters 
    ----------
    
    the directory path: string 
        
        
    """
    import os
    if not os.path.exists(path):
           os.makedirs(path)
           
def list_chronologically(input_dir):
    
    """
    Return the contents of a directory in the order in which they 
    were created, this is preferred over the sorting method because then an 
    alphabetical ordering is used, which is not always the desired order, i.e.
    when comparing weak, mixed and strong conditions. 
        
    Parameters
    ----------
    
    input_dir : string
       directory to sort
    
    Returns
    --------
    
    the folder names listed chronologically : list
            

    """

    folders=os.listdir(input_dir)
    try:
        folders_path=[input_dir+item+'/' for item in folders]
        folders_path.sort(key=lambda x: os.path.getmtime(x))
    except:
        folders_path=[input_dir+'/'+item+'/' for item in folders]
        folders_path.sort(key=lambda x: os.path.getmtime(x))

    folders=[item.split('/')[-2] for item in folders_path]
    
    return folders
