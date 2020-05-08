#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:48:21 2020

@author: santi
"""

import numpy as np
import warnings

class Muestra(object):
  """
  la clase Muestra contiene objetos que representan el litio metálico que
  colocamos en el campo magnetico.
  
  Atributos
  =========
  + chi: float         -  Susceptibilidad magnetica del material
  + matriz: np.array   -  Es la matriz de Nz*Ny*Nx que contiene el volumen 
                          simulado y a la muestra. Ceros en vacio, Chi en la 
                          muestra
  + geometria : string -  Ese el nombre del constructor de la geometria.
                          Define la forma que tendra la muestra.
                          
  uno de los inputs es volumen. Este proviene de la salida de la funcion
  SimulationVolume. Es un dict de tres arrays de tres elemtos. Lo desempaqueto
  asi N, voxelSize, FOV = volumen. En cada caso sigo la convencion [z,y,x]
  
  + N : int array      -  Numero de voxels en cada dimension
  + voxelSize: fl.array-  Tamano de voxels en cada dimension en mm
  + FOV: fl.array      -  Tamano del volumen simulado en cada dimension en mm
  
  """
  
  # defino el chi por defecto
  chi_Li = 24.1*1e-6 #(ppm) Susceptibilidad volumetrica
  
  def __init__(self, volumen, medidas, geometria='bulk', chi=chi_Li):
    # Dadas las variables de entrada, hago algunos pasos para crear la muestra
    # y el volumen simulado:
    # 1)OBTENCION DE INPUTS E INICIALIZACION
    #   Desempaqueto las varibles N, voxelSize y FOV que vienen en el input:
    #   volumen. Con esto puedo crear el volumen de simulacion, es decir
    #   la matriz. Los atributos que seran creados mas tardes son inicializados
    #   como None
    # 2)CREACION DE LA MUESTRA
    #   2.1)
    #   Chequeo si las medidas de la muestra cumplen la condicion de no ocupar 
    #   mas de la mitad del volumen y creo el atributo medidas.
    #   2.2)
    #   Determino el volumen real que tendra la muestra. Dadas las medidas de 
    #   de input y el voxelSize, determino cuantos voxels necesito en cada 
    #   dimension. Las medidas reales seran entonces N_muestra*voxelSize.
    #   Hago esto para crear la muestra en una matriz de menor tamaño que el
    #   volumen total.
    #   2.3)
    #   Construccion de la muestra. Llamo al constructor correspondiente usando
    #   su nombre, que viene con input geometria. Lo que me devuelve el
    #   constructor de geometria es una lista de indices en los cuales el
    #   constructor de muestra debera colocar los valores de chi, devolviendo
    #   un array con de tamaño N_muestra_z*N_muestra_y*N_muestra_x.
    # 3)CREACION DEL VOLUMEN DE SIMULACION
    #   Creo el array que define el volumen de simulacion. Lueg inserto en el
    #   el centro el array de la muestra
    
    # 1)_______________________________________________________________________
    N, voxelSize, FOV = volumen
    N = np.astype(int)
    self.N = N
    self.voxelSize = voxelSize
    self.FOV = FOV
    self.matriz = None        
    self.chi = chi
    self.geometria = geometria
    self.medidas = None 
    self.N_muestra = None
    self.muestra = None    
    # 2)_______________________________________________________________________
    # 2.1) MEDIDAS: dimensiones de la muestra en mm ---------------------------
    #chequeo que el FOV tenga un tamaño adecuado
    if np.min(FOV) < 2*np.max(medidas):
      warnings.warn("\n============WARNING===============\
                    \nOjo! Tal vez debas agrandar el FOV\
                    \n==================================")
    # 2.2)---------------------------------------------------------------------
    # con este metodo seteo las dimensiones de la submatriz que contiene a la 
    # muestra.
    self.set_medidas(medidas)
    # 2.3)---------------------------------------------------------------------
    # obtengo los indices de los voxels "vivos"
    indices = self.construir_geometria()
    # creacion de self.muestra
    self.construir_muestra(indices)
    # 3)_______________________________________________________________________
    self.construir_volumen()
  
  
  #============================================================================  
  #===============================METHODS======================================
  #============================================================================
  def set_medidas(self):
    """
    seteo la cantidad de voxels que contienten a la muestra
    """
    # puedo hacer la division porque medidas y voxelSize son np.arrays              
    N_muestra = self.medidas/self.voxelSize
    N_muestra = N_muestra.astype(int)
    # sobreescribo las medidas de la muestra, con las medidas correctas
    self.medidas = N_muestra*self.voxelSize
    self.N_muestra = N_muestra
    return 0
  #____________________________________________________________________________  
  def construir_volumen(self):
    """
    Este metodo es para crear la matriz y rellenarla con la muestra
    """
    Nz, Ny, Nx = self.N
    matriz = np.zeros([Nz,Ny,Nx])
    
    # guardo la variable matriz en el atributo matriz
    self.matriz = matriz
  #____________________________________________________________________________  
  def construir_muestra(self, indices):
    """
    Dados los indices, crea una matriz de N_muestra_z*N_muestra_y*N_muestra_x,
    con el valor de chi en los voxels en los que hay material
    """
    Nmz, Nmy, Nmx = self.N_muestra
    muestra_flat = np.zeros(Nmz*Nmy*Nmx)
    # el constructor me da una lista de indices flattened
    #  put(array       , indices, valor)
    np.put(muestra_flat, indices, self.chi)
    # convierto en 3d array
    np.reshape(muestra_flat, (Nmz,Nmy,Nmx))
    self.muestra = muestra
    return 0
    
    
    
    
    
    
    
    