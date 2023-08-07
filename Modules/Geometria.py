#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:00:22 2020

@author: santi
"""
import numpy as np

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
  funciones['cilindritos_aleatorios_3'] = cilindritos_aleatorios_3
  funciones['cilindros_hexagonal'] = cilindros_hexagonal
  funciones['clusters_hexagonal'] = clusters_hexagonal
  funciones['clusters_hexagonal_SinCeldaUnidad'] = clusters_hexagonal_SinCeldaUnidad
  funciones['cilindros_aleatorios_hexagonal'] = cilindros_aleatorios_hexagonal
  funciones['cilindros_45grados_hexagonal'] = cilindros_45grados_hexagonal
  funciones['cilindros_p_random2'] = cilindros_p_random2
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
  No hay microestructuras
  """
  return None

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
  lista_alturas = [1,2,3]
  if extra_info:
    return indices, lista_alturas
  else:
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
              #print('ind_suma_rand_y',ind_suma_rand_y)
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
                  #print('ind_suma_y',ind_suma_y)
                  
              
                  ind_z+=1
              #print('ind_y',ind_y)
              ind_y_lista.append(ind_y)                
              ind_suma_y_lista.append(ind_suma_y)
              #print('ind_suma_y_lista',ind_suma_y)
              ind_suma_x_lista.append(ind_suma_x)
              #print('ind_suma_x_lista',ind_suma_x)
              i=i+1
              #print('i',i)
              #print(ind_z)
              Nz_random_2.append(ind_z)
              ind_y+= nsy + ndy 
          #print('ind_x',ind_x)
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
                  #print('ind_suma_y',ind_suma_y)
                  
              
                  ind_z+=1
              ind_y+= nsy + ndy
              j=j+1
              #print('j',j)
          ind_x+= nsx + ndx        
          
  lista_alturas = [1,2,3]
  if extra_info:
    return indices, lista_alturas
  else:
    return indices

 ##############################################################################
def cilindritos_aleatorios_3(N, voxelSize, **geokwargs):
  """ 2021-01-21
  A los cilindritos inclinados les cambio la dirección de forma aleatoria 
  siendo (y,x)--> con las posibilidades de crecimiento (0,0),(1,0),(0,1) y (1,1)
  también en valores negativos. Ademas secciono la altura z en 3 pedazos donde 
  el crecimiento cambia segun la sección"""   
  #lo único que cambio de cilindritos_aleatorios_2 es que fijo la distancia 
  #entre cilindritos sin importar el ancho de estos
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
           ind_y+= ndy 
     ind_x+= ndx 
  
  
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
              #print('ind_suma_rand_y',ind_suma_rand_y)
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
                  #print('ind_suma_y',ind_suma_y)
                  
              
                  ind_z+=1
              #print('ind_y',ind_y)
              ind_y_lista.append(ind_y)                
              ind_suma_y_lista.append(ind_suma_y)
              #print('ind_suma_y_lista',ind_suma_y)
              ind_suma_x_lista.append(ind_suma_x)
              #print('ind_suma_x_lista',ind_suma_x)
              i=i+1
              #print('i',i)
              #print(ind_z)
              Nz_random_2.append(ind_z)
              ind_y+= ndy 
          #print('ind_x',ind_x)
          ind_x_lista.append(ind_x)
          ind_x+= ndx 
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
                  #print('ind_suma_y',ind_suma_y)
                  
              
                  ind_z+=1
              ind_y+= ndy 
              j=j+1
              #print('j',j)
          ind_x+= ndx        
          
  lista_alturas = [1,2,3]
  if extra_info:
    return indices, lista_alturas
  else:
    return indices

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def cilindros_hexagonal(N, voxelSize, **geokwargs):
  """ 2021-06-12
  Creo cilindritos a distancia constante entre sí. Es decir, en un arreglo
  hexagonal. La distancia se define centro a centro.
  
  Los parametros no son independientes, sino que tienen que cumplir ciertos
  requisitos. A saber:
    
    Nmx = n * d    ,  con n entero
    Nmy = m * 2a   ,  con m entero
  
  pero ademas, el parametro a debe ser tal que minimice el error de discretizar
  d y a en la relacion:
    
    (d/2)**2 + a**2  = d**2
    
  En la carpeta DataBases, el archivo 'Hexagonal_parametro_a.dat', tiene los
  valores de a optimos para cada d.
  
  d DEBE SER PAR
  """  
  
  radio = geokwargs['radio'] # debe estar en unidad de milimetros
  distancia = geokwargs['distancia'] 
  parametro_a = geokwargs['parametro_a']
  
 
  Nmz,Nmy,Nmx = N  
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar por cilindro aproximadamente
  R = int(radio/vsx)
  d = int(distancia/vsx)
  a = int(parametro_a/vsx)


  centros_CU = [(0,0),(0,d),(a,d/2),(2*a,0),(2*a,d)]

  Nceldas_x = int(Nmx/d)
  Nceldas_y = int(Nmy/(2*a))
  
  indices = []  
  R2 = R**2
  for centro in centros_CU:
    yc, xc = centro
    xc = xc-0.5
    yc = yc-0.5      
    # recorro la celda unidad
    for ind_x in range(d):      
      for ind_y in range(2*a):
        # solo guardo los xy del cilindro            
        if (ind_x-xc)**2 +(ind_y-yc)**2 < R2:
          # recorro en altura
          for ind_z in range(Nmz):
            # agrego las demas celdas en x, y
            for icx in range(Nceldas_x):
              for icy in range(Nceldas_y):                
                indices.append((ind_z,ind_y+icy*2*a, ind_x+icx*d))
  return indices
  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def clusters_hexagonal(N, voxelSize, **geokwargs):
  """ 2021-06-13
  Creo  clusters de palitos que forman cilindritos a distancia constante entre sí.
  Es decir, en un arreglo hexagonal. La distancia se define centro a centro. 
  
  Los parametros no son independientes, sino que tienen que cumplir ciertos
  requisitos. A saber:
    
    Nmx = n * d    ,  con n entero
    Nmy = m * 2a   ,  con m entero
  
  pero ademas, el parametro a debe ser tal que minimice el error de discretizar
  d y a en la relacion:
    
    (d/2)**2 + a**2  = d**2
    
  En la carpeta DataBases, el archivo 'Hexagonal_parametro_a.dat', tiene los
  valores de a optimos para cada d.
  
  d DEBE SER PAR
  """  
  
  radio = geokwargs['radio']
  distancia = geokwargs['distancia']
  parametro_a = geokwargs['parametro_a']
  try:
    p_huecos = geokwargs['p_huecos']
  except:
    p_huecos = 0.5
  
  
 
  Nmz,Nmy,Nmx = N  
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar por cilindro aproximadamente
  R = int(radio/vsx)
  d = int(distancia/vsx)
  a = int(parametro_a/vsx)


  centros_CU = [(0,0),(0,d),(a,d/2),(2*a,0),(2*a,d)]

  Nceldas_x = int(Nmx/d)
  Nceldas_y = int(Nmy/(2*a))
  
  indices = []  
  R2 = R**2
  for centro in centros_CU:
    yc, xc = centro
    xc = xc-0.5
    yc = yc-0.5      
    # recorro la celda unidad
    for ind_x in range(d):      
      for ind_y in range(2*a):
        # solo guardo los xy del cilindro            
        if (ind_x-xc)**2 +(ind_y-yc)**2 < R2:
          # recorro en altura
          if np.random.rand()>p_huecos:                
            for ind_z in range(Nmz):
              # agrego las demas celdas en x, y
              for icx in range(Nceldas_x):
                for icy in range(Nceldas_y):                
                    indices.append((ind_z,ind_y+icy*2*a, ind_x+icx*d))
  return indices

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def clusters_hexagonal_SinCeldaUnidad(N, voxelSize, R_hueco_central=0, **geokwargs):
  """ 2022-07-22
  Creo  clusters de palitos que forman cilindritos a distancia constante entre sí.
  Es decir, en un arreglo hexagonal. La distancia se define centro a centro. 
  
  Los parametros no son independientes, sino que tienen que cumplir ciertos
  requisitos. A saber:
    
    Nmx = n * d    ,  con n entero
    Nmy = m * 2a   ,  con m entero
  
  pero ademas, el parametro a debe ser tal que minimice el error de discretizar
  d y a en la relacion:
    
    (d/2)**2 + a**2  = d**2
    
  En la carpeta DataBases, el archivo 'Hexagonal_parametro_a.dat', tiene los
  valores de a optimos para cada d.
  
  d DEBE SER PAR
  
  tiene un porcentaje de huecos 
  """  
  
  radio = geokwargs['radio']
  distancia = geokwargs['distancia']
  parametro_a = geokwargs['parametro_a']
  try:
    p_huecos = geokwargs['p_huecos']
  except:
    p_huecos = 0.2
  
  
 
  Nmz,Nmy,Nmx = N  
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar por cilindro aproximadamente
  R = int(radio/vsx)
  d = int(distancia/vsx)
  a = int(parametro_a/vsx)

  
  ## vectores base:
  v0 = np.array((0,d  )) # horizontal
  v1 = np.array((a,d/2)) # diagonal
  


  Nceldas_x =Nmx//d
  Nceldas_y =Nmy//(2*a)

  print(Nceldas_x, Nceldas_y)
  
  indices = []  
  R2 = R**2
  Rh2 = (R_hueco_central//vsz)**2
  
  for ii in np.arange(-Nceldas_x,Nceldas_x+2):
    for jj in np.arange(-(2*Nceldas_y),(2*Nceldas_y)+2):                        
      yc, xc = ii*v0+jj*v1
      # controlo:----------------
      if xc<0 or yc<0 or xc>Nmx or yc>Nmy:
        continue
      elif (xc-Nmx/2)**2 +(yc-Nmy/2)**2 < Rh2:
        continue
      #--------------------------
      xc = xc-0.5
      yc = yc-0.5 
      # recorro alrededores del centro
      for ind_x in range(int(xc-R-2),int(xc+R+2)):      
        for ind_y in range(int(yc-R-2),int(yc+R+2)):
          if ind_x<0 or ind_y<0 or ind_x>=Nmx or ind_y>=Nmy:
            continue
          # solo guardo los xy del cilindro            
          if (ind_x-xc)**2 +(ind_y-yc)**2 < R2:
            # recorro en altura         
            if np.random.rand()>p_huecos:                
              for ind_z in range(Nmz):                
                indices.append((ind_z,ind_y, ind_x))

  return indices
  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def cilindros_aleatorios_hexagonal(N, voxelSize, **geokwargs):
  """ 2021-06-13
  Creo cilindritos a distancia constante entre sí. Es decir, en un arreglo
  hexagonal. La distancia se define centro a centro.
  Además, los cilindros toman direcciones aleatorias:
  A los cilindritos inclinados les cambio la dirección de forma aleatoria 
  siendo (y,x)--> con las posibilidades de crecimiento (0,0),(1,0),(0,1) y (1,1)
  también en valores negativos. Ademas secciono la altura z en 3 pedazos donde 
  el crecimiento cambia segun la sección
  
  Los parametros no son independientes, sino que tienen que cumplir ciertos
  requisitos. A saber:
    
    Nmx = n * d    ,  con n entero
    Nmy = m * 2a   ,  con m entero
  
  pero ademas, el parametro a debe ser tal que minimice el error de discretizar
  d y a en la relacion:
    
    (d/2)**2 + a**2  = d**2
    
  En la carpeta DataBases, el archivo 'Hexagonal_parametro_a.dat', tiene los
  valores de a optimos para cada d.
  
  d DEBE SER PAR
  
  """  
  
  radio = geokwargs['radio']
  distancia = geokwargs['distancia']
  parametro_a = geokwargs['parametro_a']
  
 
  Nmz,Nmy,Nmx = N  
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar por cilindro aproximadamente
  R = int(radio/vsx)
  d = int(distancia/vsx)
  a = int(parametro_a/vsx)

                
  #Esta geometría tiene 3 bloques en z donde los cilindros pueden o no cambiar 
  #la dirección de crecimiento. En el primer bloque los cilindros crecen derechos
  #hasta una altura Nz_random_1 que para cada cilindro toma valores random de 0
  #a Nz/3, luego en el segundo bloque tienen la posibilidad de inclinarse y frenar
  #a otra altura random Nz_random_2 y finalmente en el tercer bloque vuelven a tener
  #la posibilidad de inclinarse sin recordar la inclinación anterior necesariamente.


  # CREO LOS CENTROS DEL ARREGLO HEXAGONAL.  - - - - - - - - - - - - - - - - - 
  Ncentros_x = int(Nmx/d + 1)
  Ncentros_y = int(Nmy/a + 1)
  centros = []
  for iy in range(Ncentros_y):
    if iy%2==0:
      for ix in range(Ncentros_x):
        centros.append((a*iy, d*ix))
    else:
      for ix in range(Ncentros_x):
        centros.append((a*iy, d*ix+d/2))
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  
  indices = [] 
  R2 = R**2
  for centro in centros:
    ind_yc, ind_xc = centro
    xc = ind_xc - 0.5
    yc = ind_yc - 0.5
    ind_xc = int(xc)
    ind_yc = int(yc)
    
    # alturas de quiebre
    Nz_rand1 = np.random.randint(0,Nmz+1)
    Nz_rand2 = np.random.randint(Nz_rand1,Nmz+1)
    Nz_rand3 = np.random.randint(Nz_rand2,Nmz+1)
    
    # direcciones de desviacion (j,i), con ij= -1,0,1.
    dir1 = (0,0)
    dir2 = (np.random.randint(-1,2),np.random.randint(-1,2))
    dir3 = (np.random.randint(-1,2),np.random.randint(-1,2))
    for ind_y in range(ind_yc-R,ind_yc+R+1):
      for ind_x in range(ind_xc-R,ind_xc+R+1):      
        if (ind_x-xc)**2 + (ind_y-yc)**2 < R2:          
          ix = ind_x; iy = ind_y                   
          #------------------------------------------primer tramo
          for ind_z in range(Nz_rand1):    
             indices.append((ind_z,int(iy%Nmy), int(ix%Nmx))) # guardo modulo Nm para imponer condiciones periodicas
          #------------------------------------------segundo tramo                        
          for ind_z in range(Nz_rand1, Nz_rand2):
            iy += dir2[0]                          
            ix += dir2[1]              
            indices.append((ind_z,int(iy%Nmy), int(ix%Nmx))) # guardo modulo Nm para imponer condiciones periodicas
          #------------------------------------------tercer tramo
          for ind_z in range(Nz_rand2, Nmz):
            iy += dir3[0]                          
            ix += dir3[1]              
            indices.append((ind_z,int(iy%Nmy), int(ix%Nmx))) # guardo modulo Nm para imponer condiciones periodicas
                
  return indices

#------------------------------------------------------------------------------  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def cilindros_45grados_hexagonal(N, voxelSize, **geokwargs):
  """ 2023-08-07
  Creo cilindritos a distancia constante entre sí. Es decir, en un arreglo
  hexagonal. La distancia se define centro a centro.
  Además, los cilindros toman direcciones aleatorias:
  A los cilindritos inclinados a 45 grados en la direccion x
  también en valores negativos. Ademas secciono la altura z en 3 pedazos donde 
  el crecimiento cambia segun la sección
  
  Los parametros no son independientes, sino que tienen que cumplir ciertos
  requisitos. A saber:
    
    Nmx = n * d    ,  con n entero
    Nmy = m * 2a   ,  con m entero
  
  pero ademas, el parametro a debe ser tal que minimice el error de discretizar
  d y a en la relacion:
    
    (d/2)**2 + a**2  = d**2
    
  En la carpeta DataBases, el archivo 'Hexagonal_parametro_a.dat', tiene los
  valores de a optimos para cada d.
  
  d DEBE SER PAR
  
  """  
  
  radio = geokwargs['radio']
  distancia = geokwargs['distancia']
  parametro_a = geokwargs['parametro_a']
  
 
  Nmz,Nmy,Nmx = N  
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar por cilindro aproximadamente
  R = int(radio/vsx)
  d = int(distancia/vsx)
  a = int(parametro_a/vsx)

                  
  # CREO LOS CENTROS DEL ARREGLO HEXAGONAL.  - - - - - - - - - - - - - - - - - 
  Ncentros_x = int(Nmx/d + 1)
  Ncentros_y = int(Nmy/a + 1)
  centros = []
  for iy in range(Ncentros_y):
    if iy%2==0:
      for ix in range(Ncentros_x):
        centros.append((a*iy, d*ix))
    else:
      for ix in range(Ncentros_x):
        centros.append((a*iy, d*ix+d/2))
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  
  indices = [] 
  R2 = R**2
  for centro in centros:
    ind_yc, ind_xc = centro
    xc = ind_xc - 0.5
    yc = ind_yc - 0.5
    ind_xc = int(xc)
    ind_yc = int(yc)
        
    # direccion de desviacion (j,i), con ij= -1,0,1. Convencion (y,x)
    dir1 = (0,1)    
    for ind_y in range(ind_yc-R,ind_yc+R+1):
      for ind_x in range(ind_xc-R,ind_xc+R+1):      
        if (ind_x-xc)**2 + (ind_y-yc)**2 < R2:          
          ix = ind_x; iy = ind_y                             
          for ind_z in range(Nmz):
            iy += dir1[0]                          
            ix += dir1[1]              
            indices.append((ind_z,int(iy%Nmy), int(ix%Nmx))) # guardo modulo Nm para imponer condiciones periodicas          
                
  return indices  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def cilindros_aleatorios_hexagonal_SinCeldaUnidad(N, voxelSize, **geokwargs):
  """ 2021-06-13
  Creo cilindritos a distancia constante entre sí. Es decir, en un arreglo
  hexagonal. La distancia se define centro a centro.
  Además, los cilindros toman direcciones aleatorias:
  A los cilindritos inclinados les cambio la dirección de forma aleatoria 
  siendo (y,x)--> con las posibilidades de crecimiento (0,0),(1,0),(0,1) y (1,1)
  también en valores negativos. Ademas secciono la altura z en 3 pedazos donde 
  el crecimiento cambia segun la sección
  
  Los parametros no son independientes, sino que tienen que cumplir ciertos
  requisitos. A saber:
    
    Nmx = n * d    ,  con n entero
    Nmy = m * 2a   ,  con m entero
  
  pero ademas, el parametro a debe ser tal que minimice el error de discretizar
  d y a en la relacion:
    
    (d/2)**2 + a**2  = d**2
    
  En la carpeta DataBases, el archivo 'Hexagonal_parametro_a.dat', tiene los
  valores de a optimos para cada d.
  
  d DEBE SER PAR
  
  """  
  
  radio = geokwargs['radio']
  distancia = geokwargs['distancia']
  parametro_a = geokwargs['parametro_a']
  
 
  Nmz,Nmy,Nmx = N  
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar por cilindro aproximadamente
  R = int(radio/vsx)
  d = int(distancia/vsx)
  a = int(parametro_a/vsx)

                
  #Esta geometría tiene 3 bloques en z donde los cilindros pueden o no cambiar 
  #la dirección de crecimiento. En el primer bloque los cilindros crecen derechos
  #hasta una altura Nz_random_1 que para cada cilindro toma valores random de 0
  #a Nz/3, luego en el segundo bloque tienen la posibilidad de inclinarse y frenar
  #a otra altura random Nz_random_2 y finalmente en el tercer bloque vuelven a tener
  #la posibilidad de inclinarse sin recordar la inclinación anterior necesariamente.


  # CREO LOS CENTROS DEL ARREGLO HEXAGONAL.  - - - - - - - - - - - - - - - - - 
  Ncentros_x = int(Nmx/d + 1)
  Ncentros_y = int(Nmy/a + 1)
  centros = []
  for iy in range(Ncentros_y):
    if iy%2==0:
      for ix in range(Ncentros_x):
        centros.append((a*iy, d*ix))
    else:
      for ix in range(Ncentros_x):
        centros.append((a*iy, d*ix+d/2))
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  ## vectores base:
  v0 = np.array((0,d  )) # horizontal
  v1 = np.array((a,d/2)) # diagonal

  Nceldas_x =Nmx//d
  Nceldas_y =Nmy//(2*a)

  print(Nceldas_x, Nceldas_y)
  
  indices = []  
  R2 = R**2
  
  for ii in np.arange(-Nceldas_x,Nceldas_x+2):
    for jj in np.arange(-(2*Nceldas_y),(2*Nceldas_y)+2):                        
      yc, xc = ii*v0+jj*v1
      # controlo:----------------
      if xc<0 or yc<0 or xc>Nmx or yc>Nmy:
        continue
      #--------------------------
      xc = xc-0.5
      yc = yc-0.5 
      # recorro alrededores del centro
      # alturas de quiebre
      Nz_rand1 = np.random.randint(0,Nmz+1)
      Nz_rand2 = np.random.randint(Nz_rand1,Nmz+1)
      Nz_rand3 = np.random.randint(Nz_rand2,Nmz+1)
      
      # direcciones de desviacion (j,i), con ij= -1,0,1.
      dir1 = (0,0)
      dir2 = (np.random.randint(-1,2),np.random.randint(-1,2))
      dir3 = (np.random.randint(-1,2),np.random.randint(-1,2))
      for ind_y in range(ind_yc-R,ind_yc+R+1):
        for ind_x in range(ind_xc-R,ind_xc+R+1):      
          if (ind_x-xc)**2 + (ind_y-yc)**2 < R2:          
            ix = ind_x; iy = ind_y                   
            #------------------------------------------primer tramo
            for ind_z in range(Nz_rand1):    
               indices.append((ind_z,int(iy%Nmy), int(ix%Nmx))) # guardo modulo Nm para imponer condiciones periodicas
            #------------------------------------------segundo tramo                        
            for ind_z in range(Nz_rand1, Nz_rand2):
              iy += dir2[0]                          
              ix += dir2[1]              
              indices.append((ind_z,int(iy%Nmy), int(ix%Nmx))) # guardo modulo Nm para imponer condiciones periodicas
            #------------------------------------------tercer tramo
            for ind_z in range(Nz_rand2, Nmz):
              iy += dir3[0]                          
              ix += dir3[1]              
              indices.append((ind_z,int(iy%Nmy), int(ix%Nmx))) # guardo modulo Nm para imponer condiciones periodicas
    
  
                
  return indices
  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# BORRAR ESTA GEOMETRIAAAAA
def cilindros_p_random2(N, voxelSize, **geokwargs):
  """ 2022-04-06 Muri
      Igual que los cilindros aleatorios 2. Intento crear posiciones aleatorias
      en x-y, no a distancias fijas. Agrego 10 posibles inclinaciones ind_suma 
      van de -5 a 5 
      
      2023-08-02 Modificacion Santi
      
      NO ESTA FUNCIONAL POR EL MOMENTO
  """   
  
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
  
 
  #Armo los indices aleatorios desde donde va a crecer la dendrita
  rand_x = []
  rand_y = []

  for i in range(0,36,1):
      r_ind_x = 0
      r_ind_y = 0
      r_ind_x = np.random.randint(17,241)
      r_ind_y = np.random.randint(17,241)
      rand_x.append(r_ind_x)
      rand_y.append(r_ind_y)
 
    
 
  indices = []
  
  Nz_random_1 = []
   
  #n=0
  ind_x = 0
  ind_y = 0
  
  for i in range(0,36,1):
      ind_x = rand_x[i]
      ind_y = rand_y[i]
      print('ind_x',ind_x)
      print('ind_y',ind_y)
      ind_z = 0
      Nz_rand_1 = np.random.randint(0,int(N[0]/3)+1)
      print('Nz_rand_1',Nz_rand_1)
      Nz_random_1.append(Nz_rand_1)
      while ind_z < Nz_rand_1:    
          for iy in range(nsy):
              for ix in range(nsx):
                  if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                      indices.append((ind_z,ind_y+iy, ind_x+ix))
          ind_z+=1 
  #Hasta acá hice que todas las dendritas crezcan derechas hasta zmax/3
    
  Nz_random_2 = []
  ind_x_lista = []
  ind_y_lista = []
  ind_suma_x_lista = []
  ind_suma_y_lista = []
  
  j = 0
  for i in range(0,36,1):
      ind_x = rand_x[i]
      ind_y = rand_y[i]
      ind_suma_y=0
      ind_suma_x=0
      ind_z = Nz_random_1[j]
      ind_suma_rand_y= np.random.randint(0,7)-3
      ind_suma_rand_x= np.random.randint(0,7)-3
      Nz_rand_2 = np.random.randint(ind_z,int(2*N[0]/3)+1)
      while ind_z < Nz_rand_2 and ind_x + ind_suma_x <= (Nmx-2*nsx) and ind_x + ind_suma_x >= 2*nsx and ind_y + ind_suma_y <= (Nmy-2*nsy) and ind_y + ind_suma_y >= 2*nsy:
          for iy in range(nsy):
              for ix in range(nsx):
                  if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                      indices.append((ind_z,ind_y+iy+ind_suma_y, ind_x+ix+ind_suma_x))
                      
          ind_suma_x+= ind_suma_rand_x
          ind_suma_y+= ind_suma_rand_y                  
          
          ind_z+=1
          
      ind_y_lista.append(ind_y%Nmy)                
      ind_suma_y_lista.append(ind_suma_y)
      ind_suma_x_lista.append(ind_suma_x)
      j=j+1
      Nz_random_2.append(ind_z)
      ind_x_lista.append(ind_x%Nmx)
          
  #Hasta acá construi en z con orientaciones en cada uno de los cilindros
  
  k=0
  for i in range(0,36,1):
      ind_x = ind_x_lista[k]
      ind_y = ind_y_lista[k]
      ind_suma_y=ind_suma_y_lista[k]
      ind_suma_x=ind_suma_x_lista[k]
      ind_z = Nz_random_2[k]
      ind_suma_rand_y= np.random.randint(0,7)-3
      ind_suma_rand_x= np.random.randint(0,7)-3
      #print('ind_suma_rand_y',ind_suma_rand_y)
      #print('ind_z',ind_z)
      while ind_z < N[0] and ind_x + ind_suma_x <= (Nmx-2*nsx) and ind_x + ind_suma_x >= 2*nsx-1 and ind_y + ind_suma_y <= (Nmy-2*nsy) and ind_y + ind_suma_y >= 2*nsy-1:
          for iy in range(nsy):
              for ix in range(nsx):
                  if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                      # indices.append((ind_z,ind_y+iy+ind_suma_y, ind_x+ix+ind_suma_x))
                      indices.append((ind_z,(ind_y+iy+ind_suma_y)%Nmy, (ind_x+ix+ind_suma_x)%Nmx)) # MOD SAN
                      #n+=1
                      #print('n_abajo',n)
                      
          ind_suma_x+= ind_suma_rand_x
          ind_suma_y+= ind_suma_rand_y
          #print('ind_suma_y',ind_suma_y)
                  
              
          ind_z+=1
      k=k+1
  return indices
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def cilindros_aleatorios(N, voxelSize, **geokwargs):
  """ 2023-08-02
  Creo cilindritos a distancias aleatorias. 
  La distancia se define centro a centro.
  Además, los cilindros toman direcciones aleatorias:
  A los cilindritos inclinados les cambio la dirección de forma aleatoria 
  siendo (y,x)--> con las posibilidades de crecimiento (0,0),(1,0),(0,1) y (1,1)
  también en valores negativos. Ademas secciono la altura z en 3 pedazos donde 
  el crecimiento cambia segun la sección
  
  Los parametros no son independientes, sino que tienen que cumplir ciertos
  requisitos. A saber:
    
    Nmx = n * d    ,  con n entero
    Nmy = m * 2a   ,  con m entero
  
  pero ademas, el parametro a debe ser tal que minimice el error de discretizar
  d y a en la relacion:
    
    (d/2)**2 + a**2  = d**2
    
  En la carpeta DataBases, el archivo 'Hexagonal_parametro_a.dat', tiene los
  valores de a optimos para cada d.
  
  d DEBE SER PAR
  
  """  
  
  radio = geokwargs['radio']
  densidad_nominal = geokwargs['densidad_nominal']
  
  Nmz,Nmy,Nmx = N  
  vsz, vsy, vsx = voxelSize
   
  # cuantos voxels debo usar por cilindro aproximadamente
  R = int(radio/vsx)
  # cuantos silindros armo:
  Ncyl = ceil(densidad_nominal * Nmx*Nmy*vsx*vsy / np.pi / radio**2)
                
  #Esta geometría tiene 3 bloques en z donde los cilindros pueden o no cambiar 
  #la dirección de crecimiento. En el primer bloque los cilindros crecen derechos
  #hasta una altura Nz_random_1 que para cada cilindro toma valores random de 0
  #a Nz/3, luego en el segundo bloque tienen la posibilidad de inclinarse y frenar
  #a otra altura random Nz_random_2 y finalmente en el tercer bloque vuelven a tener
  #la posibilidad de inclinarse sin recordar la inclinación anterior necesariamente.


  # CREO LOS CENTROS DEL ARREGLO HEXAGONAL.  - - - - - - - - - - - - - - - - - 
  Ncentros_x = Ncentros_y = Ncyl
  centros = []
  for iy in range(Ncentros_y):
    if iy%2==0:
      for ix in range(Ncentros_x):
        centros.append((a*iy, d*ix))
    else:
      for ix in range(Ncentros_x):
        centros.append((a*iy, d*ix+d/2))
        
        
  #Armo los indices aleatorios desde donde va a crecer la dendrita
  Ncyl
  centros = []
  for i in range(Ncyl):      
      r_ind_x = np.random.randint(Nmx)
      r_ind_y = np.random.randint(Nmy)
      centros.append((r_ind_y, r_ind_x))
         
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  
  indices = [] 
  R2 = R**2
  for centro in centros:
    ind_yc, ind_xc = centro
    xc = ind_xc - 0.5
    yc = ind_yc - 0.5
    ind_xc = int(xc)
    ind_yc = int(yc)
    
    # alturas de quiebre
    Nz_rand1 = np.random.randint(0,Nmz+1)
    Nz_rand2 = np.random.randint(Nz_rand1,Nmz+1)
    Nz_rand3 = np.random.randint(Nz_rand2,Nmz+1)
    
    # direcciones de desviacion (j,i), con ij= -1,0,1.
    dir1 = (0,0)
    dir2 = (np.random.randint(-1,2),np.random.randint(-1,2))
    dir3 = (np.random.randint(-1,2),np.random.randint(-1,2))
    for ind_y in range(ind_yc-R,ind_yc+R+1):
      for ind_x in range(ind_xc-R,ind_xc+R+1):      
        if (ind_x-xc)**2 + (ind_y-yc)**2 < R2:          
          ix = ind_x; iy = ind_y                   
          #------------------------------------------primer tramo
          for ind_z in range(Nz_rand1):    
             indices.append((ind_z,int(iy%Nmy), int(ix%Nmx))) # guardo modulo Nm para imponer condiciones periodicas
          #------------------------------------------segundo tramo                        
          for ind_z in range(Nz_rand1, Nz_rand2):
            iy += dir2[0]                          
            ix += dir2[1]              
            indices.append((ind_z,int(iy%Nmy), int(ix%Nmx))) # guardo modulo Nm para imponer condiciones periodicas
          #------------------------------------------tercer tramo
          for ind_z in range(Nz_rand2, Nmz):
            iy += dir3[0]                          
            ix += dir3[1]              
            indices.append((ind_z,int(iy%Nmy), int(ix%Nmx))) # guardo modulo Nm para imponer condiciones periodicas
                
  return indices

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
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
  
#%%
if __name__=='__main__':
    import matplotlib.pyplot as plt
    from oct2py import Oct2Py
    
    """
    script para testear las geometrias
    """
    # este N es el N de la muestra ejemplo
    # N = np.array([16,228,242])  
    N = np.array([40,128,128])
    Nz,Ny,Nx = N   
    voxelSize = np.array([1e-3,1e-3,1e-3])
    
    # 'geometria' es el nombre de la geometria que vamos a utilizar
    # 'constructor' es una FUNCION. Esa funcion es diferente de acuerdo a la geometria elegida
    
    # geometria = 'cilindritos_aleatorios_3'
    # geometria = 'clusters_hexagonal_SinCeldaUnidad'
    # geometria = 'cilindros_aleatorios_hexagonal'
    geometria = 'cilindros_45grados_hexagonal'
    constructor = funciones(geometria)
    # la funcion 'constructor' me devuelve las tuplas (ind_z, ind_y, ind_x) de los indices
    # en los cuales hay litio.
    #tuplas = constructor(N, voxelSize, ancho=16e-3, distancia=20e-3)
    #tuplas = constructor(N, voxelSize, ancho=4e-3, distancia=3e-3) # para 'distancia_constante'
    #tuplas, extra_info = constructor(N, voxelSize, ancho=16e-3, distancia=20e-3, extra_info=True) # para 'distancia_constante'
    # tuplas = constructor(N, voxelSize, ancho=20e-3, porcentaje=80) # para 'porcentaje_palos'
    tuplas = constructor(N, voxelSize, radio=10e-3, distancia=22e-3, parametro_a=0.019)#, R_hueco_central=40e-3) # para 'cilindros_hexagonal'
    # tuplas = constructor(N, voxelSize, ancho=10e-3, distancia=4) # para 'porcentaje_palos'  
    # tuplas = constructor(N, voxelSize, ancho=10e-3, distancia=4) # para 'cilindros_p_random'
    
    # convierto a indices planos
    indices = np.array(tuplas).T  
    indices = np.ravel_multi_index(indices, N)
    
    # creo la matriz vacia, y coloco 1 en los indices que me da el constructor
    muestra = np.zeros(N)
    #  put(array       , indices, valor)
    np.put(muestra, indices, 1)
    
    
     
    #%%
    
    x0 = int(Nx/2)
    x0 = int(25)
    y0 = int(Ny/2)
    z0 = int(Nz/2)
    x1 = int(3/4*Nx)
    
    
    plt.figure(50)
    plt.subplot(2,2,1)
    plt.title('corte en la mitad de x')
    plt.pcolormesh(muestra[:,:,x0])
    plt.subplot(2,2,2)
    plt.title('corte en la mitad de y')
    plt.pcolormesh(muestra[:,y0,:])
    plt.subplot(2,2,3)
    plt.title('corte en la mitad de z')
    plt.pcolormesh(muestra[z0,:,:])
    plt.subplot(2,2,4)
    plt.title('corte en 3/4 de x')
    plt.pcolormesh(muestra[:,:,x1])
    plt.show()  

#%%  
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Creando figura 3D. Esto puede demorar varios minutos...")    
    fig = plt.figure(43)
    ax = fig.add_subplot(projection='3d')
    ax.voxels(np.moveaxis(muestra, 0, 2), facecolors='gray', edgecolor='k')
    print("       Listo!") 
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    

#%% 3D con OCT2PY
    # tmpvol =np.zeros((Nz+5,Ny,Nx))
    # tmpvol[1:-4,:,:] = muestra
    # tmpvol[0,:,:] = 1
    # filename = './tmp.stl'
    # with Oct2Py() as oc:
    #   print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #   print("Creando figura 3D. Esto puede demorar varios minutos...")
    #   fv = oc.isosurface(tmpvol, 0.5) # Make patch w. faces "out"
    #   oc.stlwrite(filename,fv)        # Save to binary .stl
    # print("       Listo!") 
    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
