"""
Performs a series of calculations including rounding, normalizing etc. 

"""
import numpy as np
          
def round_for_fit(data,actual_sum):
    
    """
    Round the numbers to integer by maintaining the sum by
    
    1) Flooring everything
    
    2) Calculating the error between rounded and intact
    
    3) Rounding up the numbers starting with the ones closer to the actual until the sum matches
    
    
    Parameters
    ----------
    
    data : np.array
       array containing float numbers
    actual_sum : int
       the desired sum
    
    Returns
    -------
    the rounded numbers : array 
          

    """    
    import copy
    data_rounded=[np.floor(item) for item in data]
    data_diff=[abs(data[item]-data_rounded[item]) for item in range(len(data))]# difference between rounded and itnact
    diff=actual_sum-np.sum(data_rounded) # overall difference
    list1, list2 = zip(*sorted(zip(data_diff, data),reverse=True)) # sort the items based on the error 
    index=[list(data).index(item) for item in list2] # the order in which to round up the items
    data_new=copy.copy(data_rounded)
    ind=0
    
    while diff!=0:
      data_new[index[ind]]=np.ceil(data[index[ind]])
      ind+=1
      diff=abs(actual_sum-np.sum(data_new))
      data_new=[int(item) for item in data_new]
    return data_new


def calc_rates(data,N):
    
    """
    Used to calculate the hit and false alarm rates
    
    Parameters
    ----------
    
    data : array_like
        the raw responses
    N : int
        the number of tested items (targets or lures), used for rounding the data
   
    Returns
    ------
    the rate: array_like
    
    """
    
    data=round_for_fit(data,N)
    return np.cumsum(data)/np.sum(data)


def normalize_F(F,fa=0.1):
    
    """
    Transform the F-parameter values into probabilities to facilitate the comparison to the R-parameter. 
        
    Parameters
    ----------
    
    F : np.array
      the values to be transformed
    fa : float
     the false alarm rate for which to calculate the probability, default=0.1 similar to Yonelinas et al. 2002
    
    Returns
    -------
    array of transformed probabilities 
    
    """

    from scipy.special import ndtri
    from scipy.special import ndtr    
    
    return np.asarray([ndtr(ndtri(fa)+item) for item in F])


def zscore(x):
    
    """
    Calculate the zscore
    
    Parameters
    ----------
    
    x : array_like
      the input data
    
    Returns
    -------
    z-transformed values : array_like
    
    """
    mean=np.nanmean(x)
    std=np.nanstd(x)
    return [(item-mean)/std for item in x]

def remove_outliers(data,threshold=1.645):
    
    """
    Remove the outliers based on zscore
    
    Parameters
    ----------
    
    data : array_like
      the input data
    
    threshold: float or int
        the threshold for data exclusion
    
    Returns
    -------
    data without outliers : array_like
    
    """

    from scipy.stats import zscore
    zscores = np.abs(zscore(data)).tolist()
    return [data[zscores.index(item)] for item in zscores  if -threshold<item<threshold]

def get_histograms(data,n_bins,x_max,x_min=0):
    
    """
    Obtain histograms of data given a fixed bin number and range
    
    Parameters
    ----------
    data : array_like
        the input data
    
    n_bins : int
        the number of bins
    
    x_max: float or int
         the upper boundary of the range
    
    x_min: float or int
         the lower boundary of the range, default=0
    
    Returns
    --------
    bins and frequencies : array_like
    
    """
    return np.histogram(data,bins=n_bins,range=(x_min,x_max)) # histograms of d for targets
