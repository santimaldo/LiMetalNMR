# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:37:40 2019

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
from VoigtFit import *


alturas = np.array([10,25,50,75,100,128])*1e-3
anchos = np.array([1,5,10,20,40])*1e-3
densidades = [10,25,50,75,90]



#densidades = [10,25,50,75,90]
alturas = np.array([10,100])*1e-3
#anchos = np.array([1,5,10,20])*1e-3



n_h=0
for h in alturas:
  h = int(h*1e3)
  n_a = 0
  for ancho in anchos:
    ancho = int(ancho*1e3)
    p_cubierto = []
    corrimientos = []
    s_mic = []
    s_bulk = []
    n_d=0
    for dens in densidades:
      if ancho==40:
        if dens==25:
          dens = 30
        elif dens==75:
          dens = 70

      path_p = './Espectros/centro_aleatorias_palo/SP/pCubierto/'
      file_p = 'h{:d}_ancho{:d}_dens{:d}'.format(h, ancho, dens)
      p_cub = np.loadtxt(path_p+file_p)
      p_cubierto.append(p_cub)

      n_d+=1
      dens = int(dens)  
      # directorio de datos
      # carpeta= 'centro/SP/'
      carpeta= 'centro_aleatorias_palo/SP/'
      path = "./Espectros/{}".format(carpeta)
      
    #  archivo = 'h{:d}_ancho{:d}_dens{:d}_SP_k0.50'.format(h,ancho,dens) 
      regiones = ['-microestructuras', '-bulk', '']
      
      n_r = 0
      col =  ['r','b','k']
      for region in regiones:
        archivo = 'centro{}_h{:d}_ancho{:d}_dens{:d}_SP_k0.50'.format(region,h,ancho,dens)
        # extraigo  
        datos = np.loadtxt(path+archivo)  
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
            
#        plt.figure(1231)
#        plt.subplot(2,3,n_d)
#        plt.plot(ppmAxis,spec, col[n_r], linewidth=2)
#        #plt.xlim([ppmAxis[-1], ppmAxis[0]])
#        plt.xlim(50,-50)    
#        plt.yticks([])      
        

        if region=='-microestructuras':
          corrimientos.append(ppmAxis[spec==np.max(spec)][0])
          i_mic = np.trapz(spec, x=ppmAxis)
          s_mic.append(i_mic)
        elif region=='-bulk':
          i_bulk = np.trapz(spec, x=ppmAxis)                
          s_bulk.append(i_bulk)
        n_r+=1
      #%%
      # el ultimo spec en el loop de regiones es el total. Los superpongo a todos
  #    plt.figure(1232)
  #    plt.plot(ppmAxis,spec,  linewidth=3, label='density: {:d}%'.format(dens))
    #%%
  #  plt.hlines(0,ppmAxis[-1], ppmAxis[0])
  #  plt.vlines(0,0,np.max(spec)*1.1, linestyle='dashed')
  #  #plt.xlim([ppmAxis[-1], ppmAxis[0]])    
  #  plt.yticks([])
  #  plt.xlabel(r"$^7$Li Chemical Shift [ppm]")
  #  plt.xlim(50,-50)    
  #  plt.legend()    
  #  plt.show()
      
    
    dens = np.array(p_cubierto)
    corrimientos = np.array(corrimientos)
    ###ajuste lineal
    coef = np.polyfit(dens, corrimientos, 1)
    poly1d_fn = np.poly1d(coef) 
    #
    label = r'{:d} $\mu$m'.format(ancho)
    title = r'height: {:d} $\mu$m'.format(h)
    
    #plt.figure(39203920)
    #plt.subplot(2,3,n_h+1)    
    plt.figure(100000+n_h+1)
    cmap = plt.get_cmap('jet')
    color = cmap(n_a/(anchos.size))
    plt.plot(dens, corrimientos, 'o', color=color, label=label)
    plt.plot(dens, poly1d_fn(dens), '--', color=color)
    #plt.xlabel('density (covered area/total area) [%]')
    plt.xlabel('density [%]')
    plt.ylabel(r'$\delta-\delta_{Bulk}$')
    plt.ylim([0,25])
    plt.xlim([0,100])
    #if n_a ==anchos.size-1:
    plt.legend(title='Width')
    plt.title(title)


    #plt.figure(1111)
    #plt.subplot(2,3,n_h+1)
    plt.figure(100+n_h+1)    
    signal_bulk = np.array(s_bulk)    
    signal_mic  = np.array(s_mic)    
    signal_rel  = signal_mic/signal_bulk    
    #plt.subplot(1,2,1)
    #plt.plot(dens, signal_mic, 'ro--', label = 'mic')
    #plt.plot(dens, signal_bulk, 'bo--', label = 'bulk')
    #plt.plot(dens, signal_mic ,'o', color=color, label=label)
    #plt.legend()
    #plt.subplot(1,2,2)
    #plt.title('s_mic/s_bulk')
    #plt.plot(dens, signal_rel, 'o--')
    plt.plot(dens, signal_rel,'o--', color=color, label=label)
    plt.yscale('log')
    plt.yticks([0.1,1,10],[0.1,1,10] )
    plt.hlines(1,0,100,'k')
    plt.xlabel('density [%]')
    plt.ylabel(r'Relative Amplitde')
    
    plt.xlim([0,100])
    plt.ylim([0.1,30])
    #if n_a ==anchos.size-1:
    plt.legend(title='Width')
    plt.title(title)

    
    n_a += 1
  n_h += 1

plt.show()
    