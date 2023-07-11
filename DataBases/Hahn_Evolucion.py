#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 14:21:43 2022

@author: santi

Este script consiste en simular la senal que da un nucleo (o un voxel) de litio
cuando es excitado con la secuencia Hahn Echo, variando el
valor de k y para distintos B1


Nota: no se tiene en cuenta off-resonance


LA EVOLUCION DE LA MATRIZ DENSIDAD AQUI UTILIZADA NO TIENE EN CUENTA LO NECESARIO PARA LA FORMACIÓN DEL ECO!!!!
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

def pulse(rhoi, br, k):
    r3 = np.sqrt(3)
    Ix = 0.5*np.array([[0,r3,0,0],[r3,0,2,0],[0,2,0,r3],[0,0,r3,0]])
    Iy = 1/(2j)*np.array([[0,r3,0,0],[-r3,0,2,0],[0,-2,0,r3],[0,0,-r3,0]])
    Iz = 1/2*np.array([[3,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,-3]])

    alpha = k*np.pi*np.exp(-br)

    arg = 1j*alpha*(Ix*np.cos(br)+Iy*np.sin(br))
    P1 = expm(-arg)
    P2 = expm( arg)
    rhof = P1.dot(rhoi.dot(P2))

    return rhof

def evolucion(rho, t, T1, T2, rho0=None):
    if rho0 is None:
        Iz = 1/2*np.array([[3,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,-3]])
        rho0 = Iz
    # separo la matriz densidad en parte diagonal y no diagonal
    diag = rho * np.diag(np.ones(4))
    nodiag = rho - diag
    # coherecencias decaen
    E_nodiag = nodiag*np.exp(-t/T2)
    # diagonal va al equilibrio
    E_diag = (diag-rho0)*np.exp(-t/T1) + rho0

    return E_diag + E_nodiag

#%%
guardar = False
savepath = "./Hahn/"

r3 = np.sqrt(3)
Ix = 0.5*np.array([[0,r3,0,0],[r3,0,2,0],[0,2,0,r3],[0,0,r3,0]])
Iy = 1/(2j)*np.array([[0,r3,0,0],[-r3,0,2,0],[0,-2,0,r3],[0,0,-r3,0]])
Iz = 1/2*np.array([[3,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,-3]])

kB = 1.3806488e-23
T = 300
w = 116e6 / 2*np.pi
hbar = 1.054571818e-34
Boltz = hbar*w / (kB*T) # factor de boltzmann
#rho0 = 1/2 + Boltz * Iz/2
rho0 = Iz
#rho0 =np.zeros((4,4))
#rho0[0,0] = 1


echoTime = 600e-6
T2 = 600e-6
T1 = 170e-3

#w = 0


b = 1/14
r_list = np.linspace(0, int(5/b-1), 1024)
# evanesencia: B1 = B10*beta = B10 * exp(-r/12um)
beta = np.exp(-b*r_list)
k_list = np.arange(0.5, 3.1, 0.1)
k_list = np.array([1])
# k_list = np.array([1.05,1.15])


k_list = np.array([1])
r_list = np.array([0])


#"""
#elijo cietos valores de k, sólo los  correspondientes a slices
#"""
#r_list = np.arange(0.25, 24, 0.5)
#k_list = np.exp(b*r_list)


Sx = np.zeros((r_list.size, k_list.size)).astype('complex')
Sy = np.zeros((r_list.size, k_list.size)).astype('complex')
Mx = np.zeros((r_list.size, k_list.size)).astype('complex')
My = np.zeros((r_list.size, k_list.size)).astype('complex')


for kk in range(k_list.size):
  k = k_list[kk]
  print('k = %s'%k)
  for rr in range(r_list.size):

    r = r_list[rr]

    br = b*r
    rho = rho0    
    
    tiempos = []
    Senal_t = []
    
    ### arranca secuencia
    # pulso "90":  P1·rho·P1^(-1)   
    t = 0
    rho = pulse(rho, br, k/2)
    #----------------
    tiempos.append(t)
    mx = np.trace(rho.dot(Ix)) 
    my = np.trace(rho.dot(Iy)) 
    Senal_t.append(mx+1j*my)
    #----------------
    for tt in np.linspace(0,t+echoTime/2,32):
      # evolucion E·rho·E^(-1)    
      rho = evolucion(rho, tt, T1, T2)      
      t = tt
      #----------------
      tiempos.append(t)
      mx = np.trace(rho.dot(Ix)) 
      my = np.trace(rho.dot(Iy)) 
      Senal_t.append(mx+1j*my)
      #----------------
    # pulso "180":  P1·rho·P1^(-1)         
    rho = pulse(rho, br, k)
    #----------------
    tiempos.append(t)
    mx = np.trace(rho.dot(Ix)) 
    my = np.trace(rho.dot(Iy)) 
    Senal_t.append(mx+1j*my)
    #----------------
    for tt in np.linspace(echoTime/2, echoTime*1.5,64):
      # evolucion E·rho·E^(-1)    
      rho = evolucion(rho, tt, T1, T2)      
      t = tt
      #----------------
      tiempos.append(t)
      mx = np.trace(rho.dot(Ix)) 
      my = np.trace(rho.dot(Iy)) 
      Senal_t.append(mx+1j*my)
      #----------------
    
    tiempos = np.array(tiempos)
    Senal_t = np.array(Senal_t)
    
    plt.figure(kk)
    plt.plot(tiempos/echoTime, np.real(Senal_t), 'ko-')
    plt.plot(tiempos/echoTime, np.imag(Senal_t), 'ro-')



#     # valor de expectacion luego de la secuencia
#     mx = np.trace(rho.dot(Ix)) 
#     my = np.trace(rho.dot(Iy)) 

#     # lo que llega a la bobina:
#     # MEHRING
#     sx = np.exp(-br)*(mx*np.cos(br)-my*np.sin(br))
#     sy = np.exp(-br)*(my*np.cos(br)+mx*np.sin(br))

#     # RECIPROCITY
# #    b1x = np.exp(-br)*np.cos(br)
# #    b1y = np.exp(-br)*np.sin(br)
# #    sx  = b1x*mx
# #    sy  = b1y*my

#     Sx[rr,kk] = sx
#     Sy[rr,kk] = sy
#     Mx[rr,kk] = mx
#     My[rr,kk] = my


#   S = -np.real(Sy[:,kk])+ 1j* np.real(Sx[:,kk])
#   datos = np.array([beta, np.real(S), np.imag(S)]).T
#   if guardar:
#     np.savetxt(savepath+"SMC_N{}_k{:.2f}.dat".format(N,k_list[kk]), datos)
