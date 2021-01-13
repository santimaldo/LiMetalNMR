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
<<<<<<< HEAD:Geometria.py
  funciones['mask_1'] = mask_1
  funciones['cilindritos_dist_cte'] = cilindritos_dist_cte
  funciones['cilindrito_prueba'] = cilindrito_prueba
=======
  funciones['porcentaje_palos'] = porcentaje_palos
  funciones['porcentaje_lanzas'] = porcentaje_lanzas
>>>>>>> master:Modules/Geometria.py
  if geometria in funciones:
    return funciones[geometria]
  else:
      mensaje= "\n =====ERROR=en=funciones(geometria)============\
               \n El input debe se un string con el nombre de la geometria.\
               \n O bien, la geometria solicitada no se encuentra\
                \n =============================================="
      raise Exception(mensaje)
      return 0
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
<<<<<<< HEAD:Geometria.py
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
  while ind_z < int(Nmz/2) and n < 20:
      for iy in range(nsy):
          for ix in range(nsx):
              if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                  indices.append((ind_z,ind_y+iy, ind_x+ix))
      ind_z+=1
      n+=1
      print(n)
  else:
      print("entro al else")
      while ind_z < Nmz:
          for iy in range(nsy):
              for ix in range(nsx):
                  if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                      indices.append((ind_z,ind_y+iy, ind_x+ix))
          ind_x+=2
      ind_z+=1
  return indices
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
=======
def porcentaje_palos(N, voxelSize, tolerancia=0.5, altura=None, **geokwargs):
  """
  2020-10-14
  dendritas de anchoXancho um2 en sedntido vertical, apoyadas sobre la superficie
  en posiciones aleatorias hasta cubrir un cierto porcentaje
  """
  # extraigo los geokwargs:
  ancho  = geokwargs['ancho']
  porcentaje = geokwargs['porcentaje']
  p = porcentaje/100
    
  Nmz,Nmy,Nmx = N
  vsz, vsy, vsx = voxelSize  
  
  if altura is None:
    altura = vsz*Nmz
    print ("altura de dendritas: {} um".format(altura*1e3))
  elif altura>vsz*Nmz:
    altura = vsz*Nmz
    print ("WARNING!!! la altura de dendritas solicitada es superior \
           a la medida de la muestra. Retransformando a altura = {} um".format(altura))
    
  # cuantos voxels debo usar
  nsx = int(ancho/vsx)
  nsy = int(ancho/vsy)
  nsz = int(altura/vsz)
  
  area = nsx*nsy
  AreaTotal = Nmx*Nmy
  # determino cuantas dendritas voy a crear en un principio
  Nd = int(AreaTotal*p/area)
  if Nd==0:
    msj = 'Error!!! Las microestructuras son muy anchas o la densidad solicitada es muy chica!. Con solo una microestructura, se alcanza una densidad del {:.2f}%'.format(area/AreaTotal*100)
    raise Exception(msj)
  
  n = 0
  indices = []
  while n<10:
    for iterador in range(Nd):
      ind_y = np.random.randint(0,Nmy-nsy+1)
      ind_x = np.random.randint(0,Nmx-nsx+1)          
      for iz in range(nsz):
        for iy in range(nsy):
          for ix in range(nsx):
            indices.append((iz,ind_y+iy, ind_x+ix))            
    # armo la muestra para chequear que cubri bien el area:          
    indices_array = np.array(indices).T  
    indices_array = np.ravel_multi_index(indices_array, N)    
    muestra = np.zeros(N)
    np.put(muestra, indices_array, 1)
    # calulo el area cubierta
    areaCubierta = np.sum(muestra[1,:,:])
    pCubierto = areaCubierta/AreaTotal    
    
    if abs(pCubierto-p)*100<tolerancia:
      break
    if p<pCubierto:
      print("Ups... nos pasamos...")
      break
    areaPorCubrir = p*AreaTotal - areaCubierta
    Nd = int(areaPorCubrir/area)
    print('cubierto:{:.2f}%, pongo {:d} estructuras para alcanzar el {:.2f}%'.format(pCubierto*100, Nd, p*100))
    n+=1
  print("Porcentaje cubierto: {:.3f} %".format(pCubierto*100))
  return indices, pCubierto*100
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def porcentaje_lanzas(N, voxelSize, tolerancia=0.5, altura=None, **geokwargs):
  """
  2020-10-26
  dendritas de anchoXancho um2 en sedntido vertical, apoyadas sobre la superficie
  en posiciones aleatorias hasta cubrir un cierto porcentaje.
  son lanzas porque en la punta terminan como flecha, no como rectangulos
  """
  # extraigo los geokwargs:
  ancho  = geokwargs['ancho']
  porcentaje = geokwargs['porcentaje']
  p = porcentaje/100
    
  Nmz,Nmy,Nmx = N
  vsz, vsy, vsx = voxelSize
  
  
  if altura is None:
    altura = vsz*Nmz
    print ("altura de dendritas: {} um".format(altura*1e3))
  elif altura>vsz*Nmz:
    altura = vsz*Nmz
    print ("WARNING!!! la altura de dendritas solicitada es superior \
           a la medida de la muestra. Retransformando a altura = {} um".format(altura))
    
  # cuantos voxels debo usar
  nsx = int(ancho/vsx)
  nsy = int(ancho/vsy)
  nsz = int(altura/vsz)
  if nsx == 1:
    nsz_punta = nsz
    print('iiiiujiu')
  elif nsx/2<nsz:
    nsz_punta = int(nsx/2)
  else:
    nsz_punta = 2

  area = nsx*nsy
  AreaTotal = Nmx*Nmy
  # determino cuantas dendritas voy a crear en un principio
  Nd = int(AreaTotal*p/area)
  if Nd==0:
    msj = 'Error!!! Las microestructuras son muy anchas o la densidad solicitada es muy chica!. Con solo una microestructura, se alcanza una densidad del {:.2f}%'.format(area/AreaTotal*100)
    raise Exception(msj)
  print(nsz, nsz_punta)
 
  
  n = 0
  indices = []
  while n<10:
    for iterador in range(Nd):
      ind_y = np.random.randint(0,Nmy-nsy+1)
      ind_x = np.random.randint(0,Nmx-nsx+1)                
      for iz in range(nsz_punta):
        for iy in range(nsy):
          for ix in range(nsx):
            indices.append((iz,ind_y+iy, ind_x+ix))
      n_spear = 1 # iterador para la punta de la estructura            
      for iz in range(nsz_punta,nsz):
        for iy in range(n_spear, nsy-n_spear):
          for ix in range(n_spear, nsx-n_spear):            
            indices.append((iz,ind_y+iy, ind_x+ix))            
        n_spear+=1     
    # armo la muestra para chequear que cubri bien el area:          
    indices_array = np.array(indices).T  
    indices_array = np.ravel_multi_index(indices_array, N)    
    muestra = np.zeros(N)
    np.put(muestra, indices_array, 1)
    # calulo el area cubierta
    areaCubierta = np.sum(muestra[1,:,:])
    pCubierto = areaCubierta/AreaTotal
    print(pCubierto*100, p*100)
    
    if abs(pCubierto-p)*100<tolerancia:
      break
    if p<pCubierto:
      print("Ups... nos pasamos...")
      break
    areaPorCubrir = p*AreaTotal - areaCubierta
    Nd = int(areaPorCubrir/area)
    n+=1
  print("Porcentaje cubierto: {:.3f} %".format(pCubierto*100))
  return indices
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


>>>>>>> master:Modules/Geometria.py

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
<<<<<<< HEAD:Geometria.py
  N = np.array([128,256,256])    
=======
  N = np.array([32,128,128])
  Nz, Ny, Nx = N
>>>>>>> master:Modules/Geometria.py
  voxelSize = np.array([1e-3,1e-3,1e-3])
  
  # 'geometria' es el nombre de la geometria que vamos a utilizar
  # 'constructor' es una FUNCION. Esa funcion es diferente de acuerdo a la geometria elegida
<<<<<<< HEAD:Geometria.py
  geometria = 'cilindrito_prueba'
  constructor = funciones(geometria)
=======
  geometria = 'porcentaje_lanzas'
>>>>>>> master:Modules/Geometria.py
  
  # la funcion 'constructor' me devuelve las tuplas (ind_z, ind_y, ind_x) de los indices
  # en los cuales hay litio.
<<<<<<< HEAD:Geometria.py
  tuplas = constructor(N, voxelSize, ancho=16e-3, distancia=20e-3)
  
=======
  # tuplas = constructor(N, voxelSize, ancho=4e-3, distancia=3e-3) # para 'distancia_constante'
  tuplas = constructor(N, voxelSize, ancho=20e-3, porcentaje=80) # para 'porcentaje_palos'

>>>>>>> master:Modules/Geometria.py
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
<<<<<<< HEAD:Geometria.py
  plt.pcolormesh(muestra[:,:,int(N[2]*3/4)])
  plt.figure(555555555555555555555555555)
  plt.pcolormesh(muestra[int(N[0]/2),:,:])
  
=======
#  plt.pcolormesh(muestra[:,:,int(Nx*3/4)])
  plt.pcolormesh(muestra[-1,:,:])
>>>>>>> master:Modules/Geometria.py
