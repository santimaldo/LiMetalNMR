#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""


import numpy as np
import matplotlib.pyplot as plt
from Modules.Muestra import *
from Modules.Delta import *
from Modules.Superposicion import *
from Modules.Graficador import *
from Modules.SimulationVolume import *
from Modules.Medicion import *
import time
from oct2py import Oct2Py

# funcion para crear la figura 3D
def exportar_3D(matriz, archivo):
  print(" -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ")
  print("Creando figura 3D. Esto puede demorar varios minutos...")
  Nz, Nx, Ny = matriz.shape
  tmpvol =np.zeros((Nz+5,Ny,Nx))
  tmpvol[1:-4,:,:] = matriz
  filename = archivo+'.stl'
  with Oct2Py() as oc:
    oc.addpath('./Modules/')
    fv = oc.isosurface(tmpvol, 0.5) # Make patch w. faces "out"
    oc.stlwrite(filename,fv)        # Save to binary .stl
  # octave.addpath('\\Modules')
  # fv = oc.isosurface(tmpvol, 0.5) # Make patch w. faces "out"
  # octave.stlwrite(filename,fv)        # Save to binary .stl
  
  print("       Listo!") 
  print(" -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ")

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
N = [256,256,256] # para trapped_arranged_sticks

# utilizo una funcion que dado dos argumentos define el restante. Ya sea N, 
# FOV (field of view) o  voxelSize
volumen = SimulationVolume(voxelSize=voxelSize, N=N)
#volumen = SimulationVolume(FOV=FOV, N=N)


#%% LOOP

anchos = np.array([1,10,40])*1e-3       # milimetros
alturas = np.array([10,30])*1e-3      # milimetros
porcentajes = np.array([10,50,80])    # %
# lista con listas de los parametros que quiero guardar como objeto 3D
exportar3d = [[1e-3,10e-3,50],[40e-3,10e-3,50]]


n_total = anchos.size * alturas.size * porcentajes.size

#inicio el reloj
t0 = time.time()


nn=0
for ancho in anchos:
  for h in alturas:
    for porcentaje in porcentajes:      
      nn+=1
      print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
      print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
      msj = 'altura= {:d} um,  ancho= {:d} um,  densidad p= {:d}%'.format(int(h*1e3), int(ancho*1e3), porcentaje)
      print(msj)
      print(' ')
      progreso = nn/n_total*100
      print('         ... Progreso :  {:.2f}%  ({}/{})'.format(progreso, nn, n_total))
      elapsed = (time.time() - t0)/60
      print('tiempo: {:.2f} min'.format(elapsed))
      #%% CREACION DE LA MUESTRA-----------------------------------------------------
      #------------------------------------------------------------------------------
      #------------------------------------------------------------------------------
      #Creo el objeto muestra. Le tengo que dar de entrada:
      #  el volumen
      #  la geometria: el nombre del constructor que va a usar para crear el phantom
      #microestructuras
      medidas = [h,0.128,0.128] #       
      #muestra = Muestra(volumen, medidas=medidas, geometria='porcentaje_lanzas',ancho=ancho, porcentaje=porcentaje) # para 'porcentaje_palos'
      muestra = Muestra(volumen, medidas=medidas, geometria='porcentaje_palos',ancho=ancho, porcentaje=porcentaje) # para 'porcentaje_palos'
      #%% CREACION DEL OBJETO DELTA--------------------------------------------------
      # delta es la perturbacion de campo magnetico
      delta = Delta(muestra)
      #%%
      # SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK
      superposicion = Superposicion(muestra, delta)
      #%% guardado
      regiones = ['', '-microestructuras', '-bulk']  
      # -------- centro--------------------------------------------------------------    
      for region in regiones:
        ### secuencia: ..... SP ......
        savepath = "./Espectros/centro_aleatorias_palo/SP/"
        k = 0.5
        medicion = Medicion(superposicion, volumen_medido='centro{}'.format(region))            
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=k)
        datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
        file = 'centro{}_h{:d}_ancho{:d}_dens{:d}_SP_k{:.2f}'.format(region,int(h*1e3), int(ancho*1e3), int(porcentaje), k)
        np.savetxt(savepath+file, datos)
        # para algunos casos en particular, guardo figura 3D volumen medido, pero solo cuando la region es completa
        if region=='':
          if [ancho,h,porcentaje] in exportar3d:
            exportar_3D(medicion.get_volumen_medido(), savepath+file)        
        ### secuencia: ..... SMC .....
        # savepath = './Espectros/centro_aleatorias_palo/SMC/'
        # k_list = [1, 1.1, 1.2, 1.3, 1.5, 2.0]
        # N=16                  
        # for k in k_list:        
        #   ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , k=k, N=N)
        #   datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
        #   file = 'centro{}_h{:d}_ancho{:d}_dens{:d}_SMC_N{:d}_k{:.2f}'.format(region,int(h*1e3), int(ancho*1e3), int(porcentaje), N, k)
        #   np.savetxt(savepath+file, datos)      
      # --------completo-------------------------------------------------------------
      ### En esta parte tambien guardamos el espectro teniendo en cuenta la geometria completa, no solo el centro
      # for region in regiones:
      #   ..... SP ......
      #   savepath = './Espectros/completo/SP/'
      #   k = 0.5
      #   medicion = Medicion(superposicion, volumen_medido='completo{}'.format(region))            
      #   ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=k)
      #   datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
      #   file = 'completo{}_h{:d}_ancho{:d}_dens{:d}_SP_k{:.2f}'.format(region,int(h*1e3), int(ancho*1e3), int(porcentaje), k)
      #   np.savetxt(savepath+file, datos)
      #   ## ..... SMC .....
      #   savepath = './Espectros/completo/SMC/'
      #   k_list = [1, 1.1, 1.2, 1.3, 1.5, 2.0]
      #   N=16                  
      #   for k in k_list:        
      #     ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , k=k, N=N)
      #     datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
      #     file = 'completo{}_h{:d}_ancho{:d}_dens{:d}_SMC_N{:d}_k{:.2f}'.format(region,int(h*1e3), int(ancho*1e3), int(porcentaje), N, k)
      #     np.savetxt(savepath+file, datos)              
      # -----------------------------------------------------------------------------
      duracion = (time.time()-t0)/60  - elapsed 
      del muestra, delta, superposicion, medidas   # libero RAM    
      print('tiempo en este paso: {:.2f} min'.format(duracion))        
#%%
