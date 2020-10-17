#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:00:22 2020

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt

def funciones(geometria):
  """
  toma la geometria, un string, y elige la funcion
  """
  
  funciones = {}
  funciones['bulk'] = bulk
  funciones['sticks'] = sticks
  funciones['arranged_sticks'] = arranged_sticks
  funciones['trapped_arranged_sticks'] = trapped_arranged_sticks
  funciones['distancia_constante'] = distancia_constante
  funciones['mask_1'] = mask_1
  funciones['cilindritos_dist_cte'] = cilindritos_dist_cte
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
def sticks(N, voxelSize, **geokwargs):
  """
  dendritas de en sentido vertical, apoyadas sobre la superficie
  """
  # extraigo los geokwargs:
  ancho = geokwargs['ancho']
  p = geokwargs['p']
  
  Nmz,Nmy,Nmx = N
  vsz, vsy, vsx = voxelSize
  
  # ancho_sticks
  area_sticks = (ancho)**2
  area = (Nmx*vsx)*(Nmy*vsy)
  # si todas las sticks estuvieran separadas, entonces la proporcion cubierta
  # seria p = (Ns*area_sticks)/area. Donde Ns es el numero de sticks. 
  # Como las sticks si se pueden solapar, entonces esto es una aproximacion.
  # Numerp de sticks:
  Ns = p*area/area_sticks
  
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


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def arranged_sticks(N, voxelSize, **geokwargs):
  """
  2020-06-09
  dendritas de 3x3 um2 en sedntido vertical, apoyadas sobre la superficie
  ordenadas en un arreglo cuadrado:
          x    x    x    x    
          
          x    x    x    x
          
          x    x    x    x
          
          x    x    x    x
  la idea es usarlo con N=[Nmz, 28, 28] y voxelsize de 1 um
  """
  # extraigo los geokwargs:
  ancho = 3e-3 # mm
  
  Nmz,Nmy,Nmx = N
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar
  nsx = int(ancho/vsx)
  nsy = int(ancho/vsy) 
  
  
  indices = []
  Nd_f = 4 # numero de dendritas por fila
  ind_x = 3
  for ii in range(Nd_f):
    ind_y = 3
    for jj in range(Nd_f):   
      for iz in range(Nmz):
        for iy in range(nsy):
          for ix in range(nsx):
            indices.append((iz,ind_y+iy, ind_x+ix))
      ind_y+=6
    ind_x+=6
  return indices
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def trapped_arranged_sticks(N, voxelSize, **geokwargs):
  """
  2020-06-09
  dendritas de 3x3 um2 en sedntido vertical, apoyadas sobre la superficie
  ordenadas en un arreglo cuadrado, atrapadas entre estructra grande: 30 y 31 um
  de ancho rodeando el arreglo. la region del arreglo debe ser 27x27 en xy
  la idea es usarlo con N=[Nmz, 88, 88] y voxelsize de 1 um
  """
  # extraigo los geokwargs:
  try:
    paredes = geokwargs['paredes']
  except:
    paredes = True
    
  ancho = 3e-3 # mm
  
  Nmz,Nmy,Nmx = N
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar
  nsx = int(ancho/vsx)
  nsy = int(ancho/vsy) 
  
  
  indices = []
  Nd_f = 4 # numero de dendritas por fila
  ind_x = 33
  for ii in range(Nd_f):
    ind_y = 33
    for jj in range(Nd_f):   
      for iz in range(Nmz):
        for iy in range(nsy):
          for ix in range(nsx):
            indices.append((iz,ind_y+iy, ind_x+ix))
      ind_y+=6
    ind_x+=6

  if paredes==True:    
    # agrego las partes grandes:
    # primero la s paredes que va de 0 a 30 & de 57 al final en x
    # i.e las paredes y  
    for iz in range(Nmz):
      for iy in range(Nmy-1):
        for ix in range(30):        
              indices.append((iz,iy,ix))
              indices.append((iz,iy,ix+57))
        ix+=1
      iy+=1
    iz+=1
    
    # luego las paredse en x
    for iz in range(Nmz):
      for iy in range(30):
        for ix in range(27):        
              indices.append((iz,iy,ix+30))
              indices.append((iz,iy+57,ix+30))
        ix+=1
      iy+=1
    iz+=1
  
  return indices
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def distancia_constante(N, voxelSize, **geokwargs):
  """
  2020-09-07
  dendritas de anchoXancho um2 en sedntido vertical, apoyadas sobre la superficie
  ordenadas en un arreglo cuadrado, con distancias constantes
          x    x    x    x    
          
          x    x    x    x
          
          x    x    x    x
          
          x    x    x    x
  """
  # extraigo los geokwargs:
  ancho = geokwargs['ancho']
  distancia = geokwargs['distancia']
  area = ancho*ancho
  
  Nmz,Nmy,Nmx = N
  print(N)
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar
  nsx = int(ancho/vsx)
  nsy = int(ancho/vsy)
  # distancia en voxels:
  ndx = int(distancia/vsx)
  ndy = int(distancia/vsy)
  
  
  indices = []
  Nd_f = 4 # numero de dendritas por fila
  ind_x = nsx # dejo un ancho de distancia hasta el borde
  ii = jj = 0
  n = 0
  while ind_x<=(Nmx-2*nsx):      
    ind_y = nsy
    while ind_y<=(Nmy-2*nsy):
      for iz in range(Nmz):
        for iy in range(nsy):
          for ix in range(nsx):
            indices.append((iz,ind_y+iy, ind_x+ix))
      ind_y+= ndy+nsy
      n+=1
    ind_x+= ndx+nsx
  print('Area cubierta por dendritas: {}  um2'.format(n*area))
  return indices
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def mask_1(N, voxelSize, **geokwargs):
 """
  2020-10-08
  Intento de máscara con forma de anillo, dando distintas alturas en z 
 """
 # extraigo los geokwargs:
 Rmax = geokwargs['R_max']
 Rmin = geokwargs['R_min']
 vs= voxelSize[0]
  
 Nmz,Nmy,Nmx = N
 
 
 indices = []
 
 ind_x = 0
 ind_y = 0
 ind_z = 0

 ind_Rm = int(Rmin/vs)
 ind_RM = int(Rmax/vs)

 for ind_y in range(Nmy):
     for ind_x in range(Nmx):
         if (ind_x-Nmx/2)**2 + (ind_y-Nmy/2)**2 > ind_Rm**2 and (ind_x-Nmx/2)**2 + (ind_y-Nmy/2)**2 < ind_RM**2: 
             for iz in range(Nmz):
                 indices.append((iz, ind_y, ind_x))
 return indices     


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def cilindritos_dist_cte(N, voxelSize, **geokwargs):
  """ 2020-10-16
  Creo cilindritos a distancia constante entre sí, la idea es que el 
  parámetro ancho sea el diametro del cilindro   """  
 
  ancho = geokwargs['ancho']
  distancia = geokwargs['distancia']
  area = ancho*ancho
 
  Nmz,Nmy,Nmx = N
  print(N)
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar por cilindro aproximadamente
  R = int(ancho/(2*vsx))
  print(R)
  nsx = int(ancho/vsx)
  nsy = int(ancho/vsy)
  # distancia en voxels entre los cilindros:
  ndx = int(distancia/vsx)
  ndy = int(distancia/vsy)
  
  
  indices = []
  ind_x = 2*nsx # dejo un ancho de distancia hasta el borde
  n = 0
  while ind_x<=(Nmx-2*nsx):      
    ind_y = 2*nsy
    while ind_y<=(Nmy-2*nsy):
      for iy in range(nsy):
          for ix in range(nsx):
              if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                  for iz in range(Nmz):
                      indices.append((iz,ind_y+iy, ind_x+ix))
      ind_y+= ndy+nsy
      n+=1
    ind_x+= ndx+nsx
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
#    return 
  
if __name__=='__main__':
  """
  script para testear las geometrias
  """
  # este N es el N de la muestra ejemplo
  N = np.array([128,256,256])    
  voxelSize = np.array([1e-3,1e-3,1e-3])
  
  # 'geometria' es el nombre de la geometria que vamos a utilizar
  # 'constructor' es una FUNCION. Esa funcion es diferente de acuerdo a la geometria elegida
  geometria = 'cilindritos_dist_cte'
  constructor = funciones(geometria)
  
  # la funcion 'constructor' me devuelve las tuplas (ind_z, ind_y, ind_x) de los indices
  # en los cuales hay litio.
  tuplas = constructor(N, voxelSize, ancho=16e-3, distancia=20e-3)
  
  # convierto a indices planos
  indices = np.array(tuplas).T  
  indices = np.ravel_multi_index(indices, N)
  
  # creo la matriz vacia, y coloco 1 en los indices que me da el constructor
  muestra = np.zeros(N)
  #  put(array       , indices, valor)
  np.put(muestra, indices, 1)
  
  #intento de crear la máscara
  mascara = 'mask_1'
  constructor = funciones(mascara)
  tuplas_mask = constructor(N, voxelSize, R_max=40e-3 , R_min= 10e-3)
  indices_mask = np.array(tuplas_mask).T
  indices_mask = np.ravel_multi_index(indices_mask, N)
  
  mask = np.zeros(N)   
  np.put(mask, indices_mask, 1)
  #finalmente el objeto con la mascara seria
  
  muestra_mask= muestra*mask
  
 
  #%%
  #muestra = muestra_mask
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
  