#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:45:24 2020

@author: santi
"""

import numpy as np
import warnings


def SimulationVolume(N=None, voxelSize=None, FOV=None):
  """
  Esta funcion determina el volumen de la simulacion.
  es decir determina N, voxelSize o FOV, alguno de ellos dados los otros
  dos restantes.

  N, voxelSize y FOV deben ser array_like, de 3 elementos con la convencion
  [z,y,x]

  ejemplo: dado N y FOV (en mmm) determino voxelSize

  N, voxelSize, FOV = SimulationVolume(N=[256,64,64], FOV=[1.5,10,10])

  Notar que el resultado son los tres parametros, ya que de poso los transforma
  en np.arrays!
  """
  if FOV is None:
    none = 'fov' # la variable none indica cual de los parametros no fue ingresado
    N = np.array(N)
    voxelSize = np.array(voxelSize)
    FOV = N*voxelSize
  elif voxelSize is None:
    none = 'voxelsize'
    N = np.array(N)
    FOV = np.array(FOV)
    voxelSize = FOV/N.astype(float)
  elif N is None:
    none = 'n'
    FOV = np.array(FOV)
    voxelSize = np.array(voxelSize)
    N = FOV/voxelSize

  # chequeo si el voxelSize es igual en todas las direcciones------------------
  iguales =  np.all(voxelSize==voxelSize[0])
  if not iguales:
    msg = "los elementos de voxelSize deberian ser todos iguales!!!"
    #warnings.warn(msg)
    raise Exception(msg)
  #----------------------------------------------------------------------------


  # chequeo si son potencias de 2:---------------------------------------------
  r = np.log2(N)
  check = r % 1 # donde check es cero, N es potencia de 2, ya que el ressto de la division entera por 1 no es cero
  # en los N que no sean potencia de 2, lo reemplazo por la siguiente potencia de 2
  r = r.astype(int)
  r[check!=0] = (r[check!=0]+1)
  N_new = 2**r
  print(check)
  if any(check):
    if none=='n'             :
      con = 'con una cantidad de voxels de N={}'.format(list(N_new))
      newFOV = N_new*voxelSize
      sugerencia = 'Proba con FOV={}\n'.format(list(newFOV)) + con
    else:
      sugerencia = 'Proba con N={}'.format(list(N_new))

    msg = 'La cantidad de voxels debe ser potencia de 2\n' + sugerencia
    raise Exception(msg)
  #----------------------------------------------------------------------------

  N = N.astype(int)
  #mensaje en pantalla:
  sN = str(N[0])+'*'+str(N[1])+'*'+str(N[2])
  sFOV = str(FOV[0])+'mm*'+str(FOV[1])+'mm*'+str(FOV[2])+'mm'
  sVS = str(voxelSize[0])+'mm*'+str(voxelSize[1])+'mm*'+str(voxelSize[2])+'mm'
  print('Volumen de simulacion (convencion z,y,x):')
  print('N: '+ sN + ' | voxelSize:  ' + sVS + ' | FOV:  '+ sFOV)
  return N, voxelSize, FOV




