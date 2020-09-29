#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 13:47:27 2020

@author: santi
"""

"""
Es el main, pero que corre varias veces y no hace graficos. Además lo intercalo
con el generador de espectros
"""

import numpy as np
import matplotlib.pyplot as plt
from Muestra import *
from Delta import *
from Superposicion import *
from Graficador import *
from SimulationVolume import *
from Espectro import espectro

path = '/home/santi/CuarenteDoctorado/LiMetal/simulaciones/2020-09-07_distancia_constante/'

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
N = [256,256,256] 
# con estos numeros, Nj*voxelSize_j queda
#    z: 1.536 mm  ; y: 3.84 mm  ; x: 10.24 mm
# utilizo una funcion que dado dos argumentos define el restante. Ya sea N, 
# FOV (field of view) o  voxelSize
volumen = SimulationVolume(voxelSize=voxelSize, N=N)
#volumen = SimulationVolume(FOV=FOV, N=N)
medidas = [0.028,0.088,0.088]

#%%
# ACA VA EL LOOP

distancias = [6, 9, 12, 15]
lados = [3, 6, 9, 12, 15]

distancias = [18, 21]
lados = [3, 6, 9, 12, 15]

for distancia in distancias:
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('++++++++++++++++++++++ distancia:  {} um+++++++++++++++++++++++++++++++'.format(distancia))
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    for lado in lados:
        print('--------------------------------------------------------------')
        print('-------------------- lado:  {}  um--------------------------------'.format(lado))
        print('--------------------------------------------------------------')
        # CREACION DE LA MUESTRA-----------------------------------------------------    
        muestra = Muestra(volumen, medidas=medidas, geometria='distancia_constante', ancho=lado*1e-3, distancia=distancia*1e-3)    
        # CREACION DEL OBJETO DELTA--------------------------------------------------
        delta = Delta(muestra)
        # SUPERPOSICION --------------------------------------------------
        superposicion = Superposicion(muestra, delta)
        # espectros:---------------------------------------------------------------
        # -------------------------------------------------------------------------
        del delta, muestra
        matriz = superposicion.delta_sens # todo
        ppmAxis, spec = espectro(matriz)
        spec_data = np.array([ppmAxis, np.real(spec)]).T
        np.savetxt(path+'dist{}um_lado{}um_spec.dat'.format(distancia, lado), spec_data)
        #
        matriz = superposicion.delta_sens[superposicion.z0:,:,:] # dendritas
        ppmAxis, spec = espectro(matriz)
        spec_data = np.array([ppmAxis, np.real(spec)]).T
        np.savetxt(path+'dist{}um_lado{}um_spec_dend.dat'.format(distancia, lado), spec_data)
        #
        matriz = superposicion.delta_sens[:superposicion.z0,:,:] # bulk
        ppmAxis, spec = espectro(matriz)
        spec_data = np.array([ppmAxis, np.real(spec)]).T
        np.savetxt(path+'dist{}um_lado{}um_spec_bulk.dat'.format(distancia, lado), spec_data)
        del superposicion
        
        
    
    