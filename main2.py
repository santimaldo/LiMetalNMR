#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""
#stop

#EN ESTE MAIN 2 HAGOS LOS GRÁFICOS DE LOS ESPECTROS OBTENIDOS. 


import numpy as np
import matplotlib.pyplot as plt
from Modules.SimulationVolume import *
from Modules.Muestra import *
from Modules.Delta import *
from Modules.Superposicion import *
from Modules.Graficador import *
from Modules.Medicion import *
import time

#t = time.time()
#elapsed = time.time() - t  
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

muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2', ancho=16e-3, distancia=20e-3)
#muestra = Muestra(volumen, medidas=medidas, geometria='porcentaje_palos',ancho=10e-3, porcentaje=50) # para 'porcentaje_palos'
#%% CREACION DEL OBJETO DELTA--------------------------------------------------
# delta es la perturbacion de campo magnetico
delta = Delta(muestra)
#<<<<<<< HEAD
#<<<<<<< Updated upstream

#%%

#Quiero superponer el espectro de la tita de heavyside con la del radio central en el electrodo

espectros_tita = []
superposicion = Superposicion(muestra, delta, z0=84e-3, delta_in=-8.614860948911854166, delta_out=7.349113258713176222)
medicion = Medicion(superposicion, volumen_medido='centro')
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


espectros_tita.append([ppmAxis,spec])

espectros_R = []

superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3) # si pongo 'radio', es porque lee de un perfil
medicion = Medicion(superposicion, volumen_medido='centro')
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

espectros_R.append([ppmAxis,spec])


espectro_tita = espectros_tita[0]
espectro_R = espectros_R[0]

plt.figure(40)
ax = plt.subplot(111)
ax.plot(espectro_tita[0],espectro_tita[1],'-', linewidth=7, label='Función escalón')
ax.plot(espectro_R[0],espectro_R[1],'.',linewidth=1, label=' Perfil en R = 0mm')
plt.xlim(left=350,right=150)
plt.xlabel('[ppm]')
plt.ylabel('Comparación de espectros')
ax.legend()

#%%
#espectros con los perfiles
RADIO = '000'
radios = ['000','300','450','580']
espectros = []

for RADIO in radios:
    # SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK
    #superposicion = Superposicion(muestra, delta, z0=84e-3, delta_in=-8.614860948911854166, delta_out=7.349113258713176222)
    superposicion = Superposicion(muestra, delta, radio = RADIO, z0=84e-3) # si pongo 'radio', es porque lee de un perfil

    #medicion = Medicion(superposicion, volumen_medido='completo')
    medicion = Medicion(superposicion, volumen_medido='centro')
    #>>>>>>> Stashed changes

    ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)
    #ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=1111)
    #datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
    #np.savetxt(path+'h{:d}_ancho{:d}_dens{:d}_SP_k{:.2f}'.format(int(h*1e3), int(ancho*1e3), int(porcentaje), k))

    #ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1  , figure=153)
    #ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1.1, figure=153)
    #ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1.2, figure=153)
    #ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', k=1.3, figure=153)
    espectros.append([ppmAxis, spec])


#Descomprimo los espectros
espectro_R000 = espectros[0]
espectro_R300 = espectros[1]
espectro_R450 = espectros[2]
espectro_R580 = espectros[3]

#Como el ppmAxis es elmismo para todos los espectros, uso el del primero para todos los gráficos
plt.figure(50)
ax = plt.subplot(111)
ax.plot(espectro_R000[0],espectro_R000[1],'-',linewidth=2, label=' Perfil en R = 0 mm')
ax.plot(espectro_R300[0],espectro_R300[1],'-',linewidth=2, label=' Perfil en R = 3 mm')
ax.plot(espectro_R450[0],espectro_R450[1],'-',linewidth=2, label=' Perfil en R = 4.5 mm')
ax.plot(espectro_R580[0],espectro_R580[1],'-',linewidth=2, label=' Perfil en R = 5.8 mm')
plt.xlim(left=350, right=150)
plt.xlabel('[ppm]')
plt.ylabel(' ')
plt.title('Espectro para los distintos perfiles')
ax.legend()

plt.figure(51)
ax = plt.subplot(111)
ax.plot([0,3,4.5,5.8],[0,250.332-249.910,251.168-249.910,253.260-249.910],marker='o', markersize=8, label=' Perfiles')
ax.plot([0,3,4.5,5.8],[0,0,0,0],'-',linewidth=2, label=' Tita de heavyside')
plt.xlabel('Radio [mm]')
plt.ylabel('Desplazamiento absoluto de máximos según el perfil utilizado [ppm]')
plt.title('Posición de los máximos según el radio')
plt.title('Posición de los máximos según el radio')
ax.legend()

plt.figure(53)
ax = plt.subplot(111)
ax.plot([0,3,4.5,5.8],[1563355.7600388995,1564291.2031659614,1568411.8392508423,1632141.8100303358],marker='o', markersize=8, label=' Perfiles')
ax.plot([0,3,4.5,5.8],[1563355.7600388995,1563355.7600388995,1563355.7600388995,1563355.7600388995],'-',linewidth=2, label=' Tita de heavyside')
plt.xlabel('Radio [mm]')
plt.ylabel('Valor del máximo según el perfil utilizado')
plt.title('Valor de los máximos según el radio')
ax.legend()
#%%
#Busco los máximos en cada espectro y donde se encuentran

#La notación será max_000 para el máximo del espectro correspondiente a R=0mm
# y así sucesivamente. La notación para el voxel en el que se encuentra cada
#máximo será where_000 para el correspondiente a R=0mm

max_000 = np.max(np.real(espectro_R000[1]))
print('max_000=',max_000)
where_000 = np.where(espectro_R000 == max_000)
print('where_000=',where_000)

max_300 = np.max(np.real(espectro_R300[1]))
print('max_300=',max_300)
where_300 = np.where(espectro_R300 == max_300)
print('where_300=',where_300) 

max_450 = np.max(np.real(espectro_R450[1]))
print('max_450=',max_450)
where_450 = np.where(espectro_R450 == max_450)
print('where_450=',where_450)

max_580 = np.max(np.real(espectro_R580[1]))
print('max_580=',max_580)
where_580 = np.where(espectro_R580 == max_580)
print('where_580=',where_580)

where_tita = where_000
#El maximo para el espectro de heavyside se encuentra (exactamente) en el mismo lugar 
#que el del espectro para R=0mm


#%% GRAFICOS-------------------------------------------------------------------
#gr = Graficador(muestra, delta)
# slice en x central
#gr.mapa()
#gr.mapa(dim=2, corte=0.5, completo=True)
#gr.mapa(dim=0, corte=0.6, completo=True)
#gr.mapa(dim=0, corte=0.5, completo=False)
