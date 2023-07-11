#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:18:27 2020

@author: santi
"""


import numpy as np
import matplotlib.pyplot as plt
import Modules.calculateFieldShift as cFS
from scipy import integrate
import time
from matplotlib.ticker import PercentFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.spatial.transform import Rotation as R
plt.rcParams.update({'font.size': 16})

"""
Para una disco de diametro 12 mm calculo perfiles variando el FOV

dejo fijo voxelSize
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
Bexact_voxel_list = []
Bexact_0_voxel_list = []
Bexact_list = []
muestra_list = []
eta_list = []
x_list = []




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

radio = 6
espesor = 0.7
Nxy_list = [512,256,128,64]

ErrorRelativoVolumen = []
jj=-1
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
for Nxy in Nxy_list:
  jj+=1
  print(f"Nxy = {Nxy}")
  # CREACION DE LA MUESTRA-----------------------------------------------------
  #------------------------------------------------------------------------------
  #------------------------------------------------------------------------------
  
  vS = 0.2
  Nz= 128
  FOVxy = vS*Nxy
  FOVz = vS*Nz
  
  N = [Nxy, Nxy, Nz]
  voxelSize = [vS]*3
  
  
  # x = np.linspace(-FOV/2.0, (FOV/2.0-voxelSize) ,N) # con un voxel centrado en cero
  x = np.linspace(-(FOVxy-vS)/2.0, (FOVxy-vS)/2.0,Nxy)# FOV simetrico sin voxel en cero
  # x = np.linspace(-(FOV)/2.0, (FOV)/2.0-voxelSize,N)# FOV simetrico CON voxel en cero
  y = x
  z = np.linspace(-(FOVz-vS)/2.0, (FOVz-vS)/2.0,Nz)# FOV simetrico sin voxel en cero

  Z,Y,X= np.meshgrid(z,y,x, indexing='ij')

  
  muestra = np.zeros_like(X)
  # condiciones:
  c1 = (X*X+Y*Y)<radio**2
  c2 = np.abs(Z)<espesor/2
  muestra = 1*(c1*c2)

  # calculo el campo-----------------------------------------------------------
  #------------------------------------------------------------------------------
  eta = cFS.calculateFieldShift(muestra*Chi, voxelSize)    
  Bnuc = eta*B0 + B0
  Bmac = Bnuc/(1-2/3*muestra*Chi)


  plt.figure(12672)
  plt.plot(z, eta[:,int(Nxy/2),int(Nxy/2)], 'o-', label=f"FOVxy = {FOVxy}")

  # GUARDO VARIABLES:
  Bmac_list.append(Bmac)  
  muestra_list.append(muestra)
  eta_list.append(eta)
 
plt.legend()
plt.show()  
#%%### GRAFICOS ###############################################################

Nfilas = 4
Ncols = 4


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



# #### figura de histogramas
size = 5
fig_hist= plt.figure(5, figsize=(size*2, size*2), constrained_layout=False)
gs = fig_hist.add_gridspec(Nfilas, Ncols, hspace=0, wspace=0)
axs_hist= gs.subplots(sharex=True, sharey=True)
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
  # Bexact_voxel = Bexact_voxel_list[jj]
  # Bexact_0_voxel = Bexact_0_voxel_list[jj]
  # Bexact = Bexact_list[jj]
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
  
  nx = int(N/2)
  ny = int(N/2)  
  x0 = x[nx]
  y0 = y[ny]  
  
  # MUESTRA
  ax=axs_muestra[np.unravel_index(jj,(Nfilas, Ncols))]  
  ax.set_aspect('equal', 'box')  
  ax.pcolormesh(X[:,ny,:], Z[:,ny,:], muestra[:,ny,:], cmap='gray_r', shading='nearest')
  ax.set_xlabel("x", fontsize=22)
  ax.set_ylabel("z", fontsize=22)  
  if jj in [1,2,4,5]:
    ax.set_yticks([])
  if jj!=4:
    ax.set_xticks([])
  ax.set_xlim([x[0],x[-1]])    
  ax.set_ylim([z[0],z[-1]])    
  ax.label_outer()
  # ax.text(-0.25*FOV,0.35*FOV, r"$N_{voxels} = $"+ fr" {N}$^3$", fontsize=22)

  

  
  # grafico de eta
  ax=axs_eta[np.unravel_index(jj,(Nfilas, Ncols))]  
  ax.set_aspect('equal', 'box')  
  # pcol = ax.pcolormesh(X[:,ny,:], Z[:,ny,:], eta[:,ny,:]*1e6, cmap='magma_r', vmax=vmax_eta, vmin=-vmax_eta, shading='nearest')
  pcol = ax.pcolormesh(X[:,ny,:], Z[:,ny,:], (Bmac[:,ny,:]-B0)/B0*1e6, cmap='inferno_r', shading='nearest', vmin=0, vmax=25)  
  ax.set_xlabel("x", fontsize=22)
  ax.set_ylabel("z", fontsize=22)  
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
  




  # # grafico de HISTOGRAMAS  
  ax=axs_hist[np.unravel_index(jj,(Nfilas, Ncols))]      
  
  data = (Bmac[muestra==1]-B0)/B0*1e6  
  hist, bins, _ = ax.hist(data, weights = np.ones_like(data)/np.sum(muestra), facecolor='b', edgecolor='k')
  ax.set_ylabel("")
  ax.yaxis.set_major_formatter(PercentFormatter(1))
  ax.label_outer()
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
  delta = np.mean(data)
  delta_vs_ang.append(delta)

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