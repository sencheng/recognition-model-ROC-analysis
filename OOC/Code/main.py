import numpy as np
from utils.set_params import sim_params,meta_params
import utils.simulations as sim
from analysis_test import plot_default
import os
path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
run = True
effects = ['item']

if run:
    for effect in effects:
      print('Simulating the effect of '+ effect)
      params = sim_params()
      cond_params,cond_values,conditions = meta_params(effect)
      for cond_ind, cond in enumerate(conditions):
          params_change = {'noise': [0.3],
                         'trials':100,'effect':effect,'matlab':True,
                         'offset':[10],'save_figs':True,'bias_offset':0.006}
          
          for ind, item in enumerate(cond_params):
              params_change.update({item:cond_values[ind][cond_ind]})
          params.update_params(params_change)
          # params.update_params({'notes': f'thr_assoc:{params.thr_assoc},trials:{params.trials} pairing:{params.pairing}'})
          
          try: 
              cond = np.round(cond,3)
          except:
              pass
          
          params.cond = str(cond)
          params.data_dir = params.data_dir+str(cond)+'/'
          print('Parameters updated')
          print('Running the simulation for condition: '+str(cond))
          mem_sys,data = sim.run_routine(params)
      plot_default(params.simID)
          
