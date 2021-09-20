import matplotlib.pyplot as plt
import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__), "../src/"))
from photometry_analysis import load, correct, detrend, get_bl_params, get_zscore
from gen_pulse_train import *

# script is called with animal as an argument
if __name__ == '__main__':
    SRf = int(sys.argv[1])
    bl0i = int(sys.argv[2])
    bl0f = int(sys.argv[3])
    bl1i = int(sys.argv[4])
    bl1f = int(sys.argv[5])

# create dict for baseline pre/post indices
indexes = {
    'pre'   : [int(bl0i*SRf),int(bl0f*SRf)],
    'post'  : [int(bl1i*SRf),int(bl1f*SRf)]
}

print('select photometry recording to load and correct')
from tkinter.filedialog import askopenfilename
filename = askopenfilename()    
pmd_directory = os.path.split(filename)[0]
print(pmd_directory)

# step 1: load photometry data
channels,dec = load(pmd_directory,filename,SRf)
chan1 = channels['AIn-1 - Dem (AOut-1)']
chan2 = channels['AIn-2 - Dem (AOut-2)']
t_dec = channels['Time(s)']

#step 2: correct timeseries for motion artifacts
final, corrected = correct(chan1,chan2)

# step 3: remove exponential trend (i.e. as caused by photobleaching) from the trace
detrended,trend = detrend(t_dec,corrected,indexes)

# step 4: get baseline statistics and transform timeseries to zscore
bl_params = get_bl_params(detrended,indexes)
zscore = get_zscore(detrended,bl_params)

# plot the output at each step
fig, (ax0,ax1,ax2) = plt.subplots(3,1,sharex=True)

ax0.plot(t_dec/60,chan1,color='dodgerblue',label='F, EX: 465 nm (208 Hz)')
ax0.plot(t_dec/60,chan2,color='indigo',label='AF, EX: 405 nm (531 Hz)')
ax0.plot(t_dec/60,final,color='orange',label='AF, EX: 405 nm (fitted)')
ax0.plot(t_dec/60,corrected,color='dimgray',label='Motion Corrected')

ax1.axvline(bl0i/60,linestyle='--',color='k')
ax1.axvline(bl0f/60,linestyle='--',color='k')
ax1.plot(t_dec/60,corrected,color='firebrick',label='Motion Corrected')
#ax1.plot(t_dec/60,detrended,color='dimgray',label='Detrended')
ax1.plot(t_dec/60,trend,color='red',label='Trend')

ax2.plot(t_dec/60,zscore,color='dimgray',label='Z Score')
ax2.axvline(bl0i/60,linestyle='--',color='k')
ax2.axvline(bl0f/60,linestyle='--',color='k')

ax0.set_ylabel('Fluorescence Intensity (a.u.), $F$')
ax1.set_ylabel('Fluorescence Intensity (a.u.), $F$')
ax2.set_ylabel('Detrended Z Score')

ax1.set_xlabel('Time (minutes)')

for ax in (ax0,ax1,ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc='upper right',frameon=False)
    ax.grid(True)

plt.show()