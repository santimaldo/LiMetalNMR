#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:00:22 2020

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
from oct2py import Oct2Py

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
  funciones['cilindritos_dist_cte'] = cilindritos_dist_cte
  funciones['cilindrito_prueba'] = cilindrito_prueba
  funciones['cilindritos_inclinados'] = cilindritos_inclinados
  funciones['cilindritos_aleatorios_1'] = cilindritos_aleatorios_1
  funciones['cilindritos_aleatorios_2'] = cilindritos_aleatorios_2
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
  try:
    extra_info=geokwargs['extra_info']
  except KeyError:
    extra_info=False    
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
  lista_alturas = [1,2,3]
  if extra_info:
    return indices, lista_alturas
  else:
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
def cilindrito_prueba(N, voxelSize, **geokwargs):
  """ 2020-10-22
  Creo un cilindrito torcido de prueba. Inicialmente crece derecho en z y
  luego se tuerce en x  """   
  
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
  print(nsx)
  nsy = int(ancho/vsy)
  print(nsy)
 
  
  indices = []
  ind_x = int((Nmx - nsx)/2) 
  ind_y = int((Nmy - nsy)/2) 
  ind_z = 0
  n=0
  while ind_z < int(Nmz/2):
      for iy in range(nsy):
          for ix in range(nsx):
              if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                  indices.append((ind_z,ind_y+iy, ind_x+ix))
      ind_z+=1
      n+=1

  while ind_z < Nmz and ind_x < (Nmx-2*nsx):
      for iy in range(nsy):
              for ix in range(nsx):
                  if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                      indices.append((ind_z,ind_y+iy, ind_x+ix))
      ind_x+=1
      ind_z+=1
      n+=1
  return indices
    
##########################################################################

def cilindritos_inclinados(N, voxelSize, **geokwargs):
  """ 2021-01-21
  Es la generalización a distancia cte del cilindrito de prueba"""   
  
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
  print(nsx)
  nsy = int(ancho/vsy)
  print(nsy)
  ndx = int(distancia/vsx)
  print(ndx)
  ndy = int(distancia/vsy)
  print(ndy)
  
  
  indices = []
  
   
  n=0
  
  ind_x = 2*nsx 
  while ind_x <= (Nmx-2*nsx):
     ind_y = 2*nsy
     while ind_y<= (Nmy -2*nsy):
           ind_z = 0
           while ind_z < int(Nmz/2):    
              for iy in range(nsy):
                  for ix in range(nsx):
                      if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                          indices.append((ind_z,ind_y+iy, ind_x+ix))
                  n+=1
                  #print('n_arriba',n)
              ind_z+=1 
           ind_y+= nsy + ndy
           print(ind_y)
     ind_x+= nsx + ndx
  
  ind_x = 2*nsx     
  while ind_x <= (Nmx-2*nsx):  
      ind_y = 2*nsy
      while ind_y<= (Nmy -2*nsy):
          ind_suma=0
          ind_z = int(Nmz/2)
          while ind_z < Nmz and ind_x + ind_suma < (Nmx-2*nsx):
              for iy in range(nsy):
                  for ix in range(nsx):
                      if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                          indices.append((ind_z,ind_y+iy, ind_x+ix+ind_suma))
                  n+=1
                  #print('n_abajo',n)
              ind_suma+=1
                  
              
              ind_z+=1
          ind_y+= nsy + ndy
      ind_x+= nsx + ndx
  return indices

##############################################################################
def cilindritos_aleatorios_1(N, voxelSize, **geokwargs):
  """ 2021-01-21
  A los cilindritos inclinados les cambio el parámetro de altura a la
  que comienza a inclinarse el cilindro"""   
  
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
  print(nsx)
  nsy = int(ancho/vsy)
  print(nsy)
  ndx = int(distancia/vsx)
  print(ndx)
  ndy = int(distancia/vsy)
  print(ndy)
  
  
  indices = []
  
  Nz_random = []
   
  n=0
  
  ind_x = 2*nsx 
  while ind_x <= (Nmx-2*nsx):
     ind_y = 2*nsy
     while ind_y<= (Nmy -2*nsy):
           ind_z = 0
           Nz_rand = np.random.randint(0,N[0]+1)
           Nz_random.append(Nz_rand)
           #print(Nz_rand)
           while ind_z < Nz_rand:    
              for iy in range(nsy):
                  for ix in range(nsx):
                      if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                          indices.append((ind_z,ind_y+iy, ind_x+ix))
                  n+=1
                  #print('n_arriba',n)
              ind_z+=1 
           ind_y+= nsy + ndy
     ind_x+= nsx + ndx
  
  
  i=0
  ind_x = 2*nsx
  while ind_x <= (Nmx-2*nsx):  
          ind_y = 2*nsy
          while ind_y<= (Nmy -2*nsy):
              ind_suma=0
              ind_z = Nz_random[i]
              #print('ind_z',ind_z)
              while ind_z < Nmz and ind_x + ind_suma < (Nmx-2*nsx):
                  for iy in range(nsy):
                      for ix in range(nsx):
                          if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                              indices.append((ind_z,ind_y+iy, ind_x+ix+ind_suma))
                      n+=1
                      #print('n_abajo',n)
                  ind_suma+=1
                  
              
                  ind_z+=1
              ind_y+= nsy + ndy
              i=i+1
              #print('i',i)
          ind_x+= nsx + ndx
  return indices

##############################################################################
def cilindritos_aleatorios_2(N, voxelSize, **geokwargs):
  """ 2021-01-21
  A los cilindritos inclinados les cambio la dirección de forma aleatoria 
  siendo (y,x)--> con las posibilidades de crecimiento (0,0),(1,0),(0,1) y (1,1)
  también en valores negativos. Ademas secciono la altura z en 3 pedazos donde 
  el crecimiento cambia segun la sección"""   
  
  ancho = geokwargs['ancho']
  distancia = geokwargs['distancia']
  area = ancho*ancho
 
  Nmz,Nmy,Nmx = N
  print(N)
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar por cilindro 
  R = int(ancho/(2*vsx))
  print(R)
  nsx = int(ancho/vsx)
  print(nsx)
  nsy = int(ancho/vsy)
  print(nsy)
  ndx = int(distancia/vsx)
  print(ndx)
  ndy = int(distancia/vsy)
  print(ndy)
  
  #Esta geometría tiene 3 bloques en z donde los cilindros pueden o no cambiar 
  #la dirección de crecimiento. En el primer bloque los cilindros crecen derechos
  #hasta una altura Nz_random_1 que para cada cilindro toma valores random de 0
  #a Nz/3, luego en el segundo bloque tienen la posibilidad de inclinarse y frenar
  #a otra altura random Nz_random_2 y finalmente en el tercer bloque vuelven a tener
  #la posibilidad de inclinarse sin recordar la inclinación anterior necesariamente.
  
  indices = []
  
  Nz_random_1 = []
   
  n=0
  
  ind_x = 2*nsx 
  while ind_x <= (Nmx-2*nsx):
     ind_y = 2*nsy
     while ind_y<= (Nmy -2*nsy):
           ind_z = 0
           Nz_rand_1 = np.random.randint(0,int(N[0]/3)+1)
           Nz_random_1.append(Nz_rand_1)
           #print(Nz_rand)
           while ind_z < Nz_rand_1:    
              for iy in range(nsy):
                  for ix in range(nsx):
                      if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                          indices.append((ind_z,ind_y+iy, ind_x+ix))
              ind_z+=1 
           ind_y+= nsy + ndy
     ind_x+= nsx + ndx
  
  
  Nz_random_2 = []
  ind_x_lista = []
  ind_y_lista = []
  ind_suma_x_lista = []
  ind_suma_y_lista = []
  
  i=0
  ind_x = 2*nsx
  while ind_x <= (Nmx-2*nsx):  
          ind_y = 2*nsy
          while ind_y<= (Nmy -2*nsy):
              ind_suma_y=0
              ind_suma_x=0
              ind_z = Nz_random_1[i]
              ind_suma_rand_y= np.random.randint(0,3)-1
              ind_suma_rand_x= np.random.randint(0,3)-1
              print('ind_suma_rand_y',ind_suma_rand_y)
              #print('ind_z',ind_z)
              Nz_rand_2 = np.random.randint(ind_z,int(2*N[0]/3)+1)
              #Nz_random_2.append(Nz_rand_2)
              while ind_z < Nz_rand_2 and ind_x + ind_suma_x <= (Nmx-2*nsx) and ind_x + ind_suma_x >= 2*nsx and ind_y + ind_suma_y <= (Nmy-2*nsy) and ind_y + ind_suma_y >= 2*nsy:
                  for iy in range(nsy):
                      for ix in range(nsx):
                          if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                              indices.append((ind_z,ind_y+iy+ind_suma_y, ind_x+ix+ind_suma_x))
                          
                  ind_suma_x+= ind_suma_rand_x
                  ind_suma_y+= ind_suma_rand_y
                  print('ind_suma_y',ind_suma_y)
                  
              
                  ind_z+=1
              print('ind_y',ind_y)
              ind_y_lista.append(ind_y)                
              ind_suma_y_lista.append(ind_suma_y)
              print('ind_suma_y_lista',ind_suma_y)
              ind_suma_x_lista.append(ind_suma_x)
              print('ind_suma_x_lista',ind_suma_x)
              i=i+1
              print('i',i)
              print(ind_z)
              Nz_random_2.append(ind_z)
              ind_y+= nsy + ndy 
          print('ind_x',ind_x)
          ind_x_lista.append(ind_x)
          ind_x+= nsx + ndx
  j=0
  ind_x = ind_x_lista[j]
  while ind_x <= (Nmx-2*nsx):  
          ind_y = ind_y_lista[j]
          while ind_y<= (Nmy -2*nsy):
              ind_suma_y=ind_suma_y_lista[j]
              ind_suma_x=ind_suma_x_lista[j]
              ind_z = Nz_random_2[j]
              ind_suma_rand_y= np.random.randint(0,3)-1
              ind_suma_rand_x= np.random.randint(0,3)-1
              #print('ind_suma_rand_y',ind_suma_rand_y)
              #print('ind_z',ind_z)
              while ind_z < N[0] and ind_x + ind_suma_x <= (Nmx-2*nsx) and ind_x + ind_suma_x >= 2*nsx-1 and ind_y + ind_suma_y <= (Nmy-2*nsy) and ind_y + ind_suma_y >= 2*nsy-1:
                  for iy in range(nsy):
                      for ix in range(nsx):
                          if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                              indices.append((ind_z,ind_y+iy+ind_suma_y, ind_x+ix+ind_suma_x))
                      n+=1
                      #print('n_abajo',n)
                      
                  ind_suma_x+= ind_suma_rand_x
                  ind_suma_y+= ind_suma_rand_y
                  print('ind_suma_y',ind_suma_y)
                  
              
                  ind_z+=1
              ind_y+= nsy + ndy
              j=j+1
              print('j',j)
          ind_x+= nsx + ndx        
          
          
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
  Nz,Ny,Nx = N   
  voxelSize = np.array([1e-3,1e-3,1e-3])
  
  # 'geometria' es el nombre de la geometria que vamos a utilizar
  # 'constructor' es una FUNCION. Esa funcion es diferente de acuerdo a la geometria elegida

  geometria = 'cilindritos_aleatorios_2'
  constructor = funciones(geometria)
  # la funcion 'constructor' me devuelve las tuplas (ind_z, ind_y, ind_x) de los indices
  # en los cuales hay litio.
  tuplas = constructor(N, voxelSize, ancho=16e-3, distancia=20e-3)
  # tuplas = constructor(N, voxelSize, ancho=4e-3, distancia=3e-3) # para 'distancia_constante'
  tuplas, extra_info = constructor(N, voxelSize, ancho=4e-3, distancia=3e-3, extra_info=True) # para 'distancia_constante'
  # tuplas = constructor(N, voxelSize, ancho=20e-3, porcentaje=80) # para 'porcentaje_palos'


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
  tuplas_mask = constructor(N, voxelSize, R_max=50e-3 , R_min= 0)
  indices_mask = np.array(tuplas_mask).T
  indices_mask = np.ravel_multi_index(indices_mask, N)
  
  mask = np.zeros(N)   
  np.put(mask, indices_mask, 1)
  #finalmente el objeto con la mascara seria
  
  muestra_mask= muestra*mask
  
 
  #%%
  #muestra = muestra_mask
  plt.figure(50)
  plt.subplot(2,2,1)
  plt.title('corte en la mitad de x')
  plt.pcolormesh(muestra[:,:,128])
  plt.subplot(2,2,2)
  plt.title('corte en la mitad de y')
  plt.pcolormesh(muestra[:,128,:])
  plt.subplot(2,2,3)
  plt.title('corte en la mitad de z')
  plt.pcolormesh(muestra[60,:,:])
  plt.subplot(2,2,4)
  plt.title('corte en 3/4 de x')
  plt.pcolormesh(muestra[:,:,192])
  
  
  
  fig, axs = plt.subplots(2, 2)
  axs[0, 0].pcolormesh(muestra[:,:,220])
  axs[0, 0].set_title('Corte en x')
  axs[0, 1].pcolormesh(muestra[:,220,:])
  axs[0, 1].set_title('Corte en y')
  axs[1, 0].pcolormesh(muestra[int(N[0]/4),:,:])
  axs[1, 0].set_title('Corte a un cuarto de z')
  axs[1, 1].pcolormesh(muestra[int(3*N[0]/4),:,:])
  axs[1, 1].set_title('Corte a tres cuartos de z')

  for ax in axs.flat:
    ax.set(xlabel=' ', ylabel=' ')

# Hide x labels and tick labels for top plots and y ticks for right plots.
  for ax in axs.flat:
    ax.label_outer()
  
    
  
  plt.figure(52)
  plt.pcolormesh(muestra[int(N[0]/4),:,:])
  
  plt.figure(53)
  plt.pcolormesh(muestra[:,41,:])
  
  plt.figure(54)
  plt.pcolormesh(muestra[int(3*N[0]/4),:,:])
  # #%%
  
  # #muestra_con_mascara = muestra*mask
  # #muestra = muestra_con_mascara
  # # #Gráfico #3D
  # fig = plt.figure(60)
  # ax = fig.gca(projection='3d')
  # x = np.linspace(0,99,100)
  # ax.voxels(muestra, facecolors='k', edgecolor='k')
#%%
#%%
  
  tmpvol =np.zeros((Nz+5,Ny,Nx))
  tmpvol[1:-4,:,:] = muestra
  tmpvol[0,:,:] = 1
  filename = './tmp.stl'
  with Oct2Py() as oc:
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Creando figura 3D. Esto puede demorar varios minutos...")
    fv = oc.isosurface(tmpvol, 0.5) # Make patch w. faces "out"
    oc.stlwrite(filename,fv)        # Save to binary .stl
  print("       Listo!") 
  print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")


plt.show()
