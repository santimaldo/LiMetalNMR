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
#N = [128,64,64] # para arranged_sticks
N = [256,256,256] # para trapped_arranged_sticks

# utilizo una funcion que dado dos argumentos define el restante. Ya sea N, 
# FOV (field of view) o  voxelSize
volumen = SimulationVolume(voxelSize=voxelSize, N=N)
#volumen = SimulationVolume(FOV=FOV, N=N)

#%% CREACION DE LA MUESTRA-----------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#Creo el objeto muestra. Le tengo que dar de entrada:
#  el volumen
#  la geometria: el nombre del constructor que va a usar para crear el phantom
#microestructuras
medidas = [0.028,0.088,0.088] # para trapped_arranged_sticks
#medidas = [0.028,0.028,0.028] # para arranged_sticks
# bulk:
#muestra = Muestra(volumen, medidas=medidas, geometria='bulk')
# otros
#muestra = Muestra(volumen, medidas=medidas, geometria='arranged_sticks')
muestra = Muestra(volumen, medidas=medidas, geometria='trapped_arranged_sticks', paredes=False)
#muestra = Muestra(volumen, medidas=medidas, geometria='trapped_arranged_sticks')
#muestra = Muestra(volumen, medidas=medidas, geometria='distancia_constante', ancho=12e-3, distancia=13e-3)

#%% CREACION DEL OBJETO DELTA--------------------------------------------------
# delta es la perturbacion de campo magnetico
delta = Delta(muestra)
<<<<<<< Updated upstream

#%% SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK
superposicion = Superposicion(muestra, delta)
=======
#%%
# SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK
#superposicion = Superposicion(muestra, delta, z0=84e-3)
superposicion = Superposicion(muestra, delta, radio='128', z0=84e-3) # si pongo 'radio', es porque lee de un perfil
#%%
#medicion = Medicion(superposicion, volumen_medido='completo')
medicion = Medicion(superposicion, volumen_medido='centro')
>>>>>>> Stashed changes


#%%

v=5
plt.figure(20000)
plt.pcolormesh(superposicion.delta_sens[:,118,:], cmap='seismic', vmax=v, vmin=-v)
plt.colorbar()

plt.figure(20001)
plt.pcolormesh(superposicion.delta_sens[45,:,:], cmap='seismic', vmax=v, vmin=-v)
plt.colorbar()


#%% GRAFICOS-------------------------------------------------------------------
gr = Graficador(muestra, delta)

#%%
# slice en x central
gr.mapa()
gr.mapa(dim=2, corte=0.6, completo=True)
gr.mapa(dim=0, corte=0.6, completo=True)
#gr.mapa(dim=0, corte=0.5, completo=False)

#%% CREACION DEL ESPECTRO -----------------------------------------------------

ppmAxis, spec = espectro(superposicion.delta_sens)
ppmAxis, spec_bulk = espectro(superposicion.get_delta_bulk() ) 
ppmAxis, spec_dend = espectro(superposicion.get_delta_dendritas() )

plt.figure(123456)
plt.plot(ppmAxis, spec_bulk, 'b'  , linewidth=3, label='bulk')
plt.plot(ppmAxis, spec_dend, 'r'  , linewidth=3, label='dendritas')
plt.plot(ppmAxis, spec     , 'k--', linewidth=3, label='total')
plt.xlabel(r'$^7$Li Chemical Shift [ppm]')
plt.xlim([ppmAxis[-1], ppmAxis[0]])
plt.legend()

## espectro normalizado de las dos regiones:
#plt.figure(12345)
#plt.plot(ppmAxis, spec_dend/np.max(spec_dend), 'r'  , linewidth=3, label='dendritas (normalizado)')
#plt.plot(ppmAxis, spec_bulk/np.max(spec_bulk), 'b'  , linewidth=3, label='bulk (normalizado)')
#plt.xlabel(r'$^7$Li Chemical Shift [ppm]')
#plt.xlim([ppmAxis[-1], ppmAxis[0]])
#plt.legend()



