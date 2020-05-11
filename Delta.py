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
    
  
  """
  
  def __init__(self, muestra):
    
    self.N = muestra.N
    
    
  def calcular(self):
    """
    Toma el matriz de la muestra y calcular delta
    """    
    dChi = muestra.construir_volumen()
    
    delta = cFS.calculateFieldShift()