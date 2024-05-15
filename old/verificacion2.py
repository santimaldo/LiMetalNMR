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
  if (zz*zz+yy*yy+xx*xx <= (diametro/2.0)**2):
    f = 2/3*Chi
  else:
    f = (1/3)*Chi*(diametro/2.0)**3*(2*zz**2-xx**2-yy**2)/(xx**2+yy**2+zz**2)**(2.5)  
  f = f*B0+B0
  return f

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
FOV = 0.512

Ns   = [256,128,64,32,16,8]
ErrorRelativoVolumen = []
jj=-1
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
# Calculos ###################################################################
for N in Ns:
  jj+=1
  voxelSize = FOV/float(N)
  print(f"N = {N}, voxelSize={voxelSize}")
  # CREACION DE LA MUESTRA-----------------------------------------------------
  #------------------------------------------------------------------------------
  #------------------------------------------------------------------------------
  diametro = 0.128
  # x = np.linspace(-FOV/2.0, (FOV/2.0-voxelSize) ,N) # con un voxel centrado en cero
  x = np.linspace(-(FOV-voxelSize)/2.0, (FOV-voxelSize)/2.0,N)# FOV simetrico sin voxel en cero
  # x = np.linspace(-(FOV)/2.0, (FOV)/2.0-voxelSize,N)# FOV simetrico CON voxel en cero
  y = x
  z = x
  
  Z,Y,X= np.meshgrid(z,y,x, indexing='ij')
  
  
  muestra = np.zeros_like(X)
  condicion = X*X+Y*Y+Z*Z <= (diametro/2.0)**2
  muestra[condicion] = 1

  V = 4/3*np.pi*(diametro/2)**3
  Vol = np.sum(muestra)*voxelSize**3
  ErrorRela = np.abs(Vol-V)/V*100
  ErrorRelativoVolumen.append(ErrorRela)
  print(f"Volumen discreto: {Vol}, Volumen real: {V}.  Error Relativo: {ErrorRela} %")
  # calculo el campo-----------------------------------------------------------
  #------------------------------------------------------------------------------
  eta = cFS.calculateFieldShift(muestra*Chi, [voxelSize]*3)
    
  Bnuc = eta*B0 + B0
  Bmac = Bnuc/(1-2/3*muestra*Chi)

  # calculo el campo-EXACTO----------------------------------------------------------
  #------------------------------------------------------------------------------
  # solucion exacta en el voxel 
  Bexact_voxel  = np.zeros_like(muestra)
  Bexact_0_voxel  = np.zeros_like(muestra) # exacta que pasa por el centro y que tiene misma cantidad de elementos que la muestra
  for i in range(x.size):
    for j in range(y.size):
      for k in range(z.size):
        Bexact_voxel[k,j,i] = func_exact(z[k],y[j],x[i])  
        Bexact_0_voxel[k,j,i] = func_exact(z[k],0,0)  

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

  # solucion exacta por el centro
  zz = np.linspace(z[0],z[-1],4096*8)
  Bexact_0 = np.zeros_like(zz)
  yy = 0  
  xx = 0
  for i in range(np.size(zz)):
     Bexact_0[i] = func_exact(zz[i],yy,xx)     


  # GUARDO VARIABLES:
  Bmac_list.append(Bmac)
  Bexact_voxel_list.append(Bexact_voxel)
  Bexact_0_voxel_list.append(Bexact_0_voxel)
  Bexact_list.append(Bexact)
  muestra_list.append(muestra)
  eta_list.append(eta)
  x_list.append(x)  

  

  
#%%### GRAFICOS ###############################################################

#### figura de la muestra
size = 5
fig_muestra = plt.figure(1, figsize=(size*3, size*2), constrained_layout=False)
gs = fig_muestra.add_gridspec(2, 3, hspace=0, wspace=0)
axs_muestra = gs.subplots(sharex=True, sharey=True)
# fig_muestra.suptitle('Sharing both axes')  

#### figura de la matriz eta
size = 5
fig_eta = plt.figure(2, figsize=(size*3, size*2), constrained_layout=False)
gs = fig_eta.add_gridspec(2, 3, hspace=0, wspace=0)
axs_eta = gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  

#### figura de B mac
size = 5
fig_Bmac= plt.figure(3, figsize=(size*3, size*2), constrained_layout=False)
gs = fig_Bmac.add_gridspec(2, 3, hspace=0, wspace=0)
axs_Bmac= gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
# vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  

#### figura de Errores
size = 5
fig_Error= plt.figure(4, figsize=(size*3, size*2), constrained_layout=False)
gs = fig_Error.add_gridspec(2, 3, hspace=0, wspace=0)
axs_Error= gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
# vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  


#### figura de histogramas
size = 5
fig_hist= plt.figure(5, figsize=(size*3, size*2), constrained_layout=False)
gs = fig_hist.add_gridspec(2, 3, hspace=0, wspace=0)
axs_hist= gs.subplots(sharex=True, sharey=True)
# busco el maximo de todos los etas
# vmax_eta = max([np.max(np.abs(eta_list[nn][:,int(Ns[nn]/2),:])) for nn in range(len(Ns))])*1e6
# fig_muestra.suptitle('Sharing both axes')  


jj=-1
for N in Ns:
  jj+=1  
  voxelSize = FOV/float(N)
  # cargo variables
  Bmac = Bmac_list[jj]
  Bexact_voxel = Bexact_voxel_list[jj]
  Bexact_0_voxel = Bexact_0_voxel_list[jj]
  Bexact = Bexact_list[jj]
  muestra = muestra_list[jj]
  eta = eta_list[jj]
  x = x_list[jj]  
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
  x0 = x[nx]
  y0 = y[ny]  
  
  # MUESTRA
  ax=axs_muestra[np.unravel_index(jj,(2,3))]  
  ax.set_aspect('equal', 'box')  
  ax.pcolormesh(X[:,ny,:], Z[:,ny,:], muestra[:,ny,:], cmap='gray_r', shading='nearest')
  ax.set_xlabel("x", fontsize=22)
  ax.set_ylabel("z", fontsize=22)  
  circle = plt.Circle((0, 0), diametro/2.0, color='red', ls='--', lw=3, fill=False)
  ax.add_patch(circle)  
  if jj in [1,2,4,5]:
    ax.set_yticks([])
  if jj!=4:
    ax.set_xticks([])
  ax.set_xlim([x[0],x[-1]])    
  ax.set_ylim([z[0],z[-1]])    
  ax.label_outer()
  # ax.text(-0.25*FOV,0.35*FOV, r"$N_{voxels} = $"+ fr" {N}$^3$", fontsize=22)
  ax.text(-0.4*FOV,0.35*FOV,  fr"N = {N}", fontsize=22)
  # 1 voxel :
  XX = X[int(ny/2)-1:int(ny/2)+1:,ny,int(ny/2)-1:int(ny/2)+1]    
  ZZ = Z[int(ny/2)-1:int(ny/2)+1:,ny,int(ny/2)-1:int(ny/2)+1]
  muestra_tmp = muestra[int(ny/2):int(ny/2)+2:,ny,int(ny/2):int(ny/2)+2]    
  ax.pcolormesh(XX, ZZ, XX*0, cmap='gray_r', shading='nearest', edgecolor='b')
  

  
  # grafico de eta
  ax=axs_eta[np.unravel_index(jj,(2,3))]  
  ax.set_aspect('equal', 'box')  
  pcol = ax.pcolormesh(X[:,ny,:], Z[:,ny,:], eta[:,ny,:]*1e6, cmap='seismic', vmax=vmax_eta, vmin=-vmax_eta, shading='nearest')  
  ax.set_xlabel("x", fontsize=22)
  ax.set_ylabel("z", fontsize=22)  
  circle = plt.Circle((0, 0), diametro/2.0, color='k', ls='--', lw=3, fill=False)
  ax.add_patch(circle)  
  if jj in [1,2,4,5]:
    ax.set_yticks([])
  if jj!=4:
    ax.set_xticks([])
  if jj in [2,5]:
    # Create new axes according to image position
    cax = fig_eta.add_axes([ax.get_position().x1+0.01,
                        ax.get_position().y0,
                        0.02,
                        ax.get_position().height])     
    # Plot vertical colorbar
    cbar = plt.colorbar(pcol, cax=cax)
    cbar.set_label(r'$\eta$ [ppm]', fontsize=22)      
    # cbar.set_ticks()
    # cbar.ax.set_yticklabels(labels,fontsize=16)
  ax.set_xlim([x[0],x[-1]])    
  ax.set_ylim([z[0],z[-1]])    
  ax.label_outer()
  # ax.text(-0.25*FOV,0.35*FOV, r"$N_{voxels} = $"+ fr" {N}$^3$", fontsize=22)
  ax.text(-0.4*FOV,0.35*FOV,  fr"N = {N}", fontsize=22)





  # grafico de Bmac
  Bmac_z = Bmac[:,ny,nx]
  Bexact_voxel_z = Bexact_voxel[:,ny,nx]
  Bexact_0_voxel_z = Bexact_0_voxel[:,ny,nx]
  vmin = np.min(np.array([Bmac_z,Bexact_voxel_z]))
  vmax = np.max(np.array([Bmac_z,Bexact_voxel_z]))
  
  ax=axs_Bmac[np.unravel_index(jj,(2,3))]  
  # ax.set_aspect('box')  
  # ax.axvspan(-diametro/2,diametro/2, facecolor='lightgray', alpha=0.5)
  ax.axvspan(-1,1, facecolor='lightgray', alpha=0.5)
  # ax.vlines(-diametro/2,vmin, vmax, color='r', ls='--', lw=2)
  # ax.vlines( diametro/2,vmin, vmax, color='r', ls='--', lw=2)  
  # ax.plot(z/diametro*2, (Bexact_0_voxel_z-B0)/B0*1e6 ,'ko', label=f"Exacta")  
  ax.plot(z/diametro*2 , (Bmac_z-B0)/B0*1e6,'bo--', label=fr"Salomir")
  ax.plot(zz/diametro*2 , (Bexact_0-B0)/B0*1e6, 'k--', lw = 3, label=f"Exacta" )  
  # ax.plot(z/diametro*2, Bexact_voxel_z ,'ko', label=f"Exacta x = {x0:.3f}")
  # ax.plot(zz/diametro*2 , Bexact[1], 'k--' , label=f"Exacta x = {x0:.3f}")
  # ax.plot(zz , Bexact[0], 'gray', ls='--', label=f"Exacta x = {x0-voxelSize/2:.3f}")
  # ax.plot(zz , Bexact[2], 'r'   ,  ls='--', label=f"Exacta x = {x0+voxelSize/2:.3f}")  
  ax.set_xlabel(r"$z/r_{esfera}$", fontsize=22)
  ax.set_ylabel(r"$(B_{mac}-B_0)/B_0$ [ppm]", fontsize=22)
  ax.text(-4,17.5,  fr"N = {N}", fontsize=22)   
  ax.label_outer()
  # ax.text(-0.25*FOV,0.35*FOV, r"$N_{voxels} = $"+ fr" {N}$^3$", fontsize=22)
  if jj==2:
    # ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, fontsize=10)
    ax.legend(fancybox=True, fontsize=12)


  # grafico de ERRORES
  Bmac_z = Bmac[:,ny,nx]
  Bexact_voxel_z = Bexact_voxel[:,ny,nx]
  Bexact_0_voxel_z = Bexact_0_voxel[:,ny,nx]
  vmin = np.min(np.array([Bmac_z,Bexact_voxel_z]))
  vmax = np.max(np.array([Bmac_z,Bexact_voxel_z]))
  ax=axs_Error[np.unravel_index(jj,(2,3))]      
  ax.axvspan(-1,1, facecolor='lightgray', alpha=0.5)  
  ax.plot(z/(diametro/2) , abs(Bmac[:,ny,nx]-Bexact_0_voxel[:,ny,nx])/B0*1e6,'bo--')  
  ax.axhline(0, color="k", ls='--')
  ax.set_xlabel(r"$z/r_{esfera}$", fontsize=22)
  ax.set_ylabel(r"Error Absoluto [ppm]", fontsize=22)  
  ax.label_outer()
  ax.text(-4,2.5,  fr"N = {N}", fontsize=22)

  # ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, fontsize=10)


  # grafico de HISTOGRAMAS  
  ax=axs_hist[np.unravel_index(jj,(2,3))]      
  
  data = (Bmac[muestra==1]-B0)/B0*1e6
  data = (eta[muestra==1])*1e6
  bins = np.arange(0,8,0.5)-3.75
  h = ax.hist(data, weights = np.ones_like(data)/np.sum(muestra), bins=bins, facecolor='b', edgecolor='k')
  # ax.axvline(Chi*2/3*1e6, color='k', ls='--', lw=2)
  ax.axvline(0, color='k', ls='--', lw=2)
  if jj>2:
    # ax.set_xlabel(r"$\eta$ [ppm]",fontsize=22)
    # ax.set_xlabel(r"$|B_{mac,z}^{numerico}-B_{mac,z}^{exacto}|/B_0$ [ppm]", fontsize=18)  
    ax.set_xlabel(r"Error Absoluto [ppm]", fontsize=22)  
  ax.set_ylabel("")
  ax.set_xticks(np.arange(-4,5))
  ax.yaxis.set_major_formatter(PercentFormatter(1))
  ax.text(-3.75,0.9,  fr"N = {N}", fontsize=22)
  ax.set_ylim([0,1.02])
  ax.set_xlim([-4.5,4.5])
  ax.label_outer()

print("Errores Porcentuales en el volumen de la esfera:")
for jj in range(len(Ns)):
  print(f"N = { Ns[jj]}  Error Rela = {ErrorRelativoVolumen[jj]:.2f} %")  

elapsed = (time.time() - t0)/60
print('---  tiempo: {:.2f} min'.format(elapsed))