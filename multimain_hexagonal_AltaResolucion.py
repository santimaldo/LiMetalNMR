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


# Parametros fisicos
Chi = 24.1*1e-6  # (ppm) Susceptibilidad volumetrica
B0 = 7  # T
skindepth = 14e-13  # profundida de penetracion, mm

Nxy = 512

# radio, distancia y vs estan en el archivo:
# parametros = np.loadtxt('./DataBases/ParametrosASimular_hexagonal.par')
# parametros = pd.DataFrame(parametros)
# parametros = parametros.sort_values(by=[1, 2, 0, 3, 4], ascending=True)
# parametros = np.array(parametros)

df = pd.read_csv('./DataBases/ParametrosASimular_hexagonal.par')
# df = df[df['Nz'] < 1024]
df = df[df['altura'] == 10]
df = df[df['radio'] == 2]
df = df[df['voxelSize'] == 0.250]
# min_vs = df.groupby(['radio', 'densidad_nominal', 'altura'])['voxelSize'].idxmin()
# df = df.loc[min_vs.values]
df = df.sort_values(['radio', 'densidad_nominal'], ascending=[True, True])
parametros = np.array(df)


# hago una corrida con parametros elegidos:
# parametros = np.array([np.array([0.2500, 512, 50.0000, 2.0000, 5.5000, 0.4976])])


# %%
# savepath = './Outputs/2023-08-14_Cilindros_hexagonal_AltaResolucion/'
savepath = './Outputs/2023-08-18_Cilindros_hexagonal_AltaResolucion/'
with open(savepath+'Densidades.dat', 'w') as f:
    f.write('# distancia (um)\tradio (um)\taltura (um)\tvs (um)\tdensidad\t densidad volumetrica\n')
with open(savepath+'tiempos.dat', 'w') as f:
    f.write('# N_iter\tt_total (min)\tt_iteracion(min)\tradio (um)\tdistancia (um)\taltura (um)\tvs (um)\n')
    

# inicializo una lista de cuales tienen error.
# inicio el reloj
t0 = time.time()
nnn = -1
ntotal = parametros.shape[0]
# ntotal = 1
for par in parametros:    
    nnn += 1
    # todos los datos estan en um
    vs, Nz, altura, radio, distancia, densidad_nominal, densidad = par

    h = int(altura/vs)
    r = int(radio/vs)
    d = int(distancia/vs)

    radio = vs*r
    distancia = vs*d
    altura = vs*h

    # inicio el reloj parcial
    t0parcial = time.time()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    msj = f"altura= {h:d}x{vs}um = {altura} um,\nradio= {r:d}x{vs}um = {radio} um,\ndistancia = {d:d}x{vs}um = {distancia} um,\ndensidad = {densidad:.2f}"
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
    a = get_param_a(d)
    N_celdas_x = (Nx/2)//d   # // es division entera en python3  (floor)
    N_celdas_y = (Ny/2)//(2*a)
    medidas = [h*vsz, N_celdas_y*(2*a)*vsy, N_celdas_x*d*vsx]
    distancia_mm = d*vsx
    parametro_a = a*vsy
    radio_mm = r*vsx
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ### Creacion de la muestra
    muestra = Muestra(volumen, medidas=medidas,
                      # geometria='cilindros_hexagonal',
                      # geometria='cilindros_45grados_hexagonal',
                      geometria='cilindros_con-angulo_hexagonal', angulo_target=45,
                      radio=radio_mm, distancia=distancia_mm,
                      parametro_a=parametro_a, ubicacion='superior',
                      exceptions=False)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    densidad_volumetrica = muestra.densidad_volumetrica    
    print(
        f" densidad: {densidad:.4f}, densidad_volumetrica: {densidad_volumetrica:.4f}")
    with open(savepath+'/Densidades.dat', 'a') as f:
        f.write(f'{distancia:.2f}\t{radio:.2f}\t{altura:.2f}\t{vs:.3f}\t'
                f'{densidad:.4f}\t{densidad_volumetrica:.4f}\n')    
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
    medicion = Medicion(superposicion, volumen_medido='centro')
    # guardado
    regiones = ['', '-microestructuras', '-bulk']
    # %% -------- centro--------------------------------------------------------------
    for region in regiones:
        print("\n Trabajando en medicion y espectro de la muestra{}...".format(region))
        # secuencia: ..... SP ......
        # - - - - SP
        ppmAxis, spec = medicion.CrearEspectro(
            secuencia='sp', k=0.5, volumen_medido='centro{}'.format(region),
            Norm=False)            
        datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
        file = 'SP/h{:d}_r{:.2f}_dens{:.1f}_vs{:.3f}um_SP{}.dat'.format(
            int(altura), radio, densidad_nominal, vs, region)
        np.savetxt(savepath+file, datos)

        # pulso de pi/12
        ppmAxis, spec = medicion.CrearEspectro(secuencia='sp', k=0.08,
                                               Norm=False,
                                               volumen_medido='centro{}'.format(region))        
        datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
        file = 'SP_0.08/h{:d}_r{:.2f}_dens{:.1f}_vs{:.3f}um_SP{}.dat'.format(
            int(altura), radio, densidad_nominal, vs, region)
        np.savetxt(savepath+file, datos)

        # - - - - SMC16
        ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', N=16, k=1,
                                               Norm=False,
                                               volumen_medido='centro{}'.format(region))
        datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
        file = 'SMC/h{:d}_r{:.2f}_dens{:.1f}_vs{:.3f}um_SMC{}.dat'.format(
            int(altura), radio, densidad_nominal, vs, region)
        np.savetxt(savepath+file, datos)

    del muestra, delta, superposicion, medicion
    elapsed_parcial = (time.time() - t0parcial)/60.0
    elapsed = (time.time() - t0)/60.0
    print('---  tiempo parcial: {:.2f} min'.format(elapsed_parcial))
    with open(savepath+'tiempos.dat', 'a') as f:
        f.write(
            f'{int(nnn):d}\t{elapsed:.2f}\t{elapsed_parcial:.2f}\t{distancia:.2f}\t{radio:.2f}\t{altura:.2f}\t{vs:.2f}\n')

    # del muestra, delta, superposicion, medicion, volumen
    # del ppmAxis, spec, datos
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
msj = f"progreso {nnn}/{ntotal} = {nnn/ntotal*100} %"
print(msj)
print(' ')
elapsed = (time.time() - t0)
print(
    f'---  tiempo total: {elapsed:.2f} s = {elapsed/60:.2f} min = {elapsed/60/60:.2f} h')
