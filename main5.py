
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
#Veo si puedo guardar los datos de los espectros para hacer las deconvoluciones
datos1 = np.array([np.real(espectro_1[0]),np.real(espectro_1[1])]).T
np.savetxt('./espectro_geo_CVDC.dat', datos1)
datos2 = np.array([np.real(espectro_2[0]),np.real(espectro_2[1])]).T
np.savetxt('./espectro_geo_CRDC.dat', datos2)
datos3 = np.array([np.real(espectro_3[0]),np.real(espectro_3[1])]).T
np.savetxt('./espectro_geo_CRDR1.dat', datos3)
datos4 = np.array([np.real(espectro_4[0]),np.real(espectro_4[1])]).T
np.savetxt('./espectro_geo_CRDR2.dat', datos4)
datos5 = np.array([np.real(ppmAxis_bulk),np.real(spec_bulk)]).T
np.savetxt('./espectro_bulk.dat', datos5)

#%%


#Los grafico en la misma figura para compararlos
plt.figure(50)
ax = plt.subplot(111)
ax.plot(espectro_1[0],espectro_1[1],linestyle='-', marker='.',linewidth=4,color='#554D90', label=' CVDC')
ax.plot(espectro_2[0],espectro_2[1],linestyle='-', marker='.',linewidth=4,color='#be97bdff', label=' CRDC')
ax.plot(espectro_3[0],espectro_3[1],linestyle='-', marker='.',linewidth=4,color='#597D4E', label=' CRDR1')
ax.plot(espectro_4[0],espectro_4[1],linestyle='-', marker='.',linewidth=4,color='#A6C275', label=' CRDR2')
ax.plot(ppmAxis_bulk,spec_bulk,'-',linewidth=4, color='#b6b8b6' , label=' bulk')
plt.xlim(left=350,right=150)
plt.xlabel('$\delta$ [ppm]')
plt.ylabel(' ')
ax.legend()


#%%
# Aca voy a hacer el grafico del shift en funcion de la geometria

xc2 = 245.72

xc_geo1 = 266.34
xc_geo2 = 262.34
xc_geo3 = 261.77
xc_geo4 = 258.99

shift1 = xc_geo1-xc2
shift2 = xc_geo2-xc2
shift3 = xc_geo3-xc2
shift4 = xc_geo4-xc2

print(shift1)
print(shift2)
print(shift3)
print(shift4)

plt.figure(51)
ax = plt.subplot(111)
ax.plot(1,shift1, marker='.',markersize=20,color='#554D90', label=' CVDC')
ax.plot(2,shift2, marker='.',markersize=20,color='#be97bdff', label=' CRDC')
ax.plot(3,shift3, marker='.',markersize=20,color='#597D4E', label=' CRDR1')
ax.plot(4,shift4, marker='.',markersize=20,color='#A6C275', label=' CRDR2')
plt.xlabel('geo')
plt.ylabel('$\Delta$ [ppm]')
ax.legend()

#Hago un gráfico de barras


  
fig = plt.figure(figsize = (8, 7))
 
# creating the bar plot
plt.bar( 'CVDC',shift1, color ='#554D90', width = 0.5)
plt.bar( 'CRDC',shift2, color ='#be97bdff', width = 0.5)
plt.bar( 'CRDR1',shift3, color ='#597D4E', width = 0.5)
plt.bar( 'CRDR2',shift4, color ='#A6C275', width = 0.5)
 
plt.xlabel("Geometrías")
plt.ylabel("$\Delta$ [ppm]")
plt.title('')
plt.show()



elapsed = (time.time() - t0)/60
print('---  tiempo: {:.2f} min'.format(elapsed))
