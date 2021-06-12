# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 12:28:55 2021

@author: santi
"""


import numpy as np
import matplotlib.pyplot as plt

N = 10


o = np.zeros([N,N])



radio = 3


xc = N/2 - 0.5
yc = N/2 - 0.5

r2 = radio**2
for ind_x in range(N):
  for ind_y in range(N):
    if (ind_x-xc)**2+(ind_y-xc)**2<r2:
      o[ind_y, ind_x] = 1


fig1, ax1 = plt.subplots()
ax1.set_aspect('equal')
ax1.pcolormesh(o, edgecolors='k')