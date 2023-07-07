#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 18:58:23 2020

@author: santi

para probar el histograma 2d en B1 y B0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage as ndimage
import Modules.calculateFieldShift as cFS
#%%

# Parametros fisicos
Chi =  24.1*1e-6 #(ppm) Susceptibilidad volumetrica
voxelSize = [0.001, 0.001, 0.001]# mm
n = 256
N = [n,n,n]

obj = np.zeros(N)
# i = int(n/8)
# f = int((n-n/8))


#### varias esferas------------------------------------------------------------
x = np.arange(n)-n/2
X,Y,Z = np.meshgrid(x,x,x)

radio = 20
n_esf = int((n-radio)/(2*radio) )
xcentros = np.linspace(-n/2+radio, n/2-radio ,n_esf) 
# xcentros = xcentros[1:-1]
for zc in xcentros:
  for yc in xcentros:
      for xc in xcentros:
        obj[(X-xc)**2+(Y-yc)**2+(Z-zc)**2<radio**2] = 1
        print(zc, yc, xc)
tajada = int(n/2)
#### cubos -------------------------------------------------------------------
# i = int(n/16)
# f = int((n-n/16))
# obj[i:f,i:f,i:f]=1

# obj[np.abs(X)<n/32] = 0
# obj[np.abs(Y)<n/32] = 0
# obj[np.abs(Z)<n/32] = 0
# tajada = int(n/4)


#### esfera-------------------------------------------------------------------
# x = np.arange(n)-n/2
# X,Y,Z = np.meshgrid(x,x,x)

# radio = 110
# xc=yc=zc=0
# obj[(X-xc)**2+(Y-yc)**2+(Z-zc)**2<radio**2] = 1
# tajada = int(n/2)
#------------------------------------------------------------------------------

plt.figure(0)
plt.pcolormesh(obj[:,:,tajada])

#%%
#
print("sin aliasing...")
B0 = cFS.calculateFieldShift(obj*Chi, voxelSize) * 1e6


# tajada = int(n/2)
# plt.figure(0)
# # plt.pcolormesh(B0[:,:,tajada]*obj[:,:,tajada], cmap='seismic')
# plt.pcolormesh(B0[:,:,tajada], cmap='seismic')
#plt.pcolormesh(obj[65,:,:])

print("con aliasing...")
B0_conAlias = cFS.calculateFieldShift(obj*Chi, voxelSize, substract_aliasing=False) * 1e6


# tajada = int(n/2)
# plt.figure(1)
# # plt.pcolormesh(B0[:,:,tajada]*obj[:,:,tajada], cmap='seismic')
# plt.pcolormesh(B0_NA[:,:,tajada], cmap='seismic')
#plt.pcolormesh(obj[65,:,:])

#%%
# tajada = int(n/2)


mat1 = B0[:,:,tajada]*obj[:,:,tajada]
mat2 = B0_conAlias[:,:,tajada]*obj[:,:,tajada]
vmax = 10


# mat1 = B0[:,:,tajada]
# mat2 = B0_conAlias[:,:,tajada]


plt.figure(2)
plt.subplot(1,2,1)
plt.title("Corregido")
plt.pcolormesh(mat1, cmap='seismic', vmax=vmax, vmin=-vmax)
plt.colorbar()
plt.subplot(1,2,2)
plt.title("Sin Corregir")
plt.pcolormesh(mat2, cmap='seismic', vmax=vmax, vmin=-vmax)
plt.colorbar()

plt.figure(3)
plt.pcolormesh(mat1-mat2, cmap='seismic', vmax=vmax, vmin=-vmax)
plt.colorbar()

