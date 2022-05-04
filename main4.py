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

#######################################################################
# EN ESTE MAIN COMPARO LAS 4 GEOS CON EL BULK PARA 36 CILINDRPOS
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


GEO = 'cilindritos_dist_cte'
geos = ['cilindritos_dist_cte','cilindritos_aleatorios_2','cilindros_p_random','cilindros_p_random2']

espectros_geo = []

for GEO in geos:
   
    muestra = Muestra(volumen, medidas=medidas, geometria=GEO, ancho=16e-3, distancia= 20e-3)
    delta = Delta(muestra)
    superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
    medicion = Medicion(superposicion, volumen_medido='centro')
    ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=254.4)


    espectros_geo.append([ppmAxis,spec])
    
    
#Descomprimo la lista en los dos espectros
espectro_1 = espectros_geo[0] 
espectro_2 = espectros_geo[1] 
espectro_3 = espectros_geo[2]
espectro_4 = espectros_geo[3]

muestra = Muestra(volumen, medidas=medidas, geometria = 'bulk')
delta = Delta(muestra)
superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
medicion = Medicion(superposicion, volumen_medido='centro')
ppmAxis_bulk, spec_bulk = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=254.4)



#%%


#Los grafico en la misma figura para compararlos
plt.figure(50)
ax = plt.subplot(111)
ax.plot(espectro_1[0],espectro_1[1],linestyle='-', marker='.',linewidth=2,color='#1f77b4', label=' Cil rectos')
ax.plot(espectro_2[0],espectro_2[1],linestyle='-', marker='.',linewidth=2,color='#ff7f0e', label=' cil inclinados a d fija')
ax.plot(espectro_3[0],espectro_3[1],linestyle='-', marker='.',linewidth=2,color='#2ca02c', label=' cil inclinados a d random')
ax.plot(espectro_4[0],espectro_4[1],linestyle='-', marker='.',linewidth=2,color='#d62728', label=' cil más inclinaciones')
ax.plot(ppmAxis_bulk,spec_bulk,'-',linewidth=2, color='#b6b8b6' , label=' bulk')
plt.xlim(left=350,right=150)
plt.xlabel('[ppm]')
plt.ylabel(' ')
ax.legend()



elapsed = (time.time() - t0)/60
print('---  tiempo: {:.2f} min'.format(elapsed))