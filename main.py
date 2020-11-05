#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""


import numpy as np
import matplotlib.pyplot as plt
from Modules.SimulationVolume import *
from Modules.Muestra import *
from Modules.Delta import *
from Modules.Superposicion import *
from Modules.Graficador import *
from Modules.Medicion import *


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
N = [128,64,64] # para trapped_arranged_sticks

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
#medidas = [0.028,0.088,0.088] # para trapped_arranged_sticks
#medidas = [0.028,0.028,0.028] # para arranged_sticks
#medidas = [0.032,0.128,0.128] # para arranged_sticks
medidas = [0.032,0.032,0.032] # 
# bulk:
#muestra = Muestra(volumen, medidas=medidas, geometria='bulk')
# otros
#muestra = Muestra(volumen, medidas=medidas, geometria='arranged_sticks')
#muestra = Muestra(volumen, medidas=medidas, geometria='trapped_arranged_sticks', paredes=False)
#muestra = Muestra(volumen, medidas=medidas, geometria='trapped_arranged_sticks')
#muestra = Muestra(volumen, medidas=medidas, geometria='distancia_constante', ancho=3e-3, distancia=3e-3)
#muestra = Muestra(volumen, medidas=medidas, geometria='distancia_constante', ancho=3e-3, distancia=3e-3)
muestra = Muestra(volumen, medidas=medidas, geometria='porcentaje_palos',ancho=1e-3, porcentaje=10) # para 'porcentaje_palos'
#%% CREACION DEL OBJETO DELTA--------------------------------------------------
# delta es la perturbacion de campo magnetico
delta = Delta(muestra)
#%%
# SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK
superposicion = Superposicion(muestra, delta)
#superposicion = Superposicion(muestra, delta, z0=224e-3)
#%%
#medicion = Medicion(superposicion, volumen_medido='completo')
medicion = Medicion(superposicion, volumen_medido='centro')


ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153)
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.75, figure=153)
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=1, figure=153)

ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=1111)
datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
#np.savetxt(path+'h{:d}_ancho{:d}_dens{:d}_SP_k{:.2f}'.format(int(h*1e3), int(ancho*1e3), int(porcentaje), k))

#ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1  , figure=153)
#ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1.1, figure=153)
#ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1.2, figure=153)
#ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1.3, figure=153)


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
gr = Graficador(muestra, delta)

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
