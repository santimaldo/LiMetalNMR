# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 12:28:55 2021

@author: santi
"""


import numpy as np
import matplotlib.pyplot as plt


radio = 10
N = 2*radio+2
o = np.zeros([N,N])
c = np.zeros([N,N])

xc = N/2 - 0.5
yc = N/2 - 0.5




def func_exact(x,y,B0=1, r=radio):  
  Chi = 24.1e-6
  zz = y
  yy = x
  xx = 0  
  f = (1/3)*Chi*radio**3*(2*zz**2-xx**2-yy**2)/(xx**2+yy**2+zz**2)**(2.5)  
  f = f*B0+B0
  return f



r2 = radio**2
for ind_x in range(N):
  for ind_y in range(N):
    if (ind_x-xc)**2+(ind_y-xc)**2<r2:
      o[ind_y, ind_x] = 1
      
      # c[ind_y, ind_x] = -(ind_y-yc)**4 + (ind_x-xc)**4
      c[ind_y, ind_x] = func_exact((ind_y-yc),(ind_y-yc), B0=1)
      
      # if np.random.rand()<0.5:
      #   # for iy in [0,1]:
      #   #   for ix in [0,1]:
      #   o[ind_y, ind_x] = 0


        
        
obj = o>0.5

       
obj = np.ma.masked_less(obj, 1)        
      


Drawing_uncolored_circle = plt.Circle( (xc+0.5,yc+0.5), radio, fill = False, color=(252/256,201/256,50/256), ls='--',lw=3 )
  
figure, axes = plt.subplots()  
axes.set_aspect( 1 )
axes.pcolormesh(c, vmin=)
axes.pcolormesh(obj, facecolor='None', edgecolors='k')
axes.add_artist( Drawing_uncolored_circle)
plt.show()      




