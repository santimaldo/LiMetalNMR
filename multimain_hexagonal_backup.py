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
# from Modules.Funciones import *
import time


def get_param_a(d):
  # distancias, parametros_a, errores relativos
  Ds, As, Es = np.loadtxt('./DataBases/Hexagonal_parametro_a.dat').T
  a = As[Ds==d][0]
  return a


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
vs = 0.1 # um
voxelSize = [vs*1e-3]*3# mm
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


radios = [2.5]
distancias_r = [[10]]
alturas = [10]
ntotal = 0
for ir in range(len(radios)):
  ntotal+=len(distancias_r[ir])*len(alturas)


savepath = './Outputs/Cilindros_hexagonal/'
# with open(savepath+'Densidades.dat','w') as f:
#       f.write('# radio (um)\tdistancia (um)\taltura (um)\tdensidad\n')
# with open(savepath+'tiempos.dat','w') as f:
#       f.write('# N_iter\tt_total (min)\tt_iteracion(min)\th\tr\td\n')



#inicio el reloj
t0 = time.time()
nnn = 0
for ind_h in range(len(alturas)):
  h = int(alturas[ind_h])
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
      elapsed = (time.time() - t0)/60.0
      print('tiempo: {:.2f} min'.format(elapsed))
      if nnn>0:
        t_est = elapsed*(ntotal/nnn-1)
        msj = 'tiempo restante estimado: {:.2f} min  =  {:.2f} h'.format(t_est, t_est/60.0)
        print(msj)
        
      if d<=64:
        N = [512,512,512] 
      else:
        N = [256,512,512] 
      
      N = [256]*3 # agregado para hacer una prueba el dia 08/03/2022  
      Nz,Ny,Nx = N  
      volumen = SimulationVolume(voxelSize=voxelSize, N=N)

      a = get_param_a(d)            
      # calculo cuantas celdas unitarias entran en la maxima superf que puedo simular
      # (sup max:  Nx/2*Ny/2)
      N_celdas_x = (Nx/2)//d   # // es division entera en python3  (floor)
      N_celdas_y = (Ny/2)//(2*a)
      
      medidas = [h*vsz,N_celdas_y*(2*a)*vsy,N_celdas_x*d*vsx]
      distancia = d*vsx
      parametro_a = a*vsy
      radio = r*vsx
      # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
      # Creacion de la muestra
      muestra = Muestra(volumen, medidas=medidas, geometria='cilindros_hexagonal',exceptions=False, radio=radio, distancia=distancia, parametro_a=parametro_a)       
      # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
      # calculo densidad usando celda unidad    
      A_mic  = np.sum(muestra.muestra[1,:int(2*a),:int(d)]/Chi) # la muestra vale Chi en el objeto
      A_tot  = 2*a*d
      densidad = A_mic/A_tot
      with open(savepath+'/Densidades.dat','a') as f:
        pass
        # f.write('{:d}\t{:d}\t{:d}\t{:.4f}\n'.format(r,d,h,densidad))             
      #CREACION DEL OBJETO DELTA-------------------------------------------------
      # delta es la perturbacion de campo magnetico    
      delta = Delta(muestra)
      # SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK -----------------------
      superposicion = Superposicion(muestra, delta, superposicion_lateral=True)
      ## MEDICION ---------------------------------------------------------------
      # debo sacar el borde superior de z
      if h<20:
        borde_z = 4
      else:
        borde_z = 12
      medicion = Medicion(superposicion, volumen_medido='sin-borde', borde_a_quitar=[borde_z,a,d/2])
      print("Calculando espectro sp...")
      ppmAxis , spec  = medicion.CrearEspectro(secuencia='sp' , k=0.5, Norm=False)
      print("Calculando espectro smc...")
      ppmAxis1, spec1 = medicion.CrearEspectro(secuencia='smc', N=64, k=1, Norm=False)
      datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
      #np.savetxt(path+'h{:d}_ancho{:d}_dens{:d}_SP_k{:.2f}'.format(int(h*1e3), int(ancho*1e3), int(porcentaje), k))
  
      # guardado
      regiones = ['', '-microestructuras', '-bulk']  
      # -------- centro--------------------------------------------------------------    
      for region in regiones:
        print("\n Trabajando en medicion y espectro de la muestra{}...".format(region))
        ### secuencia: ..... SP ......           
        medicion = Medicion(superposicion, volumen_medido='sin-borde{}'.format(region), borde_a_quitar=[borde_z,a,d/2])
        # - - - - SP
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5)
        datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
        file = 'SP/h{:d}_r{:d}_d{:d}_SP{}.dat'.format(int(h), int(r), int(d), region)
        # np.savetxt(savepath+file, datos)
        # - - - - SMC64
        ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', N=64, k=1, Norm=False)
        datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
        file = 'SMC64-k1/h{:d}_r{:d}_d{:d}_SMC64k1{}.dat'.format(int(h), int(r), int(d), region)
        # np.savetxt(savepath+file, datos)
      # 
      elapsed_parcial = (time.time() - t0parcial)/60.0
      elapsed         = (time.time() - t0)/60.0
      print('---  tiempo parcial: {:.2f} min'.format(elapsed_parcial))
      with open(savepath+'tiempos.dat','a') as f:
        pass
        # f.write('{:d}\t{:.2f}\t{:.2f}\t{:d}\t{:d}\t{:d}\n'.format(int(nnn), elapsed, elapsed_parcial,h,r,d))

      nnn+=1
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
elapsed = (time.time() - t0)/60.0
print('---  tiempo total: {:.2f} min = {:.2f} h'.format(elapsed, elapsed/60.0))