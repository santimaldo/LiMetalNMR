#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:10:09 2020

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors


class Graficador(object):
  """
  Esta clase contiene las visualizaciones de los datos. Como input, requiere un
  objeto de la clase Delta. recordemos que esos objetos ya contienen un objeto
  de clase muestra
  
  
  """
  
  def __init__(self, muestra, delta):
    
    self.muestra = muestra
    self.delta = delta
    
    # coordenadas lineales totales
    self.zyx = None
    # coordenadas lineales dela muestra
    self.zyx_muestra = None
    
    self.fignum = 1
    
    self.crear_coordenadas()
    self.crear_coordenadas_muestra()
    
  def crear_coordenadas(self):
    """
    crea arrays 1D con las coordenadas. Colocamos el cero al centro. Como los
    arrays son impares, el cero estará justamente entre los dos voxels centrales
    """
    Nz, Ny, Nx = self.muestra.N
    vsz, vsy, vsx = self.muestra.voxelSize
    
    z = np.linspace(-Nz/2, Nz/2, Nz)*vsz
    y = np.linspace(-Ny/2, Ny/2, Ny)*vsy
    x = np.linspace(-Nx/2, Nx/2, Nx)*vsx
    
    self.zyx = [z,y,x]
    self.z = z
    self.y = y
    self.x = x
    return 0
    
  def crear_coordenadas_muestra(self):
    """
    crea arrays 1D con las coordenadas. Colocamos el cero al centro. Como los
    arrays son impares, el cero estará justamente entre los dos voxels centrales
    """
    Nmz, Nmy, Nmx = self.muestra.N_muestra
    vsz, vsy, vsx = self.muestra.voxelSize
    
    zm = np.linspace(-Nmz/2, Nmz/2, Nmz)*vsz
    ym = np.linspace(-Nmy/2, Nmy/2, Nmy)*vsy
    xm = np.linspace(-Nmx/2, Nmx/2, Nmx)*vsx
    
    self.zyx_muestra = [zm,ym,xm]
    return 0
  
  
  def mapa(self, dim=2, corte=0.5, completo=True):
    """
    El clasico pcolormesh 
    """
    # de acuerdo a la dimencion de corte, dim, se elige cual va a ser el eje
    # X y cual el Y del grafico.ejemplo: corte en y:dim=1 --> X=x (2), Y=z (0),
    # obviamente usando la convencion 0,1,2 = z,y,x
    y_index = [1,0,0]
    x_index = [2,2,1]
    y_index = y_index[dim]
    x_index = x_index[dim]
                  
    if completo:
      # X e Y son los ejes del grafico    
      Y = self.zyx[y_index]
      X = self.zyx[x_index]
      N_slice = int(self.muestra.N[dim] * corte)
      # como el corte puede ser en cualquier dimension, muevo la dimension de
      # corte al final, es decir de la posicion dim la paso a la posicion 2,
      # para finalmente poder hacer el slice asi: f = f[:,:,N_slice]
      f = self.delta.delta
      f = np.moveaxis(f, dim, 2)
      f = f[:,:,N_slice]
    else:
      # X e Y son los ejes del grafico    
      Y = self.zyx_muestra[y_index]
      X = self.zyx_muestra[x_index]
      
      N_slice = int(self.muestra.N_muestra[dim] * corte)
      # como el corte puede ser en cualquier dimension, muevo la dimension de
      # corte al final, es decir de la posicion dim la paso a la posicion 2,
      # para finalmente poder hacer el slice asi: f = f[:,:,N_slice]
      f = self.delta.delta_r
      f = np.moveaxis(f, dim, 2)
      f = f[:,:,N_slice]
      
      
      
   
    plt.figure(self.fignum)
    vmax = np.max([np.abs(np.max(f)), np.abs(np.min(f))])
    norm = colors.Normalize(vmin=-vmax*0.8, vmax=vmax*0.8)
    plt.pcolormesh(X, Y, f, cmap='seismic', norm=norm)
    # los label de los ejes dependen de que corte se haga
    xlab = [r'$x$ [mm]', r'$x$ [mm]', r'$y$ [mm]',  ]
    ylab = [r'$y$ [mm]', r'$z$ [mm]', r'$z$ [mm]',  ]
    plt.xlabel(xlab[dim])
    plt.ylabel(ylab[dim])
    cbar = plt.colorbar()
    cbar.set_label(r'$\delta [ppm]$')

    
    
    self.fignum += 1