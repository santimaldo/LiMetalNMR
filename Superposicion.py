#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 14:04:31 2020

@author: santi
"""

import numpy as np
import scipy.ndimage as ndimage

class Superposicion(object):
  """
  Esta clase representa la superposicion de los deltas bulk y microestructuras
  
  INPUTS:
    muestra : objeto de la clase Muestra.
   
  ATRIBUTOS
  + muestra   : Muestra()   -  el objeto clase muestra definido en el main
  + delta     : array       -  es el array que devuelve calculateFieldShift
  + delta_in  : float       -  Al bulk lo aproximamos como una funcion esaclon.
                              delta_in es el valor de delta dentro de la lamina
                              de litio bulk
  + delta_out : float       -  Al bulk lo aproximamos como una funcion esaclon.
                              delta_out es el valor de delta fuera de la lamina
                              de litio bulk
  
  + z0        : int         - el indice en la direccion z en la cual comienzan
                              las dendritas. z0-1 es el ultimo indice donde hay 
                              bulk
  + slice     : list        - [[zi,zf], [yi,yf], [xi,xf]] Entre estos valores
                              recorto la matriz de volumen para definir el 
                              volumen en cual hago la superposicion.
                              
  + muestra_sup : array     - superposicion de la muestra (las dendritas), con 
                              el bulk. Es decir, lleno de litio todo el volumen
                              hasta z0-1
  
  
  + delta_bulk : array      - Matriz con valores de delta generados por el bulk,
                              es decir, la funcion escalon en z:
                                delta_in  para 0  <  z  <=  z0-1
                                delta_out para z0 <= z 
  + delta_muestra : array   - Matriz con los valores de delta generados por las
                              dendritas.
  
  + self.delta_sup : array  - Matriz con el delta superpuesto
                                  delta_sup = delta_bulk + delta_muestra   
  
  + delta_sens : array      - Matriz con los valores de delta solo en las 
                              regiones sensibles, es decir, las regiones que
                              dan senal.
  
  # ESTO TODAVIA NO ESTA IMPLEMENTADO
  para el efecto B1:
  self.erosiones = None
  self.tajadas = None
  self.tajadas_delta = None
  """
  
  def __init__(self, muestra, delta, delta_in=-12.79, delta_out=3.27):
    
    
    self.muestra = muestra
    self.delta = delta
    self.delta_in = delta_in
    self.delta_out = delta_out           
    # el nuevo valor de indice en z en el cual empiezan las dendritas:
    # [0:z0,:,:] --> bulk
    # [z0: ,:,:] --> dendritas
    self.z0 = int(36e-3/self.muestra.voxelSize[0])
    self.slice = None
    self.definir_slice()
    
    self.muestra_sup = None
    self.superponer_muestra()
    
    self.delta_bulk = None
    self.delta_muestra = None
    self.crear_delta_bulk()    
    self.crear_delta_muestra()
    self.delta_sup =  self.delta_bulk + self.delta_muestra   
    
    self.delta_sens = None
    self.crear_delta_sens()    

    self.areas()    
    
    # para el efecto B1:
    self.erosiones = None
    self.tajadas = None
    self.tajadas_delta = None
    
  def definir_slice(self):
    """
    Este metodo es para definir donde cortar la matriz del volumen y de delta.
    """    
    slz,sly,slx = self.muestra.slices    
    vsz,vsy,vsx = self.muestra.voxelSize
    slz0 = slz[0] - self.z0
    slz1 = slz[1]
    sly0 = 0
    sly1 = self.muestra.N[1]
    slx0 = 0
    slx1 = self.muestra.N[2] 
    self.slice = [[slz0,slz1],[sly0,sly1],[slx0,slx1]]
    return 0    

    
  def superponer_muestra(self):
    """
    Toma la matriz de la muestra, crea el volumen entero
    y le agraga el bulk en la parte de abajo
    """    
    slz,sly,slx = self.slice
    obj = self.muestra.construir_volumen()/self.muestra.chi
    # recorto el volumen
    obj = obj[slz[0]:slz[1], sly[0]:sly[1], slx[0]:slx[1]]
    # lleno al objeto de 1 en todos los lugaras HASTA z0 (exclusivo)    
    obj[0:self.z0,:,:] = 1     
    
    self.muestra_sup = obj
    return 0
  
  
  def crear_delta_bulk(self):
    """
    Crea el delta bulk como una funcion escalon
    """        
    slz,sly,slx = self.slice
    # defino el z donde arranca la muestra
    z0 = self.z0
    # lleno al objeto de delta_in en todos los lugaras HASTA z0 (exclusivo)
    # y de delta_out desde z0 en adelante
    delta_bulk = np.zeros_like(self.muestra_sup)
    delta_bulk[0:z0,:,:] = self.delta_in
    delta_bulk[z0:,:,:] = self.delta_out
    
    self.delta_bulk = delta_bulk
    return 0
  
  def crear_delta_muestra(self):
    """
    Crea el delta muestra recortando el delta, usando muestra.slices,
    agregando los extras
    """
    slz,sly,slx = self.slice
    delta_muestra = self.delta.delta[slz[0]:slz[1], sly[0]:sly[1], slx[0]:slx[1]]  
    self.delta_muestra = delta_muestra
    return 0        
  
  
  def crear_delta_sens(self):
    """
    Usando erosion binaria, elijo 12 um hacia adentro
    """        
    vs = self.muestra.voxelSize
    if not vs[0]==vs[1]==vs[2]:
      print("=======================WARNING=============================")
      print("los voxels deben ser CUBICOS para poder implementar la erosion binaria")
      raise ValueError('los lados deben ser iguales!!!')        
    vs = vs[0]
    d = 0.012 # mm  
    nd = int(d/vs)  
    """
    To find the edge pixels you could perform binary erosion on your mask, then XOR the result with your mask
    """
    obj = self.muestra_sup
    mask = (obj == 1)
    struct = ndimage.generate_binary_structure(3, 1)
    struct = ndimage.iterate_structure(struct, nd)
    erode = ndimage.binary_erosion(mask, struct)
    vol_sens = mask ^ erode
    # quito la parte de bulk profundo
    z0 = self.z0
    print("--se forzo a cero la señal de bulk mas prifundo que 12 um--")
    vol_sens[0:z0-(nd),:,:] = 0    
    self.delta_sens = vol_sens * self.delta_sup
    
  def areas(self):
    """
    calculos las areas (2D) "solo bulk", y "con dendritas". Ojo, no es el area 
    total de bulk, ya que existe bulk entre las dendritas. Es solo como para tener
    una idea orientativa. Tampoco es la superficie total, solo el area de litio
    cubierta
    """
    vs = self.muestra.voxelSize
    N = self.muestra.N
    Nm = self.muestra.N_muestra
    
    area_total =  N[1]*vs[1] * N[0]*vs[0]
    self.area_dendritas = Nm[1]*vs[1] * Nm[0]*vs[0]
    self.area_bulk = area_total - self.area_dendritas
    
    print('area_bulk/area_dendritas = %.2f'%(self.area_bulk/self.area_dendritas))
    return self.area_bulk/self.area_dendritas
    


  def erosiones_consecutivas(self, n_slices):
    """
    Este metodo es para hacer muchas erosiones de 1 voxel, como para seleccionar
    solo esa parte. de esta forma podemos manipular los distintos slices que 
    plantean Ilott y Jerschow, segun el decaimiento de B1 dentro del metal
    """
    obj = self.muestra_sup
    z0 = self.z0        
    # inicializo las listas en las cuales guardo erosiones y slices
    # erosion es el objeto quitando un voxel del borde, n veces
    # slices es una tajada de un voxel, a cierta profundidad. 
    erosiones = []
    tajadas = []
    
    mask = (obj == 1)
    struct = ndimage.generate_binary_structure(3, 1)
    for n in range(n_slices):
      # erosiono
      erode = ndimage.binary_erosion(mask, struct)
      # la erosion tambien se come los laterales del bulk, por eso los vuelvo a
      # rellenar con 1. La tajada va estar exactamente en z0-n-1, los 1 se llenan
      # hasta z0-n-2
      erode[0:z0-n-1,:,:] = 1
      # obtengo la tajada
      vol_sens = mask ^ erode
      # guardo
      erosiones.append(erode)
      tajadas.append(vol_sens)
      # ahora el nuevo objeto a erosionar es el de la erosion anterior
      mask = (erode==1)
    self.erosiones = erosiones
    self.tajadas = tajadas
    return erosiones, tajadas
    
  def crear_tajadas_delta(self, n_slices):
    """
    En este metodo obtengo los slices de delta
    """
    no_existe = (self.tajadas_delta is None) or (len(self.tajadas_delta)!=n_slices)
    ya_existe = (not self.tajadas_delta is None) and (len(self.tajadas_delta)==n_slices)
    
    if no_existe:  
      erosiones, tajadas = self.erosiones_consecutivas(n_slices)
      del erosiones
      tajadas_delta = []
      for tajada in tajadas:
        delta = tajada * self.delta_sup
        # quito la parte de bulk profundo
        delta[0:self.z0-(n_slices),:,:] = 0
        tajadas_delta.append(delta)
      self.tajadas_delta = tajadas_delta
    elif ya_existe:
      print("slices_delta(n_slices) says: \n\t 'ya existia, así que \
            no hice nada. Te devuelvo lo que estaba guardado'")
    return self.tajadas_delta
    
    
    
  def get_delta_dendritas(self):
    """
    metodo que devuelve una matriz con los valores de delta, solo en la region
    de la muestra, es decir, las dendritas
    """
    delta_muestra = self.delta_sens[self.z0:,:,:] # dendritas    
    return delta_muestra
  
  def get_delta_bulk(self):
    """
    metodo que devuelve una matriz con los valores de delta, solo en la region
    de la muestra
    """
    delta_bulk = self.delta_sens[0:self.z0,:,:] # bulk
    return delta_bulk
