#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""
#stop

import numpy as np
import matplotlib.pyplot as plt
from Modules.SimulationVolume import *
from Modules.Muestra import *
from Modules.Delta import *
from Modules.Superposicion import *
from Modules.Graficador import *
from Modules.Medicion import *
import time

def get_param_a(d):
    if d > 512:
        msg = ("d debe ser mas chico")
        raise Exception(msg)
    if d % 2 == 0:
        # distancias, parametros_a, errores relativos
        Ds, As, Es = np.loadtxt('./DataBases/Hexagonal_parametro_a.dat').T
        a = As[Ds == d][0]
        return a
    else:
        msg = ("la distancia debe ser tal que distancia/vs sea PAR")
        raise Exception(msg)

#inicio el reloj
t0 = time.time()
#%%----------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Parametros fisicos
Chi =  24.1*1e-6 #(ppm) Susceptibilidad volumetrica
B0 = 7 # T
skindepth = 0.014    # profundida de penetracion, mm

# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
voxel_microm = 0.25 # tamano de voxel en micros
voxelSize = [voxel_microm*1e-3]*3# mm

N = [512,256,256] 

# utilizo una funcion que dado dos argumentos define el restante. Ya sea N,
# FOV (field of view) o  voxelSize
volumen = SimulationVolume(voxelSize=voxelSize, N=N)
#volumen = SimulationVolume(FOV=FOV, N=N)
#%% CREACION DE LA MUESTRA-----------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Creo el objeto muestra. Le tengo que dar de entrada:
#  el volumen
#  la geometria: el nombre del constructor que va a usar para crear el phantom
#microestructuras
# medidas = [10e-3, 32e-3, 32e-3]
h = (1.25/voxel_microm)
d = (100/voxel_microm)
r = (50/voxel_microm)
Nz, Ny, Nx = N
vsz, vsy, vsx = voxelSize 
# parametros de la muestra
a = get_param_a(d)
# N_celdas_x = (Nx/2)//d   # // es division entera en python3  (floor)
# N_celdas_y = (Ny/2)//(2*a)
N_celdas_x = (Nx)//d   # // es division entera en python3  (floor)
N_celdas_y = (Ny)//(2*a)
medidas = [h*vsz, N_celdas_y*(2*a)*vsy, N_celdas_x*d*vsx]
distancia_mm = d*vsx
parametro_a = a*vsy
radio_mm = r*vsx

medidas = [Nz/4*vsz, Ny*vsy, Nx*vsx] # para bulk
### Creacion de la muestra
muestra = Muestra(volumen, medidas=medidas,
                  geometria = 'bulk',
                  # geometria='cilindros_hexagonal',
                  # geometria='cilindros_hexagonal',
                  # radio=radio_mm, distancia=distancia_mm,
                  # parametro_a=parametro_a, 
                  ubicacion='superior',                  
                  exceptions=False)
# muestra = Muestra(volumen, medidas=medidas, geometria='cilindros_aleatorios',densidad_nominal=1,radio=20e-3, ubicacion='superior') # para 'porcentaje_palos' 
#%% CREACION DEL OBJETO DELTA--------------------------------------------------
# delta es la perturbacion de campo magnetico
delta = Delta(muestra, skip=True)

#%%
# SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK
# superposicion = Superposicion(muestra, delta, superposicion_lateral=True)
superposicion = Superposicion(muestra, delta, radio=0) # si pongo 'radio', es porque lee de un perfil
#%%
volumen_medido = 'centro'

medicion = Medicion(superposicion, volumen_medido=f'{volumen_medido}')
# medicion = Medicion(superposicion, volumen_medido='completo',stl_file='test')
#%%
FigSP = 153
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=FigSP, Norm=False, volumen_medido=f'{volumen_medido}')
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=FigSP, Norm=False, volumen_medido=f'{volumen_medido}-bulk')
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=FigSP, Norm=False, volumen_medido=f'{volumen_medido}-microestructuras')

# FigSMC = 155; k=1; N=16
# ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}')
# ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}-bulk')
# ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}-microestructuras')

# FigSMC = 156; k=1.5; N=16
# ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}')
# ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}-bulk')
# ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}-microestructuras')

#%%

#datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
#np.savetxt(path+'h{:d}_ancho{:d}_dens{:d}_SP_k{:.2f}'.format(int(h*1e3), int(ancho*1e3), int(porcentaje), k))

#%%
elapsed = (time.time() - t0)/60
print('---  tiempo: {:.2f} min'.format(elapsed))