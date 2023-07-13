#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 07:22:30 2020

@author: muri
"""


import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D 
import Modules.calculateFieldShift as cFS 
from Modules.SimulationVolume import *
import time

#Voy a construir un electrodo cilindrica, con las dimensiones h=0.71mm
# y d=12mm. Además quiero FOVz=10*h y FOVxy=2*d

#inicio el reloj
t0 = time.time()
#%%

N = [1024,1024,1024]
voxelSize = [0.005, 0.02, 0.02]# mm

# N = np.array([1024,1024,1024])/4
# voxelSize = np.array([0.005, 0.02, 0.02])*4# mm


N, voxelSize, FOV = SimulationVolume(voxelSize=voxelSize, N=N, anisotropico=True)

coordenadas = []
for ii in range(3):
    ##### con un voxel centrado en cero:
    # xx = np.linspace(-FOV[ii]/2.0, (FOV[ii]/2.0-voxelSize[ii]) ,N[ii]) 
    ##### FOV simetrico sin voxel en cero
    xx = np.linspace(-(FOV[ii]-voxelSize[ii])/2.0, (FOV[ii]-voxelSize[ii])/2.0,N[ii]) 
    coordenadas.append(xx)
    
z, y, x = coordenadas

Z,Y,X= np.meshgrid(z,y,x, indexing='ij')

#%%

altura = 0.71
radio = 6

muestra = np.zeros_like(X)

condicion = (X*X + Y*Y <= radio**2)
muestra[condicion] = 1

mask=np.zeros_like(muestra)
condicion = (Z*Z <= altura/2.0)
mask[condicion]=1

muestra = muestra*mask

elapsed = (time.time() - t0)/60
print('---  armado de muestra: {:.2f} min'.format(elapsed))

#%%
# ahora calculamos la perturbacion de campo, suponiendo que esa matriz
# representa al litio
Chi =  24.1*1e-6 #(ppm) Susceptibilidad volumetrica

delta = cFS.calculateFieldShift(muestra * Chi, voxelSize)*1e6



elapsed = (time.time() - t0)/60
print("Tiempo en armar el disco y calcular:")
print('---  tiempo: {:.2f} min'.format(elapsed))
#%% GRAFICOS

z_slice = int(N[0]/2)



plt.figure(10)
plt.pcolormesh(x, y,muestra[z_slice,:,:])
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')


v = 5
plt.figure(11)

plt.pcolormesh(x,y,delta[int(1.5*z_slice),:,:], cmap='seismic', vmax=v, vmin=-v)
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.colorbar()

# slice en x

x_slice = int(N[2]/2)

plt.figure(20)
plt.pcolormesh(y,z,muestra[:,:,x_slice])
plt.xlabel('y [mm]')
plt.ylabel('z [mm]')


v = 4
plt.figure(21)
plt.pcolormesh(y,z,delta[:,:,x_slice], cmap='seismic', vmax=v, vmin=-v)
plt.xlabel('y [mm]')
plt.ylabel('z [mm]')
plt.colorbar()


plt.show()