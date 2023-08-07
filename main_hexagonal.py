#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021-06-12

@author: santi
"""
# stop

import numpy as np
import matplotlib.pyplot as plt
from Modules.SimulationVolume import *
from Modules.Muestra import *
from Modules.Delta import *
from Modules.Superposicion import *
from Modules.Graficador import *
from Modules.Medicion import *
import time

# stop


def get_param_a(d):
    # distancias, parametros_a, errores relativos
    Ds, As, Es = np.loadtxt('./DataBases/Hexagonal_parametro_a.dat').T
    a = As[Ds == d][0]
    return a


# inicio el reloj
t0 = time.time()
# %%----------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
save = False
# Parametros fisicos
Chi = 24.1*1e-6  # (ppm) Susceptibilidad volumetrica
B0 = 7  # T
skindepth = 0.014  # profundida de penetracion, mm

# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
voxelSize = [0.25e-3]*3  # mm

# N = [128, 1024, 1024]
#N = [256,128,128]
N = [256,512,512]
# N = [256,64,64]

# utilizo una funcion que dado dos argumentos define el restante. Ya sea N,
# FOV (field of view) o  voxelSize
volumen = SimulationVolume(voxelSize=voxelSize, N=N)
Nz, Ny, Nx = N
vsz, vsy, vsx = voxelSize
# %% CREACION DE LA MUESTRA-----------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Creo el objeto muestra. Le tengo que dar de entrada:
#  el volumen
#  la geometria: el nombre del constructor que va a usar para crear el phantom de microestructuras

path = "./Outputs/2023-07-19_CilindosRectos_HR"

# altura (h), radio(r) y distancia (d) en micrometros
h = 10
r = 2
d = 7


# Debo "preparar" los parametros para que cumplan ciertos criterios:
#   d: par,   Nmx=n*d,  Nmy=m*2*a,  'a' se lee de archivo.
h_vx = int(h*1e-3/voxelSize[0])
r_vx = int(r*1e-3/voxelSize[1])
d_vx = int(d*1e-3/voxelSize[1])
a = get_param_a(d_vx)
# densidad local:
p_loc = 0.5
rh = 50

filename = f'h{h:d}_r{r:d}_dist{d:d}_densLoc{p_loc:.2f}'

# rMAX = d/2 - 1
if r > (d_vx/2-1):
    raise Exception("El radio elegido es muy grande")

# calculo cuantas celdas unitarias entran en la maxima superf que puedo simular
# (sup max:  Nx/2*Ny/2)
N_celdas_x = (Nx/2)//d_vx   # // es division entera en python3  (floor)
N_celdas_y = (Ny/2)//(2*a)

medidas = [h_vx*vsz, N_celdas_y*(2*a)*vsy, N_celdas_x*d_vx*vsx]
distancia = d_vx*vsx
parametro_a = a*vsy
radio = r_vx*vsx
muestra = Muestra(volumen, medidas=medidas, geometria='cilindros_hexagonal',radio=radio, distancia=distancia, parametro_a=parametro_a)
muestra = Muestra(volumen, medidas=medidas, geometria='cilindros_45grados_hexagonal',radio=radio, distancia=distancia, parametro_a=parametro_a)
# muestra = Muestra(volumen, medidas=medidas, geometria='clusters_hexagonal',radio=radio, distancia=distancia, parametro_a=parametro_a, p_huecos=1-p_loc)
# muestra = Muestra(volumen, medidas=medidas, geometria='clusters_hexagonal_SinCeldaUnidad',
                  # R_hueco_central=rh*1e-3, radio=radio, distancia=distancia, parametro_a=parametro_a, p_huecos=1-p_loc)
# muestra = Muestra(volumen, medidas=medidas, geometria='cilindros_aleatorios_hexagonal',radio=radio, distancia=distancia, parametro_a=parametro_a)
# muestra = Muestra(volumen, medidas=medidas, geometria='bulk')


# calculo densidad usando celda unidad

# la muestra vale Chi en el objeto
A_mic = np.sum(muestra.muestra[1, :int(2*a), :int(d_vx)]/Chi)
A_tot = 2*a*distancia
A_bulk = A_tot-A_mic

densidad = A_mic/A_tot

# %% CREACION DEL OBJETO DELTA--------------------------------------------------
# delta es la perturbacion de campo magnetico
delta = Delta(muestra)


# %%

# SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK
# superposicion = Superposicion(muestra, delta)
# superposicion = Superposicion(muestra, delta, radio='000', z0=84e-3) # si pongo 'radio', es porque lee de un perfil
superposicion = Superposicion(muestra, delta, superposicion_lateral=True, radio=400)

# %%
plt.figure(1110101001011)
matriz = (superposicion.delta_sup *
          superposicion.muestra_sup)[-int(h*1e-3/vsz/2), :, :]
matriz_mask = np.ma.masked_where(matriz == 0, matriz)
plt.pcolormesh(matriz_mask, cmap='inferno_r')
plt.colorbar()

if save:
    header = f'Corte a la mitad de la altura de las microestructuras'
    np.savetxt(f'{path}{filename}.matriz', matriz, header=header)


# grafico para chequear
# fig1, ax1 = plt.subplots()
# ax1.set_aspect('equal')
# vmax = np.max(np.abs(superposicion.delta_sup[64,120:329,120:329]))
# # ax1.pcolormesh(superposicion.delta_sup[64,120:392,120:392], cmap='seismic', vmin=-vmax, vmax=vmax)
# ax1.pcolormesh(superposicion.delta_sup[64,:,:], cmap='seismic', vmin=-vmax, vmax=vmax)

# plt.figure(53879531798321)
# z0 = 1
# vmax = np.max(np.abs(superposicion.delta_sup[z0,:,:]))
# plt.pcolormesh(superposicion.delta_sup[60,:,:], cmap='seismic', vmin=-vmax, vmax=vmax)
# plt.colorbar()

# %%
#medicion = Medicion(superposicion, volumen_medido='completo', borde_a_quitar=[12,0,0])
# medicion = Medicion(superposicion, volumen_medido='centro',stl_file='test')
# medicion = Medicion(superposicion, volumen_medido='muestra')
medicion = Medicion(superposicion, volumen_medido='centro', borde_a_quitar=[0, 0, 0])

####, stl_file=f"{filename}")
# medicion = Medicion(superposicion, volumen_medido='completo',stl_file='test')0


# norm = True
# path = 'S:/Doctorado/pyprogs/calculateFieldShift/Outputs/Resultados/comparacion_sp-smc/bis/'
# %%

# medicion = Medicion(superposicion, volumen_medido='muestra', borde_a_quitar=[12,0,0])
ppmAxis, spec = medicion.CrearEspectro(secuencia='sp', k=0.5,figure=153, T2est=0.6e-3)
# medicion = Medicion(superposicion, volumen_medido='muestra-microestructuras', borde_a_quitar=[12,0,0])
# ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153)
# medicion = Medicion(superposicion, volumen_medido='muestra-bulk', borde_a_quitar=[12,0,0])
# ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153)

if save:
    datos = np.array(
        [ppmAxis, np.real(spec)/np.max(np.real(spec)), np.imag(spec)]).T
    np.savetxt(path+f'{filename}.dat'.format(h, r, d), datos)
# %%
# for k in [1.0,1.05,1.1,1.15,1.2,1.3,1.4,1.5,1.75,2.0,2.25]:
#   ppmAxis, spec = medicion.CrearEspectro(secuencia='smc' , N=64, k=k, figure=12345)
#   datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
#   np.savetxt(path+'h{:d}_r{:d}_d{:d}_SMC64-k{:.2f}.dat'.format(h,r,d,k), datos)


# beta = medicion.Crear_beta()
# #%%
# plt.figure(88888)
# plt.pcolormesh(beta[:,98,:])
# plt.colorbar()


# %%
elapsed = (time.time() - t0)/60
print('---  tiempo: {:.2f} min'.format(elapsed))

plt.show()
