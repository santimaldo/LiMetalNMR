#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""
#stop

import numpy as np
import matplotlib.pyplot as plt
import Modules.calculateFieldShift as cFS
from scipy import integrate
import time

"""
Para una esfera de radio 0.1 m calculo la perturbacion de campo con distintas
discretizaciones.
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
condicion = X*X+Y*Y+Z*Z <= (diametro/2.0)**2
muestra[condicion] = 1

#%% calculo el campo-----------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

eta = cFS.calculateFieldShift(muestra*Chi, [voxelSize]*3)

Bnuc = eta*B0 + B0
Bmac = Bnuc/(1-2/3*muestra*Chi)


#%% graffff
n=0
n+=1
plt.figure(n)
plt.pcolormesh(X[int(N/2),:,:], Y[int(N/2),:,:], muestra[int(N/2),:,:])

n+=1
plt.figure(n)
plt.pcolormesh(X[int(N/2),:,:], Y[int(N/2),:,:], eta[int(N/2),:,:])
plt.colorbar()

n+=1
vmax = np.max(np.abs(eta[:,int(N/2),:]))
plt.figure(n)
plt.pcolormesh(X[:,int(N/2),:], Z[:,int(N/2),:], eta[:,int(N/2),:], cmap='seismic', vmax=vmax, vmin=-vmax)
plt.xlabel("x")
plt.ylabel("z")
plt.title(r"$\delta$ con $\chi=${}".format(Chi))
plt.colorbar()

#%%% B exacto
"""
para hacer la comparacion voy a poner el valor medio de la solucion exacta dentro del voxel.
"""
def func_exact(zz,yy,xx):
  if (zz*zz+yy*yy+xx*xx <= (diametro/2.0)**2):
    f = 2/3*Chi
  else:
    f = (1/3)*Chi*(diametro/2.0)**3*(2*zz**2-xx**2-yy**2)/(xx**2+yy**2+zz**2)**(2.5)  
  f = f*B0+B0
  return f

#%%
nx = int(N/2)
ny = int(N/2)

x0 = x[nx]
y0 = y[ny]

# solucion exacta al borde del voxel
zz = np.linspace(z[0],z[-1],4096*8)
Bexact = []
Bexact_j = np.zeros_like(zz)
yy=y0
plt.figure(22)
for j in range(2):
  xx = x0+(j-1)*voxelSize/2
  print((yy,xx))  
  for i in range(np.size(zz)):
    Bexact_j[i] = func_exact(zz[i],yy,xx)
  Bexact.append(Bexact_j)  
  plt.plot(zz, Bexact_j, '--')


### ahora si calculo el valor medio para cada z
# x[N/2] = -0.5*voxelSize
x0 = x[nx]
y0 = y[ny]
vs = voxelSize
Bexact_medio = np.zeros_like(z)
for j in range(N):
  Bexact_medio[j], _ = integrate.tplquad(func_exact, x0-0.5*vs, x0+0.5*vs, y0-0.5*vs, y0+0.5*vs, z[j]-0.5*vs, z[j]+0.5*vs)
  Bexact_medio[j] = Bexact_medio[j]/(voxelSize**3) # divido por el volumen
  
  
plt.figure(22)
plt.plot(z , Bmac[:,int(N/2),int(N/2)],'o--')
plt.plot(z , Bexact_medio,'o--')
plt.legend()

#%%
plt.figure(23)
plt.plot(z , abs(Bmac[:,ny,nx]-Bexact_medio)*1e6,'o--')
plt.xlim([0,FOV/2])
plt.title(r"Error Absoluto:  $|B_{mac}^{numerico} - \frac{1}{VS^3} \int_{voxel} B_{mac}^{exacto}d^3x|$")
plt.ylabel("Error Absoluto [ppm]")
plt.xlabel("z [mm]")


plt.figure(24)
plt.plot(z , Bexact_medio,'ko')
plt.step(z+vs/2 , Bmac[:,ny,nx], 'b' , linewidth=3)
plt.plot(z , Bmac[:,ny,nx], 'bo')




elapsed = (time.time() - t0)/60
print('---  tiempo: {:.2f} min'.format(elapsed))