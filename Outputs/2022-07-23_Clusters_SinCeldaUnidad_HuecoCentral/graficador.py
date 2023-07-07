# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 20:06:09 2022

@author: santi
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})


alturas = [16]*2
radios = [10]*2
distancias = [22,22]
densidades = [0.5,0.5]

archivos = ['_SinHueco', '']


matrices = []
for ii in range(len(radios)):
    
    h = int(alturas[ii])
    d = int(distancias[ii])
    r = int(radios[ii])
    p = densidades[ii]
    print(h, d, r, p)

    file_ii = archivos[ii]    
    filename = f"h{h:d}_r{r:d}_dist{d:d}_densLoc{p:.2f}{file_ii}"
    
    matrices.append(np.loadtxt(f'{filename}.matriz'))  
          
    archivo = f'{filename}.dat'
      
      
    # extraigo  
    datos = np.loadtxt(archivo)  
    ppmAxis0 = datos[:,0]
    spec = datos[:,1]
    #spec_imag = datos[:,2]
    # retoco:
    ppmAxis = ppmAxis0
    spec = spec - spec[0]
    # reduzco los datos a una VENTANA alrededor de un CENTRO
    ventana = 200
    center = 0
    ppmAxis = ppmAxis0[np.abs(center-ppmAxis0)<ventana]
    spec = spec[np.abs(center-ppmAxis0)<ventana]
    plt.figure(1231)
    plt.plot(ppmAxis,spec,linewidth=2, label=archivo)
    #plt.xlim([ppmAxis[-1], ppmAxis[0]])
    plt.xlim(150,-150)
    plt.vlines(0, 0, np.max(spec))
    plt.yticks([])
  
        
plt.legend()    
#---------------- 

#%%
Nfilas = 1
Ncols = 2


#### figura de la muestra
size = 5
fig = plt.figure(1, figsize=(size*2, size*2), constrained_layout=False)
gs = fig.add_gridspec(Nfilas, Ncols, hspace=0, wspace=0)
axs = gs.subplots(sharex=True, sharey=True)
# fig.suptitle('Sharing both axes') 

 
for jj in range(len(matrices)):
  ax=axs[jj]  
  ax.set_aspect('equal', 'box')  
  
  delta_in = -12.78 # corrimiento bulk
  nn = 128
  matriz = matrices[jj][512-nn:512+nn,512-nn:512+nn]
  masked =  np.ma.masked_where(matriz == 0, matriz)
  # m = masked - np.min(masked)
  m = masked - delta_in
  print(np.min(m), np.max(m))    
  
  vmin=14.3
  vmax=19
  
  ax.pcolormesh(m, cmap='inferno_r', vmin=vmin, vmax=vmax)
  