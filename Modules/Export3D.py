# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 11:22:35 2021

@author: santi
"""

# funcion para crear la figura 3D
def exportar_3D(matriz, archivo):
  print(" -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ")
  print("Creando figura 3D. Esto puede demorar varios minutos...")
  Nz, Nx, Ny = matriz.shape
  tmpvol =np.zeros((Nz+5,Ny,Nx))
  tmpvol[1:-4,:,:] = matriz
  filename = archivo+'.stl'
  with Oct2Py() as oc:
    oc.addpath('./Modules/')
    fv = oc.isosurface(tmpvol, 0.5) # Make patch w. faces "out"
    oc.stlwrite(filename,fv)        # Save to binary .stl
  # octave.addpath('\\Modules')
  # fv = oc.isosurface(tmpvol, 0.5) # Make patch w. faces "out"
  # octave.stlwrite(filename,fv)        # Save to binary .stl
  
  print("       Listo!") 
  print(" -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ")