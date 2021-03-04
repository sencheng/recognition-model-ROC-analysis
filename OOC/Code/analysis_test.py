"""
Created on Wed Aug  7 23:17:54 2019

@author: olya
"""

import pickle
import os
from utils.utils import update_path
path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))


class analysis: 
    def __init__(self, simID,nn=0, effect=None, cond='30'):
        self.simID = simID
        self.params = pickle.load(open(path+'/Log/metadata_'+simID+'.pkl', "rb" ))
        self.params.data_dir = update_path(path,self.params.data_dir)
        self.params.path = update_path(path,self.params.path)
        self.nn = nn
        self.cond =cond
        if effect:
            self.params.effect=effect
        # self.params.effect ='olap'
            
    def get_name(self):
        if 'length' in self.params.effect:
            name = 'length'
        elif 'strength' in self.params.effect:
            name = 'strength'
        else:
            name=self.params.effect
        return name

    def plot(self,plot_cond, plot_params=False):
        if 'item' in self.params.effect:
           from analysis.plot_item import plot_individual
           self.plots = plot_individual(self.params,nn=self.nn, cond=self.cond)
           if plot_cond == 'general':
              self.plots.load_data()

              if self.params.effect == 'item':
                 # self.plots.correct_retrieval()
                 self.plots.distance_histograms()
                 self.plots.roc_curves()
              elif 'olap' in self.params.effect:
                  self.plots.overlap_hist()
                  
           elif plot_cond == 'dpsd':
                self.plots.load_dpsd_data()
                if self.params.effect == 'item':
                   self.plots.features_heatmap()
                   self.plots.noise_effect()
                   self.plots.roc_curves()

                elif 'olap' in self.params.effect:
                   self.plots.overlap_effect()
                   self.plots.overlap_comparison()

        elif 'assoc' in self.params.rec_test:
            from analysis.plot_assoc import plot_individual
            self.plots = plot_individual(self.params,nn=self.nn, cond=self.cond)
            if plot_cond == 'general':
              self.plots.load_data()
              # self.plots.distance_histograms(param='-assoc')
              # self.plots.distance_histograms(param='-item')
              # self.plots.rates()
        else:
          import analysis.plot_effects
          if 'olap' in self.params.effect:
              plot_params = {'roc_curves':{'run':False},
                                                'overlap_ROCs': {'run':True}}          
              name='liberal_bias'
          else:
              name = self.get_name()
          plot_class = getattr(analysis.plot_effects,name)
          self.plots = plot_class(self.params,plot_cond=plot_cond,plot_params=plot_params)
          self.plots.nn = self.nn
          self.plots.run()
          
          
          
def plot_default(simID):
    results = analysis(simID,nn=0)
    # try:
    results.plot('general')
    # except:
    #     pass
    try:
        results.plot('dpsd')  
    except:
        pass
    return results
 
    
# sim = '01-14_19:02:26' # 'last' or the simID needed
sim='last'
if sim=='last':
    simID = [text for text in open(os.getcwd()+'/utils/'+"simID.txt", "r")][0]
else:
    simID = sim
    
# params=plot_default(simID)
 
