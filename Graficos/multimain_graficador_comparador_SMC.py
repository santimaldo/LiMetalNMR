  # -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:37:40 2019

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})


alturas = [10,10]
radios = [2, 10]
densidades = [0.4, 0.4]
vss = [0.25, 0.25]
colores = ['indigo', 'orangered']
leyendas = ['Sample A', 'Sample B']

data_dir = "2023-08-10_Cilindros_hexagonal_AltaResolucion"
path0 = f"../Outputs/{data_dir}/"


# BULK: ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# archivo = '../Outputs/centro_aleatorias_palo/SP/centro-bulk_h10_ancho1_dens10_SP_k0.50'
# # extraigo  
# datos = np.loadtxt(archivo)  
# ppmAxis0 = datos[:,0]
# spec = datos[:,1]
# # retoco:
# ppmAxis = ppmAxis0
# spec = spec - spec[0]
# # reduzco los datos a una VENTANA alrededor de un CENTRO
# ventana = 200
# center = 0
# ppmAxis = ppmAxis0[np.abs(center-ppmAxis0)<ventana]
# spec_Bulk = spec[np.abs(center-ppmAxis0)<ventana]
# spec_Bulk_norm = spec_Bulk/np.max(spec_Bulk)
########++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



#seq = 'SMC'
#k = 1.0
#parametros = [ ['', h,ancho,dens,seq,k], ['-microestructuras', h,ancho,dens,seq,k], ['-bulk',h,ancho,dens,seq,k]]
#labels = ['Full sample', 'Microstructures', 'Bulk']
#col =  ['k','r','b']

regiones = ['', '-microestructuras', '-bulk']
specsSP = []
specsSMC = []
for nn in range(len(radios)):
    h = alturas[nn]
    r = radios[nn]
    dens = densidades[nn]      
    vs= vss[nn]
    for seq in ['SP', 'SMC']:
      specs1 = []
      for region in regiones:    
        path = f"{path0}{seq}/"
        archivo = 'h{:d}_r{:.2f}_dens{:.1f}_vs{:.3f}um_{}{}.dat'.format(h,r,dens,vs,seq,region)    
        datos = np.loadtxt(f"{path}{archivo}")  
        
        # extraigo      
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
        specs1.append([ppmAxis, spec])                
      if seq=='SP':
        specsSP.append(specs1)
      elif seq=='SMC':
        specsSMC.append(specs1)
#%%

# for nn in range(len(radios)):    
#     specsSP[nn][2][1] = 2 * specsSP[nn][2][1]
#     specsSP[nn][0][1] = specsSP[nn][1][1]+specsSP[nn][2][1]
    
#     specsSMC[nn][2][1] = 2 * specsSP[nn][2][1]
#     specsSMC[nn][0][1] = specsSP[nn][1][1]+specsSP[nn][2][1]
      
#%%


fix, axs = plt.subplots(2, 2, figsize=(10, 5), num=1)

for nn in range(len(radios)):    
    ax = axs[nn][0]
    for mm in range(len(regiones)):    
      ppmAxis, spec = specsSP[nn][mm]
      ax.plot(ppmAxis, spec)

for nn in range(len(radios)):    
    ax = axs[nn][1]
    for mm in range(len(regiones)):
      ppmAxis, spec = specsSMC[nn][mm]
      ax.plot(ppmAxis, spec)
    

for ax in axs.flatten():
    ax.set_xlim([50,-50])



fix, axs = plt.subplots(1, 2, figsize=(10, 5), num=2)

for nn in range(len(radios)):    
    ax = axs[nn]
    # where is the bulk:
    ppmAxis, spec = specsSP[nn][2]
    maxx = spec.max()      
    
    # for mm in range(len(regiones)):    
    ppmAxis, spec = specsSP[nn][0]
    ax.plot(ppmAxis, spec/spec.max())
    ppmAxis, spec = specsSMC[nn][0]
    ax.plot(ppmAxis, spec/spec.max())
    

for ax in axs.flatten():
    ax.set_xlim([50,-50])


# plt.figure(ancho)
# plt.title(r'spec/spec_k2,  ancho={}$\mu$m'.format(ancho))  
# plt.plot(ppmAxis,spec,   linewidth=3, color=col[iterador],label=labels[iterador])
# #plt.plot(ppmAxis, ajuste)
# plt.yticks([])
# plt.xlabel(r"$\delta-\delta_{Bulk}$ [ppm]")
# #if region!='':
#   #plt.fill_between(ppmAxis, spec, color=col[iterador], alpha=0.3)
  

# #plt.vlines(0         , 0, maxx*1.2, 'b', linestyle='dashed', linewidth=2)
# #plt.vlines(micro_peak, 0, maxx*1.2, 'r', linestyle='dashed', linewidth=2)    
# plt.hlines(0,ppmAxis[-1], ppmAxis[0])    
# #plt.xlim([ppmAxis[-1], ppmAxis[0]])    
# plt.xlim((60,-60))
# #plt.ylim((0, maxx*1.3))
# plt.legend(prop={'size':14})    


# plt.figure(1000+ancho)
# plt.title(r'$(spec-spec_k2)/(spec_k2)$,  ancho=%d $\mu$m'%(ancho))  
# iterador = 0
# integrales_dif = []
# integrales = []
# for n_S in range(len(specs)):
#   spec = specs[n_S]
#   ppmAxis = ppms[n_S]
#   #dif = spec-specs[-2]
#   dif = spec-spec_Bulk_norm
#   plt.plot(ppmAxis,dif, linewidth=3, color=col[iterador],label=labels[iterador])
#   plt.yticks([])
#   plt.xlabel(r"$\delta-\delta_{Bulk}$ [ppm]")
#   plt.hlines(0,ppmAxis[-1], ppmAxis[0])    
#   plt.xlim((60,-60))
#   plt.legend(prop={'size':14})    
#   integrales_dif.append(np.trapz(dif, x=ppmAxis))
#   integrales.append(np.trapz(spec, x=ppmAxis))
#   iterador+=1
 
