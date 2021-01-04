  # -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:37:40 2019

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
from VoigtFit import *


alturas = [10,25]
anchos = [1, 20]
densidades = [25, 10]
colores = ['indigo', 'orangered']
leyendas = ['Sample A', 'Sample B']

# BULK: ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
archivo = './Espectros/centro_aleatorias_palo/SP/centro-bulk_h10_ancho1_dens10_SP_k0.50'
# extraigo  
datos = np.loadtxt(archivo)  
ppmAxis0 = datos[:,0]
spec = datos[:,1]
# retoco:
ppmAxis = ppmAxis0
spec = spec - spec[0]
# reduzco los datos a una VENTANA alrededor de un CENTRO
ventana = 200
center = 0
ppmAxis = ppmAxis0[np.abs(center-ppmAxis0)<ventana]
spec_Bulk = spec[np.abs(center-ppmAxis0)<ventana]
spec_Bulk_norm = spec_Bulk/np.max(spec_Bulk)
########++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  
# directorio de datos
carpeta= 'centro_aleatorias_palo'
#  archivo = 'h{:d}_ancho{:d}_dens{:d}_SP_k0.50'.format(h,ancho,dens)
# parametros son: [region, h, ancho, dens, seq, k]
#parametros = [ ['', h,ancho,dens,'SP',0.5], ['-microestructuras', h,ancho,dens,'SP',0.5], ['-bulk',h,ancho,dens,'SP',0.5]]

#seq = 'SMC'
#k = 1.0
#parametros = [ ['', h,ancho,dens,seq,k], ['-microestructuras', h,ancho,dens,seq,k], ['-bulk',h,ancho,dens,seq,k]]
#labels = ['Full sample', 'Microstructures', 'Bulk']
#col =  ['k','r','b']


for nnn in range(len(anchos)):
  h = alturas[nnn]
  ancho = anchos[nnn]
  dens = densidades[nnn]
  if ancho==40:
    if dens==75:
      dens=70
    if dens==25:
      dens=30

  seq = 'SMC'
  parametros = [ ['', h,ancho,dens,seq,1], ['', h,ancho,dens,seq,1.1], ['',h,ancho,dens,seq,1.2],['',h,ancho,dens,seq,1.3], ['',h,ancho,dens,seq,1.5], ['',h,ancho,dens,seq,2]]
  labels = ['k = 1.0','k = 1.1','k = 1.2','k = 1.3', 'k = 1.5', 'k = 2.0']
  col =  ['k','r','b', 'g', 'm', 'y']

  iterador=0
  specs = []
  ppms = []
  for par in parametros:
    region, h, ancho, dens, seq, k = par
    if seq.lower()=='sp':
      path = "./Espectros/{}/SP/".format(carpeta)
    elif seq.lower()=='smc':
      path = "./Espectros/{}/SMC/".format(carpeta)
      seq = 'SMC_N16'

    base = 'centro{}_h{:d}_ancho{:d}_dens{:d}_{}_k{:.2f}'
    archivo=base.format(region,int(h),int(ancho),int(dens), seq.upper(), k)

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
   
    # del spec total determino el pico bulk
    spec000 = spec[ppmAxis<5]
    pico_bulk = np.max(spec000)
    spec = spec/pico_bulk

    specs.append(spec)    
    ppms.append(ppmAxis)
    # determino el pico de dendritas
    if 'micro' in region:
      micro_peak = ppmAxis[spec==np.max(spec)]
    elif region=='':
      maxx = np.max(spec)

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

    plt.figure(ancho)
    plt.title(r'spec/spec_k2,  ancho={}$\mu$m'.format(ancho))  
    plt.plot(ppmAxis,spec,   linewidth=3, color=col[iterador],label=labels[iterador])
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


  plt.figure(1000+ancho)
  plt.title(r'$(spec-spec_k2)/(spec_k2)$,  ancho=%d $\mu$m'%(ancho))  
  iterador = 0
  integrales_dif = []
  integrales = []
  for n_S in range(len(specs)):
    spec = specs[n_S]
    ppmAxis = ppms[n_S]
    #dif = spec-specs[-2]
    dif = spec-spec_Bulk_norm
    plt.plot(ppmAxis,dif, linewidth=3, color=col[iterador],label=labels[iterador])
    plt.yticks([])
    plt.xlabel(r"$\delta-\delta_{Bulk}$ [ppm]")
    plt.hlines(0,ppmAxis[-1], ppmAxis[0])    
    plt.xlim((60,-60))
    plt.legend(prop={'size':14})    
    integrales_dif.append(np.trapz(dif, x=ppmAxis))
    integrales.append(np.trapz(spec, x=ppmAxis))
    iterador+=1
 
  
  k_list = [1,1.1,1.2,1.3,1.5,2]
  plt.figure(98)
  #plt.title('area de (spec-spec_k2)/spec_k2')
  plt.plot(k_list, integrales_dif, 'o--', label=leyendas[nnn], color=colores[nnn], markersize=8, linewidth=2)
  plt.xlabel('k')
  plt.ylabel('Microsctructures Signal [a.u]')
  plt.hlines(0,1,2)    
  plt.legend()
  
  k_list = [1,1.1,1.2,1.3,1.5,2]
  plt.figure(99)
  plt.title('area espectro')
  plt.plot(k_list, integrales, 'o--', label=str(ancho), color=colores[nnn])
  plt.xlabel('k')
  plt.ylabel('Signal [a.u]')
  plt.legend()
  plt.hlines(0,1,2)    
  nnn+=1

plt.show()