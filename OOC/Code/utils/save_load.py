
"""
This module is used for saving and loading data and files.

"""
import pickle
import pandas as pd
import numpy as np
import os

def save_data(data,filename,file_format,folder='/Data'):
    
    """
    Saves the data for later use
    
    Parameters
    ----------
    
    data: array_like
        data to be stored
        
    filename: stringor
        filename to store to
        
    file_format: sting
        file format
    
    folder:
        folder to store to 
    
    """
    from utils.utils import check_directory
    check_directory(folder)
    if file_format == 'pkl' and type(data) == pd.core.frame.DataFrame:
        data.to_pickle(folder+'/'+filename+'.pkl')
    elif file_format == 'pkl' and isinstance(data,object):
        with open(folder+'/'+filename+'.pkl', 'wb') as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

def save_average(df,data,row,col,ignore=[]):
    
    """
    Averages the data and places it in the dataframe
    
    Parameters
    ----------
    
    df: pandas dataframe
        the dataframe where the data needs to be stored
        
    data: dictionary
        contains all the information to be stored
            
    row: string or number
        row name, in which the data needs to be placed
    
    col: string or number
        column name, in which the data needs to be placed
        
    ignore: string
        names of the dictionary keys that shouldn't be averaged
    
    """

    
    new_data_mean={}
    N_dict=np.shape(data[0])[0] # number of dictionaries inside
    for i in range(N_dict):
        keys=list(data[0][i].keys()) # dictionary keys
        for key in keys:
            if key in ignore:
                new_data_mean[key]=[item[i][key] for item in data]
            else:
                data_key=[item[i][key] for item in data]
                new_data_mean[key]=np.mean(data_key,axis=0)
    df.loc[row][col]=new_data_mean




def save_notes(notes,simID,path):
    
    """
    Save the notes about the current simulation 
        
    Parameters
    ----------
    
    notes : string
        text specifing what is special about the simulation
        
    simID : string
       simulation ID
       
    path : string
       directory to save
       
    """
    from utils.utils import check_directory
    import csv
    folder=path+'/Log/'
    check_directory(path+'/Log/')
    fields=[simID,notes]
    try:
        with open(folder+'notes.csv','a') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
    except IOError:
        with  open(folder+'notes.csv','w') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            

def load_params(simID,path):
    
    """
    Load saved simulation parameters
        
    Parameters
    ----------
    
    simID : string
       simulation ID
    path : string
       the base directory
       
    Returns
    --------
    
    all information about the given simulation: class instance

       
    """
    from utils.utils import update_path
    params=pickle.load( open(path+'/Log/metadata_'+simID+'.pkl', "rb" ))
    params.data_dir=update_path(path,params.data_dir)
    params.data_dir="/".join(params.data_dir.split(os.sep)[:9])+'/'
    params.path=update_path(path,params.path)
    return params


def load_data(input_dir):
    
    """
    Load all the data from a specific simulation
        
    Parameters
    ----------
    
    input_dir : string
       path to the simulation folder
       
    Returns
    -------
    data : array_like
    
    """

    from utils.utils import list_chronologically
    import pandas as pd
    folders=list_chronologically(input_dir)
    data_all=[{item:[]} for item in folders][0]
    for ind,folder in enumerate(folders):
        full_path=input_dir+folder+'/'
        filenames=sorted([item for item in os.listdir(full_path) if item[-3:]=='pkl'])
        data=[pd.read_pickle(full_path+file) for file in filenames]
        data_all[folder]=data
    return data_all
