"""
This modules enables interacting with matlab files used for fitting the Yonelinas model to the data by our model 

"""

import numpy as np 
import os
import pandas as pd
from utils.utils import check_directory

class matlab:
    
    """
    Class for saving and loading the data for/from matlab simulation 
    
    Parameters
    ----------
    params :  class instance
            simulation parameters

    
    """

    def __init__(self,params):
        self.params = params
    
    def prepare_data(self):
    
        """
        Select the positive responses for targets and lures 
        and save them in csv-files sorted by condition
        
            
        """
        params = self.params
        from utils.data import select_data
        input_dir = params.data_dir
        filenames = sorted([item for item in os.listdir(input_dir) if item[-3:]=='pkl' and 'std' not in item])
        data = [pd.read_pickle(input_dir+file) for file in filenames]
        print(filenames)
        self.target, self.lure = np.ones((len(filenames))).tolist(),np.ones((len(filenames))).tolist()
        for i,dat in enumerate(data):
            self.target[i] = [select_data(dat,['target'],o,params.noise)['target'] for o in params.offset]
            self.lure[i] = [select_data(dat,['lure'],o,params.noise)['lure'] for o in params.offset]
        self.filenames = [item.strip('.pkl') for item in filenames]

        path = params.data_dir+'/Matlab/Model_input/' 
        path1 = params.data_dir+'/Matlab/Model_output/' # needed for later
        check_directory(path)
        check_directory(path1)
        
        for i in range(len(self.target)):
            for ii in range(len(self.target[i])):
                name = path+self.filenames[i]+"_"+str(params.offset[ii])+".csv"
                self.save_csv(self.target[i][ii],self.lure[i][ii],name,ii+1)
        
    def save_csv(self,target,lure,name,group):
        
        """
        Save the data in csv files 
        
        Parameters
        ----------
        target: list
                contains the average number of correctly recognized targets for each condition
        
        lure: list
              contains the average number of falsely recognized lures for each condition
              
        name: string
            filename
            
        group: string
            group name

        """
        params=self.params
        from utils.calculations import round_for_fit
        import csv
        with open(name, 'w') as csvfile:
             spamwriter =csv.writer(csvfile)
             thr=np.shape(target)[-1]
             for w in range(len(params.noise)):
                 target1=round_for_fit(target[w],params.N_t)
                 lure1=round_for_fit(lure[w],params.N_t)
                 for ww in range(thr*2):
                     if ww<thr:
                         spamwriter.writerow([params.list_length]+[1]+["Noise%s" %w]+["target"]+[thr-ww]+[target1[ww]]) # because dpsd model requires integers here
                     else:
                         spamwriter.writerow([params.list_length]+[1]+["Noise%s" %w]+["lure"]+[thr-(ww-thr)]+[lure1[ww-thr]])
                



    def load_dpsd(self,fit='Rn:0',filenames=False):
        
        """
        Load the  fit parameters resulted from Yonelinas et. al dpsd model
        
        Parameters
        ----------
        params : list
                contains the average number of correctly recognized targets for each condition
        fit :    string
              fit condition to plot (defaut='Rn:0', other options are 'Full' and 'Symm')
        
        Returns
        -------
        data_all,filenames: array_like
            
        """
        params=self.params
        from scipy.io import loadmat
        import pandas as pd
        from utils.calculations import normalize_F
        from utils.utils import list_chronologically
        input_dir=params.path+'/Data/'+params.simID
        if filenames:
            filenames=filenames
        else:
            filenames = list_chronologically(input_dir)

#        print(self.input_dir)
        data_all=[[]]* len(filenames)
        for j, jj  in enumerate(filenames):

            file_dir=input_dir+'/'+jj+'/Matlab/Model_output/'+fit+'/'
            files=sorted([item for item in os.listdir(file_dir) if item[-3:]=='mat'])
            data_out=[[]]* len(files)
            
            data_cond=[loadmat(file_dir+item,struct_as_record=True)['save_data'] for item in files]
            
            for i, data in enumerate(data_cond):
                keys=list(pd.DataFrame(data[0]).columns) # get the struct fields from matlab
                data_new=dict(zip(keys, [None]*len(keys)))
        
                for key in keys:
                    if key in keys[:3]:
                        value=data[key][0][0]
                        if key=='F':
                            value=normalize_F(value) 
                            value1=value
                        value=value.T
                        data_new[key]=value
                        if key=='F':
                            data_new['F_raw']=value1 # not normalized F values
                    else:
                      value=[data[key][0][0][0][item] for item in range(len(data[key][0][0][0]))]
                    data_new[key]=value
                    data_new['info']=jj
                data_out[i]=data_new
            data_all[j]=data_out
            
        return data_all,filenames
    
