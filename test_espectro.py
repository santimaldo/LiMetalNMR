#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 19:23:12 2020

@author: santi
"""


"""
script para probar cómo hacer un espectro
"""

superposicion = s_s # superposicion sticks
#superposicion = s_ts # superposicion trapped sticks

#matriz = superposicion.delta_sens
#matriz[superposicion.z0:, 114:140, 114:140] = 0 # solo estructuras grandes en s_ts
#matriz = superposicion.delta_sens[superposicion.z0:,114:140,114:140] #s_ts solo dendritas atrapadas
#matriz = superposicion.delta_sens[superposicion.z0:,:,:] # s_s
#matriz = superposicion.delta_sens[0:superposicion.z0,:,:] # bulk
datos = matriz[matriz!= 0].flatten()


#%%

hist, bin_edges = np.histogram(datos, bins='auto')

binsize = bin_edges[1]-bin_edges[0]
bins = bin_edges[1:] - binsize/2

histograma = np.array([bins, hist]).T
np.savetxt('histograma.dat', histograma)

plt.figure(1)
plt.plot(bins, hist,'o-')


ppm = 116.64
w = (bins+257.3)*2*np.pi*ppm
w = (bins)*2*np.pi*ppm
Pw = hist

tau = np.linspace(0,20.48,2048)*1e-3


#%%
T2est = 0.3*1e-3

fid = 0
for n in range(hist.size):
  fid = fid + hist[n]*np.exp(1j* w[n] * tau - tau/T2est)

SNR = 1000
fid = fid + (np.random.random(fid.size)-0.5) * fid[0]/SNR

plt.figure(567)
plt.plot(tau, np.real(fid))


ZF = tau.size
dw = tau[1]-tau[0]
sw = 1/dw;
freq = np.zeros(ZF);
for ll in range(ZF):
    freq[ll]=(ll-1)*sw/(ZF-1)-sw/2

ppmAxis = freq/ppm - (-12.79)

spec = np.fft.fftshift(np.fft.fft(fid))

plt.figure(5678)
#plt.plot(ppmAxis, np.real(spec)/np.sum(np.real(spec)))
plt.plot(ppmAxis, np.real(spec))
plt.xlim([70,-40])
plt.xlabel(r'$\delta-\delta_{Bulk}$')
#plt.plot(ppmAxis, np.imag(spec), 'r')

