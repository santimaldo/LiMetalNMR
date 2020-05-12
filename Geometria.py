#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:00:22 2020

@author: santi
"""
import numpy as np

def funciones(geometria):
  """
  toma la geometria, un strig, y elige la funcion
  """
  
  funciones = {}
  funciones['bulk'] = bulk
  funciones['spikes'] = spikes
  if geometria in funciones:
    return funciones[geometria]
  else:
    mensaje= "\n ============WARNING=====================\
             \n La geometria solicitada no se encuentra.\
             \n Por las dudas, te devuelvo un BULK.\
             \n ========================================"
    print(mensaje)
    return funciones['bulk']
    
  

#------------------------------------------------------------------------------
def bulk(N, voxelSize):
  """
  es una funcion que devuelve las tuplas con los indices de todos los elementos
  de una matriz Nmz*Nmy*Nmx
  """
  Nmz,Nmy,Nmx = N
  
  indices = []
  for k in range(Nmz):
    for j in range(Nmy):
      for i in range(Nmx):
        indices.append((k,j,i))
  return indices
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def spikes(N, voxelSize, **geokwargs):
  """
  dendritas de en sentido vertical, apoyadas sobre la superficie
  """
  # extraigo los geokwargs:
  ancho = geokwargs['ancho']
  p = geokwargs['p']
  
  Nmz,Nmy,Nmx = N
  vsz, vsy, vsx = voxelSize
  
  # ancho_spikes
  area_spikes = (ancho)**2
  area = (Nmx*vsx)*(Nmy*vsy)
  # si todas las spikes estuvieran separadas, entonces la proporcion cubierta
  # seria p = (Ns*area_spikes)/area. Donde Ns es el numero de spikes. 
  # Como las spikes si se pueden solapar, entonces esto es una aproximacion.
  # Numerp de spikes:
  Ns = p*area/area_spikes
  
  # cuantos voxels debo usar
  nsx = int(ancho/vsx)
  nsy = int(ancho/vsy) 
  
  indices = []
  ns = 0
  while ns < Ns:
    # elijo al azar donde arranca el spike. restando nsx y nsy hago que no se 
    # pase del borde
    ind_x = np.random.randint(0,Nmx+1-nsx)
    ind_y = np.random.randint(0,Nmy+1-nsy)
    
    for iz in range(Nmz):
      for iy in range(nsy):
        for ix in range(nsx):
          indices.append((iz,ind_y+iy, ind_x+ix))
    ns+=1
  return indices
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


#class test(object):
#  def __init__(self, geometria='bulk', N=[16,16,16], voxelSize=[1,1,1], **geokwargs):
#    
#    self.N = N
#    self.voxelSize = voxelSize
#    self.func = funciones(geometria)
#    
#    self.method(**geokwargs)
#  
#  def method(self, **geokwargs):
#    
#    self.func(self.N, self.voxelSize, **geokwargs)
#    
#    return 0
    
    
if __name__=='__main__':
  """
  script para testear las geometrias
  """
  
  N = np.array([64, 64, 64])
  voxelSize = np.array([1e-3,1e-3,1e-3])
  
  geometria = 'spikes'
  constructor = funciones(geometria)
  
  tuplas = constructor(N, voxelSize, ancho=3e-3, p=0.20)
  
  indices = np.array(tuplas).T
  # convierto a indices planos
  indices = np.ravel_multi_index(indices, N)
   
  muestra_flat = np.zeros(N)
  # el constructor me da una lista de indices flattened
  #  put(array       , indices, valor)
  np.put(muestra_flat, indices, 1)
  # convierto en 3d array
  muestra = np.reshape(muestra_flat, N)
  
  #%%
  plt.figure(987654321)
  plt.subplot(2,2,1)
  plt.title('corte en la mitad de x')
  plt.pcolormesh(muestra[:,:,int(N[2]/2)])
  plt.subplot(2,2,2)
  plt.title('corte en la mitad de y')
  plt.pcolormesh(muestra[:,int(N[1]/2),:])
  plt.subplot(2,2,3)
  plt.title('corte en la mitad de z')
  plt.pcolormesh(muestra[int(N[0]/2),:,:])
  plt.subplot(2,2,4)
  plt.title('corte en 3/4 de x')
  plt.pcolormesh(muestra[:,:,int(N[2]*3/4)])
  
  
  
  
  