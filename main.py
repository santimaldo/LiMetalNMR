#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""


import numpy as np
import matplotlib.pyplot as plt
from Muestra import *
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
voxelSize = [0.071/2, 0.25, 0.25]# mm
#FOV = [0.714*30, 50.048, 50.048]
N = [512, 64, 64]
#voxelSize = [0.006, 0.03, 0.08]# mm
#Nz, Ny, Nx = [256, 128, 128]
# con estos numeros, Nj*voxelSize_j queda
#    z: 1.536 mm  ; y: 3.84 mm  ; x: 10.24 mm

# utilizo una funcion que dado dos argumentos define el restante. Ya sea N, 
# FOV (field of view) o  voxelSize
#N, voxelSize, FOV = SimulationVolume(voxelSize=voxelSize, N=N)
#N, voxelSize, FOV = SimulationVolume(N=N, FOV=FOV)

volumen = SimulationVolume(voxelSize=voxelSize, N=N)

#VSz, VSy, VSx = voxelSize
#FOVz, FOVy, FOVx = FOV 
#Nz, Ny, Nx = N


#%% CREACION DE LA MUESTRA-----------------------------------------------------

#Creo el objeto muestra. Le tengo que dar de entrada:
#  el volumen
#  la geometria: el nombre del constructor que va a usar para crear el phantom
#muestra = Muestra(volumen, geometria='spikes1')
medidas = [0.071, 10, 4]
muestra = Muestra(volumen, medidas=medidas)


#%% CREACION DEL OBJETO DELTA--------------------------------------------------
#delta = Delta(muestra)


