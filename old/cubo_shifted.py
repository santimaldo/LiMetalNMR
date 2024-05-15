#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Feb 17 2022

@author: santi
"""
#stop

import numpy as np
import matplotlib.pyplot as plt
import Modules.calculateFieldShift as cFS
from scipy import integrate
import time

"""
Este script es para verificar que ocurre si el cubo se encuentra cerca del
borde del fov
"""

#inicio el reloj
t0 = time.time()
#%%----------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Parametros fisicos
Chi =  1e-6 #(ppm) Susceptibilidad volumetrica
B0 = 7 # T

# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
FOV = 0.512
N   = 256
voxelSize = FOV/float(N)
#%% CREACION DE LA MUESTRA-----------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
diametro = 0.128
# x = np.linspace(-FOV/2.0, (FOV/2.0-voxelSize) ,N) # con un voxel centrado en cero
x = np.linspace(-(FOV-voxelSize)/2.0, (FOV-voxelSize)/2.0,N) # FOV simetrico sin voxel en cero
y = x
z = x

Z,Y,X= np.meshgrid(z,y,x, indexing='ij')


muestra = np.zeros_like(X)
r2=(diametro/2.0)**2
condicion = (X*X <= r2)
muestra[condicion] = 1
condicion = (Y*Y <= r2)
mask=np.zeros_like(muestra)
mask[condicion]=1
muestra = muestra*mask
condicion = (Z*Z <= r2)
mask=np.zeros_like(muestra)
mask[condicion]=1
muestra = muestra*mask

shift = 95
muestra_2 = np.roll(muestra, shift, axis=0)
#%% calculo el campo-----------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

eta = cFS.calculateFieldShift(muestra*Chi, [voxelSize]*3)
eta_2 = cFS.calculateFieldShift(muestra_2*Chi, [voxelSize]*3)

Bnuc = eta*B0 + B0
Bmac = Bnuc/(1-2/3*muestra*Chi)

#%%
# graffff
n=0


n+=1
vmax = np.max(np.abs(eta[:,int(N/2),:]))
plt.figure(n)
plt.pcolormesh(X[:,int(N/2),:], Z[:,int(N/2),:], eta[:,int(N/2),:], cmap='seismic', vmax=vmax, vmin=-vmax)
plt.xlabel("x")
plt.ylabel("z")
plt.title(r"$\chi=${}".format(Chi))
plt.colorbar()

n+=1
vmax = np.max(np.abs(eta_2[:,int(N/2),:]))
plt.figure(n)
plt.pcolormesh(X[:,int(N/2),:], Z[:,int(N/2),:], eta_2[:,int(N/2),:], cmap='seismic', vmax=vmax, vmin=-vmax)
plt.xlabel("x")
plt.ylabel("z")
plt.title(r"$\chi=${}".format(Chi))
plt.colorbar()


n+=1
plt.figure(n)
plt.plot(Z[:,int(N/2),int(N/2)], eta[:,int(N/2),int(N/2)])
plt.plot(Z[:,int(N/2),int(N/2)]-(shift*voxelSize), eta_2[:,int(N/2),int(N/2)], '--')
plt.xlabel("z")
plt.ylabel("ppm")


n+=1
plt.figure(n)
plt.plot(Z[:,int(N/2),int(N/2)], eta[:,int(N/2),int(N/2)])
plt.plot(Z[:,int(N/2),int(N/2)]-(shift*voxelSize), eta_2[:,int(N/2),int(N/2)], '--')
plt.xlabel("z")
plt.ylabel("ppm")

