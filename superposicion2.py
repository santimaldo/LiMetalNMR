#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 20:01:18 2020

@author: santi
"""

"""
Script para calcular el corrimiento del centro de una lamina.
"""


from calculateFieldShift import *
import numpy as np
import matplotlib.pyplot as plt


# Parametros fisicos
Chi =  24.1*1e-6 #(ppm) Susceptibilidad volumetrica
B0 = 7 # T
skindepth = 0.012 # profundida de penetracion, mm


# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
#voxelSize = [0.071, 0.391, 0.391]# mm
voxelSize = [0.004, 0.02, 0.02]# mm
N = [512, 128, 128]
#voxelSize = [0.006, 0.03, 0.08]# mm
#Nz, Ny, Nx = [256, 128, 128]
# con estos numeros, Nj*voxelSize_j queda
#    z: 1.536 mm  ; y: 3.84 mm  ; x: 10.24 mm

# utilizo una funcion que dado dos argumentos define el restante. Ya sea N, 
# FOV (field of view) o  voxelSize
N, voxelSize, FOV = SimulationVolume(voxelSize=voxelSize, N=N)
#N, voxelSize, FOV = SimulationVolume(N=N, FOV=FOV)
VSz, VSy, VSx = voxelSize
FOVz, FOVy, FOVx = FOV 
Nz, Ny, Nx = N


#%% CREACION DE LA LAMINA--------------------------------------------------------
# primero defino las dimensiones del objeto: obj_dim, expresada en mm.
microest = [0.080, 0.4, 0.4]
# Creo una matriz de ceros de tamaño Nz*Ny*Nx. esta matriz representa el 
# volumen simulado. Donde hay un 1, hay material. Donde hay un 0, hay vacio.
# El producto obj*Chi es la distribuion espacial de susceptibilidad magnetica.
obj = np.zeros([Nz, Ny, Nx])
# Para representar la lamina, defino las posiciones en las que inicia y termina
# la lamina en cada direccion.
# el objeto esa situado en el centro de FOVxy
# objeto2: 1 microestructura
objz = [int(Nz/2-microest[0]/VSz/2), int(Nz/2+microest[0]/VSz/2)]
objy = [int(Ny/2-microest[1]/VSy/2), int(Ny/2+microest[1]/VSy/2)]
objx = [int(Nx/2-microest[2]/VSx/2), int(Nx/2+microest[2]/VSx/2)]
obj[objz[0]:objz[1]+1, objy[0]:objy[1]+1, objx[0]:objx[1]+1]=1

 

#%%----------------------------------------------------------------------------

# sistema de coordenadas:
z = np.linspace(0, Nz-1, Nz)*VSz
y = np.linspace(-Ny/2 +1, Ny/2, Ny)*VSy
x = np.linspace(-Nx/2 +1, Nx/2, Nx)*VSx

delta = calculateFieldShift(obj*Chi, voxelSize)*1e6

#%% 
plt.figure(2)
x0 = int(Nx/2)
y0 = int(Ny/2)

#plt.plot(z, delta[:,y0+1,x0], '-')
plt.plot(z, delta[:,y0,x0], 'r-')
plt.legend()
#plt.plot(z, obj[:,y0,x0])
plt.xlabel(r"$z$ [mm]")
plt.ylabel(r"$\delta$ [ppm]")
#plt.xlim([-0.1, 0.5])
#plt.ylim([0,1.7])


#%%
splts = 1
subplt = 1

plt.figure(1235)
delta_slice = delta[:,:,int(Nx/2)]
vmax = np.max(np.max(delta_slice))
ax = plt.subplot(splts,1,subplt)
plt.pcolormesh(y,z, delta_slice, cmap='seismic', vmin=-vmax, vmax=vmax)
plt.xlabel(r"$y$ [mm]")
plt.ylabel(r"$z$ [mm]")
subplt += 1
  
#%%
path = '/home/santi/CuarenteDoctorado/LiMetal/superposicion/'

datos_delta = np.array([z, delta[:,y0,x0]]).T

np.savetxt(path+'datos_microestructura.dat', datos_delta)


