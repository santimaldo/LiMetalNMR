# -*- coding: utf-8 -*-
"""
Created on 13/06/2021

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12})
# from VoigtFit import *


path0 ='S:/Doctorado/pyprogs/calculateFieldShift/Outputs/Resultados/comparacion_sp-smc/'
alturas    = [22, 48]
radios     = [1,  10]
distancias = [6,  80]


path0 ='S:/Doctorado/pyprogs/calculateFieldShift/Outputs/Resultados/comparacion_sp-smc/bis/'
alturas    = [22, 48]
radios     = [1,  10]
distancias = [6,  80]
k_list = [1,1.1,1.2,1.3,1.4,1.5,1.75,2.0,2.25]


alturas    = [22, 48]
radios     = [1,  10]
distancias = [6,  80]
k_list = [1,1.05,1.1,1.15,1.2,1.3,1.4,1.5,1.75]



filas = 3
columnas = 3

Amp = [[]]*len(alturas)

for ii in range(len(radios)):
  h = int(alturas[ii])
  d = int(distancias[ii])
  r = int(radios[ii])

  # BULK
  archivo = path0+ 'bulk.dat'
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
  bulk = spec/np.max(spec[np.abs(ppmAxis)<0.5])
  
  k_ind=0
  for k in k_list:
    k_ind +=1
    archivo = path0+ 'h{:d}_r{:d}_d{:d}_SMC64-k{:.2f}.dat'.format(h, r, d, k)
      
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
    # spec = spec/np.max(spec)
    spec = spec/np.max(spec[np.abs(ppmAxis)<0.5])
    
    Amp[ii].append(np.trapz(spec-bulk, x=ppmAxis))
        
    
    if ii<filas*columnas:
      plt.figure(r)
      plt.subplot(filas,columnas,k_ind)
      plt.plot(ppmAxis,bulk, '--', color='grey', linewidth=2)    
      plt.plot(ppmAxis,spec, 'k', linewidth=2)    
      plt.plot(ppmAxis,spec-bulk, 'r', linewidth=2)    
      plt.xlim(80,-80 )  
      plt.vlines(0, 0, np.max(spec))
      plt.yticks([])      
      plt.title("h={},  r={},  dist={}".format(h, r, d))
      
  #%%
  #  plt.hlines(0,ppmAxis[-1], ppmAxis[0])
  #  plt.vlines(0,0,np.max(spec)*1.1, linestyle='dashed')
  #  #plt.xlim([ppmAxis[-1], ppmAxis[0]])    
  #  plt.yticks([])
  #  plt.xlabel(r"$^7$Li Chemical Shift [ppm]")
  #  plt.xlim(50,-50)    
  #  plt.legend()    
  #  plt.show()
      
    
#     dens = np.array(p_cubierto)
#     corrimientos = np.array(corrimientos)
#     ###ajuste lineal
#     coef = np.polyfit(dens, corrimientos, 1)
#     poly1d_fn = np.poly1d(coef) 
#     #
#     label = r'{:d} $/mu$m'.format(ancho)
#     title = r'height: {:d} $/mu$m'.format(h)
    
#     #plt.figure(39203920)
#     #plt.subplot(2,3,n_h+1)    
#     plt.figure(100000+n_h+1)
#     cmap = plt.get_cmap('jet')
#     color = cmap(n_a/(anchos.size))
#     plt.plot(dens, corrimientos, 'o', color=color, label=label)
#     plt.plot(dens, poly1d_fn(dens), '--', color=color)
#     #plt.xlabel('density (covered area/total area) [%]')
#     plt.xlabel('density [%]')
#     plt.ylabel(r'$/delta-/delta_{Bulk}$')
#     plt.ylim([0,25])
#     plt.xlim([0,100])
#     #if n_a ==anchos.size-1:
#     plt.legend(title='Width')
#     plt.title(title)


#     #plt.figure(1111)
#     #plt.subplot(2,3,n_h+1)
#     plt.figure(100+n_h+1)    
#     signal_bulk = np.array(s_bulk)    
#     signal_mic  = np.array(s_mic)    
#     signal_rel  = signal_mic/signal_bulk    
#     #plt.subplot(1,2,1)
#     #plt.plot(dens, signal_mic, 'ro--', label = 'mic')
#     #plt.plot(dens, signal_bulk, 'bo--', label = 'bulk')
#     #plt.plot(dens, signal_mic ,'o', color=color, label=label)
#     #plt.legend()
#     #plt.subplot(1,2,2)
#     #plt.title('s_mic/s_bulk')
#     #plt.plot(dens, signal_rel, 'o--')
#     plt.plot(dens, signal_rel,'o--', color=color, label=label)
#     plt.yscale('log')
#     plt.yticks([0.1,1,10],[0.1,1,10] )
#     plt.hlines(1,0,100,'k')
#     plt.xlabel('density [%]')
#     plt.ylabel(r'Relative Amplitde')
    
#     plt.xlim([0,100])
#     plt.ylim([0.1,30])
#     #if n_a ==anchos.size-1:
#     plt.legend(title='Width')
#     plt.title(title)

    
#     n_a += 1
#   n_h += 1

# plt.show()
    