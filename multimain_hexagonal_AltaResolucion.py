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

# %%----------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Parametros fisicos
Chi = 24.1*1e-6  # (ppm) Susceptibilidad volumetrica
B0 = 7  # T
skindepth = 14e-13  # profundida de penetracion, mm

Nx = 1024
Ny = 1024

# radio, distancia y vs estan en el archivo:
# parametros = np.loadtxt('./DataBases/ParametrosASimular_hexagonal.par')
# parametros = pd.DataFrame(parametros)
# parametros = parametros.sort_values(by=[1, 2, 0, 3, 4], ascending=True)
# parametros = np.array(parametros)

df = pd.read_csv('./DataBases/ParametrosASimular_hexagonal.par')
df = df[df['Nz'] < 1024]
df = df[df['altura'].isin([10])]
df = df[df['radio'].isin([1,5,50])]
### voxelSize en um:
df = df[df['voxelSize'] >= 0.250]
min_vs = df.groupby(['radio', 'densidad_nominal', 'altura'])['voxelSize'].idxmin()
df = df.loc[min_vs.values]
df = df.sort_values(['radio', 'densidad_nominal'], ascending=[True, False])
# df = df[df['densidad_nominal'] <= 0.15]
# df = df[df['densidad_nominal'].isin([0.2,0.6])]
parametros = np.array(df)

print(df)
# hago una corrida con parametros elegidos:
# parametros = np.array([np.array([0.2500, 512, 50.0000, 2.0000, 5.5000, 0.4976])])


#
# savepath = './Outputs/2023-08-14_Cilindros_hexagonal_AltaResolucion/'
savepath = './Outputs/2024-05-09_CilindrosHexagonal_cantidad-senal/'
with open(savepath+'Densidades.dat', 'w') as f:
    f.write('# distancia (um)\tradio (um)\taltura (um)\tvs (um)\tdensidad\t densidad volumetrica\n')
with open(savepath+'tiempos.dat', 'w') as f:
    f.write('# N_iter\tt_total (min)\tt_iteracion(min)\tradio (um)\tdistancia (um)\taltura (um)\tvs (um)\n')
with open(savepath+'/MasaMedida.dat', 'w') as f:
    f.write(f'# radio(um)\t altura(um)\t voxelSize(um)\t'\
                f'densidad_nominal\t densidad_volumetrica\t'\
                f'masa total(u.a)\t masa microestructuras(u.a)\t masa bulk(u.a)\n')

# inicializo una lista de cuales tienen error.
# inicio el reloj
t0 = time.time()
nnn = -1
ntotal = parametros.shape[0]
# ntotal = 1
for par in parametros:    
    nnn += 1
    if nnn<6: continue 
    # todos los datos estan en um
    vs, Nz, altura, radio, distancia, densidad_nominal, densidad = par

   
    h = int(altura/vs)
    r = int(radio/vs)
    d = int(distancia/vs)

    radio_mm = vs*r*1e-3
    distancia_mm = vs*d*1e-3
    altura_mm = vs*h*1e-3

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
    N = [Nz, Ny, Nx]
    volumen = SimulationVolume(voxelSize=voxelSize, N=N)

    ### la geometria hexagonal sobreescribe medidas[1] y medidas[2]
    medidas = [h*vsz,Ny/2*vsy,Nx/2*vsx]
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ### Creacion de la muestra
    muestra = Muestra(volumen, medidas = medidas,
                      geometria='cilindros_hexagonal',
                      # geometria='cilindros_45grados_hexagonal',
                      # geometria='cilindros_con-angulo_hexagonal', angulo_target=45,
                      radio=radio_mm, distancia=distancia_mm, ubicacion='superior',
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
    delta = Delta(muestra) #, skip=True)
    # SUPERPOSICION DE LAS MICROESTRUCTURAS CON EL BULK -----------------------
    superposicion = Superposicion(muestra, delta, superposicion_lateral=True,
                                  radio=None)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    stl_file = '{}stls/h{:d}_r{:.2f}_dens{:.1f}_vs{:.3f}um'.format(
            savepath, int(altura), radio, densidad_nominal, vs)
    medicion = Medicion(superposicion, volumen_medido='centro', 
                        stl_file=None)    
    # guardado    
    regiones = ['', '-microestructuras', '-bulk']  
    #-------- centro--------------------------------------------------------------
    masas = [] # lista para guardar las masas medidas en cada region
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
        masa_medida = np.sum(medicion.get_volumen_medido())
        masas.append(masa_medida)
                        
        # pulso de pi/12
        # ppmAxis, spec = medicion.CrearEspectro(secuencia='sp', k=0.08,
        #                                        Norm=False,
        #                                        volumen_medido='centro{}'.format(region))        
        # datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
        # file = 'SP_0.08/h{:d}_r{:.2f}_dens{:.1f}_vs{:.3f}um_SP{}.dat'.format(
        #     int(altura), radio, densidad_nominal, vs, region)
        # np.savetxt(savepath+file, datos)

        # - - - - SMC16
        # ppmAxis, spec = medicion.CrearEspectro(secuencia='smc', N=16, k=1,
        #                                        Norm=False,
        #                                        volumen_medido='centro{}'.format(region))
        # datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
        # file = 'SMC/h{:d}_r{:.2f}_dens{:.1f}_vs{:.3f}um_SMC{}.dat'.format(
        #     int(altura), radio, densidad_nominal, vs, region)
        # np.savetxt(savepath+file, datos)
    
    with open(savepath+'/MasaMedida.dat', 'a') as f:
        f.write(f'{radio:.2f}\t{altura:.2f}\t{vs:.3f}\t'\
                f'{densidad_nominal:.2f}\t{densidad_volumetrica:.4f}\t'\
                f'{masas[0]:.4f}\t{masas[1]:.4f}\t{masas[2]:.4f}\n'    )

    
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
