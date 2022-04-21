# -*- coding: utf-8 -*-
"""
Created on 13/06/2021

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
# from VoigtFit import *

path0="T:/pyprogs/calculateFieldShift/Outputs/2022-03-11_Cilindros_hexagonal_AltaResolucion/"
distancias, radios, alturas, vss, densidades = np.loadtxt(path0+'Densidades.dat').T

p_cubierto = []
delta_mic = []
delta_bulk = []
amp_mic = []
amp_bulk = []

alturas_t=[]
distancias_t=[]
radios_t=[]
densidades_t=[]

path=path0
nn=0

folders = ['','2022-03-11_','2022-03-13_']

for folder in folders:
  path0=f"T:/pyprogs/calculateFieldShift/Outputs/{folder}Cilindros_hexagonal_AltaResolucion/"
  print(path0)
  distancias, radios, alturas, vss, densidades = np.loadtxt(path0+'Densidades.dat').T
  for ii in range(radios.size):
    # path=path0+'SMC64-k1/iteracion{:d}/'.format(jj)    
    h = alturas[ii]
    d = distancias[ii]
    r = radios[ii]
    p = densidades[ii]
    vs = vss[ii]
          
    regiones = ['-microestructuras', '-bulk']
    col =  ['k','r','b']
    
    n_r=-1
    for region in regiones:
      n_r+=1
      path    = path0 + 'SP/'      
      archivo = 'h{:d}_r{:.2f}_d{:.2f}_vs{:.2f}um_SP{}.dat'.format(int(h), r, d,vs, region)
        
      # extraigo

      try:
        datos = np.loadtxt(path+archivo)  
        if n_r==0:
          alturas_t.append(h)
          distancias_t.append(d)    
          radios_t.append(r)
          densidades_t.append(p)
          nn+=1
      except:
        print(f"error al intentar leer: {archivo}")
        continue
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
      plt.subplot(1,3,n_r+1)
      plt.plot(ppmAxis,spec, col[n_r], linewidth=2)
      #plt.xlim([ppmAxis[-1], ppmAxis[0]]) 
      plt.xlim(150,-150)  
      plt.vlines(0, 0, np.max(spec))
      plt.yticks([])         
    
      if region=='-microestructuras':
        delta_mic.append(ppmAxis[spec==np.max(spec)][0])
        i_mic = np.trapz(spec, x=ppmAxis)
        amp_mic.append(i_mic)
        
        if vs == r:
          plt.figure(11111)
        else:
          plt.figure(22222)
          plt.annotate(f"r{r} vs{vs}", (p, ppmAxis[spec==np.max(spec)][0]))
        plt.scatter(p, ppmAxis[spec==np.max(spec)][0])
        
          
      elif region=='-bulk':
        delta_bulk.append(ppmAxis[spec==np.max(spec)][0])
        i_bulk = np.trapz(spec, x=ppmAxis)                
        amp_bulk.append(i_bulk)
      
      
    
#---------------- guardado


delta_mic = np.array(delta_mic)
delta_bulk = np.array(delta_bulk)
amp_mic   = np.array(amp_mic)
amp_bulk  = np.array(amp_bulk)


amp_rel = amp_mic/amp_bulk
corrimientos = delta_mic-delta_bulk

#%%
plt.figure(8491689)
try:
  plt.scatter(densidades_t,delta_mic, c=alturas_t )
except ValueError:
  plt.scatter(densidades_t[:-1],delta_mic, c=radios_t[:-1] )
  
plt.colorbar()

# datos = np.array([alturas_t, radios_t, distancias_t, densidades_t, corrimientos, amp_rel, delta_mic, delta_bulk]).T
# np.savetxt(path0+'resultados.dat', datos)
# np.savetxt(path0+'resultados.csv', datos, fmt='%.4f', delimiter=',')


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

plt.show()
    