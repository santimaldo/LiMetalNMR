#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 13:54:04 2020

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage




def espectro(matriz, KS=258.9):
    """
    funcion que crea un espectro dada una matriz de valores de B0
    
    INPUT:
      - matriz : array - Es el array del valor de delta solo en la region de la
                         muestra que quiero que contribuya al espectro
      - KS     : float - Es el Knight Shift. Su valor por defecto es 258.9, un
                         valor que puse a ojo para que el bulk coincida con los
                         experimentos. Colocando KS=0 veremos la desviacion
                         respecto al campo de 7T. Si quiero hacerlo respecto al
                         bulk debo poner KS=-superposicion.delta_in
    """
    datos = matriz[matriz!= 0].flatten()
    hist, bin_edges = np.histogram(datos, bins='auto')
    
    binsize = bin_edges[1]-bin_edges[0]
    bins = bin_edges[1:] - binsize/2
    
    histograma = np.array([bins, hist]).T
    
    ###  FID ------------------------------------------------------------------
    
    ppm = 116.64
    w = (bins+KS)*2*np.pi*ppm
    #w = (bins)*2*np.pi*ppm
    Pw = hist
    
    tau = np.linspace(0,1.024*16,2048)*1e-3
    
    T2est = 0.12*1e-3 # chequeado con una medida_ T2est = 0.12 us
    
    fid = 0
    for n in range(hist.size):
      fid = fid + hist[n]*np.exp(1j* w[n] * tau - tau/T2est)
    
    SNR = 1000
    fid = fid + (np.random.random(fid.size)-0.5) * fid[0]/SNR
    
    ###  FOURIER---------------------------------------------------------------
    ZF = tau.size
    dw = tau[1]-tau[0]
    sw = 1/dw;
    freq = np.zeros(ZF);
    for ll in range(ZF):
        freq[ll]=(ll-1)*sw/(ZF-1)-sw/2
    
    ppmAxis = freq/ppm
    
    spec = np.fft.fftshift(np.fft.fft(fid))
    
    return ppmAxis, np.real(spec)



  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  