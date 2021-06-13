# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 20:47:34 2021

@author: santi
"""


import numpy as np
import matplotlib.pyplot as plt


def get_param_a(d):
  # distancias, parametros_a, errores relativos
  Ds, As, Es = np.loadtxt('../DataBases/Hexagonal_parametro_a.dat').T
  a = As[Ds==d][0]
  return a



distancias = np.arange(4,128,2)
radios = np.arange(1,63)

densidades=np.zeros([radios.size, distancias.size])

for i in range(radios.size):
  for j in range(distancias.size):    
    # print('ij',i,i)
    r = int(radios[i])
    d = int(distancias[j])  
    if r>(d/2-1):
      # print(r,d,'no sirve')
      densidades[i,j] = 2      
      continue
    # print(r,d,'ok')
    a = get_param_a(d)
    
    # centros celde unidad:
    xc_U = np.array([0, d, d/2, 0  , d  ]) - 0.5
    yc_U = np.array([0, 0, a  , 2*a, 2*a]) - 0.5
    
    obj = np.zeros([int(2*a),d])
    
    r2 = r**2
    for ii in range(xc_U.size):
      xc = xc_U[ii]
      yc = yc_U[ii]
      #-----------------------------------------------------------cilindro  
      for ind_x in range(int(d)-1):   
        for ind_y in range(int(2*a)-1):
          if (ind_x-xc)**2+(ind_y-yc)**2<r2:
            obj[ind_y, ind_x] = 1
            
    
    A_mic  = np.sum(obj) 
    A_tot  = 2*a*d    
    densidad = A_mic/A_tot    
    densidades[i,j] = densidad


#%%    
plt.figure(2222)
plt.pcolormesh(distancias, radios, densidades)




#%%

# plt.plot(densidades[:], 'o-')
# plt.yscale('log')

