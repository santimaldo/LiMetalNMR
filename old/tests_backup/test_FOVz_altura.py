# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 16:36:25 2022

@author: santi

quiero probar en que influye la altura de la muesra
La idea es poner la muestra mas arriba asi tiene mas espacio de bulk

antes de corres esto, debo tener cargados todos los objetos
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
#%%
lista = [73,103,123]
shift=10
Nmz = muestra.N_muestra[0]
z0 = (Nz/2-Nmz/2)+shift
z = (np.arange(Nz)- z0) * vs


data = [z]
plt.figure(1)
for x in lista:
  data.append(delta.delta[:,128,x])
  if x==lista[2]:
    plt.plot(z,delta.delta[:,128,x], 'o-')
  
  
datos = np.array(data).T  
np.savetxt(f'data_shift_{shift*vs}um.dat', datos)
  
#%%
x = (np.arange(Nx)-Nx/2)*vs
y = (np.arange(Ny)-Ny/2)*vs
X,Y = np.meshgrid(x,y)


slz = superposicion.z0 + int(h/2)
sly = int(Ny/2)
slx = int(Nx/2)

obj = superposicion.muestra_sup

vmax = np.max(np.abs(delta.delta))

fig, axs = plt.subplots(1,2)
fig.suptitle(rf"$N_z\times N_y  \times N_x$ = ${Nz:d}\times{Ny:d}\times{Nx:d}$")
axs[0].pcolormesh(X,Y,delta.delta[slz,:,:], vmax=vmax, vmin=-vmax, cmap='seismic')
axs[1].pcolormesh(X,Y,(superposicion.delta_sup)[slz,:,:], vmax=vmax, vmin=-vmax, cmap='seismic')
for ax in axs:
  ax.set_aspect('equal')
  ax.hlines(0, xmin=x[0], xmax=x[-1], color='k')
  ax.vlines(0, ymin=y[0], ymax=y[-1], color='k')
  ax.set_xlabel(r'x [$\mu$m]')
  ax.set_ylabel(r'y [$\mu$m]')

objx = obj[slz,sly,:]
deltx = delta.delta[slz,sly,:]
deltsupx = superposicion.delta_sup[slz,sly,:]
objy = obj[slz,:,slx]
delty = delta.delta[slz,:,slx]
deltsupy = superposicion.delta_sup[slz,:,slx]




# datos = np.array([x, objx, deltx, deltsupx]).T
# np.savetxt(f'datos_NyNx_{Ny}x{Nx}_X.dat', datos)
# datos = np.array([y, objy, delty, deltsupy]).T
# np.savetxt(f'datos_NyNx_{Ny}x{Nx}_Y.dat', datos)


objx=1
objy=1
plt.figure(222)
plt.subplot(2,2,1)
plt.plot(x, objx*deltsupx)
plt.xlabel(r'x [$\mu$m]')
plt.ylabel(r'$\Delta\delta$ [ppm]')
plt.subplot(2,2,2)
plt.plot(y, objy*deltsupy)
plt.xlabel(r'y [$\mu$m]')
plt.ylabel(r'$\Delta\delta$ [ppm]')
# sin super
plt.subplot(2,2,3)
# plt.title("Sin superponer")
plt.plot(x, objx*deltx)
plt.xlabel(r'x [$\mu$m]')
plt.ylabel(r'$\Delta\delta$ [ppm]')
plt.subplot(2,2,4)
# plt.title("Sin superponer")
plt.plot(y, objy*delty)
plt.xlabel(r'y [$\mu$m]')
plt.ylabel(r'$\Delta\delta$ [ppm]')


