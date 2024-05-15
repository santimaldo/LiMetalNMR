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


#------------
distancias = np.arange(4,128,2)
radios = np.arange(1,63)
#------------


# radios = np.array([1,3,5,10,15,20,40,60])
# distancias = np.zeros([10])

  
densidades=np.zeros([radios.size, distancias.size])-1

for i in range(radios.size):
  r = int(radios[i])
  semidistancias = np.linspace(r+1, 512/8, 10)  # el maximo d posible es Nx/4
  for j in range(distancias.size):             
    d = int(distancias[j])  
    # d = int(semidistancias[j])*2      
    if r>(d/2-1):
      # print(r,d,'no sirve')
      densidades[i,j] = -1
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
      for ind_x in range(int(d)):   
        for ind_y in range(int(2*a)):
          if (ind_x-xc)**2+(ind_y-yc)**2<r2:
            obj[ind_y, ind_x] = 1
            
    
    A_mic  = np.sum(obj) 
    A_tot  = 2*a*d    
    densidad = A_mic/A_tot    
    densidades[i,j] = densidad
    if i==0 and j==0:
      print('deeens', densidad)


#%%    


plt.figure(2222)
plt.pcolormesh(densidades, cmap='jet', vmax=1, vmin=0)
plt.colorbar(label='densidad')
plt.xlabel('distancia [voxels]')
plt.ylabel('radio [voxels]')
plt.title('Densidad de microestructuras')

# np.savetxt('densidad_vs_r_y_d.dat', densidades)


#%%

# Rs = [1,3,5,10,15,20,40,60]


# plt.figure(9873)
# for r in Rs:
#   plt.plot(distancias, dens[r-1,:], 'o', label='R={}'.format(int(r)), markersize=8)
# plt.ylim([0,1])
# plt.legend()
# plt.grid('on')

#%%


plt.figure(333)
plt.plot(densidades.T,'o-')
  
  
  

