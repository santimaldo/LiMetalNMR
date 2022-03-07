#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 20:31:53 2020

@author: santi

Este script consiste en simular la senal que da un nucleo (o un voxel) de litio
cuando es excitado con la secuencia SMC para un cierto valor de N, variando el
valor de k y para distintos B1


Nota: no se tiene en cuenta off-resonance
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
savepath = "./SMC/"

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


Delta = 800e-6
T2 = 600e-6
T1 = 170e-3

#w = 0

N = 64
b = 1/12
r_list = np.linspace(0, int(8/b-1), 1024)
# evanesencia: B1 = B10*beta = B10 * exp(-r/12um)
beta = np.exp(-b*r_list)
k_list = np.arange(0.5, 3.1, 0.1)
# k_list = np.array([1])
# k_list = np.array([1.05,1.15])



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
    t = 0
    for n in range(N):
      # pulso:  P1·rho·P1^(-1)
      rho = pulse(rho, br, k)
      # evolucion E·rho·E^(-1)
      #rho = (E.dot(rho)).dot(np.linalg.inv(E))
      rho = evolucion(rho, Delta, T1, T2)
      t = t + Delta
    # readout k*pi/2 pulse
    rho = pulse(rho, br, k/2)

    # valor de expectacion luego de la secuencia
    mx = np.trace(rho.dot(Ix)) #* np.exp(-t/T1)
    my = np.trace(rho.dot(Iy)) #* np.exp(-t/T1)

    # lo que llega a la bobina:
    # MEHRING
    sx = np.exp(-br)*(mx*np.cos(br)-my*np.sin(br))
    sy = np.exp(-br)*(my*np.cos(br)+mx*np.sin(br))

    # RECIPROCITY
#    b1x = np.exp(-br)*np.cos(br)
#    b1y = np.exp(-br)*np.sin(br)
#    sx  = b1x*mx
#    sy  = b1y*my

    Sx[rr,kk] = sx
    Sy[rr,kk] = sy
    Mx[rr,kk] = mx
    My[rr,kk] = my


  S = -np.real(Sy[:,kk])+ 1j* np.real(Sx[:,kk])
  datos = np.array([beta, np.real(S), np.imag(S)]).T
  if guardar:
    np.savetxt(savepath+"SMC_N{}_k{:.2f}.dat".format(N,k_list[kk]), datos)
#%%
S = np.real(Sx)+ 1j* np.real(Sy)
plt.figure(431)
plt.plot(beta, np.real(S), '-')
plt.figure(432)
plt.plot(beta, np.imag(S), '-')
#%%
#np.savetxt("re_signal.dat", np.real(Sx))
#np.savetxt("im_signal.dat", np.real(Sy))
#np.savetxt("re_magnetiz.dat", np.real(Mx))
#np.savetxt("im_magnetiz.dat", np.real(My))
#np.savetxt("r.dat", r_list)
#np.savetxt("k.dat", k_list)
#%%
plt.figure(0)
#plt.pcolormesh(k_list, r_list, np.ral(Sx+1j*Sy))
#plt.pcolormesh(k_list, r_list, np.sqrt(np.abs(Sx-1j*Sy)))
#plt.pcolormesh(k_list, r_list*b, np.abs(np.real(Sx+1j*Sy)), cmap='inferno')
plt.pcolormesh(k_list, r_list*b, np.abs(Sx+1j*Sy), cmap='inferno')
plt.plot(k_list, np.log(k_list)  ,  color='orange')
plt.plot(k_list, np.log(k_list/2), color='orange')
plt.plot(k_list, np.log(k_list/3), color='orange')
plt.plot(k_list, np.log(k_list/4), color='orange')
plt.plot(k_list, np.log(k_list/5), color='orange')
plt.xlabel('k')
plt.ylabel('r/$\delta$')
plt.ylim([0,5])
#plt.xlim([0.5,3.5])
plt.colorbar()

#%%

S = -np.real(Sy)+ 1j* np.real(Sx)
#S = np.abs(My)
S = np.trapz(S, axis=0)

plt.figure(1)
plt.plot(k_list, np.abs(S), 'k')
plt.plot(k_list, -np.angle(S), 'r')
plt.xlabel('k')
plt.ylabel('phase(S) [rad]')

#%%





