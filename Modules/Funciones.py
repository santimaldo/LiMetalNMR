# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:57:23 2022

@author: santi
"""

import functools # para implementar el decorador timer
import time
import numpy as np

#-------------------------------------------------------------------------
def timer(method, timing=True):
  @functools.wraps(method)
  def wrapper_timer(*args, **kwargs):
    if timing:
      tic = time.perf_counter()
      value = method(*args, **kwargs)
      toc = time.perf_counter()
      elapsed_time = toc - tic
      print(f"Tiempo de '{method.__code__.co_name}': {elapsed_time:.2f} s = {elapsed_time/60.0:.2f} min")
    else:
      value = method(*args, **kwargs)
    return value
  return wrapper_timer
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
def timerClass(Class, timing=True):
  @functools.wraps(Class)
  def wrapper_timer(*args, **kwargs):
    print(f'- - - - - - Creando {Class.__name__}...')
    if timing:
      tic = time.perf_counter()
      value = Class(*args, **kwargs)
      toc = time.perf_counter()
      elapsed_time = toc - tic
      print(f"Tiempo total de creacion de '{Class.__name__}': {elapsed_time:.2f} s = {elapsed_time/60.0:.2f} min")
    else:
      value = Class(*args, **kwargs)
    print('- - - - - - - - - - - - - - - - - - - - - - - - \n')
    return value
  return wrapper_timer
#-------------------------------------------------------------------------


# --------------------FUNCIONES-------------------------------------------------
def find_nearest(array, value):
    """
    Encuentra el valor mas cercano a 'value' dentro de 'array'.
    Devuelve el indice del valor mas cercano
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    # return idx, array[idx]
    return idx


def autophase(ppmAxis, spec, precision = 1):
    """
    Corrijo automaticamente la fase, utilizando el método de minimizar el area
    de la parte imaginaria:   case{'MinIntImagSpec'}
    """    
    angle = np.arange(-180, 180, precision)
    spec.astype('complex')

    SPECS = []
    IntImagSpec = []
    for i in range(angle.size):
        Sp_try = spec*np.exp(-1j*angle[i]*np.pi/180)
        SPECS.append(Sp_try)
        IntImagSpec.append(np.abs(np.trapz(np.imag(Sp_try), x=ppmAxis)))
    IntImagSpec = np.array(IntImagSpec)
    # indice del minimo:
    idx = np.argmin(IntImagSpec)
    spec = SPECS[idx]
    ind_max = np.argmax(np.abs(np.real(spec)))
    if spec[ind_max] < 0:
        spec = -spec
    angle = angle[idx]
    return spec, angle
