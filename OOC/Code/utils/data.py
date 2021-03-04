"""
This module contains functions for handling data, such as selecting data from specific conditions etc.
"""
import pandas as pd

def create_dataFrame(rows, columns):
    
    """
    Creates a pandas dataframe with the given number of rows and columns
    
    Parameters
    ----------
     rows: int
           the number of rows
     columns: int
           the number of columns
    
    Returns
    --------
    
    the empty dataframe: pandas dataframe
        
    """
    df=pd.DataFrame(index=rows, columns=columns)
    return df

def get_data(data,info,row,col):
    
    """
    Retrives the required data from a larger dataset
    
    Parameters
    ----------
    
    data :    list
              the dataset containing all dataframes
              
    info :    string
              the information to be retrieved
    row: 
          row header(s) to be accessed
        
    col: 
         column header(s) to be accessed  
    
    Note: you can provide either multiple row or multiple column headers
                     
    Returns
    --------
    
    the required dataset: list
               
    """
    data_new=[]
    for data1 in data:
        try:
            data_new.append([item[info] for item in data1.loc[row,col]])
        except:
            try:
              data_new.append(data1.loc[row,col][info])

            except:
                try:
                   data_new.append([item[info] for item in data.loc[row,col]])
                except:

                    data_new.append(data.loc[row,col][info])
                data_new=data_new[0]
                break
    return data_new

def select_data(data,info,row,col):
    
    """
    Extract information from a dataframe given the row, column names and the required field
    
    Parameters
    ----------
    
    data : pandas dataFrame
      the whole data
    info : string
        the  keys to be asessed in the dictionary
        
    row, col : integer or string
        column header to be accessed 
    Returns
    --------
    
    the required information: list
               
    """

    data_new=[{item:[]} for item in info][0]
    for key in data_new.keys():
        data_new[key]=get_data(data,key,row,col)
    return data_new
