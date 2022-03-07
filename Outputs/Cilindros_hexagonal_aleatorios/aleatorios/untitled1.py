# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 15:41:01 2021

@author: santi
"""

import os
import numpy as np
import shutil

radios = [20]
distancias=[42,46,50,56,62,68,78,94,110,126]
alturas = [64]
  
  

path0 = 'S:/Doctorado/pyprogs/calculateFieldShift/Outputs/Cilindros_hexagonal_aleatorios/aleatorios/'
for caso in range(1,6):
  try:
    os.mkdir(path0+'SP/iteracion{:d}'.format(caso))
  except:
    a=1
  try:
    os.mkdir(path0+'SMC64-k1/iteracion{:d}'.format(caso))
  except:
    a=1
  
    
#%%

regiones = ['','-microestructuras', '-bulk']
for h in alturas:
  for r in radios:
    for d in distancias:
      caso = 1
      for iteracion in range(150):      
        archivo = path0+'SP/old/iteracion{:d}_h{:d}_r{:d}_d{:d}.dat'.format(iteracion,h, r, d)                
        if os.path.isfile(archivo):  # si existe...          
          for seq in ['SP', 'SMC64-k1']:
            for ii in range(3):
              region = regiones[ii]
              archivo_old = path0+'{}/old/iteracion{:d}_h{:d}_r{:d}_d{:d}{}.dat'.format(seq,iteracion+ii,h, r, d, region)
              archivo_new = path0+'{}/iteracion{:d}/h{:d}_r{:d}_d{:d}{}.dat'.format(seq,caso,h, r, d, region)
              # print(archivo_old, archivo_new)
              
              # copio:
              #os.popen("copy {} {}".format(archivo_old, archivo_new))
              shutil.copyfile(archivo_old, archivo_new)
          caso+=1    

