#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021-06-12

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
# from Modules.Funciones import *
import time


def get_param_a(d):
  if d>256:
    msg = ("d debe ser mas chico")
    raise Exception(msg)
  if d%2==0:    
    # distancias, parametros_a, errores relativos
    Ds, As, Es = np.loadtxt('./DataBases/Hexagonal_parametro_a.dat').T
    a = As[Ds==d][0]
    return a
  else:
    msg = ("la distancia debe ser tal que distancia/vs sea PAR")
    raise Exception(msg)


np.loadtxt('./DataBases/CilindrosAltaResolucion_parametros_d_r.dat')

#%%----------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Parametros fisicos
Chi =  24.1*1e-6 #(ppm) Susceptibilidad volumetrica
B0 = 7 # T
skindepth = 0.012 # profundida de penetracion, mm

# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
vs = 0.1 # um
voxelSize = [vs*1e-3]*3# mm
vsz,vsy,vsx = voxelSize
#%% CREACION DE LA MUESTRA-----------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Creo el objeto muestra. Le tengo que dar de entrada:
#  el volumen
#  la geometria: el nombre del constructor que va a usar para crear el phantom de microestructuras

# Debo "preparar" los parametros para que cumplan ciertos criterios:
#   d: par,   Nmx=n*d,  Nmy=m*2*a,  'a' se lee de archivo.

VSs = [0.1,0.05,0.01]
# VSs = [1,0.5]
radios = [0.2]*len(VSs)
distancias= [0.6,0.8,1,1.2]
alturas = [5]*len(VSs)




savepath = './Outputs/Cilindros_hexagonal_AltaResolucion/'
# with open(savepath+'Densidades.dat','w') as f:
#       f.write('# radio (um)\tdistancia (um)\taltura (um)\tdensidad\n')
# with open(savepath+'tiempos.dat','w') as f:
#       f.write('# N_iter\tt_total (min)\tt_iteracion(min)\th\tr\td\n')


# figuras 1d
fig1d, axs1d = plt.subplots(2, 2)


# inicializo una lista de cuales tienen error.
errores = []

#inicio el reloj
t0 = time.time()
nnn = 0
ntotal = len(VSs)
delta_x = []
delta_y = []
Ncx = []
Ncy = []
for ind_d in range(len(distancias)):
  for ind_vs in range(len(VSs)):  
    vs = VSs[ind_vs]
    altura = alturas[ind_vs]
    radio = radios[ind_vs]
    distancia = distancias[ind_d]
    h = int(altura/vs)
    r = int(radio/vs)
    d = round(distancia/vs)      
    
    if d<20:
      msj = 'la distancia debe ser mas grande'
      errores.append([altura, radio, distancia, msj])
    
    #inicio el reloj parcial
    t0parcial = time.time()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    msj = f"altura= {h:d}x{vs}um = {altura} um,  \
      radio= {r:d}x{vs}um = {radio} um,  \
        distancia = {d:d}x{vs}um = {distancia} um"
    print(msj)
    print(' ')
    msj = f"progreso {nnn}/{ntotal} = {nnn/ntotal*100:.2f} %"
    print(msj)
    elapsed = (time.time() - t0)
    print(f'---  tiempo: {elapsed:.2f} s = {elapsed/60:.2f} min = {elapsed/60/60:.2f} h')
    print(' ')
    
    # determinacion de Nz:------------------------------------------------------
    Nz = 256
    condicion=True
    while condicion:
      if Nz>1024:
        raise Exception("el vs es muy chico para la altura deseada")
      elif h>Nz/2:
        Nz = 2*Nz
        condicion=True
      else:
        condicion=False
    # ## determino Nx y Ny--------------------------------------------------------
    # Nx = 256
    # Ny = 256
    # a = get_param_a(d)
    # condicion=True
    # while condicion:
    #   # calculo cuantas celdas unitarias entran en la maxima superf que puedo simular
    #   # (sup max:  Nx/2*Ny/2)
    #   N_celdas_x = (Nx/2)//d   # // es division entera en python3  (floor)
    #   N_celdas_y = (Ny/2)//(2*a)
    #   if N_celdas_x*N_celdas_y==0:
    #     if N_celdas_x==0:
    #       Nx=2*Nx
    #     else:
    #       Ny=2*Ny
    #   else:
    #     condicion=False
    # # chequeo que haya quedado bien      
    # if Nx*Ny*Nz>(1024*512*512):
    #   raise Exception("Muy chico el vs, las matrices quedan muy grandes")
    # # prosigo  
    
    Ny = Nx = 512
    N = [Nz,Ny,Nx]
    
    a = get_param_a(d)
    N_celdas_x = (Nx/2)//d   # // es division entera en python3  (floor)
    N_celdas_y = (Ny/2)//(2*a)
    if N_celdas_x*N_celdas_y==0:
      raise Exception("muy chico el vs")
    volumen = SimulationVolume(voxelSize=voxelSize, N=N)
    print(f"N_celdas en (y,x):  ({N_celdas_y},{N_celdas_x})")
    continue
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    medidas = [h*vsz,N_celdas_y*(2*a)*vsy,N_celdas_x*d*vsx]
    distancia = d*vsx
    parametro_a = a*vsy
    radio = r*vsx
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Creacion de la muestra
    muestra = Muestra(volumen, medidas=medidas, geometria='cilindros_hexagonal',exceptions=False, radio=radio, distancia=distancia, parametro_a=parametro_a)       
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # calculo densidad usando celda unidad    
    A_mic  = np.sum(muestra.muestra[1,:int(2*a),:int(d)]/Chi) # la muestra vale Chi en el objeto
    A_tot  = 2*a*d
    densidad = A_mic/A_tot
    with open(savepath+'/Densidades.dat','a') as f:
      pass
      # f.write('{:d}\t{:d}\t{:d}\t{:.4f}\n'.format(r,d,h,densidad))             
    #CREACION DEL OBJETO DELTA-------------------------------------------------
    # delta es la perturbacion de campo magnetico    
    delta = Delta(muestra)
    # SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK -----------------------
    superposicion = Superposicion(muestra, delta, superposicion_lateral=True, )
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # GRAFICOS
    x = (np.arange(Nx)-Nx/2)*vs
    y = (np.arange(Ny)-Ny/2)*vs
    X,Y = np.meshgrid(x,y)
    
    slz = superposicion.z0 + (int(h/2)+1)
    sly = int(Ny/2)
    slx = int(Nx/2)
    
    obj = superposicion.muestra_sup
    vmax = np.max(np.abs(delta.delta))
    
    fig, axs = plt.subplots(1,2)
    fig.suptitle(rf"$N_z\times N_y  \times N_x$ = ${Nz:d}\times{Ny:d}\times{Nx:d}$ \n  voxelsize: {vs} $\mu$m")
    axs[0].pcolormesh(X,Y,delta.delta[slz,:,:], vmax=vmax, vmin=-vmax, cmap='seismic', shading='nearest')
    axs[1].pcolormesh(X,Y,(superposicion.delta_sup)[slz,:,:], vmax=vmax, vmin=-vmax, cmap='seismic', shading='nearest')
    for ax in axs:
      ax.set_aspect('equal')
      ax.hlines(0, xmin=x[0], xmax=x[-1], color='k')
      ax.vlines(0, ymin=y[0], ymax=y[-1], color='k')
      ax.set_xlabel(r'x [$\mu$m]')
      ax.set_ylabel(r'y [$\mu$m]')
    
    objx = obj[slz,sly,:]
    deltx = delta.delta[slz,sly,:]
    deltsupx = superposicion.delta_sup[slz,sly,:]
    objy = obj[slz,:,slx]
    delty = delta.delta[slz,:,slx]
    deltsupy = superposicion.delta_sup[slz,:,slx]
    
    ### GUARDADO  
    # datos = np.array([x, objx, deltx, deltsupx]).T
    # np.savetxt(f'datos_NyNx_{Ny}x{Nx}_X.dat', datos)
    # datos = np.array([y, objy, delty, deltsupy]).T
    # np.savetxt(f'datos_NyNx_{Ny}x{Nx}_Y.dat', datos)
    Ncx.append(N_celdas_x)
    Ncy.append(N_celdas_y)
    delta_x.append(np.mean(deltsupx[objx==1]))
    delta_y.append(np.mean(deltsupy[objy==1]))
    
    objx=1
    objy=1
    axs1d[0,0].plot(x, objx*deltsupx)
    axs1d[0,0].set_xlabel(r'x [$\mu$m]')
    axs1d[0,0].set_ylabel(r'$\Delta\delta$ [ppm]')
    # ---
    axs1d[0,1].plot(y, objy*deltsupy)
    axs1d[0,1].set_xlabel(r'y [$\mu$m]')
    axs1d[0,1].set_ylabel(r'$\Delta\delta$ [ppm]')
    # sin super
    # ---
    axs1d[1,0].plot(x, objx*deltx)
    axs1d[1,0].set_xlabel(r'x [$\mu$m]')
    axs1d[1,0].set_ylabel(r'$\Delta\delta$ [ppm]')
    # ---
    axs1d[1,1].plot(y, objy*delty)
    axs1d[1,1].set_xlabel(r'y [$\mu$m]')
    axs1d[1,1].set_ylabel(r'$\Delta\delta$ [ppm]')
    
    
    
    nnn+=1
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
msj = f"progreso {nnn}/{ntotal} = {nnn/ntotal*100} %"
print(msj)
print(' ')
elapsed = (time.time() - t0)
print(f'---  tiempo total: {elapsed:.2f} s = {elapsed/60:.2f} min = {elapsed/60/60:.2f} h')

plt.figure(377328)
plt.plot(Ncx,delta_x, 'o-', label='x')
plt.plot(Ncy,delta_y, 'o-', label='x')
plt.legend()
plt.ylabel(r'$\Delta\delta [ppm]$')
plt.xlabel(r'$N_{celdas}$')
plt.figure(3773)
plt.plot(VSs,delta_x, 'o-')
plt.plot(VSs,delta_y, 'o-')
plt.xlabel(r'VoxelSize [$\mu$m]')
plt.ylabel(r'$\Delta\delta [ppm]$')