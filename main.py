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

N = [512,512,512] 

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
h = (10/voxel_microm)
d = (2.5/voxel_microm)
r = (1/voxel_microm)
Nz, Ny, Nx = N
vsz, vsy, vsx = voxelSize 

distancia_mm = d*vsx
radio_mm = r*vsx

medidas = [Nz/4*vsz, Ny*vsy, Nx*vsx]
### Creacion de la muestra
muestra = Muestra(volumen, medidas=medidas,
                  #geometria = 'bulk',
                  geometria='cilindros_hexagonal',
                  # geometria='cilindros_hexagonal',
                  radio=radio_mm, distancia=distancia_mm,                  
                  ubicacion='superior',                  
                  exceptions=False)
# muestra = Muestra(volumen, medidas=medidas, geometria='cilindros_aleatorios',densidad_nominal=1,radio=20e-3, ubicacion='superior') # para 'porcentaje_palos' 
#%% CREACION DEL OBJETO DELTA--------------------------------------------------
# delta es la perturbacion de campo magnetico
delta = Delta(muestra)#, skip=True)

#%%
# SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK
superposicion = Superposicion(muestra, delta, superposicion_lateral=True)

Bnuc = superposicion.delta_sup - superposicion.delta_in
Bnuc[superposicion.muestra_sup==0]=np.nan
#%%
vmin = 10
vmax = 17

x = np.linspace(-(FOV-voxelSize)/2.0, (FOV-voxelSize)/2.0,N)# FOV simetrico sin voxel en cero
# x = np.linspace(-(FOV)/2.0, (FOV)/2.0-voxelSize,N)# FOV simetrico CON voxel en cero
  y = x
  z = x
  
  Z,Y,X= np.meshgrid(z,y,x, indexing='ij')

fig, ax = plt.subplots()
c = ax.pcolormesh(Bnuc[-10, :, :], vmin=vmin, vmax=vmax)
ax.axis('equal')
cbar = fig.colorbar(c)
cbar.ax.set_title(r"$\Delta\delta$ [ppm]")
plt.figure(2)
plt.plot(Bnuc[400,256,:])
plt.ylim([vmin, vmax])

# superposicion = Superposicion(muestra, delta, radio=0) # si pongo 'radio', es porque lee de un perfil
#%%
# volumen_medido = 'centro'

# medicion = Medicion(superposicion, volumen_medido=f'{volumen_medido}')
# # medicion = Medicion(superposicion, volumen_medido='completo',stl_file='test')
# #%%
# FigSP = 153
# ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=FigSP, Norm=False, volumen_medido=f'{volumen_medido}')
# # ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=FigSP, Norm=False, volumen_medido=f'{volumen_medido}-bulk')
# # ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=FigSP, Norm=False, volumen_medido=f'{volumen_medido}-microestructuras')

# # FigSMC = 155; k=1; N=16
# # ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}')
# # ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}-bulk')
# # ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}-microestructuras')

# # FigSMC = 156; k=1.5; N=16
# # ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}')
# # ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}-bulk')
# # ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=N, k=k, figure=FigSMC, Norm=False, volumen_medido=f'{volumen_medido}-microestructuras')

# #%%

# datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
# filename = "./Outputs/bulk.dat"
# np.savetxt(filename, datos)

#%%
elapsed = (time.time() - t0)/60
print('---  tiempo: {:.2f} min'.format(elapsed))