#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 18:58:23 2020

@author: santi

para probar el histograma 2d en B1 y B0
"""
#stop

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
      erode[0:z0-n-1,:,:] = 1
      # obtengo la tajada
      tajada = mask ^ erode
      # voy llenando las capas con los valores de B1. la variable de profundidad
      # es (n+1)*vs/2, ya que en la primer tajada n=0 y la profundidad es de la
      # mitad del voxelsize (si tomo el centro del voxel)
      B1 = B1 + tajada*np.exp(-(n+1)*vs/2/skdp)    
      # ahora el nuevo objeto a erosionar es el de la erosion anterior
      mask = (erode==1)
      if n<6:
        plt.figure(666)
        plt.subplot(2,3,n+1)
        plt.pcolormesh(tajada[:,:,89])
    return B1

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    #return idx, array[idx]    
    return idx
#%%  
def autophase(ppmAxis, spec):
  """
  Corrijo automaticamente la fase, utilizando el método de minimizar el area
  de la parte imaginaria:   case{'MinIntImagSpec'}
  """
  presicion = 1
#  angle=np.arange(180,-180,-presicion)
  angle=np.arange(-180,180,presicion)

  SPECS = []
  IntImagSpec = []
  for i in range(angle.size):
      Sp_try= spec*np.exp(-1j*angle[i]*np.pi/180)
      SPECS.append(Sp_try)
      IntImagSpec.append(np.abs(np.trapz(np.imag(Sp_try),x=ppmAxis)))
  IntImagSpec = np.array(IntImagSpec)
  # indice del minimo:
  idx = np.argmin(IntImagSpec)
  spec = SPECS[idx]
  ind_max = np.argmax(np.abs(np.real(spec)))
  if spec[ind_max]<0:
    spec=-spec
  return  spec
  
  
#%%----------------------------------------------------------------------------  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#stop
carpeta= 'a10_p20'
savepath = "/home/santi/CuarenteDoctorado/LiMetal/simulaciones/2020-10-14_SMC_y_espectro/dendritas_porcentaje/espectros/{}/".format(carpeta)

#%%
# Parametros fisicos
Chi =  24.1*1e-6 #(ppm) Susceptibilidad volumetrica
voxelSize = [0.001, 0.001, 0.001]# mm
n = 256
N = [n,n,n]


#del muestra
#del delta

#slz, sly, slx = muestra.slices
#obj = superposicion.muestra_sup[:,sly[0]:sly[1],slx[0]:slx[1]]
#B0  = superposicion.delta_sup[:,sly[0]:sly[1],slx[0]:slx[1]]
#B0  = B0*obj
##para single pulse:
#delta_sens = superposicion.delta_sens[:,sly[0]:sly[1],slx[0]:slx[1]]

### COMPLETA:
obj = superposicion.muestra_sup
B0  = superposicion.delta_sup
B0  = B0*obj
### para single pulse:
delta_sens = superposicion.delta_sens

#para single pulse:
delta_sens = superposicion.delta_sens
#%%
B1 = Crear_B1(obj)
#%%
plt.figure(200000)
v = 10
plt.pcolormesh(B0[80,:,:], cmap='seismic', vmin=-v, vmax=v)
#plt.pcolormesh(B1[80,:,:])
plt.colorbar()
#plt.figure(22222)
#plt.plot(B1[tajada,:,tajada],'o')

#%%
b0 = B0.flatten()
b1 = B1.flatten()

b0 = b0[b1!=0]
b1 = b1[b1!=0]
#%%

#b0=B0.flatten()
#b0= b0[B1.flatten()!=0]
#b0 = B0[60:,:,:].flatten()

plt.figure(0)
hist, b0_bin_edges = np.histogram(b0, bins=32, density=True)
b0bins=b0_bin_edges
plt.plot(b0_bin_edges[1:],hist,'o')
#%%
plt.figure(3)
hist, b1_bin_edges = np.histogram(np.log(b1+1),bins=64, density=True)
b1bins=b1_bin_edges

b1_bin_edges = np.exp(b1_bin_edges)-1

b1_bin_edges = b1_bin_edges[1:]
b1_bin_edges = b1_bin_edges[hist!=0]
hist=hist[hist!=0]
plt.plot(b1_bin_edges,hist,'o')
#%%
#%%
##%%
HH, xedges, yedges = np.histogram2d(b0, np.log(b1+1),bins=(b0bins,b1bins), density=True)
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
ax = fig.add_subplot(132, title='pcolormesh: actual edges')
#        ,aspect='equal')
ax.pcolormesh(X,Y,H,cmap='PuRd')
fig.colorbar(cm.ScalarMappable(cmap='PuRd'), ax=ax)
#%%
r = H
r = r[~np.all(H == 0, axis=1)]
XX = X[~np.all(H == 0, axis=1)]
YY = Y[~np.all(H == 0, axis=1)]

plt.figure(432)
plt.pcolormesh(XX+258.9,YY,r)
plt.xlim([265,243])
plt.xlabel('Chemical Shift [ppm]')
plt.ylabel(r'$B_1/B_{1,0}$')
plt.title(r'Histograma $B_0-B_1$')
plt.colorbar()
#%%



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
HH = r
k_list = [1, 1.1, 1.2, 1.5, 2.0]
k_list = [1]
N = 16
loadpath = "./S_N_k/"

n =0
for k in k_list:
  n+=1
  SNK = np.loadtxt(loadpath+"SMC_N{:d}_k{:.1f}.dat".format(N,k), dtype=complex)
  
  Beta = SNK[:,0]
  SNK = SNK[:,1]
  
  
  ppm = 116.6 # Hz
  T2est = 0.12*1e-3 # chequeado con una medida_ T2est = 0.12 us
  t = np.linspace(0,1.024*4,2048)*1e-3
  fid = np.zeros_like(t).astype(complex)
  
  for j in range((YY[:,0]).size):        
      # B1
      b1j = YY[j,0] 
      ind = find_nearest(Beta, b1j)
      snk = SNK[ind]
      for i in range((XX[0,:]).size):
        # B0
        b0j = XX[0,i]
        w = 2*np.pi*ppm * (b0j+258.9)    
        # fid
        fid += HH[j,i]*snk*np.exp(1j*w *t - t/T2est)
  #------------------------
#  plt.figure(43211111)
#  plt.plot(t, np.imag(fid))
  
  #FOURIER---------------------------------------------------------------
  ZF = t.size
  dw = t[1]-t[0]
  sw = 1/dw;
  freq = np.zeros(ZF);
  for ll in range(ZF):
      freq[ll]=(ll-1)*sw/(ZF-1)-sw/2
  
  ppmAxis = freq/ppm
  
  spec = np.fft.fftshift(np.fft.fft(fid))
  
  s = autophase(ppmAxis,spec)
  
  plt.figure(1)
  vline = 246.5
  plt.subplot(2,3,n+1)
  plt.title("SMC with N={}, k={:.1f}".format(N,k))
  plt.vlines(vline, ymin=0,ymax=1.1*(np.max(np.real(s))), linestyle='dashed')
  plt.plot(ppmAxis, np.real(s), linewidth=3)
  plt.xlim([350,150])
  if n>3:
    plt.xlabel(r"$^7$Li Chemical Shift [ppm]")
  #plt.legend()
  
  plt.figure(9875432)
  plt.plot(ppmAxis, np.real(s)/np.max(np.real(s)), linewidth=3, label="k={:.1f}".format(k))
  
  datos=np.array([ppmAxis, np.real(s), np.imag(s)]).T
  np.savetxt(savepath+"spec_N{}_k{:.1f}.dat".format(N,k), datos)
  



#CREACION DEL ESPECTRO SINGLE PULSE-----------------------------------------

ppmAxis0, spec = espectro(delta_sens)

 
datos=np.array([ppmAxis0, np.real(spec), np.imag(spec)]).T
np.savetxt(savepath+"spec_single_pulse.dat", datos)
  
plt.figure(1)
plt.subplot(2,3,1)
plt.title("Single Pulse")
plt.vlines(vline, ymin=0,ymax=1.1*(np.max(np.real(spec))), linestyle='dashed')
plt.plot(ppmAxis0, spec, 'k', linewidth=3)
#plt.xlabel(r'$^7$Li Chemical Shift [ppm]')
plt.xlim([350,150])

#%%
plt.figure(9875432)
plt.plot(ppmAxis0, spec/np.max(spec), 'k', linewidth=3, label="single pulse")
plt.xlim([350,150])
plt.xlabel(r"$^7$Li Chemical Shift [ppm]")
plt.ylabel("Normalized Spectrum")
plt.legend()
#%%
#plt.figure(123456321)
#plt.title("SMC with k=1.2")
#plt.plot(ppmAxis, s1_2, linewidth=3, label="N = 16")
#plt.plot(ppmAxis, s30[2], linewidth=3, label="N = 30")

#plt.plot(ppmAxis, s1_0, linewidth=3, label="k ={:.1f}".format(1.0))
#plt.plot(ppmAxis, s1_1, linewidth=3, label="k ={:.1f}".format(1.1))
#plt.plot(ppmAxis, s1_2, linewidth=3, label="k ={:.1f}".format(1.2))
#plt.plot(ppmAxis, s1_5, linewidth=3, label="k ={:.1f}".format(1.5))
#plt.plot(ppmAxis, s2_0, linewidth=3, label="k ={:.1f}".format(2.0))
#plt.plot(ppmAxis, s1_0/np.max(s1_0), linewidth=3, label="k ={:.1f}".format(1.0))
#plt.plot(ppmAxis, s1_1/np.max(s1_1), linewidth=3, label="k ={:.1f}".format(1.1))
#plt.plot(ppmAxis, s1_2/np.max(s1_2), linewidth=3, label="k ={:.1f}".format(1.2))
#plt.plot(ppmAxis, s1_5/np.max(s1_5), linewidth=3, label="k ={:.1f}".format(1.5))
#plt.plot(ppmAxis, s2_0/np.max(s2_0), linewidth=3, label="k ={:.1f}".format(2.0))
#plt.xlim([ppmAxis[-1], ppmAxis[0]])
#plt.xlim([350,150])
#
#plt.legend()

