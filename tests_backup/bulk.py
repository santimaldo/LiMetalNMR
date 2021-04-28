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


#def SimulationVolume(N=None, voxelSize=None, FOV=None):
#  """
#  Esta funcion determina el volumen de la simulacion.
#  es decir determina N, voxelSize o FOV, alguno de ellos dados los otros 
#  dos restantes.
#  
#  N, voxelSize y FOV deben ser array_like, de 3 elementos con la convencion
#  [z,y,x]
#  
#  ejemplo: dado N y FOV (en mmm) determino voxelSize
#    
#  N, voxelSize, FOV = SimulationVolume(N=[256,64,64], FOV=[1.5,10,10])
#  
#  Notar que el resultado son los tres parametros, ya que de poso los transforma
#  en np.arrays!
#  """ 
#  if FOV is None:
#    N = np.array(N)
#    voxelSize = np.array(voxelSize)  
#    FOV = N*voxelSize
#  elif voxelSize is None:  
#    N = np.array(N)
#    FOV = np.array(FOV)
#    voxelSize = FOV/N.astype(float)
#  elif N is None:  
#    FOV = np.array(FOV)
#    voxelSize = np.array(voxelSize)  
#    N = FOV/voxelSize
#    
#  N = N.astype(int)
#  #mensaje en pantalla:
#  sN = str(N[0])+'*'+str(N[1])+'*'+str(N[2])
#  sFOV = str(FOV[0])+'mm*'+str(FOV[1])+'mm*'+str(FOV[2])+'mm'
#  sVS = str(voxelSize[0])+'mm*'+str(voxelSize[1])+'mm*'+str(voxelSize[2])+'mm'
#  print('Volumen de simulacion (convencion z,y,x):')  
#  print('N: '+ sN + ' | voxelSize:  ' + sVS + ' | FOV:  '+ sFOV)
#  return N, voxelSize, FOV  
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
voxelSize = [0.03, 0.1, 0.1]# mm
#FOV = [0.714*30, 50.048, 50.048]
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
obj_dim = [0.714, 4, 4]

# Creo una matriz de ceros de tamaño Nz*Ny*Nx. esta matriz representa el 
# volumen simulado. Donde hay un 1, hay material. Donde hay un 0, hay vacio.
# El producto obj*Chi es la distribuion espacial de susceptibilidad magnetica.
obj = np.zeros([Nz, Ny, Nx])
# Para representar la lamina, defino las posiciones en las que inicia y termina
# la lamina en cada direccion.
z_lamina = int(obj_dim[0]/voxelSize[0] +1)
objz = [0, z_lamina]
objz = [int(Nz/2-obj_dim[0]/VSz/2), int(Nz/2+obj_dim[0]/VSz/2)]
# el objeto esa situado en el centro de FOVxy
objy = [int(Ny/2-obj_dim[1]/VSy/2), int(Ny/2+obj_dim[1]/VSy/2)]
objx = [int(Nx/2-obj_dim[2]/VSx/2), int(Nx/2+obj_dim[2]/VSx/2)]
# el objeto tiene el mismo tamaño que el FOVxy
#objy = [0, Ny+1]
#objx = [0, Nx+1]

obj[objz[0]:objz[1], objy[0]:objy[1], objx[0]:objx[1]] = 1
#%%----------------------------------------------------------------------------

# sistema de coordenadas:
z = np.linspace(0, Nz-1, Nz)*VSz
y = np.linspace(-Ny/2 +1, Ny/2, Ny)*VSy
x = np.linspace(-Nx/2 +1, Nx/2, Nx)*VSx

delta = calculateFieldShift(obj*Chi, voxelSize)
delta = delta*1e6



#%% 
plt.figure(2)
x0 = int(Nx/2)
y0 = int(Ny/2)

#plt.plot(z, delta[:,y0+1,x0], '-')
plt.plot(z-Nz/2*VSz+obj_dim[0]/2,delta[:,y0,x0], '-')
#plt.plot(z, obj[:,y0,x0])
plt.xlabel(r"$z$ [mm]")
plt.ylabel(r"$\delta$ [ppm]")
#plt.xlim([-0.1, 0.5])
#plt.ylim([0,1.7])


#%%
splts = 1
subplt = 1



plt.figure(3)
delta_slice = delta[:,:,int(Nx/2)]
vmax = np.max(np.max(delta_slice))
ax = plt.subplot(splts,1,subplt)
plt.pcolormesh(y,z, delta_slice, cmap='seismic', vmin=-vmax, vmax=vmax)
#aspecto = (Nz*voxelSize[0])/(Ny*voxelSize[1])
#ax.set_aspect(aspecto)
plt.xlabel(r"$y$ [mm]")
plt.ylabel(r"$z$ [mm]")

plt.figure(4)
delta_slice = delta[:,int(Ny/2),:]
vmax = np.max(np.max(delta_slice))
ax = plt.subplot(splts,1,subplt)
plt.pcolormesh(x,z,delta_slice, cmap='seismic', vmin=-vmax, vmax=vmax)
#ax.set_aspect((Nz*voxelSize[0])/(Nx*voxelSize[2]))
plt.xlabel(r"$x$ [mm]")
plt.ylabel(r"$z$ [mm]")

subplt += 1
if subplt==splts+1:
  subplt=1
  
  
#%%
#dif = delta[261,64,:] - delta[260,64,:]
#
#plt.figure(16)
#plt.plot(x,dif)
#plt.plot(x,delta[261,64,:])
#plt.plot(x,delta[260,64,:])
#  
#  
#%% ACA VOY A ESTUDIAR EL PLANO XY

# limetes de los indices del objeto: (np.where(obj==1))
# z 245,265
# y 24, 39
# x 44, 83

# primer z out: z[21]


d = delta[245:,24:40, 44:84]

Nz, Ny, Nx = np.shape(d)
z = np.linspace(0, (N-1)*VSz, N) - 0.7455
y = np.linspace(-(Ny-1)/2, (Ny-1)/2, Ny)*VSy
x= np.linspace(-(Nx-1)/2, (Nx-1)/2, Nx)*VSx

#plt.figure(4835641)
#plt.plot(z, d[:,:,20])

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

#%% puedo analizar en funcion de z solo para un cuadramte
plt.figure(222)
puntos = [[0,0], [3,0], [2,2], [3,5], [0,5], [2,7], [3,9], [0,9]]
for punto in puntos:
  xind = punto[1]
  yind = punto[0]
  leyenda ='x='+str(x[xind])+',  y='+str(y[yind])
  plt.plot(z, d[:,yind,xind], label=leyenda)
plt.legend()
plt.xlim([0,0.5])
plt.ylim([0,7.5])
