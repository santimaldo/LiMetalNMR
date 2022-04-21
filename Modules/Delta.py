#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 14:04:31 2020

@author: santi
"""

import numpy as np
import Modules.calculateFieldShift as cFS
from Modules.Funciones import timerClass


@timerClass
class Delta(object):
  """
  Esta clase representa al corrimiento en el campo magnetico.
  
  INPUTS:
    muestra : objeto de la clase Muestra.
   
  ATRIBUTOS
  + muestra : Muestra()   -  el objeto clase muestra definido en el main
  + delta   : array       -  es el array que devuelve calculateFieldShift
  + delta_r : array -  es delta pero evaluado solo en la muestra
  """
  
  def __init__(self, muestra):
    
    self.muestra = muestra
    self.delta = None
    self.delta_r = None
    
    self.calcular()
#    self.recortar()
    
    
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
    defino un delta_r que es el recorte solo en la región de la muestra
    """
    slz,sly,slx = self.muestra.slices
    
    delta_r = self.delta[slz[0]:slz[1], sly[0]:sly[1], slx[0]:slx[1]]
    
    self.delta_r = delta_r
    return 0    
  
  def delta_r_xy(self):
    """
    delta evaluado en todo z, pero recortado a xy de la muestra
    """
    # hago cero todos los voxels en los cuales no hay muestra.
    # self.muestra.muestra/self.muestra.chi es 0 en aire y 1 en muestra
    slz,sly,slx = self.muestra.slices
    
    delta_r_xy = self.delta[:, sly[0]:sly[1], slx[0]:slx[1]]
    return delta_r_xy
    
  def delta_muestra(self):
    """
    delta evaluado solo en la mustra y cero afuera.
    """
    # hago cero todos los voxels en los cuales no hay muestra.
    # self.muestra.muestra/self.muestra.chi es 0 en aire y 1 en muestra
    delta_muestra = self.delta_r*self.muestra.muestra/self.muestra.chi    
    return delta_muestra
    
    
    
    
    
