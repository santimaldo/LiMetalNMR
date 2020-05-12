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
#voxelSize = [0.1, 0.1, 0.1]# mm
FOV = [0.1, 0.1, 0.1]
N = [64,64,64]
#voxelSize = [0.006, 0.03, 0.08]# mm
#Nz, Ny, Nx = [256, 128, 128]
# con estos numeros, Nj*voxelSize_j queda
#    z: 1.536 mm  ; y: 3.84 mm  ; x: 10.24 mm

# utilizo una funcion que dado dos argumentos define el restante. Ya sea N, 
# FOV (field of view) o  voxelSize

#volumen = SimulationVolume(voxelSize=voxelSize, N=N)
volumen = SimulationVolume(FOV=FOV, N=N)


#%% CREACION DE LA MUESTRA-----------------------------------------------------

#Creo el objeto muestra. Le tengo que dar de entrada:
#  el volumen
#  la geometria: el nombre del constructor que va a usar para crear el phantom
#muestra = Muestra(volumen, geometria='spikes1')
medidas = [0.05, 0.05, 0.05]
# bulk:
# muestra = Muestra(volumen, medidas=medidas, geometria='fdas')
muestra = Muestra(volumen, medidas=medidas, geometria='spikes', ancho=3e-3, p=0.2)


#%% CREACION DEL OBJETO DELTA--------------------------------------------------
delta = Delta(muestra)

#%% GRAFICOS-------------------------------------------------------------------
gr = Graficador(muestra, delta)

# slice en x central
gr.mapa(dim=2, corte=0.45, completo=True)


