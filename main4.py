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

#%%
#En este bloque hago lo mismo que en el anterior pero ahora para un radio fijo R=0 vario el nro de cilindros (lo controlo con la distancia)
dist= 20e-3
distancias= [20e-3,30e-3,45e-3,74e-3,164e-3]
distancias= [164e-3,74e-3,45e-3,30e-3,20e-3]

espectros_d = []
lista_medias = []
lista_desviaciones = []

lista_medias_total = []      # todo lo que diga _total es porque adquiere senal de toda la muestra
lista_desviaciones_total = []

cont=0
t0 = time.time()
#elapsed = time.time() - t  
for dist in distancias:
    td = time.time()
    print('===================================================================')
    print('distancia: {} um'.format(dist*1000))
    print('progreso: {}/{}'.format(int(cont), len(distancias)))
    tiempo = time.time() - t0
    try:
      tiempo_estimado = tiempo*len(distancias)/cont 
      tiempo_restante = tiempo_estimado-tiempo
      print('tiempo total estimado: {} min, o bien, {} h'.format(tiempo_estimado/60., tiempo_estimado/3600.))
      print('tiempo restante      : {} min, o bien, {} h'.format(tiempo_restante/60., tiempo_restante/3600.))      
    except:
      pass
    print('-------------------------------------------------------------------')
    espectros_prom = 0
    espectros_prom_mic = 0
    espectros_prom_bulk = 0
    
    espectros_prom_total = 0
    espectros_prom_mic_total = 0
    espectros_prom_bulk_total = 0
    
    ppmAxis_prom = 0
    
    espectros_max = []
    espectros_max_total = []

    for i in range(1,11):  
        ti = time.time()  
        muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2', ancho=16e-3, distancia= dist)
        delta = Delta(muestra)
        superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
        # superposicion = Superposicion(muestra, delta, z0=84e-3)
        
        # senal total
        medicion = Medicion(superposicion, volumen_medido='completo-microestructuras')
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=False, KS=258)
        espectros_prom_mic_total += np.real(spec)
        ppmAxis_prom+=ppmAxis
        x_max = posicion_del_max(spec, ppmAxis)
        espectros_max_total.append(x_max)
        
        medicion = Medicion(superposicion, volumen_medido='completo-bulk')
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=False, KS=258)
        espectros_prom_bulk_total += np.real(spec)
        ppmAxis_prom+=ppmAxis
                
        medicion = Medicion(superposicion, volumen_medido='completo')
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
                
        medicion = Medicion(superposicion, volumen_medido='centro')
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=False, KS=258)
        espectros_prom += np.real(spec)    
        ppmAxis_prom+=ppmAxis
        
        elapsed = time.time() - ti
        print("Una geometria demora: {} min".format(elapsed/60.0))
    
    datos = np.array([ppmAxis_prom/6.0, espectros_prom, espectros_prom_mic, espectros_prom_bulk, espectros_prom_total, espectros_prom_mic_total, espectros_prom_bulk_total]).T
    np.savetxt('./espectros_distancia_{}_um.dat'.format(int(dist*1000)), datos)
    
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
    
    
    datos = np.array([desplazamiento, desplazamiento_total]).T
    np.savetxt('./desplazamientos_distancia_{}_um.dat'.format(int(dist*1000)), datos)
    
    cont += 1
    elapsed = time.time() - td
    print("Una distancia demora: {} min".format(elapsed/60.0))
    
    
datos = np.array([distancias, lista_medias, lista_desviaciones, lista_medias, lista_desviaciones_total]).T
np.savetxt('./corrimiento_vs_distancia.dat'.format(dist*1000), datos)


print('===================================================================')
print('===================================================================')
print('===================================================================')
tiempo = time.time() - t0
print('tiempo total: {} min, o bien, {} h'.format(tiempo/60., tiempo/3600.))


#%%
# #Armo el espectro del bulk y lo agrego a al gráfico

