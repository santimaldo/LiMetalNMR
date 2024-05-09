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
plt.rcParams.update({'font.size': 16})

"""
Para una esfera de radio 1 um = 1e-6 m calculo la perturbacion de campo con distintas
discretizaciones.

como tengo la solucion exacta, debo usar metros

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

def autophase(ppmAxis, spec):
  """
  Corrijo automaticamente la fase, utilizando el método de minimizar el area
  de la parte imaginaria:   case{'MinIntImagSpec'}
  """
  precision = 1
  angle=np.arange(-180,180,precision)

  SPECS = []
  IntImagSpec = []
  for i in range(angle.size):
      Sp_try= spec*np.exp(-1j*angle[i]*np.pi/180)
      SPECS.append(Sp_try)
      IntImagSpec.append(np.abs(np.trapz(np.imag(Sp_try),x=ppmAxis)))
  IntImagSpec = np.array(IntImagSpec)
  # indice del minimo:
  idx = np.argmin(IntImagSpec)
  spec = SPECS[idx]
  ind_max = np.argmax(np.abs(np.real(spec)))
  if spec[ind_max]<0:
    spec=-spec
  angle=angle[idx]
  return  spec, angle

def crearEspectro(muestra, eta, x, y, z):
    print("Calculando espectro...")

    eta_obj = eta*muestra
    #FID-----------------------------------------------------------------------
    ppm = 116.641899 # Hz
    # T2est = 0.14*1e-3 # T2est=0.14ms estimado con ancho de espectro. 2020-11-13
    T2est = 10*1e-3 # T2est=0.14ms estimado con ancho de espectro. 2020-11-13
    dw = 20e-6 # sacado de los experimentos. Esto da un SW=857ppm aprox
    NP = 1024 # experimentalmente usamos 2048, pero con 4096 sale mas lindo
    t = np.arange(NP)*dw
    fid = np.zeros_like(t).astype(complex)
    
    #### INTEGRANDO:
    # for jj in range(t.size):
    #   tt = t[jj]
    #   # Valor de la frecuencia en cada voxel
    #   w = 2*np.pi*ppm*(eta_obj)           
    #   # Valor de la fid en cada voxel en el tiempo tt     
    #   fid_t = np.exp(1j*w *tt - tt/T2est)
    #   fid[jj] = Integrar(fid_t, x,y,z)
    
    #### SUMENDO:
    eta_obj = eta[muestra==1]      
    for jj in range(t.size):
      tt = t[jj]
      # Valor de la frecuencia en cada voxel
      w = 2*np.pi*ppm*(eta_obj)           
      # Valor de la fid en cada voxel en el tiempo tt     
      fid_t = np.exp(1j*w *tt - tt/T2est)
      fid[jj] = np.sum(fid_t)
    #FOURIER-------------------------------------------------------------------
    freq = np.fft.fftshift(np.fft.fftfreq(NP, d=dw))
    ppmAxis = freq/ppm
    spec = np.fft.fftshift(np.fft.fft(fid))
    # corrijo la fase:
    spec, angle = autophase(ppmAxis,spec)
    return ppmAxis, np.real(spec)
  
  
"""
para hacer la comparacion voy a poner el valor medio de la solucion exacta dentro del voxel.
"""
def func_exact(zz,yy,xx):
  if (zz*zz+yy*yy+xx*xx <= radius**2):
    f = 2/3*Chi
  else:
    f = (1/3)*Chi*radius**3*(2*zz**2-xx**2-yy**2)/(xx**2+yy**2+zz**2)**(2.5)  
  f = f*B0+B0
  return f

"""
##############################################################################
"""

# inicializo VARIABLES:
Bmac_list = []
Bexact_voxel_list = []
Bexact_0_voxel_list = []
Bexact_0x_voxel_list = []
Bexact_list = []
muestra_list = []
eta_list = []
x_list = []




#inicio el reloj
t0 = time.time()
#----------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# sphere radius
radius = 5 * 1e-6 # m

# Parametros fisicos
Chi =  24.1e-6 #(ppm) Susceptibilidad volumetrica
B0 = 7 # T

# recordar que la convencion de python es {z,y,x}
FOV = 32 * 1e-6 # m

voxelSizes_um   = [0.125, 0.25, 0.5, 1]
ErrorRelativoVolumen = []
Ns = []
Ndiams = []
jj=-1
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
for vs_um in voxelSizes_um:
  jj+=1
  voxelSize = vs_um*1e-6  
  N = int(FOV/voxelSize)
  Ns.append(N)
  N_diam = int(2*radius/voxelSize)
  Ndiams.append(N_diam)
  print(f"N = {N}, voxelSize={voxelSize*1e6} um, "\
        f"voxels-per-diameter: {N_diam} ")
  # CREACION DE LA MUESTRA-----------------------------------------------------
  #------------------------------------------------------------------------------
  #------------------------------------------------------------------------------  
  # x = np.linspace(-FOV/2.0, (FOV/2.0-voxelSize) ,N) # con un voxel centrado en cero
  x = np.linspace(-(FOV-voxelSize)/2.0, (FOV-voxelSize)/2.0,N)# FOV simetrico sin voxel en cero
  # x = np.linspace(-(FOV)/2.0, (FOV)/2.0-voxelSize,N)# FOV simetrico CON voxel en cero
  y = x
  z = x
  
  Z,Y,X= np.meshgrid(z,y,x, indexing='ij')
  
  
  muestra = np.zeros_like(X)
  condicion = X*X+Y*Y+Z*Z <= radius**2
  muestra[condicion] = 1

  V = 4/3*np.pi*(radius)**3
  Vol = np.sum(muestra)*voxelSize**3
  ErrorRela = np.abs(Vol-V)/V*100
  ErrorRelativoVolumen.append(ErrorRela)
  print(f"Volumen discreto: {Vol*1e+18:.2f} um^3, Volumen real: {V*1e+18:.2f} um^3.  Error Relativo: {ErrorRela} %")
  # calculo el campo-----------------------------------------------------------
  #------------------------------------------------------------------------------
  eta = cFS.calculateFieldShift(muestra*Chi, [voxelSize]*3)
    
  Bnuc = eta*B0 + B0
  Bmac = Bnuc/(1-2/3*muestra*Chi)

  # calculo el campo-EXACTO----------------------------------------------------------
  #------------------------------------------------------------------------------
  # solucion exacta en el voxel 
  Bexact_voxel  = np.zeros_like(muestra)
  Bexact_0_voxel  = np.zeros_like(muestra) # exacta que pasa por el centro (eje z) y que tiene misma cantidad de elementos que la muestra
  Bexact_0x_voxel  = np.zeros_like(muestra) # exacta que pasa por el centro (eje x) y que tiene misma cantidad de elementos que la muestra
  for i in range(x.size):
    for j in range(y.size):
      for k in range(z.size):
        Bexact_voxel[k,j,i] = func_exact(z[k],y[j],x[i])  
        Bexact_0_voxel[k,j,i] = func_exact(z[k],0,0)  
        Bexact_0x_voxel[k,j,i] = func_exact(0,0,x[k])  

  nx = int(N/2)
  ny = int(N/2)  
  x0 = x[nx]
  y0 = y[ny]
  
  # solucion exacta al borde del voxel
  zz = np.linspace(z[0],z[-1],4096*8)
  Bexact = []
  yy=y0  
  for j in range(3):
     Bexact_j = np.zeros_like(zz)
     xx = x0+(j-1)*voxelSize/2
     for i in range(np.size(zz)):
       Bexact_j[i] = func_exact(zz[i],yy,xx)
     Bexact.append(Bexact_j)

  # solucion exacta por el centro a lo largo del eje z
  zz = np.linspace(z[0],z[-1],4096*8)
  Bexact_0 = np.zeros_like(zz)
  yy = 0  
  xx = 0
  for i in range(np.size(zz)):
     Bexact_0[i] = func_exact(zz[i],yy,xx)

  # solucion exacta por el centro a lo largo del eje x
  x_ex = np.linspace(x[0],x[-1],4096*8)
  Bexact_0x = np.zeros_like(x_ex)  
  for i in range(np.size(zz)):
     Bexact_0x[i] = func_exact(0,0,x_ex[i])            


  # GUARDO VARIABLES:
  Bmac_list.append(Bmac)
  Bexact_voxel_list.append(Bexact_voxel)
  Bexact_0_voxel_list.append(Bexact_0_voxel)
  Bexact_0x_voxel_list.append(Bexact_0_voxel)
  Bexact_list.append(Bexact)
  muestra_list.append(muestra)
  eta_list.append(eta)
  x_list.append(x)  

  

  
#%%### GRAFICOS ###############################################################

#### figura de la muestra
size = 5
fig_muestra = plt.figure(1, figsize=(size*2, size*2), constrained_layout=False)
gs = fig_muestra.add_gridspec(2, 2, hspace=0, wspace=0)
axs_muestra = gs.subplots(sharex=True, sharey=True)
# fig_muestra.suptitle('Sharing both axes')  

#### figura de la matriz eta
size = 5
fig_eta = plt.figure(2, figsize=(size*2, size*2), constrained_layout=False)
gs = fig_eta.add_gridspec(2, 2, hspace=0, wspace=0)
axs_eta = gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  

#### figura de B mac (eje z)
size = 5
fig_Bmac= plt.figure(3, figsize=(size*2, size*2), constrained_layout=False)
gs = fig_Bmac.add_gridspec(2, 2, hspace=0, wspace=0)
axs_Bmac= gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
# vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  

#### figura de Errores (eje z)
size = 5
fig_Error= plt.figure(4, figsize=(size*2, size*2), constrained_layout=False)
gs = fig_Error.add_gridspec(2, 2, hspace=0, wspace=0)
axs_Error= gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
# vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  

#### figura de B mac (eje x)
size = 5
fig_Bmac_x= plt.figure(5, figsize=(size*2, size*2), constrained_layout=False)
gs = fig_Bmac_x.add_gridspec(2, 2, hspace=0, wspace=0)
axs_Bmac_x= gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
# vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  

#### figura de Errores (eje x)
size = 5
fig_Error_x= plt.figure(6, figsize=(size*2, size*2), constrained_layout=False)
gs = fig_Error_x.add_gridspec(2, 2, hspace=0, wspace=0)
axs_Error_x= gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
# vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  


#### figura de histogramas
size = 5
fig_hist= plt.figure(8, figsize=(size*2, size*2), constrained_layout=False)
gs = fig_hist.add_gridspec(2, 2, hspace=0, wspace=0)
axs_hist= gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
# vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  


jj=-1
for N in Ns:
  jj+=1  
  voxelSize = FOV/float(N)
  voxelSize_um = voxelSizes_um[jj]
  N_diam = Ndiams[jj]
  # cargo variables
  Bmac = Bmac_list[jj]
  Bexact_voxel = Bexact_voxel_list[jj]
  Bexact_0_voxel = Bexact_0_voxel_list[jj]
  Bexact_0x_voxel = Bexact_0x_voxel_list[jj]
  Bexact = Bexact_list[jj]
  muestra = muestra_list[jj]
  eta = eta_list[jj]
  # paso a micros:
  x = x_list[jj] *1e6 
  FOV_um = FOV*1e6

  y = x
  z = x  
  Z,Y,X= np.meshgrid(z,y,x, indexing='ij')

  ### SETEO PARAMETROS GRAFICOS###  
  title_Nvoxels = r"$N_{voxels} = $"+ f" {N}"
  
  esf_lim_col =  'k' # color del limite de la esfera
  esf_lim_w   =  2 # ancho de linea del limite de la esfera
  xlim_hist = [11.4,22.4] # limites del histograma
  ################################
  
  nx = int(N/2)
  ny = int(N/2)  
  nz = int(N/2)
  x0 = x[nx]
  y0 = y[ny]  
  
  # MUESTRA
  ax=axs_muestra[np.unravel_index(jj,(2,2))]  
  ax.set_aspect('equal', 'box')  
  ax.pcolormesh(X[:,ny,:], Z[:,ny,:], muestra[:,ny,:], cmap='gray_r', shading='nearest')
  ax.set_xlabel(r"x [$\mu$m]", fontsize=22)
  ax.set_ylabel(r"z [$\mu$m]", fontsize=22)  
  circle = plt.Circle((0, 0), radius*1e6, color='red', ls='--', lw=2, fill=False)
  ax.add_patch(circle)    
  ax.set_xlim([x[0],x[-1]])    
  ax.set_ylim([z[0],z[-1]])    
  ax.label_outer()  
  legend = fr"voxel length: {voxelSize_um} $\mu$m"\
             "\n"\
            f"# voxels per diameter: {N_diam}"
  ax.text(-0.4*FOV_um,0.3*FOV_um,  legend, fontsize=16)
  # 1 voxel :
  XX = X[int(ny/2)-1:int(ny/2)+1:,ny,int(ny/2)-1:int(ny/2)+1]    
  ZZ = Z[int(ny/2)-1:int(ny/2)+1:,ny,int(ny/2)-1:int(ny/2)+1]
  muestra_tmp = muestra[int(ny/2):int(ny/2)+2:,ny,int(ny/2):int(ny/2)+2]    
  ax.pcolormesh(XX, ZZ, XX*0, cmap='gray_r', shading='nearest', edgecolor='b')            
  ax.text(XX[0,1]+1,ZZ[0,0],  "voxels", fontsize=16, color='b')
  
  
  # grafico de eta o (Bmac-B0)/B0
  ax=axs_eta[np.unravel_index(jj,(2,2))]  
  ax.set_aspect('equal', 'box')  
  #pcol = ax.pcolormesh(X[:,ny,:], Z[:,ny,:], eta[:,ny,:]*1e6, cmap='seismic', vmax=vmax_eta, vmin=-vmax_eta, shading='nearest')  
  deltaB_mac = (Bmac[:,ny,:]-B0)/B0*1e6
  vmax_eta = 17
  pcol = ax.pcolormesh(X[:,ny,:], Z[:,ny,:], deltaB_mac, cmap='seismic', vmax=vmax_eta, vmin=-vmax_eta, shading='nearest')  
  ax.set_xlabel(r"x [$\mu$m]", fontsize=22)
  ax.set_ylabel(r"z [$\mu$m]", fontsize=22)  
  circle = plt.Circle((0, 0), radius*1e6, color='k', ls='--', lw=2, fill=False)
  ax.add_patch(circle)  
  if jj in [1,3]:
    # Create new axes according to image position
    cax = fig_eta.add_axes([ax.get_position().x1+0.01,
                        ax.get_position().y0,
                        0.02,
                        ax.get_position().height])     
    # Plot vertical colorbar
    cbar = plt.colorbar(pcol, cax=cax)
    cbar.set_label(r"$(B_{mac}-B_0)/B_0$ [ppm]", fontsize=22)      
    # cbar.set_ticks()
    # cbar.ax.set_yticklabels(labels,fontsize=16)
  ax.set_xlim([x[0],x[-1]])    
  ax.set_ylim([z[0],z[-1]])    
  ax.label_outer()
  # ax.text(-0.25*FOV_um,0.35*FOV_um, r"$N_{voxels} = $"+ fr" {N}$^3$", fontsize=22)
  ax.text(-0.4*FOV_um,0.3*FOV_um,  legend, fontsize=16)





  # grafico de Bmac (eje z)
  Bmac_z = Bmac[:,ny,nx]
  Bexact_voxel_z = Bexact_voxel[:,ny,nx]
  Bexact_0_voxel_z = Bexact_0_voxel[:,ny,nx]
  vmin = np.min(np.array([Bmac_z,Bexact_voxel_z]))
  vmax = np.max(np.array([Bmac_z,Bexact_voxel_z]))
  
  ax=axs_Bmac[np.unravel_index(jj,(2,2))]  
  # ax.set_aspect('box')  
  # ax.axvspan(-radius,radius, facecolor='lightgray', alpha=0.5)
  ax.axvspan(-1,1, facecolor='lightgray', alpha=0.5)
  ax.plot(z/(radius*1e6) , (Bmac_z-B0)/B0*1e6,'bo--', label=fr"Numeric")
  ax.plot(zz/(radius) , (Bexact_0-B0)/B0*1e6, 'k--', lw = 3, label=f"Exact" )  
  ax.set_xlabel(r"$z/r_{sphere}$", fontsize=22)
  ax.set_ylabel(r"$(B_{mac}-B_0)/B_0$ [ppm]", fontsize=22)
  ax.set_ylim([-1,24])
  ax.set_xlim([-6,6])
  ax.set_xticks(np.linspace(-5,5,6))
  ax.text(-5,20,  legend, fontsize=16)
  ax.label_outer()
  # ax.text(-0.25*FOV_um,0.35*FOV_um, r"$N_{voxels} = $"+ fr" {N}$^3$", fontsize=22)
  if jj==2:
    # ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, fontsize=10)
    ax.legend(loc='center right', fancybox=True, fontsize=12)


  # grafico de ERRORES
  Bmac_z = Bmac[:,ny,nx]
  Bexact_voxel_z = Bexact_voxel[:,ny,nx]
  Bexact_0_voxel_z = Bexact_0_voxel[:,ny,nx]
  vmin = np.min(np.array([Bmac_z,Bexact_voxel_z]))
  vmax = np.max(np.array([Bmac_z,Bexact_voxel_z]))
  ax=axs_Error[np.unravel_index(jj,(2,2))]      
  ax.axvspan(-1,1, facecolor='lightgray', alpha=0.5)  
  ax.plot(z/(radius*1e6) , (Bmac[:,ny,nx]-Bexact_voxel[:,ny,nx])/B0*1e6,'bo--')  
  ax.axhline(0, color="k", ls='--')
  ax.set_xlabel(r"$z/r_{sphere}$", fontsize=22)
  ax.set_ylabel(r"$(B_{Numeric}-B_{Exact})/B_0$ [ppm]", fontsize=20)  
  ax.label_outer()
  ax.set_xlim([-6,6])
  ax.set_ylim([-0.9,1.5])
  ax.set_xticks(np.linspace(-5,5,6))  
  ax.text(-5,1,  legend, fontsize=16)

  # ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, fontsize=10)


  # grafico de Bmac (eje x)
  Bmac_x = Bmac[nz,ny,:]
  Bexact_voxel_x = Bexact_voxel[nz,ny,:]
  Bexact_0x_voxel_x = Bexact_0x_voxel[nz,ny,:]
  vmin = np.min(np.array([Bmac_z,Bexact_voxel_x]))
  vmax = np.max(np.array([Bmac_z,Bexact_voxel_x]))
  
  ax=axs_Bmac_x[np.unravel_index(jj,(2,2))]  
  # ax.set_aspect('box')  
  # ax.axvspan(-radius,radius, facecolor='lightgray', alpha=0.5)
  ax.axvspan(-1,1, facecolor='lightgray', alpha=0.5)
  ax.plot(x/(radius*1e6) , (Bmac_x-B0)/B0*1e6,'bo--', label=fr"Numeric")
  ax.plot(x_ex/(radius) , (Bexact_0x-B0)/B0*1e6, 'k--', lw = 3, label=f"Exact" )  
  ax.set_xlabel(r"$x/r_{sphere}$", fontsize=22)
  ax.set_ylabel(r"$(B_{mac}-B_0)/B_0$ [ppm]", fontsize=22)
  ax.set_ylim([-9,22])
  ax.set_xticks(np.linspace(-7,7,8))
  ax.text(-8,18,  legend, fontsize=16)
  ax.label_outer()
  # ax.text(-0.25*FOV_um,0.35*FOV_um, r"$N_{voxels} = $"+ fr" {N}$^3$", fontsize=22)
  if jj==2:
    # ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, fontsize=10)
    ax.legend(loc='center right', fancybox=True, fontsize=12)


  # grafico de ERRORES (eje x)
  Bmac_x = Bmac[nz,ny,:]
  Bexact_voxel_x = Bexact_voxel[nz,ny,:]
  Bexact_0x_voxel_x = Bexact_0x_voxel[nz,ny,:]
  vmin = np.min(np.array([Bmac_z,Bexact_voxel_x]))
  vmax = np.max(np.array([Bmac_z,Bexact_voxel_x]))
  ax=axs_Error_x[np.unravel_index(jj,(2,2))]      
  ax.axvspan(-1,1, facecolor='lightgray', alpha=0.5)  
  #ax.plot(x/(radius*1e6) , abs(Bmac[nz,ny,:]-Bexact_voxel[nz,ny,:])/B0*1e6,'bo--')  
  ax.plot(x/(radius*1e6) , (Bmac[nz,ny,:]-Bexact_voxel[nz,ny,:])/B0*1e6,'bo--')  
  ax.axhline(0, color="k", ls='--')
  ax.set_xlabel(r"$x/r_{sphere}$", fontsize=22)
  ax.set_ylabel(r"$(B_{Numeric}-B_{Exact})/B_0$ [ppm]", fontsize=20)  
  ax.label_outer()
  ax.set_ylim([-2.4,1.6])
  ax.set_xticks(np.linspace(-7,7,8))  
  ax.text(-8,1,  legend, fontsize=14)




  # grafico de HISTOGRAMAS  
  ax=axs_hist[np.unravel_index(jj,(2,2))]      
  
  #data = (Bmac[muestra==1]-B0)/B0*1e6
  #data = (eta[muestra==1])*1e6
  #bins = np.arange(0,8,0.5)-3.75
  #h = ax.hist(data, weights = np.ones_like(data)/np.sum(muestra), bins=bins, facecolor='b', edgecolor='k')
  data = (Bmac[muestra==1]-Bexact_voxel[muestra==1])/B0*1e6  
  h = ax.hist(data, weights = np.ones_like(data)/np.sum(muestra), facecolor='b', edgecolor='k')
  # ax.axvline(Chi*2/3*1e6, color='k', ls='--', lw=2)
  ax.axvline(0, color='k', ls='--', lw=2)
  if jj>2:
    # ax.set_xlabel(r"$\eta$ [ppm]",fontsize=22)
    # ax.set_xlabel(r"$|B_{mac,z}^{numerico}-B_{mac,z}^{exacto}|/B_0$ [ppm]", fontsize=18)  
    ax.set_xlabel(r"$(B_{Numeric}-B_{Exact})/B_0$ [ppm]", fontsize=20)  
  ax.set_ylabel("")
  ax.set_xticks(np.arange(-4,5))
  ax.yaxis.set_major_formatter(PercentFormatter(1))
  ax.text(-3.75,0.9,  legend, fontsize=16)
  ax.set_ylim([0,1.02])
  ax.set_xlim([-4.5,4.5])
  ax.label_outer()

print("Errores Porcentuales en el volumen de la esfera:")
for jj in range(len(Ns)):
  print(f"N = { Ns[jj]}  Error Rela = {ErrorRelativoVolumen[jj]:.2f} %")  

elapsed = (time.time() - t0)/60
print('---  tiempo: {:.2f} min'.format(elapsed))
# %%
