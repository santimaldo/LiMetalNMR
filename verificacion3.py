#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""
#stop

import numpy as np
import matplotlib.pyplot as plt
import Modules.calculateFieldShift as cFS
from scipy import integrate
import time

"""
Para una esfera de radio 0.1 m calculo la perturbacion de campo con distintas
discretizaciones.

Dejo fijo el FOV y cambio el voxelSize, la esgera es siempre del mismo diametro

En este caso, no comparo con exacta, porque hago 4 ESFERAS, y no se la exacta

Pero la verdad que no me dio resultados resaltables
"""


"""
##############################################################################
FUNCIONES:
"""
def Integrar(Matriz, x, y, z):
  """
  Integracion 3d  
  x,y,z son vectores 1D
  """
  i = (integrate.simps(integrate.simps(integrate.simps(Matriz, x=z), x=y),x=x))
  return i

def autophase(ppmAxis, spec):
  """
  Corrijo automaticamente la fase, utilizando el método de minimizar el area
  de la parte imaginaria:   case{'MinIntImagSpec'}
  """
  precision = 1
  angle=np.arange(-180,180,precision)

  SPECS = []
  IntImagSpec = []
  for i in range(angle.size):
      Sp_try= spec*np.exp(-1j*angle[i]*np.pi/180)
      SPECS.append(Sp_try)
      IntImagSpec.append(np.abs(np.trapz(np.imag(Sp_try),x=ppmAxis)))
  IntImagSpec = np.array(IntImagSpec)
  # indice del minimo:
  idx = np.argmin(IntImagSpec)
  spec = SPECS[idx]
  ind_max = np.argmax(np.abs(np.real(spec)))
  if spec[ind_max]<0:
    spec=-spec
  angle=angle[idx]
  return  spec, angle

def crearEspectro(muestra, eta, x, y, z):
    print("Calculando espectro...")
    
    #FID-----------------------------------------------------------------------
    ppm = 116.641899 # Hz
    # T2est = 0.14*1e-3 # T2est=0.14ms estimado con ancho de espectro. 2020-11-13
    T2est = 1*1e-3 # T2est=0.14ms estimado con ancho de espectro. 2020-11-13
    dw = 20e-6 # sacado de los experimentos. Esto da un SW=857ppm aprox
    NP = 1024 # experimentalmente usamos 2048, pero con 4096 sale mas lindo
    t = np.arange(NP)*dw
    fid = np.zeros_like(t).astype(complex)
    
    #### INTEGRANDO:
    # eta_obj = eta*muestra            
    # for jj in range(t.size):
    #   tt = t[jj]
    #   # Valor de la frecuencia en cada voxel
    #   w = 2*np.pi*ppm*(eta_obj)           
    #   # Valor de la fid en cada voxel en el tiempo tt     
    #   fid_t = np.exp(1j*w *tt - tt/T2est)
    #   fid[jj] = Integrar(fid_t, x,y,z)
    
    #### SUMANDO:    
    eta_obj = eta[muestra==1]      
    for jj in range(t.size):
      tt = t[jj]
      # Valor de la frecuencia en cada voxel
      w = 2*np.pi*ppm*(eta_obj)           
      # Valor de la fid en cada voxel en el tiempo tt     
      fid_t = np.exp(1j*w *tt - tt/T2est)
      fid[jj] = np.sum(fid_t)
    #FOURIER-------------------------------------------------------------------
    freq = np.fft.fftshift(np.fft.fftfreq(NP, d=dw))
    ppmAxis = freq/ppm
    spec = np.fft.fftshift(np.fft.fft(fid))
    # corrijo la fase:
    spec, angle = autophase(ppmAxis,spec)
    return ppmAxis, np.real(spec)
"""
##############################################################################
"""


#inicio el reloj
t0 = time.time()
#----------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Parametros fisicos
Chi =  24.1e-6 #(ppm) Susceptibilidad volumetrica
B0 = 7 # T

# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
FOV = 0.512

Ns   = [256,128,64,32,16,8]
jj=-1
for N in Ns:
  jj+=1
  voxelSize = FOV/float(N)
  print(f"voxelSize={voxelSize}")
  # CREACION DE LA MUESTRA-----------------------------------------------------
  #------------------------------------------------------------------------------
  #------------------------------------------------------------------------------
  diametro = 0.128
  # x = np.linspace(-FOV/2.0, (FOV/2.0-voxelSize) ,N) # con un voxel centrado en cero
  x = np.linspace(-(FOV-voxelSize)/2.0, (FOV-voxelSize)/2.0,N) # - voxelSize/2# FOV simetrico sin voxel en cero
  y = x
  z = x
  
  Z,Y,X= np.meshgrid(z,y,x, indexing='ij')
  
  
  muestra = np.zeros_like(X)
  
  # centro 4 esferas en distintos puntos en el plano x-z
  centros = [-1,1]
  for i in centros:
    for j in centros:
      condicion = (X+i*diametro)**2+Y**2+(Z+j*diametro)**2 <= (diametro/2.0)**2
      muestra[condicion] = 1

  # calculo el campo-----------------------------------------------------------
  #------------------------------------------------------------------------------
  #------------------------------------------------------------------------------
  
  eta = cFS.calculateFieldShift(muestra*Chi, [voxelSize]*3)
  # eta = muestra
  
  Bnuc = eta*B0 + B0
  Bmac = Bnuc/(1-2/3*muestra*Chi)


  # graffff
  plt.figure(1110)
  plt.subplot(2,3,jj+1)
  plt.pcolormesh(X[:,int(N/2),:], Z[:,int(N/2),:], muestra[:,int(N/2),:], cmap='gray_r', shading='nearest')
  plt.xlabel("x")
  plt.ylabel("z")
  plt.title("Esfera discretizada")  
  for i in centros:
    for j in centros:      
      ax = plt.gca()
      circle = plt.Circle((i*diametro, j*diametro), diametro/2.0, color='k', fill=False)
      ax.add_patch(circle)
  
  # grafico de delta
  vmax = np.max(np.abs(eta[:,int(N/2),:]))
  plt.figure(1111)
  plt.subplot(2,3,jj+1)
  plt.pcolormesh(X[:,int(N/2),:], Z[:,int(N/2),:], eta[:,int(N/2),:], cmap='seismic', vmax=vmax, vmin=-vmax, shading='nearest')
  plt.xlabel("x")
  plt.ylabel("z")
  plt.title(r"$\delta$ con $\chi=${}".format(Chi))
  plt.colorbar()
  for i in centros:
    for j in centros:      
      ax = plt.gca()
      circle = plt.Circle((i*diametro, j*diametro), diametro/2.0, color='k', fill=False)
      ax.add_patch(circle)
  
  
  ##### NMR -------------------------------------------------------------------
  
  plt.figure(1112246871)
  plt.subplot(2,3,jj+1)
  plt.hist(eta[muestra==1])
  plt.xlabel(r"$\delta$ [ppm]")
  plt.ylabel("Intensity [a.u]")
  plt.title(r"$N_{voxels} = $"+ f" {N}")

  ppmAxis, spec = crearEspectro(muestra, eta, x, y, z)    
  # plt.figure(1112246872)
  # plt.subplot(2,3,jj+1)
  # plt.plot(ppmAxis, spec)
  # plt.xlabel(r"$\delta$ [ppm]")
  # plt.ylabel("Intensity [a.u]")
  # plt.title(r"$N_{voxels} = $"+ f" {N}")
  
  plt.figure(1112246873)  
  plt.plot(ppmAxis, spec/np.max(spec), label = r"$N_{voxels} = $"+ f" {N}")
  plt.xlabel(r"$\delta$ [ppm]")
  plt.ylabel("Intensity [a.u]")
  plt.title("Espectros Normalizados")
  
  

elapsed = (time.time() - t0)/60
print('---  tiempo: {:.2f} min'.format(elapsed))