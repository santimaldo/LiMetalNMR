#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021-06-12

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
from Modules.SimulationVolume import *
from Modules.Muestra import *
from Modules.Delta import *
from Modules.Superposicion import *
from Modules.Graficador import *
from Modules.Medicion import *
import os
import time
from datetime import datetime
import pandas as pd

# %%----------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Parametros fisicos
Chi = 24.1*1e-6  # (ppm) Susceptibilidad volumetrica
B0 = 7  # T
skindepth = 14e-13  # profundida de penetracion, mm

# Number of voxels in each dimension
Nz = 128
Ny = 512
Nx = 512

savepath = './Outputs/tmp/'
if not os.path.exists(savepath):
    os.makedirs(savepath)


t0 = time.time()
# todos los datos estan en um
vs = 1 # voxelSize
altura = 10
radio = 2
densidad_nominal = 0.5

h = int(altura/vs)
r = int(radio/vs)
d = int(distancia/vs)

radio_mm = vs*r*1e-3
distancia_mm = vs*d*1e-3
altura_mm = vs*h*1e-3

# Crecion del volumen simulado - - - - - - - - - - - - - - - - - - - - -
voxelSize = [vs*1e-3]*3  # mm
vsz, vsy, vsx = voxelSize
N = [Nz, Ny, Nx]
volumen = SimulationVolume(voxelSize=voxelSize, N=N)

### la geometria hexagonal sobreescribe medidas[1] y medidas[2]
medidas = [h*vsz,Ny/2*vsy,Nx/2*vsx]
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
### Creacion de la muestra
muestra = Muestra(volumen, medidas = medidas,
                  geometria='cilindros_hexagonal',            
                  radio=radio_mm, densidad=densidad_nominal, ubicacion='superior',
                  exceptions=False)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# CREACION DEL OBJETO DELTA-------------------------------------------------
# delta es la perturbacion de campo magnetico
delta = Delta(muestra)
# SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK -----------------------
superposicion = Superposicion(muestra, delta, superposicion_lateral=True,
                                radio=None)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
medicion = Medicion(superposicion, volumen_medido='centro', 
                    stl_file=None)    
# guardado    
regiones = ['', '-microestructuras', '-bulk']  
#-------- centro--------------------------------------------------------------
for region in regiones:
    print("\n Trabajando en medicion y espectro de la muestra{}...".format(region))
    # secuencia: ..... SP ......
    # - - - - SP
    ppmAxis, spec = medicion.CrearEspectro(secuencia='sp', k=0.5,
                                           volumen_medido=f'centro{region}',
                                           Norm=False)            
    datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T    
    file = 'SP/h{:d}_r{:.2f}_dens{:.1f}_vs{:.3f}um_SP{}.dat'.format(
        int(altura), radio, densidad_nominal, vs, region)
    np.savetxt(savepath+file, datos)
    

elapsed = (time.time() - t0)
print(
f'---  tiempo total: {elapsed:.2f} s = {elapsed/60:.2f} min = {elapsed/60/60:.2f} h')
