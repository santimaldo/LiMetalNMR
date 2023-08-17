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
# from Modules.Funciones import *
import time
from datetime import datetime
import pandas as pd


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

# %%----------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


# Niteraciones de cada conjunto de parametros:
Niteraciones = 10
Nxy = 512

# Parametros fisicos
Chi = 24.1*1e-6  # (ppm) Susceptibilidad volumetrica
B0 = 7  # T
skindepth = 14e-13  # profundida de penetracion, mm


# parametros : vs, Nz, altura, radio
parametros = [0.25, 512, 10, 2]

# densidades nominales: (terminan siendo equivalentes a arange(0.1, 0.9, 0.1)
densidades = [0.1, 0.2, 0.3, 0.45, 0.65, 0.8, 1.2]  # , 1.5]
densidades_target = np.arange(0.1, 0.9, 0.1)


# %%
# savepath = './Outputs/2023-08-02_Cilindros_aleatorios_hexagonal_AltaResolucion/'
savefolder = '2023-08-17_Cilindros_aleatorios_AltaResolucion'
savepath = f'./Outputs/{savefolder}/'

with open(savepath+'Densidades.dat', 'w') as f:
    f.write('# N_iter\tradio (um)\taltura (um)\tvs (um)\tdensidad\n')
with open(savepath+'tiempos.dat', 'w') as f:
    f.write('# N_iter\tt_total (min)\tt_iteracion(min)\tdensidad target\tradio (um)\tdistancia (um)\taltura (um)\tvs (um)\n')


# inicializo una lista de cuales tienen error.
# inicio el reloj
t0 = time.time()
nnn = -1
ntotal = Niteraciones * len(densidades)
for n_iter in range(Niteraciones):
    for ii in range(len(densidades)):
        nnn += 1
        densidad_nominal = densidades[ii]
        densidad_target = densidades_target[ii]

        # todos los datos estan en um
        vs, Nz, altura, radio = parametros

        h = int(altura/vs)
        r = int(radio/vs)

        radio = vs*r
        altura = vs*h

        # inicio el reloj parcial
        t0parcial = time.time()
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(
            f"++++++++++++++++++   ITERACION:  {n_iter}  ++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        msj = f"altura= {h:d}x{vs}um = {altura} um,\nradio= {r:d}x{vs}um = {radio} um,\ndensidad = {densidad_target:.2f}"
        print(msj)
        print(' ')
        msj = f"      hora: {datetime.now().strftime('%H:%M:%S')}"
        print(msj)
        print(' ')
        msj = f"progreso {nnn}/{ntotal} = {nnn/ntotal*100:.2f} %"
        print(msj)
        elapsed = (time.time() - t0)
        print(
            f'---  tiempo: {elapsed:.2f} s = {elapsed/60:.2f} min = {elapsed/60/60:.2f} h')
        if nnn > 0:
            t_est = elapsed*(ntotal/nnn-1)
            msj = 'tiempo restante estimado: {:.2f} min  =  {:.2f} h'.format(
                t_est/60, t_est/60/60)
            print(msj)
            print(' ')

        # Crecion del volumen simulado - - - - - - - - - - - - - - - - - - - - -
        voxelSize = [vs*1e-3]*3  # mm
        vsz, vsy, vsx = voxelSize
        Nx = Ny = Nxy
        N = [Nz, Ny, Nx]
        volumen = SimulationVolume(voxelSize=voxelSize, N=N)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # parametros de la muestra
        Nmx = (Nx/2)
        Nmy = (Ny/2)
        medidas = [h*vsz, Nmy*vsy, Nmx*vsx]
        radio_mm = r*vsx
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Creacion de la muestra
        muestra = Muestra(volumen, medidas=medidas,
                          geometria='cilindros_aleatorios',
                          radio=radio_mm,
                          densidad_nominal=densidad_nominal,
                          ubicacion='superior')
        # exceptions=False)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        densidad_volumetrica = muestra.densidad_volumetrica
        densidad_area = muestra.densidad
        print(
            f" densidad: {densidad_area:.4f}, densidad_volumetrica: {densidad_volumetrica:.4f}")
        with open(savepath+'/Densidades.dat', 'a') as f:
            f.write(f'{n_iter}\t{radio:.2f}\t{altura:.2f}\t{vs:.3f}\t'
                    f'{densidad_area:.4f}\t{densidad_volumetrica:.4f}\n')
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # CREACION DEL OBJETO DELTA-------------------------------------------------
        # delta es la perturbacion de campo magnetico
        delta = Delta(muestra)  # , skip=True)
        # SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK -----------------------
        superposicion = Superposicion(muestra, delta, superposicion_lateral=True,
                                      radio=0)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if n_iter == 0:
            stl_file = f"{savefolder}/stls/" \
                       f"h{int(altura)}_r{int(radio)}_"\
                       f"dens{round(densidad_volumetrica, 1)}"
            medicion = Medicion(superposicion, volumen_medido='centro',
                                stl_file=stl_file)
        else:
            medicion = Medicion(superposicion, volumen_medido='centro')
        # guardado
        regiones = ['', '-microestructuras', '-bulk']
        # %% -------- centro--------------------------------------------------------------
        for region in regiones:
            print(
                "\n Trabajando en medicion y espectro de la muestra{}...".format(region))
            # secuencia: ..... SP ......
            # - - - - SP
            ppmAxis, spec = medicion.CrearEspectro(secuencia='sp', k=0.5,
                                                   Norm=False,
                                                   volumen_medido='centro{}'.format(region))
            datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
            file = 'SP/h{:d}_r{:.2f}_dens{:.2f}_vs{:.3f}um_niter{}_SP{}.dat'.format(
                int(altura), radio, densidad_target, vs, n_iter, region)
            np.savetxt(savepath+file, datos)

            # pulso de pi/12
            ppmAxis, spec = medicion.CrearEspectro(secuencia='sp', k=0.08,
                                                   Norm=False,
                                                   volumen_medido='centro{}'.format(region))
            datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
            file = 'SP_0.08/h{:d}_r{:.2f}_dens{:.2f}_vs{:.3f}um_niter{}_SP{}.dat'.format(
                int(altura), radio, densidad_target, vs, n_iter, region)
            np.savetxt(savepath+file, datos)

            # - - - - SMC16
            ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', N=16, k=1,
                                                   Norm=False,
                                                   volumen_medido='centro{}'.format(region))
            datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
            file = 'SMC/h{:d}_r{:.2f}_dens{:.2f}_vs{:.3f}um_niter{}_SMC{}.dat'.format(
                int(altura), radio, densidad_target, vs, n_iter, region)
            np.savetxt(savepath+file, datos)

        elapsed_parcial = (time.time() - t0parcial)/60.0
        elapsed = (time.time() - t0)/60.0

        print('---  tiempo parcial: {:.2f} min'.format(elapsed_parcial))
        with open(savepath+'tiempos.dat', 'a') as f:
            f.write(
                f'{int(nnn):d}\t{elapsed:.2f}\t{elapsed_parcial:.2f}\t{densidad_target:.2f}\t{radio:.2f}\t{altura:.2f}\t{vs:.2f}\n')

        del muestra, delta, superposicion, medicion, volumen
        del ppmAxis, spec, datos
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
msj = f"progreso {nnn}/{ntotal} = {nnn/ntotal*100} %"
print(msj)
print(' ')
elapsed = (time.time() - t0)
print(
    f'---  tiempo total: {elapsed:.2f} s = {elapsed/60:.2f} min = {elapsed/60/60:.2f} h')
