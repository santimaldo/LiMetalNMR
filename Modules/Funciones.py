# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:57:23 2022

@author: santi
"""

import functools # para implementar el decorador timer
import time


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