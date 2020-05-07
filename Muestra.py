#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:48:21 2020

@author: santi
"""

import numpy as np

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
  
  def __init__(self, volumen, geometria='bulk', chi=chi_Li):
    N, voxelSize, FOV = volumen        
    self.N = N
    self.voxelSize = voxelSize
    self.FOV = FOV
    
    self.chi = chi
    self.geometria = geometria
    self.matriz = self.crear_matriz()
    
  
  def crear_matriz(self):
    """
    Este metodo es para crear la matriz y rellenarla con la muestra
    """
    Nz, Ny, Nz = self.N
    matriz = np.zeros([Nz,Ny,Nz])
    
    # guardo la variable matriz en el atributo matriz
    self.matriz = matriz
    
    
    
    
    
    