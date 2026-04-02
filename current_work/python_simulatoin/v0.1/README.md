# v0.1
1. Code built by Austin to look at getting the FFT code working. 
1. Questions, for Puja, 
    1. Should we detrend in the function? 
    1. I took thie detrend out of this code as its not needed for this dataset in general. 
1. This code work for a few datasets, but should just use data_II/Test_X as these are more intresting. 

## run_partMLC_step
1. For running the code, you can either (comment out as not needed):
    1. Perform forecasting using all frequencies 
    1.  Perform forecasting using selected frequencies 
    1. Perform forecasting using peaks selected from FFT picked from the freq peaks
1. predits 1 ms into the future, but that could change as needed. 


## run_partMLC_rolling_all
1. A rolling implementaion of step that uses all frequenceies (i.e. ifft) to predict the results. 
1. Executes on every data piece. 


## run_partMLC_rolling_online_fft
1. A rolling implementaion of step that selectes frequences at each step based on FFT. 
1. Executes on every data piece. 
1. I only did bery limted tunning of the FFT selecter.
1. Did not seem to work very well, maybe the phase issue? Either way, I stopped messing with it. 
1. I just gave up.
