# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 20:48:44 2021

@author: santi
"""


# %%

import numpy as np
import matplotlib.pyplot as plt

3save = True

N = 100
d = 10
a = 9

o = np.zeros([N, N])


nx = int(N/d)
ny = int(N/a)

for i in range(ny):
    if i % 2 == 0:
        for j in range(nx):
            o[int(i*a), int(j*d)] = 1
    else:
        for j in range(nx):
            o[int(i*a), int(j*d-d/2)] = 1


plt.figure(1)
plt.pcolormesh(o)


yy, xx = np.where(o == 1)
plt.figure(2)
plt.scatter(xx, yy)


plt.figure(3)
xc = 45
yc = 45
dist = np.sqrt((xx-xc)**2+(yy-yc)**2)
plt.hist(dist, bins=500)


# %%
plt.rcParams.update({'font.size': 14})

d = np.arange(2, 512, 2)
a = np.arange(2, 512)

D, A = np.meshgrid(d, a)

d_app = D*D/4 + A*A
d2 = D*D

error = (d2 - d_app)/d2

vmax = np.max(abs(error))
vmax = 1


plt.figure(9)
plt.pcolormesh(D, A, error, cmap='seismic', vmin=-vmax, vmax=vmax)
plt.xlabel("Parámetro $a$ [voxels]")
plt.ylabel("Distancia [voxels]")
plt.title("Error relativo:   $(d - d_{app})/d $")
plt.colorbar()


Eabs = np.abs(error)
aa = np.argmin(Eabs, axis=0)
plt.figure(10)
plt.pcolormesh(D, A, error, cmap='seismic', vmin=-vmax, vmax=vmax, alpha=0.8)
plt.plot(d, d, 'k--')
plt.plot(d, a[aa], 'o')
plt.ylabel("Paámetro $a$ [voxels]")
plt.xlabel("Distancia [voxels]")
plt.title("Valores de $a$ que mejor aproximan $d$")


plt.figure(11)
minErr = np.min(Eabs, axis=0)
plt.plot(d, minErr, 'o-')
plt.xlabel("Distancia [voxels]")
plt.ylabel("$(d - d_{app})/d $")
plt.title("Error relativo de la mejor aproximación")

# %%
if save:
    data = np.array([d.astype(int), a[aa].astype(int), minErr]).T
    np.savetxt('../DataBases/Hexagonal_Parametro_a.dat', data)
