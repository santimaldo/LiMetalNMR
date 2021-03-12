#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""
#stop

import numpy as np
import matplotlib.pyplot as plt
from Modules.SimulationVolume import *
from Modules.Muestra import *
from Modules.Delta import *
from Modules.Superposicion import *
from Modules.Graficador import *
from Modules.Medicion import *
import time

#inicio el reloj
t0 = time.time()
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

N = [256,512,512] 

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
medidas = [0.128,0.256,0.256]

# muestra = Muestra(volumen, medidas=medidas, geometria='distancia_constante', ancho=16e-3, distancia=20e-3)

muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2',ancho=16e-3, distancia=20e-3) # para 'porcentaje_palos'

#%% CREACION DEL OBJETO DELTA--------------------------------------------------
# delta es la perturbacion de campo magnetico
delta = Delta(muestra)

#%%
# SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK
superposicion = Superposicion(muestra, delta)
# superposicion = Superposicion(muestra, delta, radio='000', z0=84e-3) # si pongo 'radio', es porque lee de un perfil
#%%
#medicion = Medicion(superposicion, volumen_medido='completo')
medicion = Medicion(superposicion, volumen_medido='completo',stl_file='test')


ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153)
#ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=1111)
#datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
#np.savetxt(path+'h{:d}_ancho{:d}_dens{:d}_SP_k{:.2f}'.format(int(h*1e3), int(ancho*1e3), int(porcentaje), k))

#ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1  , figure=153)
#ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1.1, figure=153)
#ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1.2, figure=153)
#ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1.3, figure=153)


elapsed = (time.time() - t0)/60
print('---  tiempo: {:.2f} min'.format(elapsed))