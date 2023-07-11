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
import pandas as pd


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
Nz = 1024
Ny = Nx = 256
N = [Nz,Ny,Nx]


altura = 25 # u
# radio, distancia y vs estan en el archivo:
parametros = np.loadtxt('./DataBases/CilindrosAltaResolucion_parametros_d_r.dat')
df = pd.DataFrame(parametros)
df = df.sort_values(3,ascending=False)
parametros = np.array(df)



#%%
savepath = './Outputs/2022-03-11_Cilindros_hexagonal_AltaResolucion/'
savepath = './Outputs/Cilindros_hexagonal_AltaResolucion/'
savepath = './Outputs/2022-03-13_Cilindros_hexagonal_AltaResolucion/'
with open(savepath+'Densidades.dat','w') as f:
      f.write('# radio (um)\tdistancia (um)\taltura (um)\tvs (um)\tdensidad\n')
with open(savepath+'tiempos.dat','w') as f:
      f.write('# N_iter\tt_total (min)\tt_iteracion(min)\tradio (um)\tdistancia (um)\taltura (um)\tvs (um)\n')



# inicializo una lista de cuales tienen error.
#inicio el reloj
t0 = time.time()
nnn = -1
ntotal = parametros.shape[0]
# ntotal = 1
for par in parametros:
  nnn+=1
  # if nnn<22:
  #   continue # hago esto para terminar lo que corri el 13-03-2022
  
  if nnn<10:
    continue 
  elif nnn>10:
    continue
  
  distancia, radio, vs, densidad = par
  
  h = round(altura/vs)
  r = round(radio/vs)
  d = round(distancia/vs)   
  
  if np.abs(radio-r*vs)>vs:
    continue
  elif np.abs(altura-h*vs)>vs:
    continue
  elif np.abs(distancia-d*vs)>vs:
    continue
  
  radio = vs*r
  distancia = vs*d
  altura = vs*h
  
  
  #inicio el reloj parcial
  t0parcial = time.time()
  print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
  print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
  print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
  print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
  msj = f"altura= {h:d}x{vs}um = {altura} um,\nradio= {r:d}x{vs}um = {radio} um,\ndistancia = {d:d}x{vs}um = {distancia} um,\ndensidad = {densidad:.2f}"
  print(msj)
  print(' ')
  msj = f"progreso {nnn}/{ntotal} = {nnn/ntotal*100:.2f} %"
  print(msj)
  elapsed = (time.time() - t0)
  print(f'---  tiempo: {elapsed:.2f} s = {elapsed/60:.2f} min = {elapsed/60/60:.2f} h')
  if nnn>0:
    t_est = elapsed*(ntotal/nnn-1)
    msj = 'tiempo restante estimado: {:.2f} min  =  {:.2f} h'.format(t_est/60, t_est/60/60)
    print(msj)
    print(' ')
  
  with open(savepath+'/Densidades.dat','a') as f:
    f.write(f'{distancia:.2f}\t{radio:.2f}\t{altura:.2f}\t{vs:.2f}\t{densidad:.4f}\n')
  # Crecion del volumen simulado - - - - - - - - - - - - - - - - - - - - -
  voxelSize = [vs*1e-3]*3# mm
  vsz,vsy,vsx = voxelSize
  volumen = SimulationVolume(voxelSize=voxelSize, N=N)
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  # parametros de la muestra
  a = get_param_a(d)
  N_celdas_x = (Nx/2)//d   # // es division entera en python3  (floor)
  N_celdas_y = (Ny/2)//(2*a)  
  medidas = [h*vsz,N_celdas_y*(2*a)*vsy,N_celdas_x*d*vsx]
  distancia_mm = d*vsx
  parametro_a = a*vsy
  radio_mm = r*vsx
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  # Creacion de la muestra
  muestra = Muestra(volumen, medidas=medidas, geometria='cilindros_hexagonal',exceptions=False, radio=radio_mm, distancia=distancia_mm, parametro_a=parametro_a)       
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #CREACION DEL OBJETO DELTA-------------------------------------------------
  # delta es la perturbacion de campo magnetico    
  delta = Delta(muestra)
  # SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK -----------------------
  superposicion = Superposicion(muestra, delta, superposicion_lateral=True, )
  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  medicion = Medicion(superposicion)
  # guardado
  regiones = ['-microestructuras', '-bulk']  
  # -------- centro--------------------------------------------------------------    
  for region in regiones:
    print("\n Trabajando en medicion y espectro de la muestra{}...".format(region))
    ### secuencia: ..... SP ......           
    # - - - - SP
    ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, volumen_medido='completo{}'.format(region))
    datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
    file = 'SP/h{:d}_r{:.2f}_d{:.2f}_vs{:.2f}um_SP{}.dat'.format(int(altura), radio, distancia, vs, region)
    np.savetxt(savepath+file, datos)
    # pulso de pi/12
    # ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.08, volumen_medido='completo{}'.format(region))
    # datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
    # file = 'SP_0.08/h{:d}_r{:.2f}_d{:.2f}_vs{:.2f}um_SP{}.dat'.format(int(altura), radio, distancia, vs, region)
    # np.savetxt(savepath+file, datos)
    
    # - - - - SMC16
    # ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', N=16, k=1, Norm=False, volumen_medido='completo{}'.format(region))
    # datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
    # file = 'SMC16-k1/h{:d}_r{:.2f}_d{:.2f}_vs{:.2f}um_SMC64k1{}.dat'.format(int(altura), radio, distancia, vs, region)
    # np.savetxt(savepath+file, datos)
  
  elapsed_parcial = (time.time() - t0parcial)/60.0
  elapsed         = (time.time() - t0)/60.0
  print('---  tiempo parcial: {:.2f} min'.format(elapsed_parcial))
  with open(savepath+'tiempos.dat','a') as f:
    f.write(f'{int(nnn):d}\t{elapsed:.2f}\t{elapsed_parcial:.2f}\t{distancia:.2f}\t{radio:.2f}\t{altura:.2f}\t{vs:.2f}\n')

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
msj = f"progreso {nnn}/{ntotal} = {nnn/ntotal*100} %"
print(msj)
print(' ')
elapsed = (time.time() - t0)
print(f'---  tiempo total: {elapsed:.2f} s = {elapsed/60:.2f} min = {elapsed/60/60:.2f} h')