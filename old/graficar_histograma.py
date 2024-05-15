# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 11:31:30 2020

@author: Santi
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
plt.rcParams.update({'font.size': 14})

#%%

#beta = medicion.Crear_beta()
X, Y, H2D = medicion.CrearHistograma2D(graficos=1111745)

#%%

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.pcolormesh(beta[:,113,55:200], cmap='inferno')


#%%
fig = plt.figure(2)
v = 8
ax = fig.add_subplot(311)
ax.pcolormesh(superposicion.delta_bulk[:,128,:], cmap='seismic', vmin=-v, vmax=v)
ax.set_aspect(1)
ax = fig.add_subplot(312)
ax.pcolormesh(superposicion.delta_muestra[:,128,:], cmap='seismic', vmin=-v, vmax=v)
ax.set_aspect(1)
ax = fig.add_subplot(313)
ax.pcolormesh(superposicion.delta_sup[:,128,:], cmap='seismic', vmin=-v, vmax=v)
ax.set_aspect(1)

#%%
plt.figure(3)
#plt.pcolormesh(X,Y, 1+H2D,  norm=colors.LogNorm(vmin=1,vmax=np.max(H2D)), cmap='inferno')
plt.pcolormesh(X,Y, H2D, cmap='inferno')
plt.yscale('log')
plt.ylim([0.01,1])
plt.xlim([np.max(X[0,:]) ,np.min(X[0,:])])
plt.ylabel(r'$\eta$' )
plt.xlabel(r'$\beta$')
