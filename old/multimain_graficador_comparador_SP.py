# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:37:40 2019

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
from VoigtFit import *


h = 10
ancho = 10
dens = 10

  
# directorio de datos
carpeta= 'centro_aleatorias_palo'
path = "./Espectros/{}/".format(carpeta)
#  archivo = 'h{:d}_ancho{:d}_dens{:d}_SP_k0.50'.format(h,ancho,dens)
# parametros son: [region, h, ancho, dens, seq, k]
parametros = [ ['', h,ancho,dens,'SP',0.5], ['-microestructuras', h,ancho,dens,'SP',0.5], ['-bulk',h,ancho,dens,'SP',0.5]]
col =  ['k','r','b']
labels = ['Full sample', 'Microstructures', 'Bulk']

h= [10,25]
ancho = [1,20]
dens  = [25,10]
k = 0.5
seq = 'SP'
parametros = [ ['', h[0],ancho[0],dens[0],seq,k],# ['-microestructuras', h,ancho[0],dens[0],'SP',0.5], ['-bulk',h,ancho[0],dens[0],'SP',0.5],\
               ['', h[1],ancho[1],dens[1],seq,k]]
#               ['', h,ancho[2],dens[2],'SP',0.5]]# ['-microestructuras', h,ancho[1],dens[1],'SP',0.5], ['-bulk',h,ancho[1],dens[1],'SP',0.5]]
#col =  ['k','r','b']*2
#labels = ['Full sample', 'Microstructures', 'Bulk']*2
col = ['indigo','orangered']
labels = ['ancho=1, dens=10','ancho=40, dens=10','ancho=40, dens=70']


iterador=0
for par in parametros:
  print(par)
  region, h, ancho, dens, seq, k = par
  if seq.lower()=='sp':
    path = "./Espectros/{}/SP/".format(carpeta)
  elif seq.lower() in 'smc':
    path = "./Espectros/{}/SMC/".format(carpeta)
    seq = 'SMC_N16'

  base = 'centro{}_h{:d}_ancho{:d}_dens{:d}_{}_k{:.2f}'
  archivo=base.format(region,int(h),int(ancho),int(dens), seq, k)

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

  # determino el pico de dendritas
  if 'micro' in region:
    micro_peak = ppmAxis[spec==np.max(spec)]
  elif region=='':
    maxx = np.max(spec)
  #elif 'bulk' in region:
  #  spec=spec*0.95
   
  #Npicos = 2
  #vf = VoigtFit(ppmAxis,spec, Npicos=Npicos, center=[0,20], fijar=['m1_center'])
  #vf = VoigtFit(ppmAxis,spec, Npicos=Npicos, center=[0,20])
  #vf = VoigtFit(ppmAxis,spec, Npicos=Npicos, center=[246,260,250])
  #ajuste, componentes = vf.componentes(ppmAxis)
    
  # reajusto
#  params = vf.params
#  vf = VoigtFit(ppmAxis,spec, Npicos=Npicos, params=params)
#  ajuste, componentes = vf.componentes(ppmAxis)
  
#  plt.figure(1231)
#  plt.subplot(3,3,nn)
#  plt.plot(ppmAxis,spec)
#  plt.plot(ppmAxis, ajuste, 'k')
#  for comp in componentes:
#      plt.plot(ppmAxis, comp, '--')
#  plt.xlim([ppmAxis[-1], ppmAxis[0]])
#  plt.yticks([])      
  
  #%%

  plt.figure(1232)
  #plt.plot(ppmAxis,spec,   linewidth=3, color=col[iterador],label=labels[iterador])
  plt.plot(ppmAxis,spec/np.max(spec),   linewidth=3, color=col[iterador],label=labels[iterador])
  #plt.plot(ppmAxis, ajuste)
  plt.yticks([])
  plt.xlabel(r"$\delta-\delta_{Bulk}$ [ppm]")
  #if region!='':
    #plt.fill_between(ppmAxis, spec, color=col[iterador], alpha=0.3)
  iterador+=1

#plt.vlines(0         , 0, maxx*1.2, 'b', linestyle='dashed', linewidth=2)
#plt.vlines(micro_peak, 0, maxx*1.2, 'r', linestyle='dashed', linewidth=2)    
plt.hlines(0,ppmAxis[-1], ppmAxis[0])    
#plt.xlim([ppmAxis[-1], ppmAxis[0]])    
plt.xlim((60,-60))
#plt.ylim((0, maxx*1.3))
plt.legend(prop={'size':14})    
plt.show()