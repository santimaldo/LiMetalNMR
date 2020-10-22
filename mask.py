#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 19:06:07 2020

@author: santi
"""

def Recortar_circulo_central(self):
  """
  Este metodo sirve para recortar las matrices de interes en su circulo central
  """
  N = self.muestra_sup.shape
  z = np.arange(N[0])-N[0]/2
  y = np.arange(N[1])-N[1]/2
  x = np.arange(N[2])-N[2]/2
  Z,Y,X = np.meshgrid(z,y,x,indexing='ij')
  
  # vamos a seleccionar un circulo cuyo diametro va a ser la mitad del tamaño
  # de la muestra (es decir, la region con microestructuras)
  cilindro = (X/(N[2]/4))**2+(Y/(N[1]/4))**2 <1
  
  self.muestra_sup = self.muestra_sup[cilindro] 