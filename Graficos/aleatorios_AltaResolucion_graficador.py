# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:11:37 2023

@author: Santi


Script para graficar los resultados de simular con radio 2 um y altura 10 um.

Simulaciones:
  cilindros rectos, arreglo hexagonal
  cilindros con cambios de orientacion 45 grados, arreglo hexagonal
  cilindros con cambios de orientacion angulos aleatorios, arreglo aleatorio
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as mpatches


fontsize = 16
plt.rcParams.update({'font.size': fontsize})
fig = plt.figure(num=1, figsize=(7,5))
gs = fig.add_gridspec(1,1,wspace=0.05)
axs = gs.subplots()


savefig = False
filename = "RandomOrientations"
plot_Deltadelta = True

# markersize:
ms = 10

# colores:
cmap = matplotlib.colormaps['gray']
color_rectos = cmap(0)
color_45 = cmap(0.6)  
  
cmap = matplotlib.colormaps['inferno']
color_randhex= cmap(0.3)
color_rand = cmap(0.65)

# leyendas:
label_rectos = r"$\mathbf{A}$: Hexagonal / $0^{\circ}$"
label_45 = r"$\mathbf{B}$: Hexagonal / $45^{\circ}$"
label_randhex = r"$\mathbf{C}$: Hexagonal / random ($0^{\circ}$ or $45^{\circ}$)"
label_rand = r"$\mathbf{D}$: Random    / random (beween $14^{\circ}$ and $76^{\circ}$)"


# cilindros rectos ------------------------------------------------------------
data_dir0 = "2023-08-14_Cilindros_hexagonal_AltaResolucion"
df0 = pd.read_csv(f"../Outputs/{data_dir0}/datos.csv")

data = df0
data = data[(data['radio']==2) & (data['altura']==10)]
data = data.sort_values(by='densidad', ascending=True)
eje_x = data['densidad']             
ax = axs
if plot_Deltadelta:
    eje_y = data['delta_mic']-data['delta_bulk']
else:
    eje_y = data['delta_mic']
    
label = "Straight cylinders"
ax.plot(eje_x, eje_y, 'o', color=color_rectos, lw=2, ms=ms, label=label_rectos)

coef = np.polyfit(eje_x,eje_y,1)
linear_fit= np.poly1d(coef) 
ax.plot(eje_x, linear_fit(eje_x), '--', color='k', lw=1)# marker=marker,
# end cilindros rectos --------------------------------------------------------


# cilindros A 45 GRADOS:-------------------------------------------------------
data_dir45 = "2023-08-07_Cilindros_45grados_hexagonal_AltaResolucion"
df45 = pd.read_csv(f"../Outputs/{data_dir45}/datos.csv")
data = df45
data = data.sort_values(by='densidad', ascending=True)
eje_x = data['densidad']             
ax = axs
if plot_Deltadelta:
    eje_y = data['delta_mic']-data['delta_bulk']
else:
    eje_y = data['delta_mic']
    

ax.plot(eje_x, eje_y, 'o', color=color_45, lw=2, ms=ms, label=label_45)

coef = np.polyfit(eje_x,eje_y,1)
linear_fit= np.poly1d(coef) 
ax.plot(eje_x, linear_fit(eje_x), '--', color='gray', lw=1)# marker=marker,
# end cilindros A 45 GRADOS:---------------------------------------------------



# cilindros aleatorios hexagonal-----------------------------------------------
# data_dir_randhex= "2023-08-02_Cilindros_aleatorios_hexagonal_AltaResolucion"
# df_randhex = pd.read_csv(f"../Outputs/{data_dir_randhex}/datos.csv")

# data = df_randhex
# eje_x = data['densidad_volumetrica']         
# # eje_x = data['densidad']         
# ax = axs
# if plot_Deltadelta:
#     eje_y = data['delta_mic']-data['delta_bulk']
# else:
#     eje_y = data['delta_mic']

# ax.scatter(eje_x, eje_y, s = 10*ms, facecolor=color_randhex, #edgecolor='purple',
#            marker='o', alpha=0.3)       
# # ghost data, pra la legend:
# ax.scatter([1000], [1000], s = 10*ms, facecolor=color_randhex, #edgecolor='purple',
#            marker='o', label=label_randhex, alpha=0.9)         
# end cilindros aleatorios hexagonal-------------------------------------------


# cilindros aleatorios pos aleatoria-------------------------------------------
data_dir_rand= "2023-08-16_Cilindros_aleatorios_AltaResolucion"
df_rand = pd.read_csv(f"../Outputs/{data_dir_rand}/datos.csv")

data = df_rand
eje_x = data['densidad_volumetrica']         
# eje_x = data['densidad']         
ax = axs
if plot_Deltadelta:
    eje_y = data['delta_mic']-data['delta_bulk']
else:
    eje_y = data['delta_mic']


ax.scatter(eje_x, eje_y, s = 10*ms, facecolor=color_rand, #edgecolor='purple',
           marker='o', alpha=0.3)
# ghost data, pra la legend:
ax.scatter([1000], [1000], s = 10*ms, facecolor=color_rand, #edgecolor='purple',
           marker='o', label=label_rand, alpha=0.9)

# end cilindros aleatorios pos aleatoria---------------------------------------


# limites:---------------------------------------------------------------------
ax.set_xlim([0.05, 0.75])
if plot_Deltadelta:
    ax.set_ylim([0, 22])            
else:
    ax.set_ylim([-5, 25])            
    ax.axhline(y=0, color='gray', ls='--', lw=1)
title = "          Arrangement / angle"
ax.legend(fontsize=fontsize-5, frameon=False, 
          title=title, title_fontsize=fontsize-5,
          loc="lower left", alignment='left')

    
# agrego ejes y leyendas:------------------------------------------------------
ax.set_xlabel('Density')
# ax.set_xlabel('Density')
if plot_Deltadelta:
# ax.set_ylabel(r'$\delta_{mic}-\delta_{bulk}$ [ppm]')
    ax.set_ylabel(r'$\Delta\delta$ [ppm]')        
else:
    ax.set_ylabel(r'$\delta$ [ppm]')




if savefig:
    fig.savefig(f"./{filename}.png", format='png', bbox_inches='tight')    
    fig.savefig(f"./{filename}.eps", format='eps',bbox_inches='tight')
    fig.savefig(f"./{filename}.pdf", format='pdf',bbox_inches='tight')
    fig.savefig(f"./{filename}.svg", format='svg',bbox_inches='tight')




#%%--------------
# eje_x = df0['densidad']             
# eje_y = (df0['delta_mic']-df0['delta_bulk']) - (df45['delta_mic']-df45['delta_bulk'])
# plt.figure(1)
# plt.plot(eje_x, eje_y, 'o')
