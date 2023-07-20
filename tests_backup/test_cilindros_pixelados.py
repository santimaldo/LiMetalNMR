# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 12:28:55 2021

@author: santi
"""


import numpy as np
import matplotlib.pyplot as plt


radio = 5
N = 2*radio+2
o = np.zeros([N,N])
c = np.zeros([N,N])

xc = N/2 - 0.5
yc = N/2 - 0.5

r2 = radio**2
for ind_x in range(N):
    for ind_y in range(N):
        if (ind_x-xc)**2+(ind_y-xc)**2<r2:
            o[ind_y, ind_x] = 1
      
                
obj =  o >0.5
      
obj = np.ma.masked_less(obj, 1)        
      
Drawing_uncolored_circle = plt.Circle( (xc+0.5,yc+0.5), radio, fill = False, color='r', ls='--',lw=3 )
  
figure, axes = plt.subplots()  
axes.set_aspect( 1 )
axes.pcolormesh(o, cmap='Blues')
axes.pcolormesh(obj, facecolor='None', edgecolors='k')
axes.add_artist( Drawing_uncolored_circle)
plt.show()      




