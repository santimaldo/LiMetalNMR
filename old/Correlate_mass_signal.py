# -*- coding: utf-8 -*-
"""
Created on 14/05/2024

@author: santi
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import simpson
plt.rcParams.update({'font.size': 20})

path0 ='./Outputs/2024-05-09_CilindrosHexagonal_cantidad-senal/'

df = pd.read_csv(f"{path0}MasaMedida.dat", delimiter='\t', )
# agrego nuevas columnas:
nombres = ['total', 'microestructuras', 'bulk']
for nmr in ["delta", "amp"]:
  for reg in nombres:
    df[f"{nmr}_{reg}"] = np.nan
    

regiones = ['','-microestructuras', '-bulk']
#%%
for ii in range(len(df)):  
  for n_r in range(len(regiones)):            

    archivo = f'h{df.altura[ii]:.0f}_'\
              f'r{df.radio[ii]:.2f}_'\
              f'dens{df.densidad_nominal[ii]:.1f}_'\
              f'vs{df.voxelSize[ii]:.3f}um_SP'\
              f'{regiones[n_r]}.dat'
              
              
    # extraigo  
    datos = np.loadtxt(f"{path0}SP/{archivo}")  
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
        

    delta = ppmAxis[spec==np.max(spec)][0]      
    df[f"delta_{nombres[n_r]}"][ii] = amp

    amp = simpson(spec, x=ppmAxis)
    df[f"amp_{nombres[n_r]}"][ii] = amp

#%%

fig, ax = plt.subplots(num=1)
region = 'microestructuras'
s_norm = df[f"amp_{region}"][(df.radio==1) & (df.densidad_nominal==0.1)]
for radio in df.radio.unique():
  # lithium density 0.534 g/cm3
  df_r = df[df.radio==radio] 
  masa_real = (df_r['voxelSize']*1e-4)**3 * df_r[f"masa_{region}"] / 0.534
  scatter = ax.scatter(masa_real, df_r[f"amp_{region}"]/float(s_norm), s=df_r.densidad_nominal*100)
  ax.set_xlabel("mass [g]")  
  # ax = df_r.plot.scatter(x='masa_microestructuras', y='amp_microestructuras')

# ordeno
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
#     label = r'{:d} $\mu$m'.format(ancho)
#     title = r'height: {:d} $\mu$m'.format(h)
    
#     #plt.figure(39203920)
#     #plt.subplot(2,3,n_h+1)    
#     plt.figure(100000+n_h+1)
#     cmap = plt.get_cmap('jet')
#     color = cmap(n_a/(anchos.size))
#     plt.plot(dens, corrimientos, 'o', color=color, label=label)
#     plt.plot(dens, poly1d_fn(dens), '--', color=color)
#     #plt.xlabel('density (covered area/total area) [%]')
#     plt.xlabel('density [%]')
#     plt.ylabel(r'$\delta-\delta_{Bulk}$')
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
    