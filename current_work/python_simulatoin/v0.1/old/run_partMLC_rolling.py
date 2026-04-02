
"""
This script is for time series prediction based of fft.
Author: Puja Chowdhury
Supervised by: Dr. Austin Downey
Last Updated:Mar 15 17:05:01 2021
updated details: deleting computation time from testdata

"""

#%% Load Libraries
import time as tm
from timeit import default_timer
import IPython as IP
IP.get_ipython().magic('reset -sf')
import numpy as np
import pickle
import math
import numpy as np
from numpy import fft, math
import sklearn
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import partMLC

def range_with_floats(start, stop, step):
    while stop > start:
        yield start
        start += step

plt.close('all')




#%% Load data
data_pickle = pickle.load(open('data/nonstationarity_data.pkl', 'rb'))
aa = data_pickle['acceleration']
tt = data_pickle['time']
dt = (tt[-1]-tt[0])/tt.shape[0]
Fs = 1/dt

#%% Plot the original data
plt.figure()
plt.plot(tt,aa)
plt.xlabel('time (s)')
plt.ylabel('acceleration (g)')
plt.title('original data (time series)')
plt.grid()

#%% FFT over original data
N = aa.size
T = np.arange(0, N)
P = np.polyfit(T, aa, 1)
X_notrend = aa - P[0] * T  # detrended x
X_freqdom = fft.fft(X_notrend)  # detrended x in frequency domain
F = fft.fftfreq(N, d=dt)  # frequencies
plt.figure()
plt.plot(np.absolute(F),np.absolute(X_freqdom), '--',  label='frequency domain')
plt.xlabel('frequency')
plt.ylabel('amplitude')
plt.title('original data (frequency domain)')
plt.grid()


#%% Configuration
window_time = 1          # training time use for the fft in seconds
window_steps = int(Fs * window_time)
forecast_horizon_time = 0.001 # time of prediction
forecast_horizon_steps = int(Fs * forecast_horizon_time)


# series_length=1.18
# sliding_size=0.001
# computation_time=0#0.001



# # data_pickle = pickle.load(open('../data/3_data_sets/testing data_cut_data/data_fft_und.pkl', 'rb')) # adapted for MLP data
# Ts=(data_pickle['time'][-1]-data_pickle['time'][0])/data_pickle['time'].shape[0]
# dt=Ts
# Fs =math.floor(1/Ts)
# zero_crop=500480
# strt_crop = 468530-int((input_time+computation_time)*Fs)
# end_crop = 533086+int((input_time+computation_time)*Fs)
# acceleration=data_pickle['acceleration'][strt_crop:end_crop]
# time=data_pickle['time'][strt_crop:end_crop]





#%%

# x_test_data = acceleration[int((input_time+computation_time)* Fs):] 
# # pickel file nameing
# saveNameIdx='100010' # input time * 1000,time_to_predict * 1000, computation_time *1000
# #%% plot the orginal data and the FFT
# plt.figure()
# plt.plot(time,acceleration)
# plt.xlabel('time')
# plt.ylabel('acceleration')

#plt.savefig('plots/original_data_time_series')


#%% data dictionary
td_section = {}  
td_section['time_org']=[]
td_section['x_train_data']=[]
td_section['x_test_data']=[]
td_section['signal_pred_time']=[]
td_section['signal_pred_data']=[]
td_section['mae'] = []
td_section['mse'] = []
td_section['rmse'] = []
td_section['trac'] = []
    
# # split the data
# count=0
# for i in range_with_floats(0,series_length, sliding_size):
#     # starting_point=round(i*Fs)
#     starting_point=int(round(i*Fs))    
#     ending_point_train =int(round(starting_point + (input_time * Fs)))
#     ending_point_test = int(round(starting_point + (time_to_predict * Fs)))
#     x_train_data_org = acceleration[starting_point:ending_point_train]
#     x_test_data_split = x_test_data[starting_point:ending_point_test]
    
#     time_org=time[starting_point:ending_point_train]
#     td_section['time_org'].append(time_org)
#     td_section['x_train_data'].append(x_train_data_org)
#     td_section['x_test_data'].append(x_test_data_split)
#     td_section['signal_pred_time'].append(time[ending_point_train+int(round(computation_time*Fs)):ending_point_train+int(round(computation_time*Fs))+int(round(time_to_predict*Fs))])
#     count+=1
    

#%% Process the data

for i in range(2):


    xx = aa[0+i:window_steps+i]
    # Processing frequency:
    n = xx.size
    t1 = np.arange(0, n)
    p = np.polyfit(t1, xx, 1)
    xx_notrend = xx - p[0] * t1  # detrended x
    xx_freqdom = fft.fft(xx_notrend)  # detrended x in frequency domain
    f = fft.fftfreq(n, d=dt)  # frequencies
    
    ## sorted  frequencies with more impect on the original FFT

    freq_list = [20,60,70,80,100,120,140,150,160,170,180,200,220,240,
                -20,-60,-70,-80,-100,-120,-140,-150,-160,-170,-180,-200,-220,-240]

    #signal_pred = partMLC.fft_prediction(xx,dt,forecast_horizon_steps,freq_list,returnVector=True) # Returns the vector of data up to forcast_horizon_steps if returnVector=True
    signal_pred = partMLC.fft_prediction(xx,dt,forecast_horizon_steps,returnVector=True) # Returns the vector of data up to forcast_horizon_steps if returnVector=True
#     ## error calculation
#     td_section['mae'].append(mean_absolute_error(td_section['x_test_data'][select_idx], signal_pred))
#     td_section['mse'].append(sklearn.metrics.mean_squared_error(td_section['x_test_data'][select_idx], signal_pred))
#     td_section['rmse'].append(math.sqrt(sklearn.metrics.mean_squared_error(td_section['x_test_data'][select_idx], signal_pred)))   
#     td_section['trac'].append(np.dot(td_section['x_test_data'][select_idx].conj().T, signal_pred)** 2/((np.dot(td_section['x_test_data'][select_idx].conj().T, td_section['x_test_data'][select_idx])) *(np.dot(signal_pred.conj().T, signal_pred))))
   
#     td_section['signal_pred_data'].append(signal_pred)


# print('saving pickle')

# #%%
# signal_pred_data_all = np.concatenate(td_section['signal_pred_data'], axis=0, out=None)
# x_test_data_all = np.concatenate(td_section['x_test_data'], axis=0, out=None)
# Sig_pred_time_all = np.concatenate(td_section['signal_pred_time'], axis=0, out=None)
# error = abs(x_test_data_all-signal_pred_data_all)

# plt.figure()
# fig1 = plt.figure()
# ax = fig1.add_subplot(211)
# ax.plot(Sig_pred_time_all,error,'-',linewidth=.5, label='error for 0.5 sec learning window')
# ax.plot([0,0],[-.01, .19],'--',color='black')
# # ax.set_ylim([-.01, .19])
# plt.xlabel('time (s)')
# plt.ylabel('error (m/s$^2$)')
# plt.grid()
# plt.xlim()
# ax = fig1.add_subplot(212)
# ax.plot(Sig_pred_time_all,x_test_data_all,'-',linewidth=.5, label='valid')
# ax.plot(Sig_pred_time_all,signal_pred_data_all,'--',linewidth=.5, label='prediction')
# ax.plot([0,0],[-.19, .19],'--',color='black')
# ax.set_ylim([-.17, .19])
# plt.xlabel('time (s)')
# plt.ylabel('acceleration (m/s$^2$)')
# plt.legend(ncol=2)
# plt.grid()
# fig1.tight_layout()
# # plt.savefig('plots_FFT/truth_pred_error_IP_1s_pred_1ms_ct_0s.png', dpi=400)
# #%%
# #%%
# plt.figure()
# fig2 = plt.figure()
# ax = fig2.add_subplot(111)
# ax.plot(Sig_pred_time_all,x_test_data_all,'-',linewidth=.5, label='valid')
# ax.plot(Sig_pred_time_all,signal_pred_data_all,'--',linewidth=.5, label='prediction')
# ax.plot([0,0],[-.19, .19],'--',color='black')
# ax.set_xlim([-.17, .19])
# plt.xlabel('time (s)')
# plt.ylabel('acceleration (m/s$^2$)')
# plt.legend(ncol=2)
# plt.grid()
# fig2.tight_layout()
# # plt.savefig('plots_FFT/truth_pred_error_IP_1s_pred_1ms_ct_0s_zoomed.png', dpi=400)
