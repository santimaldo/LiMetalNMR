# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 15:41:01 2021

@author: santi
"""

import os
import numpy as np
import shutil

path0 = 'S:/Doctorado/pyprogs/calculateFieldShift/Outputs/Resultados/aleatorios/'

radios = [20]
distancias=[42,46,50,56,62,68,78,94,110,126]
alturas = [16,64]
casos=np.arange(4,9)
    
#%%

regiones = ['','-microestructuras', '-bulk']
for h in alturas:
  for r in radios:
    for d in distancias:      
      for caso in casos:      
        archivo = path0+'SP/old/h{:d}_r{:d}_d{:d}iteracion{:d}.dat'.format(caso,int(h), int(r), int(d))
        if os.path.isfile(archivo):  # si existe...                    
          for ii in range(3):
            region = regiones[ii]

            file_old = 'SMC64-k1/old/h{:d}_r{:d}_d{:d}_iteracion{:d}{}.dat'.format(caso,int(h), int(r), int(d), region)
            file_new = 'SMC64-k1/h{:d}_r{:d}_d{:d}_iteracion{:d}{}.dat'.format(int(h), int(r), int(d), caso-3, region)
            # copio:            
            shutil.copyfile(path0+file_old, path0+file_new)
            
            file_old = 'SP/old/h{:d}_r{:d}_d{:d}iteracion{:d}{}.dat'.format(caso,int(h), int(r), int(d), region)
            file_new = 'SP/h{:d}_r{:d}_d{:d}_iteracion{:d}{}.dat'.format(int(h), int(r), int(d), caso-3, region)
            # copio:            
            shutil.copyfile(path0+file_old, path0+file_new)


