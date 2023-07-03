# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 11:22:35 2021

@author: santi
"""
import numpy as np
#from oct2py import Oct2Py

# funcion para crear la figura 3D
def exportar_3D(matriz, archivo):
  print(" -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ")
  print("Creando figura 3D. Esto puede demorar varios minutos...")
  Nz, Nx, Ny = matriz.shape
  tmpvol =np.zeros((Nz+5,Ny+10,Nx+10)) # le doy margenes para que se vean los bordes
  tmpvol[1:-4,5:-5,5:-5] = matriz  
  with Oct2Py() as oc:    
    fv = oc.isosurface(tmpvol, 0.5) # Make patch w. faces "out"
    try:      
      filename = '../Outputs/{}.stl'.format(archivo)
      oc.stlwrite(filename,fv)        # Save to binary .stl      
    except:
      oc.addpath('./Modules/')
      filename = './Outputs/{}.stl'.format(archivo)
      oc.stlwrite(filename,fv)        # Save to binary .stl
  print("       Listo!") 
  print(" -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ")