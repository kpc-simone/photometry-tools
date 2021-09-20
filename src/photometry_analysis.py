from lmfit import minimize, Parameters, minimize, Parameters, Parameter, report_fit, printfuncs
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys, os

def load(directory, datafile, SR_desired):
    
    photometry_df = pd.read_csv(os.path.join(directory,datafile),skiprows=1)
    print(photometry_df.head())
    
    SR_actual = len(photometry_df['Time(s)']) / photometry_df['Time(s)'].max()
    dec = int(SR_actual / SR_desired)
    print(SR_actual,dec)
    
    channels = {}
    for col in photometry_df.columns:
        channels[col] = photometry_df.loc[:,col].iloc[::dec]
    
    return channels, dec

def compute_residual(ps, template, data_to_fit):
    
    a1 = ps['a1']
    b1 = ps['b1']
    
    data = a1 * data_to_fit + b1
    
    return template - data

def correct(chan1, chan2):
    params = Parameters()
    params.add('a1',value = 2, min = -20, max = 20)
    params.add('b1',value = -0.5, min = -20, max = 20)

    result = minimize(compute_residual, params, args=(chan1, chan2), method='leastsq')
    final = chan1 - result.residual.reshape(chan2.shape)
    corrected = ( chan1 - final ) / final
    
    return final, corrected

def exponential(x,a,tau,offset):
    
    return a * np.exp(- x / tau) + offset
        
def detrend(time,series,indexes,func=exponential):
    pre_start = indexes['pre'][0]
    pre_end = indexes['pre'][1]
    post_start = indexes['post'][0]
    post_end = indexes['post'][1]

    #print(ind#xes)
    ts = np.concatenate( (time.iloc[pre_start:pre_end],time.iloc[post_start:post_end] ),axis=0)
    ydata = np.concatenate( (series.iloc[pre_start:pre_end],series.iloc[post_start:post_end] ),axis=0)
    
    popt, pcov = curve_fit(exponential, ts, ydata, np.array([1.0,10.0,1.0]))
    fdata = exponential(time, *popt)
    detrended = series-fdata
    
    return detrended,fdata

def get_bl_params(series,indexes):
    pre_start = indexes['pre'][0]
    pre_end = indexes['pre'][1]

    bl_params = {}
    
    bl_params['mean'] = series[pre_start:pre_end].mean()
    bl_params['stddev'] = series[pre_start:pre_end].std()
    
    return bl_params

def get_zscore(series,bl_params):
    
    mean = bl_params['mean']
    stddev = bl_params['stddev']
    
    zscore = (series - mean) / (stddev)
    
    return zscore
    