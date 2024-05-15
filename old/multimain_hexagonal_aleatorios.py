#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021-06-12

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


def get_param_a(d):
  if d>256:
    msg = ("d debe ser mas chico")
    raise Exception(msg)
  if d%2==0:    
    # distancias, parametros_a, errores relativos
    Ds, As, Es = np.loadtxt('./DataBases/Hexagonal_parametro_a.dat').T
    a = As[Ds==d][0]
    return a
  else:
    msg = ("la distancia debe ser tal que distancia/vs sea PAR")
    raise Exception(msg)


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
vsz,vsy,vsx = voxelSize
#%% CREACION DE LA MUESTRA-----------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Creo el objeto muestra. Le tengo que dar de entrada:
#  el volumen
#  la geometria: el nombre del constructor que va a usar para crear el phantom de microestructuras

# Debo "preparar" los parametros para que cumplan ciertos criterios:
#   d: par,   Nmx=n*d,  Nmy=m*2*a,  'a' se lee de archivo.

# corrida 1
radios = [1,3,10,20,40,60]
distancias_r=[[4,6,8,10,16,22]               ,\
             [8,18,28,34,44,54]             ,\
             # [14,20,34,48,58,66,76,86]            ,\
             [22,34,50,70,94,108,126]          ,\
             #[42,46,50,56,62,68,78,94,110,126]          ,\
             [62,72,86,98,110,126]         ,\
             #[82,88,94,100,104,108,112,116,122,126]     ,\
             [108,118,122,126]              ,\
             [122,124,126]                              ]   
  
# corrida 2
radios = [1,3,5,10,20,30,40,50]
distancias_r=[[12]               ,\
             [10,14]             ,\
             [14,20,28,38,46,58,66,76,86]            ,\
             [26,30,40]          ,\
             [42, 48, 54]          ,\
             [62,72,86,98,110,126]  ,\
             [82,88,94,100]         ,\
             [102,110,116,122,126]  ]   
alturas = [64,16,128]


# corrida 3
radios = [20]
distancias_r=[[42,46,50,56,62,68,78,94,110,126]]
alturas = [64]


# corrida 4
radios = [1,3,5,10,30,40,50,60]
distancias_r=[[12,4,6,8,10,16,22]               ,\
             [10,14,8,18,28,34,44,54]            ,\
             [14,20,28,38,46,58,66,76,86]       ,\
             [26,30,40,22,34,50,70,94,108,126]    ,\
             [62,72,86,98,110,126]  ,\
             [82,88,94,100,108,118,126]      ,\
             [102,110,116,122,126]  ,\
             [122,124,126] ]
alturas = [64,16,128]

# corrida 4
radios = [20]
distancias_r=[[42,46,50,56,62,68,78,94,110,126]]
# alturas = [16,64]
alturas = [64]


# NCASOS=4  :   1 rectos y 3 clusters
NCASOS=4

ntotal = 0
for ir in range(len(radios)):
  ntotal+=len(distancias_r[ir])*len(alturas)
ntotal=ntotal*NCASOS

N = [256,512,512] 
Nz,Ny,Nx = N  
volumen = SimulationVolume(voxelSize=voxelSize, N=N)


savepath0 = './Outputs/Resultados/'
with open(savepath0+'Densidades.dat','w') as f:
      f.write('# radio (um)\tdistancia (um)\taltura (um)\tdensidad\n')
with open(savepath0+'tiempos.dat','w') as f:
      f.write('# N_iter\tN_caso\tt_total (min)\tt_iteracion(min)\th\tr\td\n')

contador=0
t0 = time.time()
nnn = 0
for ind_h in range(len(alturas)):
  h = int(alturas[ind_h])
  #inicio el reloj
  for caso in range(NCASOS):
    for ind_r in range(len(radios)):
      distancias = distancias_r[ind_r]
      r = int(radios[ind_r])
      for ind_d in range(len(distancias)):
        d = int(distancias[ind_d])      
        #inicio el reloj parcial
        t0parcial = time.time()
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        msj = 'altura= {:d} um,  radio= {:d} um,  distancia = {:d} um'.format(h,r,d)
        print(msj)
        print(' ')
        progreso = nnn/ntotal*100
        print('         ... Progreso :  {:.2f}%  ({}/{})'.format(progreso, nnn, ntotal))
        elapsed = (time.time() - t0)/60
        print('tiempo: {:.2f} min'.format(elapsed))
        if nnn>0:
          t_est = elapsed*(ntotal/nnn-1)
          msj = 'tiempo restante estimado: {:.2f} min  =  {:.2f} h'.format(t_est, t_est/60)
          print(msj)

  
        a = get_param_a(d)            
        # calculo cuantas celdas unitarias entran en la maxima superf que puedo simular
        # (sup max:  Nx/2*Ny/2)
        N_celdas_x = (Nx/2)//d   # // es division entera en python3  (floor)
        N_celdas_y = (Ny/2)//(2*a)
        
        medidas = [h*vsz,N_celdas_y*(2*a)*vsy,N_celdas_x*d*vsx]
        distancia = d*vsx
        parametro_a = a*vsy
        radio = r*vsx
        if caso==0:
          savepath = savepath0 + 'rectos/'
          muestra = Muestra(volumen, medidas=medidas, geometria='cilindros_hexagonal',radio=radio, distancia=distancia, parametro_a=parametro_a)       
        elif caso==1:
          savepath = savepath0 + 'clusters/p_huecos_20/'
          p_huecos = 0.2
          muestra = Muestra(volumen, medidas=medidas, geometria='clusters_hexagonal',radio=radio, distancia=distancia, parametro_a=parametro_a, p_huecos=p_huecos)       
        elif caso==2:
          savepath = savepath0 + 'clusters/p_huecos_50/'
          p_huecos = 0.5
          muestra = Muestra(volumen, medidas=medidas, geometria='clusters_hexagonal',radio=radio, distancia=distancia, parametro_a=parametro_a, p_huecos=p_huecos)       
        elif caso==3:
          savepath = savepath0 + 'clusters/p_huecos_80/'
          p_huecos = 0.8
          muestra = Muestra(volumen, medidas=medidas, geometria='clusters_hexagonal',radio=radio, distancia=distancia, parametro_a=parametro_a, p_huecos=p_huecos)         
        elif caso>3:  
          savepath =savepath0 + 'aleatorios/'
          muestra = Muestra(volumen, medidas=medidas, geometria='cilindros_aleatorios_hexagonal',radio=radio, distancia=distancia, parametro_a=parametro_a)       
        # calculo densidad usando celda unidad    
        if caso<1:
          A_mic  = np.sum(muestra.muestra[1,:int(2*a),:int(d)]/Chi) # la muestra vale Chi en el objeto
          A_tot  = 2*a*d      
          densidad = A_mic/A_tot    
        else:
          A_mic  = np.sum(muestra.muestra[1,:,:]/Chi) # la muestra vale Chi en el objeto
          A_tot  = muestra.N_muestra[1]*muestra.N_muestra[2]
          densidad = A_mic/A_tot              
        with open(savepath+'/Densidades.dat','a') as f:
          f.write('{:d}\t{:d}\t{:d}\t{:.4f}\n'.format(r,d,h,densidad))             
        #CREACION DEL OBJETO DELTA-------------------------------------------------
        # delta es la perturbacion de campo magnetico
        delta = Delta(muestra)
        # SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK -----------------------
        superposicion = Superposicion(muestra, delta, superposicion_lateral=True)
        ## MEDICION ---------------------------------------------------------------
        regiones = ['', '-microestructuras', '-bulk'] 
        
        borde = 12
        if h<30:
          borde = 3
        # -------- centro--------------------------------------------------------------    
        for region in regiones:
          ### secuencia: ..... SP ......           
          medicion = Medicion(superposicion, volumen_medido='muestra{}'.format(region), borde_a_quitar=[borde,0,0])
          # - - - - SP
          ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5)
          datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
          file = 'SP/h{:d}_r{:d}_d{:d}{}.dat'.format(int(h), int(r), int(d), region)          
          if caso>3:
            file = 'SP/h{:d}_r{:d}_d{:d}iteracion{:d}{}.dat'.format(caso,int(h), int(r), int(d), region)
          np.savetxt(savepath+file, datos)
          # - - - - SMC64
          ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', N=64, k=1, Norm=False)
          datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
          file = 'SMC64-k1/h{:d}_r{:d}_d{:d}{}.dat'.format(int(h), int(r), int(d), region)
          if caso>3:
            file = 'SMC64-k1/h{:d}_r{:d}_d{:d}_iteracion{:d}{}.dat'.format(caso,int(h), int(r), int(d), region)
            contador += 1
          np.savetxt(savepath+file, datos)
        # 
        elapsed_parcial = (time.time() - t0parcial)/60
        elapsed         = (time.time() - t0)/60
        print('---  tiempo parcial: {:.2f} min'.format(elapsed_parcial))
        with open(savepath0+'tiempos.dat','a') as f:
          f.write('{:d}\t{:d}\t{:.2f}\t{:.2f}\t{:d}\t{:d}\t{:d}\n'.format(caso,int(nnn), elapsed, elapsed_parcial,h,r,d))
  
        nnn+=1
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
elapsed = (time.time() - t0)/60
print('---  tiempo total: {:.2f} min = {:.2f} h'.format(elapsed, elapsed/60))