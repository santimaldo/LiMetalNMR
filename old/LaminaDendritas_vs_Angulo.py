#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""
# stop

import numpy as np
import matplotlib.pyplot as plt
import Modules.calculateFieldShift as cFS
from scipy import integrate
import time
from matplotlib.ticker import PercentFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.spatial.transform import Rotation as R

from Modules.SimulationVolume import *
from Modules.Muestra import *
from Modules.Delta import *
from Modules.Superposicion import *
from Modules.Graficador import *
from Modules.Medicion import *
#%%


plt.rcParams.update({'font.size': 16})

"""
Para una esfera de radio 0.1 m calculo la perturbacion de campo con distintas
discretizaciones.

Dejo fijo el FOV y cambio el voxelSize, la esgera es siempre del mismo diametro
"""


"""
##############################################################################
FUNCIONES:
"""
def Integrar(Matriz, x, y, z):
  """
  Integracion 3d  
  x,y,z son vectores 1D
  """
  i = (integrate.simps(integrate.simps(integrate.simps(Matriz, x=z), x=y),x=x))
  return i

  
def Rotacion_y(X,Y,Z,ang):
  """
  ang en radianes
  """  
  # define rotation by rotation angle and axis, here 45DEG around z-axis
  r = R.from_rotvec(ang * np.array([0, 1, 0]))
  
  # arrange point coordinates in shape (N, 3) for vectorized processing
  XYZ = np.array([X.ravel(), Y.ravel(), Z.ravel()]).transpose()
  
  # apply rotation
  XYZrot = r.apply(XYZ)
  
  # return to original shape of meshgrid
  Xrot = XYZrot[:, 0].reshape(X.shape)
  Yrot = XYZrot[:, 1].reshape(X.shape)
  Zrot = XYZrot[:, 2].reshape(X.shape)
  return Xrot, Yrot, Zrot
  

"""
##############################################################################
"""

# inicializo VARIABLES:
Bmac_list = []
muestra_list = []
eta_list = []
x_list = []
specs_list = []


objetos_muestra = []
deltas = []
superposiciones = []
mediciones = []


#inicio el reloj
t0 = time.time()
#----------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Parametros fisicos
Chi =  24.1e-6 #(ppm) Susceptibilidad volumetrica
B0 = 7 # T

# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
voxelSize = 0.012
N = 256
volumen = SimulationVolume(voxelSize=[voxelSize]*3, N=[N]*3)
FOV = voxelSize*N

# FOV = 3.2
# N = 64
# voxelSize = 0.1
# volumen = SimulationVolume(FOV=[FOV]*3, N=[N]*3)



semiLado = 3/2 # mm
semiEspesor = 0.7/2 # mm

# x = np.linspace(-FOV/2.0, (FOV/2.0-voxelSize) ,N) # con un voxel centrado en cero
x = np.linspace(-(FOV-voxelSize)/2.0, (FOV-voxelSize)/2.0,N)# FOV simetrico sin voxel en cero
# x = np.linspace(-(FOV)/2.0, (FOV)/2.0-voxelSize,N)# FOV simetrico CON voxel en cero
y = x
z = x

Z,Y,X= np.meshgrid(z,y,x, indexing='ij')

ny = int(N/2) # slice en y para los graficos
ny = 140

# angulos  =  np.array([0,5,15,30,45,60,75,85,90])*np.pi/180
angulos  =  np.array([0,5,10,15,20,25,30,45,90,180])*np.pi/180
# angulos  =  np.linspace(0,90,16)*np.pi/180
# angulos  =  np.array([0])*np.pi/180
AgregarDendritas = True

ErrorRelativoVolumen = []
jj=-1
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
for ang in angulos:
  jj+=1
  print(f"Angulo = {ang*180/np.pi}°")
  # CREACION DE LA MUESTRA-----------------------------------------------------
  #------------------------------------------------------------------------------
  #------------------------------------------------------------------------------
  
  Xrot, Yrot, Zrot = Rotacion_y(X,Y,Z,ang)  
  
  
  ### Lamina
  muestra = np.zeros_like(X)
  # condiciones:
  c1 = np.zeros_like(X)
  c2 = np.zeros_like(X)
  c3 = np.zeros_like(X)
  c1[np.abs(Xrot)<semiLado] = 1
  c2[np.abs(Yrot)<semiLado] = 1
  c3[np.abs(Zrot)<semiEspesor] = 1

  muestra = c1*c2*c3
  ### Dendritas
  espacio = 10*0.012
  ancho = 4*0.012
  altura = 7*0.012
  
  if AgregarDendritas:
    z0 = semiEspesor
    x0 = -semiLado
    while x0<semiLado-espacio:    
      x0 += espacio + ancho
      y0 = -semiLado
      while y0<semiLado-espacio:      
        y0 += espacio + ancho      
        condicion = 1 * (np.abs(Xrot-x0)<ancho) * (np.abs(Yrot-y0)<ancho) * (np.abs(Zrot-(z0+altura/2))<altura/2)
        muestra += condicion  
    muestra = 1*(muestra>0)
  
  obj_muestra = Muestra(volumen, medidas=volumen[2], geometria='bulk', exceptions=False) # para 'porcentaje_palos'   
  obj_muestra.muestra = muestra*Chi
  
  delta = Delta(obj_muestra)
  
  superposicion = Superposicion(obj_muestra, delta, superposicion=False)
#%%
# for medicion in mediciones:
  medicion = Medicion(superposicion, volumen_medido='esfera')
  ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, Norm=True, T2est=0.3*1e-3)
#%%  
  
  Vol = np.sum(muestra)*voxelSize**3  
  print(f"Volumen discreto: {Vol}")
  # calculo el campo-----------------------------------------------------------
  #------------------------------------------------------------------------------
  eta = delta.delta*1e-6 # delta ya esta en ppm, asi que escribo eta en valor absoluto
  Bnuc = eta*B0 + B0
  Bmac = Bnuc/(1-2/3*muestra*Chi)
    

  # GUARDO VARIABLES:
  Bmac_list.append(Bmac)
  muestra_list.append(muestra)
  eta_list.append(eta)
  specs_list.append([ppmAxis, spec])
  
  objetos_muestra.append(obj_muestra)
  deltas.append(delta)
  superposiciones.append(superposicion)
  mediciones.append(medicion)
 

  
#%%### GRAFICOS ###############################################################

Nfilas = 3
Ncols = 3


#### figura de la muestra
size = 5
fig_muestra = plt.figure(1, figsize=(size*2, size*2), constrained_layout=False)
gs = fig_muestra.add_gridspec(Nfilas, Ncols, hspace=0, wspace=0)
axs_muestra = gs.subplots(sharex=True, sharey=True)
# fig_muestra.suptitle('Sharing both axes')  

# #### figura de la matriz eta
size = 5
fig_eta = plt.figure(2, figsize=(size*2, size*2), constrained_layout=False)
gs = fig_eta.add_gridspec(Nfilas, Ncols, hspace=0, wspace=0)
axs_eta = gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(N/2),:])) for nn in range(angulos.size)])*1e6
# fig_muestra.suptitle('Sharing both axes')  

#### figura de espectros
size = 5
fig_spec= plt.figure(3, figsize=(size*2, size*2), constrained_layout=False)
gs = fig_spec.add_gridspec(Nfilas, Ncols, hspace=0, wspace=0)
axs_spec= gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
# vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  

# #### figura de Errores
# size = 5
# fig_Error= plt.figure(4, figsize=(size*3, size*2), constrained_layout=False)
# gs = fig_Error.add_gridspec(2, 3, hspace=0, wspace=0)
# axs_Error= gs.subplots(sharex=True, sharey=True)
# # busco el maximo de todos los etas
# # vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# # fig_muestra.suptitle('Sharing both axes')  


# #### figura de histogramas
# size = 5
# fig_hist= plt.figure(5, figsize=(size*2, size*2), constrained_layout=False)
# gs = fig_hist.add_gridspec(Nfilas, Ncols, hspace=0, wspace=0)
# axs_hist= gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
# vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  


delta_vs_ang=[]
jj=-1
for ang in angulos:
  jj+=1  
  voxelSize = FOV/float(N)
  # cargo variables
  Bmac = Bmac_list[jj]
  ppmAxis, spec = specs_list[jj]
  # Bexact_0_voxel = Bexact_0_voxel_list[jj]
  # Bexact = Bexact_list[jj]
  medicion = mediciones[jj]
  muestra = muestra_list[jj]
  eta = eta_list[jj]
  # x = x_list[jj]  
  # y = x
  # z = x  
  # Z,Y,X= np.meshgrid(z,y,x, indexing='ij')
  
  ### SETEO PARAMETROS GRAFICOS###  
  title_Nvoxels = r"$N_{voxels} = $"+ f" {N}"
  
  esf_lim_col =  'k' # color del limite de la esfera
  esf_lim_w   =  2 # ancho de linea del limite de la esfera
  xlim_hist = [11.4,22.4] # limites del histograma
  ################################
  

  
  # MUESTRA
  ax=axs_muestra[np.unravel_index(jj,(Nfilas, Ncols))]  
  ax.set_aspect('equal', 'box')  
  ax.pcolormesh(X[:,ny,:], Z[:,ny,:], muestra[:,ny,:], cmap='gray_r', shading='nearest')
  ax.set_xlabel("x [mm]", fontsize=22)
  ax.set_ylabel("z [mm]", fontsize=22)  
  if jj in [1,2,4,5]:
    ax.set_yticks([])
  if jj!=4:
    ax.set_xticks([])
  ax.set_xlim([x[0],x[-1]])    
  ax.set_ylim([z[0],z[-1]])    
  ax.label_outer()
  # ax.text(-0.25*FOV,0.35*FOV, r"$N_{voxels} = $"+ fr" {N}$^3$", fontsize=22)

  

  
  # grafico de Bmac
  matriz = (Bmac[:,ny,:]-B0)/B0*1e6
  # metriz = eta[:,ny,:]
  ax=axs_eta[np.unravel_index(jj,(Nfilas, Ncols))]  
  ax.set_aspect('equal', 'box')  
  # pcol = ax.pcolormesh(X[:,ny,:], Z[:,ny,:], eta[:,ny,:]*1e6, cmap='magma_r', vmax=vmax_eta, vmin=-vmax_eta, shading='nearest')
  pcol = ax.pcolormesh(X[:,ny,:], Z[:,ny,:], matriz, cmap='inferno_r', shading='nearest')  
  ax.set_xlabel("x [mm]", fontsize=22)
  ax.set_ylabel("z [mm]", fontsize=22)  
  # if jj in [1,2,4,5]:
  #   ax.set_yticks([])
  # if jj!=4:
  #   ax.set_xticks([])
  # if jj in [2,5]:
  #   # Create new axes according to image position
  #   cax = fig_eta.add_axes([ax.get_position().x1+0.01,
  #                       ax.get_position().y0,
  #                       0.02,
  #                       ax.get_position().height])     
  #   # Plot vertical colorbar
  #   cbar = plt.colorbar(pcol, cax=cax)
  #   cbar.set_label(r'$\eta$ [ppm]', fontsize=22)      
  #   # cbar.set_ticks()
  #   # cbar.ax.set_yticklabels(labels,fontsize=16)
  ax.set_xlim([x[0],x[-1]])    
  ax.set_ylim([z[0],z[-1]])    
  ax.label_outer()
  # ax.text(-0.25*FOV,0.35*FOV, r"$N_{voxels} = $"+ fr" {N}$^3$", fontsize=22)
  





  # # grafico de Espectros
  ppmAxis, spec = medicion.CrearEspectro(secuencia='sp' , k=0.5, figure=153, Norm=True, T2est=0.25*1e-3)
  
  filename = f"S:/Doctorado/LiMetal/Analisis/2019-12_Dendritas_vsAngulo/2022-05_SIMULACIONES/spec_{ang*180/np.pi:.0f}grad.dat"
  datos = np.array([ppmAxis, np.real(spec), np.imag(spec)]).T
  np.savetxt(filename, datos)
  
  ax=axs_spec[np.unravel_index(jj,(Nfilas,Ncols))]  
  # ax.set_aspect('box')    
  # ax.vlines(-diametro/2,vmin, vmax, color='r', ls='--', lw=2)
  ax.plot(ppmAxis, np.real(spec), 'b', lw = 3)    
  ax.set_xlabel(r"$\delta$ [ppm]", fontsize=22)  
  # ax.text(-4,17.5,  fr"N = {N}", fontsize=22)   
  ax.label_outer()
  ax.set_xlim([50, -50])

  # # grafico de ERRORES
  # Bmac_z = Bmac[:,ny,nx]
  # Bexact_voxel_z = Bexact_voxel[:,ny,nx]
  # Bexact_0_voxel_z = Bexact_0_voxel[:,ny,nx]
  # vmin = np.min(np.array([Bmac_z,Bexact_voxel_z]))
  # vmax = np.max(np.array([Bmac_z,Bexact_voxel_z]))
  # ax=axs_Error[np.unravel_index(jj,(2,3))]      
  # ax.axvspan(-1,1, facecolor='lightgray', alpha=0.5)  
  # ax.plot(z/(diametro/2) , abs(Bmac[:,ny,nx]-Bexact_0_voxel[:,ny,nx])/B0*1e6,'bo--')  
  # ax.axhline(0, color="k", ls='--')
  # ax.set_xlabel(r"$z/r_{esfera}$", fontsize=22)
  # ax.set_ylabel(r"Error Absoluto [ppm]", fontsize=22)  
  # ax.label_outer()
  # ax.text(-4,2.5,  fr"N = {N}", fontsize=22)

  # # ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, fontsize=10)


  # # grafico de HISTOGRAMAS  
  # ax=axs_hist[np.unravel_index(jj,(Nfilas, Ncols))]      
  
  # data = (Bmac[muestra==1]-B0)/B0*1e6  
  # hist, bins, _ = ax.hist(data, weights = np.ones_like(data)/np.sum(muestra), facecolor='b', edgecolor='k')
  # ax.set_ylabel("")
  # ax.yaxis.set_major_formatter(PercentFormatter(1))
  # ax.label_outer()
  ####
  # ind = np.where(hist==np.max(hist))[0]  
  # delta = (bins[ind] + bins[1] - bins[0])/2
  # delta_vs_ang.append(delta[0])
  
  # defino delta como lo que se encuentra al medio de la lamina
  Xrot, Yrot, Zrot = Rotacion_y(X,Y,Z,ang)  
  mask = np.zeros_like(X)
  mask[Xrot**2+Yrot**2<(0.05*semiLado)**2] = 1
  mask2 = np.zeros_like(X)
  mask2[np.abs(Zrot)<(semiEspesor/4)] = 1
  mask = mask*mask2
  # mask = muestra*mask
  data = (Bmac[mask==1]-B0)/B0*1e6  
  delta_ang = np.mean(data)
  delta_vs_ang.append(delta_ang)

# print("Errores Porcentuales en el volumen de la esfera:")
# for jj in range(len(Ns)):
#   print(f"N = { Ns[jj]}  Error Rela = {ErrorRelativoVolumen[jj]:.2f} %")  


plt.figure(100)
plt.plot(angulos*180/np.pi, delta_vs_ang, 'o-')
plt.xlabel("Ángulo [°]")
plt.ylabel(r"$(B_{in,z}-B_0)/B_0$ [ppm]")
plt.axhline(0   , color="k", ls='--')
plt.axhline(24.1, color="k", ls='--')



elapsed = (time.time() - t0)/60
print('---  tiempo: {:.2f} min'.format(elapsed))