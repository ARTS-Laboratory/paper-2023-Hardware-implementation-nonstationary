#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:05:28 2019

Life satisfaction index example

@author: austin
"""

import IPython as IP
IP.get_ipython().magic('reset -sf')

import numpy as np
import scipy as sp
import pandas as pd
from scipy import fftpack, signal # have to add 
import matplotlib as mpl
import matplotlib.pyplot as plt
import sklearn as sk
import time 
from sklearn import linear_model
from sklearn import pipeline
from sklearn import datasets
from sklearn import multiclass

cc = plt.rcParams['axes.prop_cycle'].by_key()['color'] 
plt.close('all')


#%%




rand_4096 = (np.random.rand(4096)*2-1)*5
rand_254 = (np.random.rand(254))*5

np.savetxt('rand_4096.txt',rand_4096)


tt = time.clock()
rand_254_sorted = np.sort(rand_254)
compute_time = time.clock()-tt

compute_time






