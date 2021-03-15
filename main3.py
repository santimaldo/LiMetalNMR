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

#muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2', ancho=16e-3, distancia=20e-3)
#muestra = Muestra(volumen, medidas=medidas, geometria='porcentaje_palos',ancho=10e-3, porcentaje=50) # para 'porcentaje_palos'
#%% CREACION DEL OBJETO DELTA--------------------------------------------------
# delta es la perturbacion de campo magnetico
#delta = Delta(muestra)


#%%
# El primer bloque de este código va a mostrar la diferencia entre espectros 
# según la geometría utilizada, las cuales inicialmente seran los cilindros 
# derechos vs los inclinados. 

espectros_geo = []
geo='cilindritos_dist_cte'
lista_geometrias = ['cilindritos_dist_cte','cilindritos_aleatorios_2']

for geo in lista_geometrias:
    
    muestra = Muestra(volumen, medidas=medidas, geometria = geo, ancho=16e-3, distancia=20e-3)
    delta = Delta(muestra)
    superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
    medicion = Medicion(superposicion, volumen_medido='centro')
    ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


    espectros_geo.append([ppmAxis,spec])
 
#Armo el espectro del bulk y lo agrego a la lista
muestra = Muestra(volumen, medidas=medidas, geometria = 'bulk')
delta = Delta(muestra)
superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
medicion = Medicion(superposicion, volumen_medido='centro')
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

espectros_geo.append([ppmAxis,spec])

#Descomprimo la lista en los dos espectros
espectro_geo_cc = espectros_geo[0] #cc= cilindritos a distancia constante
espectro_geo_ca2 = espectros_geo[1] #ca2= cilindritos aleatorios 2
espectro_geo_bulk = espectros_geo[2]

#Los grafico en la misma figura para compararlos
plt.figure(10)
ax = plt.subplot(111)
ax.plot(espectro_geo_cc[0],espectro_geo_cc[1],'-',linewidth=2, label=' Geometría: cilindros rectos')
ax.plot(espectro_geo_ca2[0],espectro_geo_ca2[1],'-',linewidth=2, label=' Geometría: cilindros aleatorios')
ax.plot(espectro_geo_bulk[0],espectro_geo_bulk[1],'-',linewidth=2, color='#b6b8b6' , label=' bulk')
plt.xlim(left=350, right=150)
plt.xlabel('[ppm]')
plt.ylabel(' ')
plt.title('Espectros para las distintas geometrías (c36)') #c36 es la abreviación de 36 cilindros
ax.legend()


#%%
#En este bloque voy a comparar un espectro producto de una misma geometría 
#para cantidades distintas de cilindros. Primero vamos con la geo cc

espectros_d = []
dist=20e-3
distancias = [20e-3,30e-3,45e-3,74e-3,164e-3]



for dist in distancias:
    muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_dist_cte', ancho=16e-3, distancia= dist)
    delta = Delta(muestra)
    superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
    medicion = Medicion(superposicion, volumen_medido='centro')
    ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


    espectros_d.append([ppmAxis,spec])
    
#Armo el espectro del bulk y lo agrego a la lista
muestra = Muestra(volumen, medidas=medidas, geometria = 'bulk')
delta = Delta(muestra)
superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
medicion = Medicion(superposicion, volumen_medido='centro')
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

espectros_d.append([ppmAxis,spec])


#Descomprimo la lista en los dos espectros
espectro_d_d1 = espectros_d[0] 
espectro_d_d2 = espectros_d[1] 
espectro_d_d3 = espectros_d[2]
espectro_d_d4 = espectros_d[3]
espectro_d_d5 = espectros_d[4]
espectro_d_d0 = espectros_d[5]

#Los grafico en la misma figura para compararlos
plt.figure(30)
ax = plt.subplot(111)
ax.plot(espectro_d_d1[0],espectro_d_d1[1],'-',linewidth=2, label=' #cilindros = 36')
ax.plot(espectro_d_d2[0],espectro_d_d2[1],'-',linewidth=2, label=' #cilindros = 25')
ax.plot(espectro_d_d3[0],espectro_d_d3[1],'-',linewidth=2, label=' #cilindros = 16')
ax.plot(espectro_d_d4[0],espectro_d_d4[1],'-',linewidth=2, label=' #cilindros = 9')
ax.plot(espectro_d_d5[0],espectro_d_d5[1],'-',linewidth=2, label=' #cilindros = 4')
ax.plot(espectro_d_d0[0],espectro_d_d0[1],'-',linewidth=2, color='#b6b8b6' , label=' bulk')
plt.xlim(left=350, right=150)
plt.xlabel('[ppm]')
plt.ylabel(' ')
plt.title('Espectros para distintas cantidades de cilindros en geo cc')
ax.legend()   
    
#%%
#EXPORTACIÓN DE DATOS 
#Exporto los arrays para abrirlos en el origin, deconvolucionarlos y analizar 
#el desplazamiento de máximos en función de la cantidad de cilindros 
#La notación es "datos_d4" corresponde a los datos de los cilindros con distancia 
#tq tenemos 4 en el lado, osea que en total tenemos 16 cilindros.
#Generalizando "datos_dn" corresponde a la geo con nxn cilindros.

datos_d2 = np.array([espectro_d_d5[0],np.real(espectro_d_d5[1])]).T
np.savetxt('datos_d2_cc.txt',datos_d2)

datos_d3 = np.array([espectro_d_d4[0],np.real(espectro_d_d4[1])]).T
np.savetxt('datos_d3_cc.txt',datos_d3)

datos_d4 = np.array([espectro_d_d3[0],np.real(espectro_d_d3[1])]).T
np.savetxt('datos_d4_cc.txt',datos_d4) 
 
datos_d5 = np.array([espectro_d_d2[0],np.real(espectro_d_d2[1])]).T
np.savetxt('datos_d5_cc.txt',datos_d5)

datos_d6 = np.array([espectro_d_d1[0],np.real(espectro_d_d1[1])]).T
np.savetxt('datos_d6_cc.txt',datos_d6)
#%%
#En este bloque voy a comparar un espectro producto de una misma geometría 
#para cantidades distintas de cilindros. Vamos con la geo ca2

espectros_d = []
dist=20e-3
distancias = [20e-3,30e-3,45e-3,74e-3,164e-3]



for dist in distancias:
    muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2', ancho=16e-3, distancia= dist)
    delta = Delta(muestra)
    superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
    medicion = Medicion(superposicion, volumen_medido='centro')
    ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


    espectros_d.append([ppmAxis,spec])

#Armo el espectro del bulk y lo agrego a la lista
muestra = Muestra(volumen, medidas=medidas, geometria = 'bulk')
delta = Delta(muestra)
superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
medicion = Medicion(superposicion, volumen_medido='centro')
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

espectros_d.append([ppmAxis,spec])
    
#Descomprimo la lista en los dos espectros
espectro_d_d1 = espectros_d[0] 
espectro_d_d2 = espectros_d[1] 
espectro_d_d3 = espectros_d[2]
espectro_d_d4 = espectros_d[3]
espectro_d_d5 = espectros_d[4]
espectro_d_d0 = espectros_d[5]

#Los grafico en la misma figura para compararlos
plt.figure(40)
ax = plt.subplot(111)
ax.plot(espectro_d_d1[0],espectro_d_d1[1],'-',linewidth=2, label=' #cilindros = 36')
ax.plot(espectro_d_d2[0],espectro_d_d2[1],'-',linewidth=2, label=' #cilindros = 25')
ax.plot(espectro_d_d3[0],espectro_d_d3[1],'-',linewidth=2, label=' #cilindros = 16')
ax.plot(espectro_d_d4[0],espectro_d_d4[1],'-',linewidth=2, label=' #cilindros = 9')
ax.plot(espectro_d_d5[0],espectro_d_d5[1],'-',linewidth=2, label=' #cilindros = 4')
ax.plot(espectro_d_d0[0],espectro_d_d0[1],'-',linewidth=2, color='#b6b8b6' , label=' bulk')
plt.xlim(left=350, right=150)
plt.xlabel('[ppm]')
plt.ylabel(' ')
plt.title('Espectros para distintas cantidades de cilindros en geo ca2')
ax.legend()   

#%%
#EXPORTACIÓN DE DATOS 
#Exporto los arrays para abrirlos en el origin, deconvolucionarlos y analizar 
#el desplazamiento de máximos en función de la cantidad de cilindros 
#La notación es "datos_d4" corresponde a los datos de los cilindros con distancia 
#tq tenemos 4 en el lado, osea que en total tenemos 16 cilindros.
#Generalizando "datos_dn" corresponde a la geo con nxn cilindros.

datos_d2 = np.array([espectro_d_d5[0],np.real(espectro_d_d5[1])]).T
np.savetxt('datos_d2_ca2.txt',datos_d2)

datos_d3 = np.array([espectro_d_d4[0],np.real(espectro_d_d4[1])]).T
np.savetxt('datos_d3_ca2.txt',datos_d3)

datos_d4 = np.array([espectro_d_d3[0],np.real(espectro_d_d3[1])]).T
np.savetxt('datos_d4_ca2.txt',datos_d4) 
 
datos_d5 = np.array([espectro_d_d2[0],np.real(espectro_d_d2[1])]).T
np.savetxt('datos_d5_ca2.txt',datos_d5)

datos_d6 = np.array([espectro_d_d1[0],np.real(espectro_d_d1[1])]).T
np.savetxt('datos_d6_ca2.txt',datos_d6)

#%%
#Sección de gráficos del desplazamiento de los maximos segun la cantidad de 
#cdilindros

x = [4,9,16,25,36]
f = [267.29-249.5,266.95-249.5,265.608-249.5,266.594-249.5,266.446-249.5]  #geo ca2
g = [271.57-249.5,271.602-249.5,271.459-249.5,271.130-249.5,270.639-249.5] #geo cc


plt.figure(41)
ax = plt.subplot(111)
ax.plot(x,f,marker='o', markersize=8, label=' Geometría ca2')
ax.plot(x,g,marker='o', markersize=8, label=' Geometría cc')
plt.xlabel('Cantidad de cilindros')
plt.ylabel('Desplazamiento [ppm]')
plt.title('Desplazamiento de los máximos respecto al máximo del bulk')
ax.legend()


#%%
#En esta parte del código voy a graficar el espectro de la geo ca2 para 9 cilindros
#y luego promediarlo en un espectro final 

espectros_c9 = []
i=1
rango = [1,2,3,4,5]



for i in rango:
    muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2', ancho=16e-3, distancia= 74e-3)
    delta = Delta(muestra)
    superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
    medicion = Medicion(superposicion, volumen_medido='centro')
    ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


    espectros_c9.append([ppmAxis,spec])
    
#Descomprimo la lista en los dos espectros
espectro_1 = espectros_c9[0] 
espectro_2 = espectros_c9[1] 
espectro_3 = espectros_c9[2]
espectro_4 = espectros_c9[3]
espectro_5 = espectros_c9[4]

#Los grafico en la misma figura para compararlos
plt.figure(50)
ax = plt.subplot(111)
ax.plot(espectro_1[0],espectro_1[1],'-',linewidth=2, label=' 1')
ax.plot(espectro_2[0],espectro_2[1],'-',linewidth=2, label=' 2')
ax.plot(espectro_3[0],espectro_3[1],'-',linewidth=2, label=' 3')
ax.plot(espectro_4[0],espectro_4[1],'-',linewidth=2, label=' 4')
ax.plot(espectro_5[0],espectro_5[1],'-',linewidth=2, label=' 5')
plt.xlim(left=350, right=150)
plt.xlabel('[ppm]')
plt.ylabel(' ')
plt.title('Distintas iteraciones para el espectro de 9 cilindos geo ca2')
ax.legend()   


#AHORA los promedio en un único espectro, promediando los arrays en cada coordenada

ppmAxis_medio = np.array([espectro_1[0],espectro_2[0],espectro_3[0],espectro_4[0],espectro_5[0]])
spec_medio    = np.array([espectro_1[1],espectro_2[1],espectro_3[1],espectro_4[1],espectro_5[1]])

prom_ppmAxis= np.mean(ppmAxis_medio,axis=0)

prom_spec = np.mean(spec_medio,axis=0) 

plt.figure(51)
ax = plt.subplot(111)
ax.plot(prom_ppmAxis,prom_spec,'-',linewidth=2, label= 'Espectro 9c')
plt.xlim(left=350, right=150)
plt.xlabel('[ppm]')
plt.ylabel('')
plt.title('Promedio espectro 9c para 5 iteraciones de geo ca2')
ax.legend()


#%% GRAFICOS-------------------------------------------------------------------
#gr = Graficador(muestra, delta)
# slice en x central
#gr.mapa()
#gr.mapa(dim=2, corte=0.5, completo=True)
#gr.mapa(dim=0, corte=0.6, completo=True)
#gr.mapa(dim=0, corte=0.5, completo=False)
