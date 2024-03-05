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


data_dir = "2023-08-14_Cilindros_hexagonal_AltaResolucion"
df = pd.read_csv(f"../Outputs/{data_dir}/datos.csv")

savefig = False
filename = "Cylinders"
plot_Deltadelta = False


plt.rcParams.update({'font.size': 16})
fig = plt.figure(num=1, figsize=(10, 5))
gs = fig.add_gridspec(1, 2, wspace=0.05)
axs = gs.subplots()
fig1 = plt.figure(num=2, figsize=(10, 5))
gs1 = fig1.add_gridspec(1, 2, wspace=0.05)
axs1 = gs1.subplots()


alturas = df['altura'].unique()
radios = df['radio'].unique()
vss = df['vs'].sort_values().unique()

# quito un puntos que esta feos.
# try:
#     condicion1 = (df['radio']==20) & (df['densidad_nominal']==0.8) & (df['vs']==0.25) & (df['altura']==50)
#     condicion2 = (df['radio']==1) & (df['densidad_nominal']==0.6) & (df['vs']==0.125) & (df['altura']==50)
#     # condicion2 = False
#     index = df.index[condicion1 | condicion2]
#     df.drop(index, inplace=True)
# except:
#     pass

marks = ['^', 'o', 's', 'v', '*', 'p']

savedata = True  # para guardar los dataframes
filename = False
# filename = "Deltadelta_vs_density"
plot_Deltadelta = True
# con esto utilizo solo el menor voxelsize para cada par (radio, densidad)
sin_repetir_data = True
letra = ['a', 'b']
hh = 0
for h in alturas:
    data_h = df[(df['altura'] == h)]
    nn = 0
    for vs in vss:
        if sin_repetir_data:
            min_vs = data_h.groupby(['radio', 'densidad_nominal'])[
                'vs'].idxmin()
            data = data_h.loc[min_vs.values]
        else:
            data = data_h[data_h['vs'] == vs]

        # eje_x = data['distancia'] - 2*data['radio']
        eje_x = data['densidad']

        colorscale = [np.where(radios == r)[0][0] for r in data['radio']]
        cmap = 'inferno'
        vmin = 0
        vmax = 5.5

        ax = axs[hh]

        if plot_Deltadelta:
            eje_y = data['delta_mic']-data['delta_bulk']
        else:
            eje_y = data['delta_mic']
        if sin_repetir_data:
            label = r"$\delta_{mic}$"
            marker = 'o'
        else:
            marker = marks[nn]
            label = rf"{vs:.3f}$\mu$m"

        ax.scatter(eje_x, eje_y, marker=marker,
                   c=colorscale, vmin=vmin, vmax=vmax, cmap=cmap,
                   edgecolor='k',
                   s=100, label=label)
        if not plot_Deltadelta:
            ax.scatter(eje_x, data['delta_bulk'], marker='^',
                       c=colorscale, vmin=vmin, vmax=vmax, cmap=cmap,
                       edgecolor='k',
                       s=100, label=r"$\delta_{bulk}$")
        ax.set_xlim([-0.08, 1.08])
        if plot_Deltadelta:
            ax.set_ylim([0, 25])
        else:
            ax.set_ylim([-10, 25])
            ax.axhline(y=0, color='gray', ls='--', lw=1)
        # ----------- amp
        eje_y = data['amp_mic'] / data['amp_bulk']
        ax = axs1[hh]
        ax.scatter(eje_x, eje_y, marker='o',
                   c=colorscale, vmin=vmin, vmax=vmax, cmap=cmap,
                   edgecolor='k',
                   s=100, label=f"vs = {vs} um")
        ax.set_yscale('log')
        ax.axhline(y=1, ls='--', color='k')
        ax.set_xlim([-0.08, 1.08])
        ax.set_ylim([0.1, 30])

        if sin_repetir_data:
            break
        nn += 1

    hh += 1

# agrego ejes y leyendas:------------------------------------------------------
for ax in axs:
    ax.set_xlabel('Density')
    if plot_Deltadelta:
        # ax.set_ylabel(r'$\delta_{mic}-\delta_{bulk}$ [ppm]')
        ax.set_ylabel(r'$\Delta\delta$ [ppm]')
    else:
        ax.set_ylabel(r'$\delta$ [ppm]')
for ax in axs1:
    ax.set_xlabel('Density')
    ax.set_ylabel(r'$A_{mic}/A_{bulk}$')


# colorbar manual ----------------------------------------------------------
cMap = matplotlib.colormaps[cmap]
yi = 9
yi1 = 1.5
yf1 = 8
altos1 = np.logspace(np.log10(yi1), np.log10(yf1), radios.size+1)
for rr in range(radios.size+1):
    if rr < radios.size:
        radio = radios[rr]
        color = cMap(int(rr/vmax*256))
        # figura de deltas:
        ancho = 0.1  # unidades de densidad
        alto = 1.4
        xi = 0.82
        axs[0].text(xi+1.25*ancho, yi, f'{radio:.0f}', fontsize=14,
                    horizontalalignment='left',
                    verticalalignment='center')
        axs[0].add_patch(
            matplotlib.patches.Rectangle(xy=(xi, yi-alto/2.1),
                                         width=ancho, height=alto,
                                         facecolor=color))  # , edgecolor='k'))

        # figura de amplitudes:
        alto1 = np.diff(altos1)[rr]
        xi1 = 0.06
        axs1[0].text(xi1+1.25*ancho, altos1[rr]+alto1/2.5, f'{radio:.0f}', fontsize=14,
                     horizontalalignment='left',
                     verticalalignment='center')
        axs1[0].add_patch(
            matplotlib.patches.Rectangle(xy=(xi1,  altos1[rr]),
                                         width=ancho, height=alto1,
                                         facecolor=color))  # , edgecolor='k'))
    else:
        axs[0].text(xi+0.5*ancho, yi*1.02, r'Radius ($\mu$m)', fontsize=15,
                    horizontalalignment='center',
                    verticalalignment='center')
        axs1[0].text(xi1+1*ancho, altos1[rr]*1.2, r'Radius ($\mu$m)', fontsize=15,
                     horizontalalignment='center',
                     verticalalignment='center')

    yi += alto
    yi1 += alto1
# leyenda voxelsize:
ax = axs[0]
# access legend objects automatically created from data
handles, labels = ax.get_legend_handles_labels()
# where some data has already been plotted to ax
handles, labels = ax.get_legend_handles_labels()
# handles is a list, so append manual patch
# plot the legend
ax.legend(handles=handles, frameon=False, fontsize=14,
          loc="upper right")  # , bbox_to_anchor=(0.8,1),
# title=r"Voxel width ($\mu$m)", title_fontsize=15)

# Leyenda altura:
pos_x = -0.05
pos_y = 23.5
fontsize = 15
for ax in [axs, axs1]:
    ax[0].text(pos_x, pos_y, rf'a)    Height = ${alturas[0]:.0f}\,\mu$m',
               fontsize=fontsize,
               horizontalalignment='left', verticalalignment='center')
    # ax[1].text(pos_x, pos_y, rf'b)    Height = ${alturas[1]:.0f}\,\mu$m',
    #             fontsize=fontsize,
    #             horizontalalignment='left', verticalalignment='center')
    ax[1].label_outer()


if filename:
    fig.savefig(f"{path0}/{filename}.png", format='png', bbox_inches='tight')
    fig.savefig(f"{path0}/{filename}.eps", format='eps', bbox_inches='tight')

    fig1.savefig(f"{path0}/Amplitud_vs_density.png",
                 format='png', bbox_inches='tight')
    fig1.savefig(f"{path0}/Amplitud_vs_density.eps",
                 format='eps', bbox_inches='tight')
