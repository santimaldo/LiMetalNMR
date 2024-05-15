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
import calculateFieldShift as cFS
#%%


def Crear_B1(obj):
    """
    Mediante erosiones de 1 voxel vamos creando una matriz de B1
    """
#    obj = self.muestra_sup
    z0 = 60
    vs = 1e-3
    B1 = np.zeros_like(obj)
    skdp = 12e-3
    # esto es para las erosiones:      
    mask = (obj == 1)
    struct = ndimage.generate_binary_structure(3, 1)      
    # hago suficientes slices como para llegar a una profundidad de 5xSkinDepth
    # es decir, 60um
    n_slices = int(5*skdp/vs)
    for n in range(n_slices):
      # erosiono:
      erode = ndimage.binary_erosion(mask, struct)
      # la erosion tambien se come los laterales del bulk, por eso los vuelvo a
      # rellenar con 1. La tajada va estar exactamente en z0-n-1, los 1 se llenan
      # hasta z0-n-2
      ## COMENTO POR AHORA YA QUE NO VOY A SUPERPONER
      #erode[0:z0-n-1,:,:] = 1
      # obtengo la tajada
      tajada = mask ^ erode
      # voy llenando las capas con los valores de B1. la variable de profundidad
      # es (n+1)*vs/2, ya que en la primer tajada n=0 y la profundidad es de la
      # mitad del voxelsize (si tomo el centro del voxel)
      B1 = B1 + tajada*np.exp(-(n+1)*vs/2/skdp)    
      # ahora el nuevo objeto a erosionar es el de la erosion anterior
      mask = (erode==1)
      if n<6:
        plt.figure(1)
        plt.subplot(2,3,n+1)
        plt.pcolormesh(tajada[:,:,89])
    return B1
    
#%%----------------------------------------------------------------------------  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Parametros fisicos
Chi =  24.1*1e-6 #(ppm) Susceptibilidad volumetrica
voxelSize = [0.001, 0.001, 0.001]# mm
n = 256
N = [n,n,n]

obj = np.zeros(N)
i = int(n/4)
f = int((n-n/4))
obj[i:f,i:f,i:f] = 1


#%%

B0 = cFS.calculateFieldShift(obj*Chi, voxelSize) * 1e6
#superposicion: NO
#obj[:60,:,:] = 1
#B0[:60,:,:] = B0[:60,:,:] - 12.79
#B0[60:,:,:] = B0[60:,:,:] + 3.27

b0=B0.flatten()

#%%
tajada = int(n/2)
plt.figure(0)
plt.pcolormesh(B0[:,:,tajada]*obj[:,:,tajada])
#plt.pcolormesh(obj[65,:,:])

#%%
B1 = Crear_B1(obj)
plt.figure(2)
plt.pcolormesh(B1[:,:,tajada])
plt.figure(22222)
plt.plot(B1[tajada,:,tajada],'o')

#%%
b1 = B1.flatten()

b0 = b0[b1!=0]
b1 = b1[b1!=0]
#%%

#b0=B0.flatten()
#b0= b0[B1.flatten()!=0]
#b0 = B0[60:,:,:].flatten()

plt.figure(1)
hist, b0_bin_edges = np.histogram(b0, bins='auto', density=False)
b0bins=b0_bin_edges
plt.plot(b0_bin_edges[1:],hist,'o')
#%%
plt.figure(3)
hist, b1_bin_edges = np.histogram(np.log(b1+1),bins='auto', density=False)
b1bins=b1_bin_edges

b1_bin_edges = np.exp(b1_bin_edges)-1

b1_bin_edges = b1_bin_edges[1:]
b1_bin_edges = b1_bin_edges[hist!=0]
hist=hist[hist!=0]
plt.plot(b1_bin_edges,hist,'o')
#%%
#%%
##%%
HH, xedges, yedges = np.histogram2d(b0, np.log(b1+1),bins=(b0bins,b1bins), density=False)
#%%
deltax = xedges[1:]-xedges[:-1]
xx = xedges[0:-1] + deltax

yedges_exp = np.exp(yedges)-1
deltay = yedges_exp[1:]-yedges_exp[:-1]
yy = yedges_exp[0:-1] + deltay

X, Y = np.meshgrid(xx, yy)

H = HH.T

#mask = np.reshape([H!=0], H.shape)
#
#X=X^mask
#Y=Y^mask
#H=H^mask
#
#%%
fig=plt.figure(1232)
ax = fig.add_subplot(132, title='pcolormesh: actual edges'
        ,aspect='equal')
ax.pcolormesh(X,Y,H,cmap='PuRd')
fig.colorbar(cm.ScalarMappable(cmap='PuRd'), ax=ax)
#%%
r = H
r = r[~np.all(H == 0, axis=1)]


plt.figure(432)
plt.pcolormesh(r)
plt.colorbar()
#%%

XX = X[~np.all(H == 0, axis=1)]
YY = Y[~np.all(H == 0, axis=1)]

plt.figure(32)
plt.plot(XX[0,:],np.sum(r,axis=0),'o')
plt.figure(23)
plt.plot(YY[:,0],np.sum(r,axis=1),'o')

#%%


fig = plt.figure(48192)
ax = fig.gca(projection='3d')
# Plot the surface.
surf = ax.plot_surface(XX, YY, r, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

#%%
print("Arranco SMC...")
k = 1.5
N = 30
loadpath = "./S_N_k/"
SNK = np.loadtxt(loadpath+"SMC_N{:d}_k{:.1f}.dat".format(N,k), dtype=complex)

Beta = SNK[:,0]
SNK = SNK[:,1]


ppm = 116.6 # Hz
T2est = 0.12*1e-3 # chequeado con una medida_ T2est = 0.12 us
t = np.linspace(0,1.024*4,2048)*1e-3
fid = np.zeros_like(t).astype(complex)

for b0j in XX[0,:]:
  for b1j in YY[:,0]:        
    # B1
    ind, beta = find_nearest(Beta, b1j)
    snk = SNK[ind]
    # B0
    w = 2*np.pi*ppm * (b0j+258.9)
    # fid
    fid += snk*np.exp(1j*w *t - t/T2est)
#------------------------
plt.figure(43211111)
plt.plot(t, np.imag(fid))
  
#FOURIER---------------------------------------------------------------
ZF = t.size
dw = t[1]-t[0]
sw = 1/dw;
freq = np.zeros(ZF);
for ll in range(ZF):
    freq[ll]=(ll-1)*sw/(ZF-1)-sw/2

ppmAxis = freq/ppm
spec = np.fft.fftshift(np.fft.fft(fid))

plt.figure(123456321)
plt.plot(ppmAxis, -np.imag(spec), linewidth=3)
plt.xlim([ppmAxis[-1], ppmAxis[0]])
#plt.legend()