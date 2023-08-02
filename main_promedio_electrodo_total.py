# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 18:33:19 2023

@author: Santi y Muri
"""

#stop

#En este main integro el espectro promedio del electrodo


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
# delta es la perturbacion de campo magnetico
#delta = Delta(muestra)



lista_radios = ['000','030','050','080','100','130','160','180','200','230','260','290','310','340','370','390','420','440','470','500','520','550','570','600'] 

        
espectros_R = []

RADIO = '000'
for RADIO in lista_radios:

    muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_aleatorios_2', ancho=16e-3, distancia= 20e-3)
    delta = Delta(muestra)
    superposicion = Superposicion(muestra, delta, radio = RADIO, z0=84e-3)
    medicion = Medicion(superposicion, volumen_medido='centro')
    ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

    espectros_R.append([ppmAxis,spec])
    
    


#%%
#Contruyo el promedio del espectro total

A_mic = 256*256 #um
L_mic = 256     #um

R_e = 6000 #um 



A_elec = np.pi*R*R #um*um
print(A_elec)
veces = A_elec/A_mic
print(veces)


w_it = 0
w = 0

w_it_list = []


for RADIO in lista_radios :
    w_it = 20*np.pi*float(RADIO)/L_mic -1.3
    w_it_list.append([float(int(w_it))])
    w = w + int(w_it)
        
print(w)

lista_espectros_R = []

#Descomprimo la lista en los dos espectros para asignarle el peso correspondiente wi 
espectro_1 = espectros_R[0] 
espectro_2 = espectros_R[1] 
espectro_3 = espectros_R[2]
espectro_4 = espectros_R[3]
espectro_5 = espectros_R[4]
espectro_6 = espectros_R[5]
espectro_7 = espectros_R[6]
espectro_8 = espectros_R[7]
espectro_9 = espectros_R[8]
espectro_10 = espectros_R[9]
espectro_11 = espectros_R[10]
espectro_12 = espectros_R[11]
espectro_13 = espectros_R[12] 
espectro_14 = espectros_R[13] 
espectro_15 = espectros_R[14]
espectro_16 = espectros_R[15]
espectro_17 = espectros_R[16]
espectro_18 = espectros_R[17]
espectro_19 = espectros_R[18]
espectro_20 = espectros_R[19]
espectro_21 = espectros_R[20]
espectro_22 = espectros_R[21]
espectro_23 = espectros_R[22]
espectro_24 = espectros_R[23]



    

Spec_prom = (w_it_list[0]*espectro_1[1] + w_it_list[1]*espectro_2[1]+ w_it_list[2]*espectro_3[1]+ w_it_list[3]*espectro_4[1]+
             w_it_list[4]*espectro_5[1]+ w_it_list[5]*espectro_6[1]+ w_it_list[6]*espectro_7[1]+ w_it_list[7]*espectro_8[1]+ 
             w_it_list[8]*espectro_9[1]+ w_it_list[9]*espectro_10[1]+ w_it_list[10]*espectro_11[1]+ w_it_list[11]*espectro_12[1]
             + w_it_list[12]*espectro_13[1]+ w_it_list[13]*espectro_14[1]+ w_it_list[14]*espectro_15[1]+ w_it_list[15]*espectro_16[1]
             + w_it_list[16]*espectro_17[1]+ w_it_list[17]*espectro_18[1]+ w_it_list[18]*espectro_19[1]+ w_it_list[9]*espectro_20[1]
             + w_it_list[20]*espectro_21[1]+ w_it_list[21]*espectro_22[1]+ w_it_list[22]*espectro_23[1]+ w_it_list[23]*espectro_24[1])/1721


    


#%%

#Armo el espectro del bulk y lo agrego a al gráfico

muestra = Muestra(volumen, medidas=medidas, geometria = 'bulk')
delta = Delta(muestra)
superposicion = Superposicion(muestra, delta, radio = '000', z0=84e-3)
medicion = Medicion(superposicion, volumen_medido='centro')
ppmAxis_bulk, spec_bulk = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


#%%
#Los grafico en la misma figura para compararlos
plt.figure(52)
ax = plt.subplot(111)
ax.plot(espectro_1[0],Spec_prom,linestyle='-', marker='.',linewidth=2,color='#1f77b4', label=' Spec_prom')
ax.plot(ppmAxis_bulk,spec_bulk,'-',linewidth=2, color='#b6b8b6' , label=' bulk')
plt.xlim(left=350,right=150)
plt.xlabel('[ppm]')
plt.ylabel(' ')
ax.legend()
