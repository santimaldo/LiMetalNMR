#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""
#stop

#EN ESTE MAIN 3 HAGOS LA COMPARACIÓN DE ESPECTROS SEGÚN SU GEOMETRÍA Y SEGÚN LOS
#LOS PARÁMETROS DE SU GEOMETRÍA. 


import numpy as np
import matplotlib.pyplot as plt
from Modules.SimulationVolume import *
from Modules.Muestra import *
from Modules.Delta import *
from Modules.Superposicion import *
from Modules.Graficador import *
from Modules.Medicion import *
import time

def posicion_del_max(spec,ppmAxis):
    max_spec = np.max(np.real(spec))
    where_max = np.where(np.real(spec) == max_spec)
    pos = ppmAxis[where_max[0][0]]
    return pos

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
N = [256,1024,1024] 
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
medidas = [0.128,0.512,0.512]

#muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2', ancho=16e-3, distancia=20e-3)
#muestra = Muestra(volumen, medidas=medidas, geometria='porcentaje_palos',ancho=10e-3, porcentaje=50) # para 'porcentaje_palos'
#%% CREACION DEL OBJETO DELTA--------------------------------------------------
# delta es la perturbacion de campo magnetico
#delta = Delta(muestra)


# #%%
# # El primer bloque de este código va a mostrar la diferencia entre espectros 
# # según la geometría utilizada, las cuales inicialmente seran los cilindros 
# # derechos vs los inclinados. 

# espectros_geo = []
# geo='cilindritos_dist_cte'
# lista_geometrias = ['cilindritos_dist_cte','cilindritos_aleatorios_2']

# for geo in lista_geometrias:
    
#     muestra = Muestra(volumen, medidas=medidas, geometria = geo, ancho=16e-3, distancia=20e-3)
#     delta = Delta(muestra)
#     superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
#     medicion = Medicion(superposicion, volumen_medido='centro')
#     ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


#     espectros_geo.append([ppmAxis,spec])
 
# #Armo el espectro del bulk y lo agrego a la lista
# muestra = Muestra(volumen, medidas=medidas, geometria = 'bulk')
# delta = Delta(muestra)
# superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
# medicion = Medicion(superposicion, volumen_medido='centro')
# ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

# espectros_geo.append([ppmAxis,spec])

# #Descomprimo la lista en los dos espectros
# espectro_geo_cc = espectros_geo[0] #cc= cilindritos a distancia constante
# espectro_geo_ca2 = espectros_geo[1] #ca2= cilindritos aleatorios 2
# espectro_geo_bulk = espectros_geo[2]

# #Los grafico en la misma figura para compararlos
# plt.figure(10)
# ax = plt.subplot(111)
# ax.plot(espectro_geo_cc[0],espectro_geo_cc[1],'-',linewidth=2, label=' Geometría: cilindros rectos')
# ax.plot(espectro_geo_ca2[0],espectro_geo_ca2[1],'-',linewidth=2, label=' Geometría: cilindros aleatorios')
# ax.plot(espectro_geo_bulk[0],espectro_geo_bulk[1],'-',linewidth=2, color='#b6b8b6' , label=' bulk')
# plt.xlim(left=350, right=150)
# plt.xlabel('[ppm]')
# plt.ylabel(' ')
# plt.title('Espectros para las distintas geometrías (c36)') #c36 es la abreviación de 36 cilindros
# ax.legend()


# #%%
# #En este bloque voy a comparar un espectro producto de una misma geometría 
# #para cantidades distintas de cilindros. Primero vamos con la geo cc

# espectros_d = []
# dist=20e-3
# distancias = [20e-3,30e-3,45e-3,74e-3,164e-3]



# for dist in distancias:
#     muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_dist_cte', ancho=16e-3, distancia= dist)
#     delta = Delta(muestra)
#     superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
#     medicion = Medicion(superposicion, volumen_medido='centro')
#     ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


#     espectros_d.append([ppmAxis,spec])
    
# #Armo el espectro del bulk y lo agrego a la lista
# muestra = Muestra(volumen, medidas=medidas, geometria = 'bulk')
# delta = Delta(muestra)
# superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
# medicion = Medicion(superposicion, volumen_medido='centro')
# ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

# espectros_d.append([ppmAxis,spec])


# #Descomprimo la lista en los dos espectros
# espectro_d_d1 = espectros_d[0] 
# espectro_d_d2 = espectros_d[1] 
# espectro_d_d3 = espectros_d[2]
# espectro_d_d4 = espectros_d[3]
# espectro_d_d5 = espectros_d[4]
# espectro_d_d0 = espectros_d[5]

# #Los grafico en la misma figura para compararlos
# plt.figure(30)
# ax = plt.subplot(111)
# ax.plot(espectro_d_d1[0],espectro_d_d1[1],'-',linewidth=2, label=' #cilindros = 36')
# ax.plot(espectro_d_d2[0],espectro_d_d2[1],'-',linewidth=2, label=' #cilindros = 25')
# ax.plot(espectro_d_d3[0],espectro_d_d3[1],'-',linewidth=2, label=' #cilindros = 16')
# ax.plot(espectro_d_d4[0],espectro_d_d4[1],'-',linewidth=2, label=' #cilindros = 9')
# ax.plot(espectro_d_d5[0],espectro_d_d5[1],'-',linewidth=2, label=' #cilindros = 4')
# ax.plot(espectro_d_d0[0],espectro_d_d0[1],'-',linewidth=2, color='#b6b8b6' , label=' bulk')
# plt.xlim(left=350, right=150)
# plt.xlabel('[ppm]')
# plt.ylabel(' ')
# plt.title('Espectros para distintas cantidades de cilindros en geo cc')
# ax.legend()   
    
# #%%
# #EXPORTACIÓN DE DATOS 
# #Exporto los arrays para abrirlos en el origin, deconvolucionarlos y analizar 
# #el desplazamiento de máximos en función de la cantidad de cilindros 
# #La notación es "datos_d4" corresponde a los datos de los cilindros con distancia 
# #tq tenemos 4 en el lado, osea que en total tenemos 16 cilindros.
# #Generalizando "datos_dn" corresponde a la geo con nxn cilindros.

# datos_d2 = np.array([espectro_d_d5[0],np.real(espectro_d_d5[1])]).T
# np.savetxt('datos_d2_cc.txt',datos_d2)

# datos_d3 = np.array([espectro_d_d4[0],np.real(espectro_d_d4[1])]).T
# np.savetxt('datos_d3_cc.txt',datos_d3)

# datos_d4 = np.array([espectro_d_d3[0],np.real(espectro_d_d3[1])]).T
# np.savetxt('datos_d4_cc.txt',datos_d4) 
 
# datos_d5 = np.array([espectro_d_d2[0],np.real(espectro_d_d2[1])]).T
# np.savetxt('datos_d5_cc.txt',datos_d5)

# datos_d6 = np.array([espectro_d_d1[0],np.real(espectro_d_d1[1])]).T
# np.savetxt('datos_d6_cc.txt',datos_d6)
# #%%
# #En este bloque voy a comparar un espectro producto de una misma geometría 
# #para cantidades distintas de cilindros. Vamos con la geo ca2

# espectros_d = []
# dist=20e-3
# distancias = [20e-3,30e-3,45e-3,74e-3,164e-3]



# for dist in distancias:
#     muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2', ancho=16e-3, distancia= dist)
#     delta = Delta(muestra)
#     superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
#     medicion = Medicion(superposicion, volumen_medido='centro')
#     ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


#     espectros_d.append([ppmAxis,spec])

# #Armo el espectro del bulk y lo agrego a la lista
# muestra = Muestra(volumen, medidas=medidas, geometria = 'bulk')
# delta = Delta(muestra)
# superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
# medicion = Medicion(superposicion, volumen_medido='centro')
# ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

# espectros_d.append([ppmAxis,spec])
    
# #Descomprimo la lista en los dos espectros
# espectro_d_d1 = espectros_d[0] 
# espectro_d_d2 = espectros_d[1] 
# espectro_d_d3 = espectros_d[2]
# espectro_d_d4 = espectros_d[3]
# espectro_d_d5 = espectros_d[4]
# espectro_d_d0 = espectros_d[5]

# #Los grafico en la misma figura para compararlos
# plt.figure(40)
# ax = plt.subplot(111)
# ax.plot(espectro_d_d1[0],espectro_d_d1[1],'-',linewidth=2, label=' #cilindros = 36')
# ax.plot(espectro_d_d2[0],espectro_d_d2[1],'-',linewidth=2, label=' #cilindros = 25')
# ax.plot(espectro_d_d3[0],espectro_d_d3[1],'-',linewidth=2, label=' #cilindros = 16')
# ax.plot(espectro_d_d4[0],espectro_d_d4[1],'-',linewidth=2, label=' #cilindros = 9')
# ax.plot(espectro_d_d5[0],espectro_d_d5[1],'-',linewidth=2, label=' #cilindros = 4')
# ax.plot(espectro_d_d0[0],espectro_d_d0[1],'-',linewidth=2, color='#b6b8b6' , label=' bulk')
# plt.xlim(left=350, right=150)
# plt.xlabel('[ppm]')
# plt.ylabel(' ')
# plt.title('Espectros para distintas cantidades de cilindros en geo ca2')
# ax.legend()   

# #%%
# #EXPORTACIÓN DE DATOS 
# #Exporto los arrays para abrirlos en el origin, deconvolucionarlos y analizar 
# #el desplazamiento de máximos en función de la cantidad de cilindros 
# #La notación es "datos_d4" corresponde a los datos de los cilindros con distancia 
# #tq tenemos 4 en el lado, osea que en total tenemos 16 cilindros.
# #Generalizando "datos_dn" corresponde a la geo con nxn cilindros.

# datos_d2 = np.array([espectro_d_d5[0],np.real(espectro_d_d5[1])]).T
# np.savetxt('datos_d2_ca2.txt',datos_d2)

# datos_d3 = np.array([espectro_d_d4[0],np.real(espectro_d_d4[1])]).T
# np.savetxt('datos_d3_ca2.txt',datos_d3)

# datos_d4 = np.array([espectro_d_d3[0],np.real(espectro_d_d3[1])]).T
# np.savetxt('datos_d4_ca2.txt',datos_d4) 
 
# datos_d5 = np.array([espectro_d_d2[0],np.real(espectro_d_d2[1])]).T
# np.savetxt('datos_d5_ca2.txt',datos_d5)

# datos_d6 = np.array([espectro_d_d1[0],np.real(espectro_d_d1[1])]).T
# np.savetxt('datos_d6_ca2.txt',datos_d6)

# #%%
# #Sección de gráficos del desplazamiento de los maximos segun la cantidad de 
# #cdilindros

# x = [4,9,16,25,36]
# f = [267.29-249.5,266.95-249.5,265.608-249.5,266.594-249.5,266.446-249.5]  #geo ca2
# g = [271.57-249.5,271.602-249.5,271.459-249.5,271.130-249.5,270.639-249.5] #geo cc


# plt.figure(41)
# ax = plt.subplot(111)
# ax.plot(x,f,marker='o', markersize=8, label=' Geometría ca2')
# ax.plot(x,g,marker='o', markersize=8, label=' Geometría cc')
# plt.xlabel('Cantidad de cilindros')
# plt.ylabel('Desplazamiento [ppm]')
# plt.title('Desplazamiento de los máximos respecto al máximo del bulk')
# ax.legend()


# #%%
# #En esta parte del código voy a graficar el espectro de la geo ca2 para 9 cilindros
# #y luego promediarlo en un espectro final 


# espectros_c9 = []
# i=1
# rango = [1,2,3,4,5,6,7,8,9,10]



# for i in rango:
#     muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2', ancho=16e-3, distancia= 74e-3)
#     delta = Delta(muestra)
#     superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
#     medicion = Medicion(superposicion, volumen_medido='centro')
#     ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


#     espectros_c9.append([ppmAxis,spec])
    
# #Descomprimo la lista en los dos espectros
# espectro_1 = espectros_c9[0] 
# espectro_2 = espectros_c9[1] 
# espectro_3 = espectros_c9[2]
# espectro_4 = espectros_c9[3]
# espectro_5 = espectros_c9[4]
# espectro_6 = espectros_c9[5]
# espectro_7 = espectros_c9[6]
# espectro_8 = espectros_c9[7]
# espectro_9 = espectros_c9[8]
# espectro_10 = espectros_c9[9]

# #Los grafico en la misma figura para compararlos
# plt.figure(50)
# ax = plt.subplot(111)
# ax.plot(espectro_1[0],espectro_1[1],'-',linewidth=2, label=' 1')
# ax.plot(espectro_2[0],espectro_2[1],'-',linewidth=2, label=' 2')
# ax.plot(espectro_3[0],espectro_3[1],'-',linewidth=2, label=' 3')
# ax.plot(espectro_4[0],espectro_4[1],'-',linewidth=2, label=' 4')
# ax.plot(espectro_5[0],espectro_5[1],'-',linewidth=2, label=' 5')
# ax.plot(espectro_6[0],espectro_6[1],'-',linewidth=2, label=' 6')
# ax.plot(espectro_7[0],espectro_7[1],'-',linewidth=2, label=' 7')
# ax.plot(espectro_8[0],espectro_8[1],'-',linewidth=2, label=' 8')
# ax.plot(espectro_9[0],espectro_9[1],'-',linewidth=2, label=' 9')
# ax.plot(espectro_10[0],espectro_10[1],'-',linewidth=2, label=' 10')
# plt.xlim(left=350, right=150)
# plt.xlabel('[ppm]')
# plt.ylabel(' ')
# plt.title(' ')
# ax.legend()   

# #%%
# #AHORA los promedio en un único espectro, promediando los arrays en cada coordenada

# ppmAxis_medio = np.array([espectro_1[0],espectro_2[0],espectro_3[0],espectro_4[0],espectro_5[0],espectro_6[0],espectro_7[0],espectro_8[0],espectro_9[0],espectro_10[0]])
# spec_medio    = np.array([espectro_1[1],espectro_2[1],espectro_3[1],espectro_4[1],espectro_5[1],espectro_6[1],espectro_7[1],espectro_8[1],espectro_9[1],espectro_10[1]])

# prom_ppmAxis= np.mean(ppmAxis_medio,axis=0)

# prom_spec = np.mean(spec_medio,axis=0) 

# plt.figure(51)
# ax = plt.subplot(111)
# ax.plot(prom_ppmAxis,prom_spec,'-',linewidth=2, label= 'Espectro promedio')
# plt.xlim(left=350, right=150)
# plt.xlabel('[ppm]')
# plt.ylabel('')
# plt.title(' ')
# ax.legend()

#%%
#En este bloque veo el comportamiento según el radio interno utilizado para 36 cilindros con los 10 promedios


# RADIO = '000'
# radios = ['000','300','450','580']

# espectros_R = []

# for RADIO in radios:
#     espectros_prom = []
#     i=1
#     rango = [1,2,3,4,5,6,7,8,9,10]

#     for i in rango:
#         muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2', ancho=16e-3, distancia= 20e-3)
#         delta = Delta(muestra)
#         superposicion = Superposicion(muestra, delta, radio = RADIO, z0=84e-3)
#         medicion = Medicion(superposicion, volumen_medido='centro')
#         ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


#         espectros_prom.append([ppmAxis,spec])
    
    
#     #Descomprimo la lista en los dos espectros
#     espectro_1 = espectros_prom[0] 
#     espectro_2 = espectros_prom[1] 
#     espectro_3 = espectros_prom[2]
#     espectro_4 = espectros_prom[3]
#     espectro_5 = espectros_prom[4]
#     espectro_6 = espectros_prom[5]
#     espectro_7 = espectros_prom[6]
#     espectro_8 = espectros_prom[7]
#     espectro_9 = espectros_prom[8]
#     espectro_10 = espectros_prom[9]
        
#     #Lo promedio en un único espectro
#     ppmAxis_medio = np.array([espectro_1[0],espectro_2[0],espectro_3[0],espectro_4[0],espectro_5[0],espectro_6[0],espectro_7[0],espectro_8[0],espectro_9[0],espectro_10[0]])
#     spec_medio    = np.array([espectro_1[1],espectro_2[1],espectro_3[1],espectro_4[1],espectro_5[1],espectro_6[1],espectro_7[1],espectro_8[1],espectro_9[1],espectro_10[1]])

#     prom_ppmAxis= np.mean(ppmAxis_medio,axis=0)

#     prom_spec = np.mean(spec_medio,axis=0) 

#     espectros_R.append([prom_ppmAxis,prom_spec])
    
    
# #Descomprimo los espectros promedios para cada radio interno R
# espectro_R0 = espectros_R[0]
# espectro_R3 = espectros_R[1]
# espectro_R4 = espectros_R[2]
# espectro_R5 = espectros_R[3]

#%%

# #Armo el espectro del bulk y lo agrego a al gráfico

# muestra = Muestra(volumen, medidas=medidas, geometria = 'bulk')
# delta = Delta(muestra)
# superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
# medicion = Medicion(superposicion, volumen_medido='centro')
# ppmAxis_bulk, spec_bulk = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

# #Los grafico en la misma figura para compararlos
# plt.figure(52)
# ax = plt.subplot(111)
# ax.plot(espectro_R0[0],espectro_R0[1],linestyle='-', marker='.',linewidth=2,color='#1f77b4', label=' R = 0mm')
# ax.plot(espectro_R3[0],espectro_R3[1],linestyle='-', marker='.',linewidth=2,color='#ff7f0e', label=' R = 3mm')
# ax.plot(espectro_R4[0],espectro_R4[1],linestyle='-', marker='.',linewidth=2,color='#2ca02c', label=' R = 4,5mm')
# ax.plot(espectro_R5[0],espectro_R5[1],linestyle='-', marker='.',linewidth=2,color='#d62728', label=' R = 5,8mm')
# ax.plot(ppmAxis_bulk,spec_bulk,'-',linewidth=2, color='#b6b8b6' , label=' bulk')
# plt.xlim(left=350,right=150)
# plt.xlabel('[ppm]')
# plt.ylabel(' ')
# ax.legend()

#%%
#En este bloque hago lo mismo que en el anterior pero ahora para un radio fijo R=0 vario el nro de cilindros (lo controlo con la distancia)
dist= 20e-3
distancias= [20e-3,30e-3,45e-3,74e-3,164e-3,220e-3,480e-3]
espectros_d = []
lista_medias = []
lista_desviaciones = []

lista_medias_total = []      # todo lo que diga _total es porque adquiere senal de toda la muestra
lista_desviaciones_total = []


#t = time.time()
#elapsed = time.time() - t  
for dist in distancias:
    espectros_prom = 0
    espectros_prom_mic = 0
    espectros_prom_bulk = 0
    
    espectros_prom_total = 0
    espectros_prom_mic_total = 0
    espectros_prom_bulk_total = 0
    
    ppmAxis_prom
    
    espectros_max = []
    espectros_max_total = []
    i=1

    for i in range(1,11):  
        muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2', ancho=16e-3, distancia= dist)
        delta = Delta(muestra)
        superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
        
        # senal total
        medicion = Medicion(superposicion, volumen_medido='microestructuras')
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=False, KS=258)
        espectros_prom_mic += np.real(spec)
        ppmAxis_prom+=ppmAxis
        x_max = posicion_del_max(spec, ppmAxis)
        espectros_max_total.append(x_max)
        
        medicion = Medicion(superposicion, volumen_medido='bulk')
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=False, KS=258)
        espectros_prom_bulk_total += np.real(spec)
        ppmAxis_prom+=ppmAxis
        x_max = posicion_del_max(spec, ppmAxis)
        espectros_max.append(x_max)
                
        medicion = Medicion(superposicion, volumen_medido='')
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=False, KS=258)
        espectros_prom_total += np.real(spec)    
        ppmAxis_prom+=ppmAxis
        
        
        # senal centro
        medicion = Medicion(superposicion, volumen_medido='centro-microestructuras')
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=False, KS=258)
        espectros_prom_mic += np.real(spec)
        ppmAxis_prom+=ppmAxis
        x_max = posicion_del_max(spec, ppmAxis)
        espectros_max.append(x_max)
        
        medicion = Medicion(superposicion, volumen_medido='centro-bulk')
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=False, KS=258)
        espectros_prom_bulk += np.real(spec)
        ppmAxis_prom+=ppmAxis
        x_max = posicion_del_max(spec, ppmAxis)
        espectros_max.append(x_max)
                
        medicion = Medicion(superposicion, volumen_medido='centro')
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=False, KS=258)
        espectros_prom += np.real(spec)    
        ppmAxis_prom+=ppmAxis
    
    datos = np.array([ppmAxis_prom/6.0, espectros_prom, espectros_prom_mic, espectros_prom_bulk, espectros_prom_total, espectros_prom_mic_total, espectros_prom_bulk_total]).T
    np.savetxt('./espectros_distancia_{}_um.dat'.format(dist*1000), datos)
    
    x_bulk = 249.5
    desplazamiento = np.array(espectros_max) - x_bulk
    
    desplazamiento_medio = np.mean(desplazamiento)
    lista_medias.append(desplazamiento_medio)
    desviacion_desplazamiento = np.std(desplazamiento)
    lista_desviaciones.append(desviacion_desplazamiento)
    print('desplazamiento medio = ',desplazamiento_medio)
    print('desviacion_desplazamiento = ', desviacion_desplazamiento)
    
    
    desplazamiento_total = np.array(espectros_max_total) - x_bulk
    desplazamiento_medio_total = np.mean(desplazamiento_total)
    lista_medias_total.append(desplazamiento_medio_total)
    desviacion_desplazamiento_total = np.std(desplazamiento_total)
    lista_desviaciones_total.append(desviacion_desplazamiento_total)
    print('desplazamiento medio_total = ',desplazamiento_medio_total)
    print('desviacion_desplazamiento_total = ', desviacion_desplazamiento_total)
    
    
datos = np.array([distancias, lista_medias, lista_desviaciones, lista_medias, lista_esviaciones_total]).T
np.savetxt('./corrimiento_vs_distancia.dat'.format(dist*1000), datos)
#%%
# #Armo el espectro del bulk y lo agrego a al gráfico

