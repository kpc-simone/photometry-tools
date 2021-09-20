import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys,os

def get_utrain_params(ttl_chan, t_dec, ampls, wdths):
    
    in_a_pulse = False
    old_value = 0
    tr = 0 
    
    u_starts = np.zeros( (len(ampls),))
    u_wdths  = np.zeros( (len(ampls),))
    u_ampls = np.zeros( (len(ampls),))
    
    for idx, value in ttl_chan.items():
        if in_a_pulse:
            # at the end of a pulse, 
            # get its amplitude and widths
            if value > old_value and value == 1:
                u_ampls[tr] = ampls[tr]
                u_wdths[tr] = wdths[tr]
                
                in_a_pulse = False
                tr += 1
        else:
            # at the beginning of a pulse, 
            # get its start time
            if value > old_value and value == 1:
                u_starts[tr] =  t_dec[idx]
                in_a_pulse = True

        old_value = value
        
    u_params = {
    
        'u_starts'  : u_starts,
        'u_widths'  : u_wdths,
        'u_ampls'   : u_ampls,
    
    }
        
    return u_params

def gen_stim_train(ttl_chan, intsy):
    
    stim_train = pd.Series(0.0, index = ttl_chan.index)
    in_a_pulse = False
    old_value = 0
    tr = 0 
    
    for index, value in ttl_chan.items():

        if in_a_pulse:
            stim_train[index] = intsy[tr]
            if value > old_value and value == 1:
                in_a_pulse = False
                tr += 1
        else:
            stim_train[index] = 0.0
            if value > old_value and value == 1:
                in_a_pulse = True

        old_value = value
            
    return stim_train