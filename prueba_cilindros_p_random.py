# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 15:54:51 2022

@author: Muri
"""


import numpy as np
import matplotlib.pyplot as plt



""" 2022-04-06
      Igual que los cilindros aleatorios 2. Intento crear posiciones aleatorias
      en x-y, no a distancias fijas."""   
 

N = np.array([256,256,256]) 
distancia = 20e-3
ancho  = 16e-3
voxelSize = np.array([1e-3,1e-3,1e-3])
Nmx,Nmy,Nmz = N

print(N)
vsz, vsy, vsx = voxelSize
   
# cuantos voxels debo usar por cilindro 
R = int(ancho/(2*vsx))
print(R)
nsx = int(ancho/vsx)
print(nsx)
nsy = int(ancho/vsy)
print(nsy)
ndx = int(distancia/vsx)
print(ndx)
ndy = int(distancia/vsy)
print(ndy)
  
 
#Armo los indices aleatorios desde donde va a crecer la dendrita
rand_x = []
rand_y = []

for i in range(0,36,1):
    r_ind_x = 0
    r_ind_y = 0
    r_ind_x = np.random.randint(17,241)
    r_ind_y = np.random.randint(17,241)
    rand_x.append(r_ind_x)
    rand_y.append(r_ind_y)
 
    
 
indices = []
  
Nz_random_1 = []
   
#n=0
ind_x = 0
ind_y = 0
  
for i in range(0,36,1):
    ind_x = rand_x[i]
    ind_y = rand_y[i]
    print('ind_x',ind_x)
    print('ind_y',ind_y)
    ind_z = 0
    Nz_rand_1 = np.random.randint(0,int(N[0]/3)+1)
    print('Nz_rand_1',Nz_rand_1)
    Nz_random_1.append(Nz_rand_1)
    while ind_z < Nz_rand_1:    
        for iy in range(nsy):
            for ix in range(nsx):
                if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                    indices.append((ind_z,ind_y+iy, ind_x+ix))
                    ind_z+=1 
#Hasta acá hice que todas las dendritas crezcan derechas hasta zmax/3
    
Nz_random_2 = []
ind_x_lista = []
ind_y_lista = []
ind_suma_x_lista = []
ind_suma_y_lista = []
  
j = 0
for i in range(0,36,1):
    ind_x = rand_x[i]
    ind_y = rand_y[i]
    ind_suma_y=0
    ind_suma_x=0
    ind_z = Nz_random_1[j]
    ind_suma_rand_y= np.random.randint(0,3)-1
    ind_suma_rand_x= np.random.randint(0,3)-1
    Nz_rand_2 = np.random.randint(ind_z,int(2*N[0]/3)+1)
    while ind_z < Nz_rand_2 and ind_x + ind_suma_x <= (Nmx-2*nsx) and ind_x + ind_suma_x >= 2*nsx and ind_y + ind_suma_y <= (Nmy-2*nsy) and ind_y + ind_suma_y >= 2*nsy:
        for iy in range(nsy):
            for ix in range(nsx):
                if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                    indices.append((ind_z,ind_y+iy+ind_suma_y, ind_x+ix+ind_suma_x))
                    
        ind_suma_x+= ind_suma_rand_x
        ind_suma_y+= ind_suma_rand_y                  
         
        ind_z+=1
         
    ind_y_lista.append(ind_y)                
    ind_suma_y_lista.append(ind_suma_y)
    ind_suma_x_lista.append(ind_suma_x)
    j=j+1
    Nz_random_2.append(ind_z)
    ind_x_lista.append(ind_x)
         
 #Hasta acá construi en z con orientaciones en cada uno de los cilindros
  
k=0
for i in range(0,36,1):
    ind_x = ind_x_lista[k]
    ind_y = ind_y_lista[k]
    ind_suma_y=ind_suma_y_lista[k]
    ind_suma_x=ind_suma_x_lista[k]
    ind_z = Nz_random_2[k]
    ind_suma_rand_y= np.random.randint(0,3)-1
    ind_suma_rand_x= np.random.randint(0,3)-1
    #print('ind_suma_rand_y',ind_suma_rand_y)
    #print('ind_z',ind_z)
    while ind_z < N[0] and ind_x + ind_suma_x <= (Nmx-2*nsx) and ind_x + ind_suma_x >= 2*nsx-1 and ind_y + ind_suma_y <= (Nmy-2*nsy) and ind_y + ind_suma_y >= 2*nsy-1:
        for iy in range(nsy):
            for ix in range(nsx):
                if (ix-nsx/2)**2 + (iy-nsy/2)**2 < R**2:
                    indices.append((ind_z,ind_y+iy+ind_suma_y, ind_x+ix+ind_suma_x))
                     #n+=1
                      #print('n_abajo',n)
                      
        ind_suma_x+= ind_suma_rand_x
        ind_suma_y+= ind_suma_rand_y
        #print('ind_suma_y',ind_suma_y)
                  
              
        ind_z+=1
    k=k+1




if __name__=='__main__':
  """
  script para testear las geometrias
  """
  # este N es el N de la muestra ejemplo
  #N = np.array([128,256,256])

  Nz,Ny,Nx = N   
  #voxelSize = np.array([1e-3,1e-3,1e-3])
  
  # 'geometria' es el nombre de la geometria que vamos a utilizar
  # 'constructor' es una FUNCION. Esa funcion es diferente de acuerdo a la geometria elegida

  constructor = 'cilindros_p_random'
  # la funcion 'constructor' me devuelve las tuplas (ind_z, ind_y, ind_x) de los indices
  # en los cuales hay litio.
  #tuplas = constructor(N, voxelSize, ancho=16e-3, distancia=20e-3)
  #tuplas = constructor(N, voxelSize, ancho=4e-3, distancia=3e-3) # para 'distancia_constante'
  tuplas = constructor(N, voxelSize, ancho=16e-3, distancia=20e-3, extra_info=False) # para 'distancia_constante'
  #tuplas = constructor(N, voxelSize, ancho=20e-3, porcentaje=80) # para 'porcentaje_palos'
  #tuplas = constructor(N, voxelSize, radio=9e-3, distancia=20e-3, parametro_a=17e-3) # para 'cilindros_hexagonal'


  # convierto a indices planos
  indices = np.array(tuplas).T  
  
  indices = np.ravel_multi_index(indices, N)
  
  # creo la matriz vacia, y coloco 1 en los indices que me da el constructor
  muestra = np.zeros(N)
  #  put(array       , indices, valor)
  np.put(muestra, indices, 1)
  