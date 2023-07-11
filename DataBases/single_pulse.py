#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 20:31:53 2020

@author: santi

Este script consiste en simular la senal que da un nucleo (o un voxel) de litio
cuando es excitado con un cierto tiempo de pulso


Nota: no se tiene en cuenta off-resonance
"""

from scipy.linalg import expm
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})


def pulse(rhoi, br, k):
    r3 = np.sqrt(3)
    Ix = 0.5*np.array([[0, r3, 0, 0], [r3, 0, 2, 0],
                      [0, 2, 0, r3], [0, 0, r3, 0]])
    Iy = 1/(2j)*np.array([[0, r3, 0, 0], [-r3, 0, 2, 0],
                          [0, -2, 0, r3], [0, 0, -r3, 0]])
    Iz = 1/2*np.array([[3, 0, 0, 0], [0, 1, 0, 0],
                      [0, 0, -1, 0], [0, 0, 0, -3]])

    alpha = k*np.pi*np.exp(-br)

    arg = 1j*alpha*(Ix*np.cos(br)+Iy*np.sin(br))
    P1 = expm(-arg)
    P2 = expm(arg)
    rhof = P1.dot(rhoi.dot(P2))

    return rhof


def evolucion(rho, t, T1, T2, rho0=None):
    if rho0 is None:
        Iz = 1/2*np.array([[3, 0, 0, 0], [0, 1, 0, 0],
                          [0, 0, -1, 0], [0, 0, 0, -3]])
        rho0 = Iz
    # separo la matriz densidad en parte diagonal y no diagonal
    diag = rho * np.diag(np.ones(4))
    nodiag = rho - diag
    # coherecencias decaen
    E_nodiag = nodiag*np.exp(-t/T2)
    # diagonal va al equilibrio
    E_diag = (diag-rho0)*np.exp(-t/T1) + rho0

    return E_diag + E_nodiag


# %%
savepath = "./SinglePulse/"
savepath = "S:/tmp/"


r3 = np.sqrt(3)
Ix = 0.5*np.array([[0, r3, 0, 0], [r3, 0, 2, 0], [0, 2, 0, r3], [0, 0, r3, 0]])
Iy = 1/(2j)*np.array([[0, r3, 0, 0], [-r3, 0, 2, 0],
                      [0, -2, 0, r3], [0, 0, -r3, 0]])
Iz = 1/2*np.array([[3, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -3]])

kB = 1.3806488e-23
T = 300
w = 116e6 / 2*np.pi
hbar = 1.054571818e-34
Boltz = hbar*w / (kB*T)  # factor de boltzmann
#rho0 = 1/2 + Boltz * Iz/2
rho0 = Iz
#rho0 =np.zeros((4,4))
#rho0[0,0] = 1

T2 = 600e-6
T1 = 170e-3
#w = 0
N = 16
b = 1/14  # 1/um
r_list = np.linspace(0, int(8/b-1), 1024)
# evanesencia: B1 = B10*beta = B10 * exp(-b*r)
beta = np.exp(-b*r_list)


k_list = np.arange(0, 2.1, 0.1)
k_list[0] = 0.08  # pulso de pi/12


# k_list = np.array([0.5])  # DESCOMENTAR ESTO PARA CREAR SOLO EL PULSO DE PI/2


# """
# elijo cietos valores de k, sólo los  correspondientes a slices
# """
#r_list = np.arange(0.25, 24, 0.5)
#k_list = np.exp(b*r_list)

Sx = np.zeros((r_list.size, k_list.size)).astype('complex')
Sy = np.zeros((r_list.size, k_list.size)).astype('complex')
Mx = np.zeros((r_list.size, k_list.size)).astype('complex')
My = np.zeros((r_list.size, k_list.size)).astype('complex')

for kk in range(k_list.size):
    k = k_list[kk]
    print('k = %s' % k)
    for rr in range(r_list.size):

        r = r_list[rr]

        br = b*r
        rho = rho0
        t = 0

        rho = pulse(rho, br, k)

        # valor de expectacion luego de la secuencia
        mx = np.trace(rho.dot(Ix))  # * np.exp(-t/T1)
        my = np.trace(rho.dot(Iy))  # * np.exp(-t/T1)

        # lo que llega a la bobina:
        # MEHRING
        sx = np.exp(-br)*(mx*np.cos(br)-my*np.sin(br))
        sy = np.exp(-br)*(my*np.cos(br)+mx*np.sin(br))

        # RECIPROCITY
#    b1x = np.exp(-br)*np.cos(br)
#    b1y = np.exp(-br)*np.sin(br)
#    sx  = b1x*mx
#    sy  = b1y*my

        Sx[rr, kk] = sx
        Sy[rr, kk] = sy
        Mx[rr, kk] = mx
        My[rr, kk] = my

    if k <= 2:
        S = -np.real(Sy[:, kk]) + 1j * np.real(Sx[:, kk])
        datos = np.array([beta, np.real(S), np.imag(S)]).T
        np.savetxt(
            savepath+"SinglePulse_k{:.2f}.dat".format(k_list[kk]), datos)
# %%
#S = np.real(Sx)- 1j* np.real(Sy)
S = -np.real(Sy) + 1j * np.real(Sx)
# plt.figure(431)
# plt.plot(beta, np.real(S), '-')
# plt.figure(432)
# plt.plot(beta, np.imag(S), '-')

if S.shape[1] == 1:  # grafico esto solo si corro para un valor de k
    plt.figure(433)
    absS = np.abs(S)[:]/np.abs(np.max(np.abs(S)))
    plt.plot(b*r_list, absS, 'b-', lw=2,
             label=rf"Senal para pulso de {k}$\pi$")
    plt.plot(b*r_list, np.exp(-b*r_list), '--',
             color='gray', label="exp(-z/skdp)")
    if k_list[0] < 1:
        # para que profundidad, la senal es 1%:
        x1pc = b*r_list[absS[:, 0] < 0.01*absS[0, 0]][0]
        plt.axvline(x1pc, ls='--', color='k')
        plt.axvline(x1pc, ls='--', color='k')
        plt.text(x1pc, 0.1, f"1% de la senal en z/skdp={x1pc:.2f}")
    plt.legend()
    plt.xlabel(r"z/skindepth")
    plt.ylabel(r"Signal")

# %%
if S.shape[1] > 1:  # grafico esto solo si corro para varios k
    plt.figure(0)
    #plt.pcolormesh(k_list, r_list, np.ral(Sx+1j*Sy))
    #plt.pcolormesh(k_list, r_list, np.sqrt(np.abs(Sx-1j*Sy)))
    #plt.pcolormesh(k_list, r_list*b, np.abs(np.real(Sx+1j*Sy)), cmap='inferno')
    plt.pcolormesh(k_list, r_list*b, np.abs(S), cmap='inferno')
    plt.xlabel(r'k/$\pi$')
    plt.ylabel('r/$\delta$')
    plt.ylim([0, 5])
    plt.title("Single Pulse Intensity")
    # plt.xlim([0.5,3.5])
    # plt.colorbar()
    #
    # %%

    S = -np.real(Sy) + 1j * np.real(Sx)
    #S = np.abs(My)
    S = np.trapz(S, axis=0)

    plt.figure(1)
    plt.plot(k_list, np.imag(S)*0, 'k--')
    plt.plot(k_list, np.imag(S), 'r', linewidth=3)
    plt.plot(k_list, np.real(S), 'k', linewidth=3)
    plt.xlabel(r'k/$\pi$')
    plt.xlim([0, 8])
    plt.yticks([])
    plt.grid()
    #plt.ylabel('phase(S) [rad]')

    # %%
    plt.figure(2)
    plt.plot(k_list, np.abs(S), 'k')
    #plt.plot(k_list, np.imag(S), 'r')
    plt.xlabel('k')
    #plt.ylabel('phase(S) [rad]')

    # %%
    # grafico la posicion en la cual la senal es del 1 %
    S = -np.real(Sy) + 1j * np.real(Sx)

    x1pc_list = np.zeros_like(k_list)
    for ii in range(k_list.size):
        absS = np.abs(S)[:, ii]/np.max(np.abs(S[0, ii]))
        absS = absS[r_list > b]
        rnew = r_list[r_list > b]
        x1pc = b*rnew[absS_1pc < 0.01*max(absS_1pc)]
        if x1pc.size > 0:
            x1pc_list[ii] = x1pc[0]

    plt.figure(3)
    plt.plot(k_list[x1pc_list != 0], x1pc_list[x1pc_list != 0], 'o')
    plt.xlabel(r"k  (pulso de k$\pi$")
    plt.ylabel(r"z/skdp donde S=$0.01\times S_0$")

    # %%
