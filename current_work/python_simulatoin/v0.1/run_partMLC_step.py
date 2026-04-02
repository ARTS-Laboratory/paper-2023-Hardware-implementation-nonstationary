
"""
This script is for time series prediction based of fft.
Author: Puja Chowdhury
Supervised by: Dr. Austin Downey
Last Updated:Mar 15 17:05:01 2021
updated details: deleting computation time from testdata

"""

#%% Load Libraries
import IPython as IP
IP.get_ipython().magic('reset -sf')

import time as tm
from timeit import default_timer
import numpy as np
import scipy as sp
from scipy import fft, signal
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


def butter_lowpass(cutoff, fs, order=5):
    return sp.signal.butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = sp.signal.lfilter(b, a, data)
    return y



plt.close('all')




#%% Load data
# data_pickle = pickle.load(open('data/nonstationarity_data.pkl', 'rb'))
# aa = data_pickle['acceleration']
# tt = data_pickle['time']-data_pickle['time'][0]


D = np.loadtxt('data/data_II/Test_1.lvm',skiprows=23)
aa = D[:,3]
tt = D[:,0]

#%% Down sample the data
downsample_factor = 10
aa = aa[::downsample_factor]
tt = tt[::downsample_factor]
dt = (tt[-1]-tt[0])/tt.shape[0]
Fs = 1/dt


#%% apply a low pass filter 

# # Filter requirements.
# order = 2
# cutoff = 6000  # desired cutoff frequency of the filter, Hz


# # Get the filter coefficients so we can check its frequency response.
# b, a = butter_lowpass(cutoff, Fs, order)

# # Plot the frequency response.
# w, h = sp.signal.freqz(b, a, fs=Fs, worN=8000)
# plt.subplot(2, 1, 1)
# plt.plot(w, np.abs(h), 'b')
# plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
# plt.axvline(cutoff, color='k')
# plt.xlim(0, 0.3*Fs)
# plt.title("Lowpass Filter Frequency Response")
# plt.xlabel('Frequency [Hz]')
# plt.grid()


# # Filter the data, and plot both the original and filtered signals.
# filtered = butter_lowpass_filter(aa, cutoff, Fs, order)

# plt.subplot(2, 1, 2)
# plt.plot(tt, aa)
# plt.plot(tt, filtered)
# #plt.axis([0, 1, -2, 2])
# plt.xlabel('frequency')
# plt.ylabel('amplitude')
# plt.title('filtering data')
# plt.tight_layout()
# plt.show()

#%% generate data

# for simplicity, use the same time vector
# data_pickle = pickle.load(open('data/nonstationarity_data.pkl', 'rb'))
# tt = data_pickle['time']-data_pickle['time'][0]

# frequency_list_build_signal = [50,75,82] # list of frequencies used to build the signal in Hz.

# aa = np.zeros(tt.shape[0])
# for i in frequency_list_build_signal:
#     aa = aa + np.sin(i*2*np.pi*tt)





#%% Plot the original data
plt.figure()
plt.plot(tt,aa)
plt.xlabel('time (s)')
plt.ylabel('acceleration (g)')
plt.title('original data (time series)')
plt.grid()


#%% FFT over original data (Austin Code)

# Number of sample points
N = aa.size

#yf = sp.fft.fft(aa)
yf = 2.0/N * np.abs(sp.fft.fft(aa)[0:N//2])
xf = sp.fft.fftfreq(N, dt)[:N//2]


plt.figure()
# plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.plot(xf, yf)
plt.grid()
plt.xlabel('frequency')
plt.ylabel('amplitude')
plt.title('original data (frequency domain)')
plt.xlim([0,400])
plt.show()






#%% Configuration
window_time = 1          # training time use for the fft in seconds
window_steps = int(Fs * window_time)
forecast_horizon_time = 0.1 # time of prediction
forecast_horizon_steps = int(Fs * forecast_horizon_time)



#%% Process the data

# set the first step
i = 0


xx = aa[0+i:window_steps+i]
# Processing frequency:
n = xx.size
t1 = np.arange(0, n)
p = np.polyfit(t1, xx, 1)
xx_notrend = xx - p[0] * t1  # detrended x
xx_freqdom = fft.fft(xx_notrend)  # detrended x in frequency domain
f = fft.fftfreq(n, d=dt)  # frequencies




#%% Perform forecasting using all frequencies 
#signal_pred = partMLC.fft_prediction(xx,dt,forecast_horizon_steps,returnVector=True) # Returns the vector of data up to forcast_horizon_steps if returnVector=True



#%% Perform forecasting using selected frequencies 

# frequency_list = [50,75,82]
# frequency_list_conjugated = np.hstack((np.asarray(frequency_list),np.asarray(frequency_list)*-1))
# signal_pred = partMLC.fft_prediction(xx,dt,forecast_horizon_steps,frequency_list_conjugated,returnVector=True) # Returns the vector of data up to forcast_horizon_steps if returnVector=True


#%% Perform forecasting using peaks selected from FFT picked from the freq peaks

frequency_peaks_height = 5     # percent of the peak measured from the max peak
frequency_peaks_distance = 100   # bins away that a new peak must be
 
# find the peaks and conjugate
frequency_peaks_bins = sp.signal.find_peaks(yf,distance=frequency_peaks_distance,
                                            height = np.max(yf)*(frequency_peaks_height/100))
frequency_list = xf[frequency_peaks_bins[0]]
frequency_list_conjugated = np.hstack((np.asarray(frequency_list),np.asarray(frequency_list)*-1))
print(frequency_list)

# Returns the vector of data up to forcast
signal_pred = partMLC.fft_prediction(xx,dt,forecast_horizon_steps,frequency_list_conjugated,returnVector=True) 








#%% plot the results

tt_signal_pred = tt[i+window_steps:i+window_steps+forecast_horizon_steps]

plt.figure()
plt.plot(tt,aa)
plt.plot(tt_signal_pred,signal_pred)
plt.plot(tt_signal_pred[-1],signal_pred[-1],'x')
plt.xlim([tt[i],tt[i+window_steps+forecast_horizon_steps+5]])



























