
"""
This module handles distance metrics and threshold pleacemet

"""
import numpy as np
        
def set_metric(dist_metric):
    
    """
    Sets the metric for distance calculations
    
    Parameters
    ----------
    
    dist_metric: string
                 which distance metric to use, e.g. corr (correlation distance), 
                 cosine, euclidean
    Returns
    ------
    distance measure
    """
    if dist_metric == 'corr':
        from scipy.stats import pearsonr
        pdist = pearsonr
    else:
        from scipy.spatial import distance
        pdist = getattr(distance, dist_metric)
    return pdist
    
def set_threshold(params,distances):
  
    """
    Sets the threshold based on the input distances
   
    Parameters
    --------------------------
    
    params: class instance
          contains simulation parameters
    distances: array_like
                 contains the relevant distance values
    Returns
    -------
    thresholds : array_like

    """

    from utils.calculations import remove_outliers
    N_thr = params.N_thr 
    distances_clean = remove_outliers(distances)
    thr_range= np.linspace(min(distances_clean),max(distances_clean),N_thr)
    thr_range = thr_range+params.bias_offset
    thr_range[-1] = 100 # set the last threshold to a large number to ensure that all items have been given a response
    return thr_range
   

