#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 07:22:30 2020

@author: muri
"""
import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D 
import time

import Modules.calculateFieldShift as cFS 
import Modules.SimulationVolume as SV


#Voy a construir un electrodo cilindrica, con las dimensiones h=0.71mm
# y d=12mm. Además quiero FOVz=10*h y FOVxy=2*d

#inicio el reloj
t0 = time.time()
#%%

N = [1024,1024,1024]
voxelSize = [0.005, 0.02, 0.02]# mm

# N = np.array([1024,1024,1024])/4
# voxelSize = np.array([0.02, 0.02, 0.02])*4# mm


N, voxelSize, FOV = SV.SimulationVolume(voxelSize=voxelSize, N=N, anisotropico=True)


coordenadas = []
for ii in range(3):
    ##### con un voxel centrado en cero:
    # xx = np.linspace(-FOV[ii]/2.0, (FOV[ii]/2.0-voxelSize[ii]) ,N[ii]) 
    ##### FOV simetrico sin voxel en cero
    xx = np.linspace(-(FOV[ii]-voxelSize[ii])/2.0, (FOV[ii]-voxelSize[ii])/2.0,N[ii]) 
    coordenadas.append(xx)
    
z, y, x = coordenadas

Z,Y,X= np.meshgrid(z,y,x, indexing='ij')

#%%

altura = 0.71
radio = 6
print( f"-----------------------------------------")
print( f"Electrodo de radio {radio} mm y espesor {altura} mm\n")
print("Creando...")

muestra = np.zeros_like(X)

condicion = (X*X + Y*Y <= radio**2)
muestra[condicion] = 1

mask=np.zeros_like(muestra)
condicion = (Z*Z <= altura/2.0)
mask[condicion]=1

muestra = muestra*mask

elapsed = (time.time() - t0)/60
print('---  armado de muestra: {:.2f} min\n'.format(elapsed))

#%%
print("Calculando delta...")
t0delta = time.time()
# ahora calculamos la perturbacion de campo, suponiendo que esa matriz
# representa al litio
Chi =  24.1*1e-6 #(ppm) Susceptibilidad volumetrica


delta = cFS.calculateFieldShift(muestra * Chi, voxelSize)*1e6



elapsed = (time.time() - t0delta)/60
print("Tiempo en calcular delta:")
print('---  tiempo: {:.2f} min\n'.format(elapsed))
#%% GRAFICOS

z_slice = int(N[0]/2)



plt.figure(10)
plt.pcolormesh(x, y,muestra[z_slice,:,:])
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')


v = 5
plt.figure(11)

plt.pcolormesh(x,y,delta[int(z_slice),:,:], cmap='seismic', vmax=v, vmin=-v)
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.colorbar()

# slice en x

x_slice = int(N[2]/2)

plt.figure(20)
plt.pcolormesh(y,z,muestra[:,:,x_slice])
plt.xlabel('y [mm]')
plt.ylabel('z [mm]')


v = 4
plt.figure(21)
plt.pcolormesh(y,z,delta[:,:,x_slice], cmap='seismic', vmax=v, vmin=-v)
plt.xlabel('y [mm]')
plt.ylabel('z [mm]')
plt.colorbar()


plt.show()

#%%
print("Creando Perfiles...")

t0perfiles = time.time()

# calculo perfiles - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
ancho = voxelSize[2]*2

Nslices = int(radio/ancho)
header = f"Electrodo circular de radio {radio} mm"\
         f" y espesor {altura*1000} um.\n"\
         f"Volumen de simulacion (convencion z,y,x):\n"\
         f"N: {N[0]} x {N[1]} x {N[2]} | "\
         f"voxelSize:  {voxelSize[0]}mm x {voxelSize[0]}mm x {voxelSize[0]}mm"\
         f" | FOV:  {FOV[0]}mm x {FOV[1]}mm x {FOV[2]}mm\n\n"\
         f"z [mm]\t\t delta[ppm]"
         
perfiles_out = []
radios = np.zeros(Nslices)
for ii in range(Nslices):
    Rext = (ii+1/2)*ancho
    if ii==0:
        Rint = 0
        Rslice = 0
    else:
        Rint = (ii-1/2)*ancho    
        Rslice =  (Rint+Rext)/2 # para ii=0 defino radio 0    
    radios[ii] = Rslice
            
    condicion1 = (X*X + Y*Y >= Rint**2)
    condicion2 = (X*X + Y*Y <= Rext**2)
    
    # in - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    condicion_in = (muestra * (Z>0)) * (condicion1*condicion2)
    
    delta_in = np.ma.masked_array(delta, 
                                  mask=np.logical_not(condicion_in))    
    perfil = np.mean(delta_in, axis=(1,2))
    perfil = perfil.data[perfil.mask==False]
    z_in = np.arange(perfil.size)*voxelSize[0]
    datos = np.array([z_in, perfil]).T
    np.savetxt(f"./DataBases/Bulk_perfiles/perfil_radio{int(Rslice*1000):04d}.in",
               datos, header=header)
    # in - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    condicion_out = ((1-muestra) * (Z>0)) * (condicion1*condicion2)
    
    delta_out = np.ma.masked_array(delta, 
                                  mask=np.logical_not(condicion_out))    
    perfil = np.mean(delta_out, axis=(1,2))
    perfil = perfil.data[perfil.mask==False]
    perfiles_out.append(perfil)
    z_out = np.arange(perfil.size)*voxelSize[0]
    datos = np.array([z_out, perfil]).T
    np.savetxt(f"./DataBases/Bulk_perfiles/perfil_radio{int(Rslice*1000):04d}.out",
               datos, header=header)
    
    

elapsed = (time.time() - t0perfiles)/60
print("Tiempo en calcular y guardar perfiles:")
print('---  tiempo: {:.2f} min\n'.format(elapsed))

perfiles_out = np.array(perfiles_out).T
#%%


plt.figure(5468)
v = 4
plt.pcolormesh(radios, z_out, perfiles_out, shading='nearest',
               cmap='seismic', vmax=v, vmin=-v)
plt.xlabel("radio [mm]")
plt.ylabel(" z [mm]")
plt.title("Out")
plt.colorbar(label = r"$\delta$ [ppm]")


elapsed = (time.time() - t0)/60
print("Tiempo total:")
print('---  tiempo: {:.2f} min'.format(elapsed))
