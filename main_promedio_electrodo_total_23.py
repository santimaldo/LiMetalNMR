

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 18:33:19 2023

@author: Santi y Muri
"""

#stop

#En este main integro el espectro promedio del electrodo


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
N = [512,1024,1024]
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



lista_radios = ['0000','0320','0520','0800','1000','1320','1600','1800','2000','2320','2600','2960','3000','3440','3720','3920','4000','4400','4720','5000','5199','5480','5720','5960'] 

        
espectros_R = []

RADIO = '0000'


muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_dist_cte', ancho=16e-3, distancia= 20e-3)
delta = Delta(muestra)
for RADIO in lista_radios:
    superposicion = Superposicion(muestra, delta, radio = RADIO)
    medicion = Medicion(superposicion, volumen_medido='centro')
    ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

    espectros_R.append([ppmAxis,spec])
#%%
#Contruyo el promedio del espectro total

A_med = 256*256 #um
L_med = 256     #um

R_e = 6000 #um 



A_elec = np.pi*R_e*R_e #um*um
print(A_elec)
veces = A_elec/A_med
print('veces=',veces)


w_it = 0
w = 0

w_it_list = []


for RADIO in lista_radios :
    if RADIO == '0000':
        w_it = 1                                  # Porque para R=0 tiene que aparecer una vez
        print('w_it',w_it)
        w_it_list.append([int(w_it)])
    else:
        w_it =2*np.pi*float(RADIO)/L_med -1.2     # El -1.2 es para fitear la cantidad de veces que entra el area de las mic en el area del electrodo
        print('w_it',w_it)
        w_it_list.append([int(w_it)])
    
    w = w + int(w_it)
        
print('w',w)


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
             + w_it_list[20]*espectro_21[1]+ w_it_list[21]*espectro_22[1]+ w_it_list[22]*espectro_23[1]+ w_it_list[23]*espectro_24[1])/1725

#Divido por 1725 porque es la cantidad de veces que entra el área de las mic en el electrodo

#Exporto la data de S_prom
datos_espectro_prom23= np.array([np.real(espectro_1[0]),np.real(Spec_prom)]).T
np.savetxt('./datos_espectro_prom23.dat', datos_espectro_prom23)


#%%
#Construyo el espectro del centro y lo guardo

muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_dist_cte', ancho=16e-3, distancia= 20e-3)
delta = Delta(muestra)
superposicion = Superposicion(muestra, delta, radio = '0000')
medicion = Medicion(superposicion, volumen_medido='centro')
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

datos_espectro_centro= np.array([np.real(ppmAxis),np.real(spec)]).T
np.savetxt('./datos_espectro_centro.dat', datos_espectro_centro)    

#Construyo el espectro del borde y lo guardo

muestra = Muestra(volumen, medidas=medidas, geometria='cilindritos_dist_cte', ancho=16e-3, distancia= 20e-3)
delta = Delta(muestra)
superposicion = Superposicion(muestra, delta, radio = '5960')
medicion = Medicion(superposicion, volumen_medido='centro')
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)

datos_espectro_borde= np.array([np.real(ppmAxis),np.real(spec)]).T
np.savetxt('./datos_espectro_borde.dat', datos_espectro_borde)    



#%%
#Armo el espectro del bulk y lo agrego a al gráfico

muestra = Muestra(volumen, medidas=medidas, geometria = 'bulk')
delta = Delta(muestra)
superposicion = Superposicion(muestra, delta, radio = '0000')
medicion = Medicion(superposicion, volumen_medido='centro')
ppmAxis_bulk, spec_bulk = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, KS=258)


#%%
#Los grafico en la misma figura para compararlos
plt.figure(52)
ax = plt.subplot(111)
plt.set_cmap('inferno')
ax.plot(espectro_1[0],Spec_prom,linestyle='-', marker='.',linewidth=2, label=' Spec_prom')
ax.plot(ppmAxis_bulk,spec_bulk,'.',linewidth=2, label=' bulk')
plt.xlim(left=350,right=150)
plt.xlabel('$\delta$ (ppm)')
plt.ylabel(' ')
ax.legend()
