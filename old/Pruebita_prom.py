# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 15:20:22 2023

@author: Usuario
"""
import numpy as np

# A_mic = 1024*1024 #um
# L_mic = 1024     #um

# R_e = 6000 #um 


# A_elec = np.pi*R_e*R_e #um*um
# print(A_elec)
# veces = A_elec/A_mic
# print(veces)


# w_it = 0
# w = 0

# w_it_list = []
# lista_radios = []
# RADIO=0



# for i in range(7) :
#     RADIO = float(i)*L_mic
#     print('RADIO',RADIO)
#     if i == 0:
#         w_it = 1                            # Porque para R=0 tiene que aparecer una vez
#         print('w_it',w_it)
#         w_it_list.append([int(w_it)])
#     else:
#         w_it =2*np.pi*RADIO/L_mic -3.6      # El -3.6 es para fitear la cantidad de veces que entra el area de las mic en el area del electrodo
#         print('w_it',w_it)
#         w_it_list.append([int(w_it)])
    
#     w = w + int(w_it)
        
# print('w',w)

# #Ahora otra forma de hacerlo es una que propuso el Santi con las áreas...

# A_i_list = []
# A = 0
# A_i = 0

# for i in range(7) :
#     RADIO = float(i)*L_mic
#     print('RADIO',RADIO)
#     if i == 0:
#         A_i = np.pi*(L_mic**2)                            # Porque para R=0 tiene que aparecer una vez
#         print('A_i',A_i)
#         A_i_list.append([int(A_i)])
#     else:
#         A_i = np.pi*((RADIO+1)**2-(RADIO-1)**2)       # El -3.6 es para fitear la cantidad de veces que entra el area de las mic en el area del electrodo
#         print('A_i',A_i)
#         A_i_list.append([int(A_i)])
    
#     A = A + int(A_i)
#     A_norm = A/A_elec
        
# print('A_norm',A_norm)


lista_radios = ['0000','0320','0520','0800','1000','1320','1600','1800','2000','2320','2600','2960','3000','3440','3720','3920','4000','4400','4720','5000','5199','5480','5720','5960'] 
A_med = 256*256 #um
L_med = 256     #um

R_e = 6000 #um 



A_elec = np.pi*R_e*R_e #um*um
print(A_elec)
veces = A_elec/A_med
print('veces=',veces)


w_it = 0
w = 0

w_it_list = []


for RADIO in lista_radios :
    if RADIO == '0000':
        w_it = 1                                  # Porque para R=0 tiene que aparecer una vez
        print('w_it',w_it)
        w_it_list.append([int(w_it)])
    else:
        w_it =2*np.pi*float(RADIO)/L_med -1.2     # El -1.2 es para fitear la cantidad de veces que entra el area de las mic en el area del electrodo
        print('w_it',w_it)
        w_it_list.append([int(w_it)])
    
    w = w + int(w_it)
        
print('w',w)







