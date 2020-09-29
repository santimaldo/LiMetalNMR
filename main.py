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
#voxelSize = [0.001, 0.250, 0.250]# mm
#FOV = [0.1, 0.1, 0.1]
#N = [512,128,128]
voxelSize = [0.001, 0.001, 0.001]# mm
#N = [128,64,64] # para arranged_sticks
N = [256,256,256] # para trapped_arranged_sticks

# con estos numeros, Nj*voxelSize_j queda
#    z: 1.536 mm  ; y: 3.84 mm  ; x: 10.24 mm

# utilizo una funcion que dado dos argumentos define el restante. Ya sea N, 
# FOV (field of view) o  voxelSize

volumen = SimulationVolume(voxelSize=voxelSize, N=N)
#volumen = SimulationVolume(FOV=FOV, N=N)
#%% CREACION DE LA MUESTRA-----------------------------------------------------

#Creo el objeto muestra. Le tengo que dar de entrada:
#  el volumen
#  la geometria: el nombre del constructor que va a usar para crear el phantom
#muestra = Muestra(volumen, geometria='spikes1')
#medidas = [0.71, 4, 10]
#microestructuras
medidas = [0.028,0.088,0.088] # para trapped_arranged_sticks
#medidas = [0.028,0.028,0.028] # para arranged_sticks
# bulk:
#muestra = Muestra(volumen, medidas=medidas, geometria='bulk')
#muestra = Muestra(volumen, medidas=medidas, geometria='arranged_sticks')
muestra = Muestra(volumen, medidas=medidas, geometria='trapped_arranged_sticks', paredes=False)
#muestra = Muestra(volumen, medidas=medidas, geometria='trapped_arranged_sticks')
#muestra = Muestra(volumen, medidas=medidas, geometria='distancia_constante', ancho=12e-3, distancia=3e-3)

#%% CREACION DEL OBJETO DELTA--------------------------------------------------
delta = Delta(muestra)


#%%
superposicion = Superposicion(muestra, delta)
s2 = Superposicion(muestra, delta)

#%%

v=5
plt.figure(20000)
plt.pcolormesh(superposicion.delta_sens[:,118,:], cmap='seismic', vmax=v, vmin=-v)
plt.colorbar()

plt.figure(20001)
plt.pcolormesh(superposicion.delta_sens[45,:,:], cmap='seismic', vmax=v, vmin=-v)
plt.colorbar()

#%%
#delta que contribuye a la señal es superposicion.delta_sens
# datos es un array 1D con esos datos para hacer el histograma
#datos = superposicion.delta_sens[s.delta_sens != 0].flatten()
#plt.hist(datos)


#%% GRAFICOS-------------------------------------------------------------------
gr = Graficador(muestra, delta)

#%%
# slice en x central
gr.mapa()
gr.mapa(dim=2, corte=0.6, completo=True)
gr.mapa(dim=0, corte=0.6, completo=True)
#gr.mapa(dim=0, corte=0.5, completo=False)
