#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 14:04:31 2020

@author: santi
"""

import numpy as np
import calculateFieldShift as cFS

class Delta(object):
  """
  Esta clase representa al corrimiento en el campo magnetico.
  
  INPUTS:
    muestra : objeto de la clase Muestra.
   
  ATRIBUTOS
  + muestra : Muestra()   -  el objeto clase muestra definido en el main
  + delta   : array       -  es el array que devuelve calculateFieldShift
  + delta_muestra : array -  es delta pero evaluado solo en la muestra
  """
  
  def __init__(self, muestra):
    
    self.muestra = muestra
    self.delta = None
    self.delta_muestra = None
    
    self.calcular()
    self.recortar()
    
    
  def calcular(self):
    """
    Toma el matriz de la muestra y calcular delta
    """    
    dChi = self.muestra.construir_volumen()
    voxelSize = self.muestra.voxelSize
    
    # el paso mas importante de todos:
    delta = cFS.calculateFieldShift(dChi, voxelSize) * 1e6
    
    self.delta = delta
    return 0
  
  def recortar(self):
    """
    defino un delta_muestra que es el recorte solo en la región de la muestra
    """
    chi = self.muestra.chi
    slz,sly,slx = self.muestra.slices
    
    
    delta_muestra = self.delta[slz[0]:slz[1], sly[0]:sly[1], slx[0]:slx[1]]
    # hago cero todos los voxels en los cuales no hay muestra.
    # self.muestra.muestra/self.muestra.chi es 0 en aire y 1 en muestra
    delta_muestra = delta_muestra*self.muestra.muestra/self.muestra.chi
    self.delta_muestra = delta_muestra
    return 0    
    
    
    
    