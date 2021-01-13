#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""


import numpy as np
import matplotlib.pyplot as plt
from Muestra import *
from Delta import *
from Superposicion import *
from Graficador import *
from SimulationVolume import *
from Espectro import espectro
from Medicion import *
import time


#%%----------------------------------------------------------------------------  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Parametros fisicos
Chi =  24.1*1e-6 #(ppm) Susceptibilidad volumetrica
B0 = 7 # T
skindepth = 0.012 # profundida de penetracion, mm


# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
voxelSize = [0.001, 0.001, 0.001]# mm
N = [256,256,256] # para trapped_arranged_sticks

# utilizo una funcion que dado dos argumentos define el restante. Ya sea N, 
# FOV (field of view) o  voxelSize
volumen = SimulationVolume(voxelSize=voxelSize, N=N)
#volumen = SimulationVolume(FOV=FOV, N=N)


#%% LOOP

anchos = np.array([1,5,10,20,40])*1e-3
alturas = np.array([10,25,50,75,100,128])*1e-3
porcentajes = np.array([10,30,50,70,90])


porcentajes = np.array([75])
anchos = np.array([40])*1e-3

n_total = anchos.size * alturas.size * porcentajes.size

#inicio el reloj
t0 = time.time()




nn=0
for ancho in anchos:
  for h in alturas:
    for porcentaje in porcentajes:
      nn+=1
      print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
      print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
      msj = 'altura= {:d} um,  ancho= {:d} um,  densidad p= {:d}%'.format(int(h*1e3), int(ancho*1e3), porcentaje)
      print(msj)
      print(' ')
      progreso = nn/n_total*100
      print('         ... Progreso :  {:.2f}%  ({}/{})'.format(progreso, nn, n_total))
      elapsed = (time.time() - t0)/60
      print('tiempo: {:.2f} min'.format(elapsed))
      #%% CREACION DE LA MUESTRA-----------------------------------------------------
      #------------------------------------------------------------------------------
      #------------------------------------------------------------------------------
      #Creo el objeto muestra. Le tengo que dar de entrada:
      #  el volumen
      #  la geometria: el nombre del constructor que va a usar para crear el phantom
      #microestructuras
      medidas = [h,0.128,0.128] #       
      #muestra = Muestra(volumen, medidas=medidas, geometria='porcentaje_lanzas',ancho=ancho, porcentaje=porcentaje) # para 'porcentaje_palos'
      muestra = Muestra(volumen, medidas=medidas, geometria='porcentaje_palos',ancho=ancho, porcentaje=porcentaje) # para 'porcentaje_palos'
      #%% CREACION DEL OBJETO DELTA--------------------------------------------------
      # delta es la perturbacion de campo magnetico
      delta = Delta(muestra)
      #%%
      # SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK
      superposicion = Superposicion(muestra, delta)
      #%% guardado
      regiones = ['', '-microestructuras', '-bulk']  
      # -------- centro--------------------------------------------------------------    
      for region in regiones:
        # ..... SP ......
        path = './Espectros/centro_aleatorias_palo/SP/'
        k = 0.5
        medicion = Medicion(superposicion, volumen_medido='centro{}'.format(region))            
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=k)
        datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
        file = 'centro{}_h{:d}_ancho{:d}_dens{:d}_SP_k{:.2f}'.format(region,int(h*1e3), int(ancho*1e3), int(porcentaje), k)
        np.savetxt(path+file, datos)
        # ..... SMC .....
        path = './Espectros/centro_aleatorias_palo/SMC/'
        k_list = [1, 1.1, 1.2, 1.3, 1.5, 2.0]
        N=16                  
        for k in k_list:        
          ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , k=k, N=N)
          datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
          file = 'centro{}_h{:d}_ancho{:d}_dens{:d}_SMC_N{:d}_k{:.2f}'.format(region,int(h*1e3), int(ancho*1e3), int(porcentaje), N, k)
          np.savetxt(path+file, datos)      
      # --------completo-------------------------------------------------------------
#      for region in regiones:
#        # ..... SP ......
#        path = './Espectros/completo/SP/'
#        k = 0.5
#        medicion = Medicion(superposicion, volumen_medido='completo{}'.format(region))            
#        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=k)
#        datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
#        file = 'completo{}_h{:d}_ancho{:d}_dens{:d}_SP_k{:.2f}'.format(region,int(h*1e3), int(ancho*1e3), int(porcentaje), k)
#        np.savetxt(path+file, datos)
#        # ..... SMC .....
#        path = './Espectros/completo/SMC/'
#        k_list = [1, 1.1, 1.2, 1.3, 1.5, 2.0]
#        N=16                  
#        for k in k_list:        
#          ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , k=k, N=N)
#          datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
#          file = 'completo{}_h{:d}_ancho{:d}_dens{:d}_SMC_N{:d}_k{:.2f}'.format(region,int(h*1e3), int(ancho*1e3), int(porcentaje), N, k)
#          np.savetxt(path+file, datos)              
      # -----------------------------------------------------------------------------
      duracion = (time.time()-t0)/60  - elapsed 
      del muestra, delta, superposicion, medidas   # libero RAM
      print('tiempo en este paso: {:.2f} min'.format(duracion))        
#%%

#v=5
#plt.figure(20000)
#plt.pcolormesh(superposicion.delta_sens[:,64,:], cmap='seismic', vmax=v, vmin=-v)
#plt.colorbar()
##%%
#plt.figure(20001)
#plt.pcolormesh(superposicion.delta_sens[65,:,:], cmap='seismic', vmax=v, vmin=-v)
#plt.colorbar()


#%% GRAFICOS-------------------------------------------------------------------
#gr = Graficador(muestra, delta)

#%%
# slice en x central
#gr.mapa()
#gr.mapa(dim=2, corte=0.5, completo=True)
#gr.mapa(dim=0, corte=0.6, completo=True)
#gr.mapa(dim=0, corte=0.5, completo=False)

#%% CREACION DEL ESPECTRO -----------------------------------------------------

#ppmAxis, spec = espectro(superposicion.delta_sens)
#ppmAxis, spec_bulk = espectro(superposicion.get_delta_bulk()) 
#ppmAxis, spec_dend = espectro(superposicion.get_delta_dendritas())
#ppmAxis, spec_bulk = espectro(superposicion.get_delta_bulk() , KS=-superposicion.delta_in) 
#ppmAxis, spec_dend = espectro(superposicion.get_delta_dendritas(), KS=-superposicion.delta_in )


#plt.figure(123456)
#plt.plot(ppmAxis, spec_bulk, 'b'  , linewidth=3, label='bulk')
#plt.plot(ppmAxis, spec_dend, 'r'  , linewidth=3, label='dendritas')
#plt.plot(ppmAxis, spec     , 'k', linewidth=3, label='total')
#plt.xlabel(r'$^7$Li Chemical Shift [ppm]')
#plt.xlim([ppmAxis[-1], ppmAxis[0]])
#plt.legend()

# espectro normalizado de las dos regiones:
#plt.figure(12345)
#plt.plot(ppmAxis, spec_dend/np.max(spec_dend), 'r'  , linewidth=3, label='dendritas (normalizado)')
#plt.plot(ppmAxis, spec_bulk/np.max(spec_bulk), 'b'  , linewidth=3, label='bulk (normalizado)')
#plt.xlabel(r'$^7$Li Chemical Shift [ppm]')
#plt.xlim([ppmAxis[-1], ppmAxis[0]])
#plt.legend()
#
#
#
