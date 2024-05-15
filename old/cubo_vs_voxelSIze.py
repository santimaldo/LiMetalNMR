#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Feb 17 2022

@author: santi
"""
#stop

import numpy as np
import matplotlib.pyplot as plt
import Modules.calculateFieldShift as cFS
from scipy import integrate
import time

"""
Un cubo con FOV fijo y cambio N y voxelSize 
"""

#inicio el reloj
t0 = time.time()
#%%----------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Parametros fisicos
Chi =  1e-6 #(ppm) Susceptibilidad volumetrica
B0 = 7 # T

# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
FOV = 0.512
Ns   = [32,64,128,256,512]
# Ns   = [64]

#%% CREACION DE LA MUESTRA-----------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
datos = []
for N in Ns:
    print(f"N={N}")
    voxelSize = FOV/float(N)    
    diametro = 0.058
    # x = np.linspace(-FOV/2.0, (FOV/2.0-voxelSize) ,N) # con un voxel centrado en cero
    x = np.linspace(-(FOV-voxelSize)/2.0, (FOV-voxelSize)/2.0,N) # FOV simetrico sin voxel en cero
    y = x
    z = x
    
    Z,Y,X= np.meshgrid(z,y,x, indexing='ij')
        
    muestra = np.zeros_like(X)
    r2=(diametro/2.0)**2
    condicion = (X*X <= r2)
    muestra[condicion] = 1
    condicion = (Y*Y <= r2)
    mask=np.zeros_like(muestra)
    mask[condicion]=1
    muestra = muestra*mask
    condicion = (Z*Z <= r2)
    mask=np.zeros_like(muestra)
    mask[condicion]=1
    muestra = muestra*mask
    
    #%% calculo el campo-----------------------------------------------------------
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    
    eta = cFS.calculateFieldShift(muestra*Chi, [voxelSize]*3)
    
    
    Bnuc = eta*B0 + B0
    Bmac = Bnuc/(1-2/3*muestra*Chi)
    
    
    
    #%%
    # graffff    
    
    datos.append(np.array([Z[:,int(N/2),int(N/2)], eta[:,int(N/2),int(N/2)]]))
    
    
    plt.figure(1)
    plt.plot(Z[:,int(N/2),int(N/2)], eta[:,int(N/2),int(N/2)], 'o-', label=f'N={N}, voxelSize={voxelSize} mm')
    plt.xlabel("z")
    plt.ylabel("ppm")
    
plt.title(fr"Cubo de lado {diametro} mm, FOV=({FOV} mm)$^3$")    
plt.legend()    
