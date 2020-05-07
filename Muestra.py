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
  
  + N : int            -  Numero de voxels en cada dimension
  
  
  
  """
  
  # defino el chi por defecto
  chi_Li = 24.1*1e-6 #(ppm) Susceptibilidad volumetrica
  
  def __init__(self, volumen, medidas, geometria='bulk', chi=chi_Li):
    N, voxelSize, FOV = volumen
    self.N = N
    self.voxelSize = voxelSize
    self.FOV = FOV
    
    self.chi = chi
    self.geometria = geometria
    
    # MEDIDAS: dimensiones de la muestra en mm ----------- 
    #chequeo que el FOV tenga un tamaño adecuado
    if np.min(FOV) < 2*np.max(medidas):
      warnings.warn("\n============WARNING===============\
                    \nOjo! Tal vez debas agrandar el FOV\
                    \n==================================")
    self.medidas = None 
    self.N_muestra = None
    self.set_medidas(medidas)
    
       
    self.matriz = None
    self.crear_matriz()
    
  
  def crear_matriz(self):
    """
    Este metodo es para crear la matriz y rellenarla con la muestra
    """
    Nz, Ny, Nx = self.N
    matriz = np.zeros([Nz,Ny,Nx])
    
    # guardo la variable matriz en el atributo matriz
    self.matriz = matriz
  
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
  
  def crear_muestra(self):
    """
    insercion de la muestra en la matriz
    """
    muestra_vol = np.zeros()
    Nz, Ny, Nx = self.N
    
    # el constructor me da una lista de indices flattened
    
    
    
    
    
    
    
    