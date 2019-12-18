#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:03:41 2019

@author: lupe
"""

import numpy as np
import matplotlib.pyplot as plt
from calculateFieldShift import *



Chi =  24.1*1e-6 # (ppm) Susceptibilidad volumetrica
Chi = 1.0

obj = np.zeros([128,128,128])
obj[39:79,39:79,39:79] = Chi


obj = np.zeros([8,8,8])
obj[2:5,2:5,2:5] = Chi


voxelSize = [1,1,1]



dChi_3D = obj

delta, Zc = calculateFieldShift(dChi_3D, voxelSize)
delta = delta * 1e6 # paso a ppm

#%%
#c_lim = max([abs(np.amin(delta)), abs(np.amax(delta))])
#
#
#plt.figure(1)
#a = delta[:,63,:]
#a = a.T
#plt.imshow(a, cmap='bwr', vmin=-c_lim, vmax=c_lim)
#plt.colorbar
#
#
#plt.figure(2)
#plt.contour(a, 20, cmap='bwr', vmin=-c_lim, vmax=c_lim)
#plt.colorbar