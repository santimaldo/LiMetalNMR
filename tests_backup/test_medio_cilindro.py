#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on  2021-06-10

@author: santi
"""

"""
Script para calcular el corrimiento un cilindro
"""


from calculateFieldShift import *
import numpy as np
import matplotlib.pyplot as plt

#%%----------------------------------------------------------------------------  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Parametros fisicos
Chi =  24.1*1e-6 #(ppm) Susceptibilidad volumetrica
B0 = 7 # T
skindepth = 0.012 # profundida de penetracion, mm


# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
voxelSize = np.array([0.001, 0.001, 0.001])# mm
N = np.array([128,64,64])

# utilizo una funcion que dado dos argumentos define el restante. Ya sea N, 
# FOV (field of view) o  voxelSize

FOV = N*voxelSize

VSz, VSy, VSx = voxelSize
FOVz, FOVy, FOVx = FOV 
Nz, Ny, Nx = N


# CREACION DEL CILINDRO-----------------------------------------------------
# primero defino las dimensiones del objeto: obj_dim, expresada en mm.
#%%
semialtura =  30 # la altura sera entonces 2*semialtura+1 (voxels)
radio = 6

obj = np.zeros([Nz, Ny, Nx])

xc = Nx/2 - 0.5
yc = Ny/2 - 0.5

r2 = radio**2
for ind_z in range(int(Nz/2-semialtura), int(Nz/2+semialtura)+1):
  # for ind_x in range(int(Nx/2-radio-1),int(Nx/2+radio+2)):
  for ind_x in range(int(Nx/2),int(Nx/2+radio+2)):   # MEDIO CILINDRO
    for ind_y in range(int(Ny/2-radio-1),int(Ny/2+radio+2)):
      if (ind_x-xc)**2+(ind_y-yc)**2<r2:
        obj[ind_z, ind_y, ind_x] = 1
# print('listo')
#----------------------------------------------------------------------------

delta = calculateFieldShift(obj*Chi, voxelSize)
delta = delta*1e6


x0 = int(Nx/2)
y0 = int(Ny/2)
z0 = int(Nz/2+semialtura/2)


#la diagonal:   -------------------------------------------
xx,yy = np.meshgrid(np.array(range(Nx)),np.array(range(Ny)))
obj2d = obj[z0,:,:]
delta2d = delta[z0,:,:]
obj_diag = obj2d[xx==yy]
delta_diag = delta2d[xx==yy]
#-----------------------------------------------------------


plt.figure(3)
plt.plot(delta_diag, 'o-')
plt.plot(delta[z0,:,x0], 'o-')
plt.plot(delta[z0,y0,:], 'o-')
plt.xlabel(r"[voxels]")
plt.ylabel(r"$\delta$ [ppm]")


data = np.array([obj[z0,y0,:], delta[z0,y0,:],obj[z0,:,x0], delta[z0,:,x0], delta[z0,:,x0], obj_diag, delta_diag]).T
np.savetxt('S:/Doctorado/LiMetal/simulaciones/2021-06-10_superposicion_lateral/medio_cilindro/temp.dat', data)


#%%
fig1, ax1 = plt.subplots()
ax1.set_aspect('equal')
# ax1.pcolormesh(obj2d, edgecolors='k')
ax1.pcolormesh(obj2d+0.5*obj2d[:,::-1], edgecolors='k')
# vmax = np.max(np.max(delta2d))
# ax1.pcolormesh(delta2d, cmap='seismic', vmin=-vmax, vmax=vmax)
plt.xlim([25,40])
plt.ylim([25,40])
# plt.plot(np.array(range(Nx)),np.array(range(Ny)),'r')

#%%
splts = 1
subplt = 1

plt.figure(30)
delta_slice = delta[:,:,int(Nx/2)]
vmax = 0.2*np.max(np.max(delta_slice))
ax = plt.subplot(splts,1,subplt)
plt.pcolormesh(y,z, delta_slice, cmap='seismic', vmin=-vmax, vmax=vmax)
#aspecto = (Nz*voxelSize[0])/(Ny*voxelSize[1])
#ax.set_aspect(aspecto)
plt.xlabel(r"$y$ [mm]")
plt.ylabel(r"$z$ [mm]")
#%%
plt.figure(40)
delta_slice = delta[int(Nz/2),:,:]
vmax = np.max(np.max(delta_slice))
ax = plt.subplot(splts,1,subplt)
plt.pcolormesh(x,z,delta_slice, cmap='seismic', vmin=-vmax, vmax=vmax)
#ax.set_aspect((Nz*voxelSize[0])/(Nx*voxelSize[2]))
plt.xlabel(r"$x$ [mm]")
plt.ylabel(r"$y$ [mm]")

subplt += 1
if subplt==splts+1:
  subplt=1
  
  
#%%
plt.pcolormesh(obj[z0,:,:])



#%%
plt.figure(410)
d_in = d[20,:,:]
d_out = d[21,:,:]
d_out2 = d[26,:,:]
d_out3 = d[31,:,:]

vmax= 5
vmin= -10
plt.subplot(2,2,1)
plt.pcolormesh(d_in, cmap='seismic', vmin=vmin, vmax=vmax)
plt.subplot(2,2,2)
plt.pcolormesh(d_out, cmap='seismic', vmin=vmin, vmax=vmax)
plt.subplot(2,2,3)
plt.pcolormesh(d_out2, cmap='seismic', vmin=vmin, vmax=vmax)
plt.subplot(2,2,4)
#plt.pcolormesh(d_out-d_in, cmap='seismic') #, vmin=-16.5, vmax=-15.5)
plt.pcolormesh(d_out3, cmap='seismic', vmin=vmin, vmax=vmax)
