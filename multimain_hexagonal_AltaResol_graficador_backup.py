# -*- coding: utf-8 -*-
"""
Created on 13/06/2021

@author: santi
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from VoigtFit import *
plt.rcParams.update({'font.size': 20})
import matplotlib
import matplotlib.patches as mpatches


p_cubierto = []
delta_mic = []
delta_bulk = []
amp_mic = []
amp_bulk = []

alturas_t = []
distancias_t = []
radios_t = []
densidades_t = []
vss_t = []

nn = 0
# folders = ['','2022-03-11_','2022-03-13_']
folders = ['2023-07-20']

for folder in folders:
    path0 = f"./Outputs/{folder}_Cilindros_hexagonal_AltaResolucion/"
    print(path0)
    distancias, radios, alturas, vss, densidades = np.loadtxt(
        path0+'Densidades.dat').T
    for ii in range(radios.size):
        # path=path0+'SMC64-k1/iteracion{:d}/'.format(jj)
        h = alturas[ii]
        d = distancias[ii]
        r = radios[ii]
        p = densidades[ii]
        vs = vss[ii]

        regiones = ['-microestructuras', '-bulk']
        col = ['k', 'r', 'b']

        n_r = -1
        for region in regiones:
            n_r += 1
            path = path0 + 'SP/'
            archivo = 'h{:d}_r{:.2f}_d{:.2f}_vs{:.3f}um_SP{}.dat'.format(
                int(h), r, d, vs, region)

            # extraigo

            try:
                datos = np.loadtxt(path+archivo)
                if n_r == 0:
                    alturas_t.append(h)
                    distancias_t.append(d)
                    radios_t.append(r)
                    densidades_t.append(p)
                    vss_t.append(vs)
                    nn += 1
            except:
                print(f"error al intentar leer: {archivo}")
                continue
            ppmAxis0 = datos[:, 0]
            spec = datos[:, 1]
            #spec_imag = datos[:,2]

            # retoco:
            ppmAxis = ppmAxis0
            spec = spec - spec[0]
            # reduzco los datos a una VENTANA alrededor de un CENTRO
            ventana = 200
            center = 0
            ppmAxis = ppmAxis0[np.abs(center-ppmAxis0) < ventana]
            spec = spec[np.abs(center-ppmAxis0) < ventana]

            plt.figure(1231)
            plt.subplot(1, 3, n_r+1)
            plt.plot(ppmAxis, spec, col[n_r], linewidth=2)
            #plt.xlim([ppmAxis[-1], ppmAxis[0]])
            plt.xlim(150, -150)
            plt.vlines(0, 0, np.max(spec))
            plt.yticks([])

            if region == '-microestructuras':
                delta_mic.append(ppmAxis[spec == np.max(spec)][0])
                i_mic = np.trapz(spec, x=ppmAxis)
                amp_mic.append(i_mic)

                # if vs == r:
                #     plt.figure(11111)
                # else:
                #     plt.figure(22222)
                #     plt.annotate(f"r{r} vs{vs}",
                #                  (p, ppmAxis[spec == np.max(spec)][0]))
                # plt.scatter(p, ppmAxis[spec == np.max(spec)][0])

            elif region == '-bulk':
                delta_bulk.append(ppmAxis[spec == np.max(spec)][0])
                i_bulk = np.trapz(spec, x=ppmAxis)
                amp_bulk.append(i_bulk)


#---------------- guardado


delta_mic = np.array(delta_mic)
delta_bulk = np.array(delta_bulk)
amp_mic = np.array(amp_mic)
amp_bulk = np.array(amp_bulk)

alturas_t = np.array(alturas_t)
distancias_t = np.array(distancias_t)
radios_t = np.array(radios_t)
densidades_t = np.array(densidades_t)
vss_t = np.array(vss_t)


df = pd.DataFrame(list(zip(alturas_t, radios_t, 
                           densidades_t, distancias_t, vss_t,
                           delta_mic, delta_bulk, amp_mic, amp_bulk,
                           np.around(densidades_t, decimals=1))),
                  columns =['altura', 'radio', 'densidad', 'distancia', 'vs',
                            'delta_mic', 'delta_bulk', 'amp_mic', 'amp_bulk',
                            'densidad_nominal'])



amp_rel = amp_mic/amp_bulk
corrimientos = delta_mic-delta_bulk

# %%
# ACA GRAFICO TODOS LOS VOXELSIZE CON UNA FORMA DE SCATTER DISTINTA PARA CADA
# VS
plt.rcParams.update({'font.size': 16})
fig = plt.figure(num=1, figsize=(10,5))
gs = fig.add_gridspec(1,2,wspace=0.05)
axs = gs.subplots()
fig1, axs1 = plt.subplots(1,2,num=2, figsize=(10,5))
# try:
# plt.scatter(densidades_t, delta_mic, c=alturas_t)
marks = ['^','o', 's', 'v', '*', 'p']


alturas = df['altura'].unique()
radios = df['radio'].unique()
vss = df['vs'].sort_values().unique()

# con esto utilizo solo el menor voxelsize para cada par (radio, densidad)
sin_repetir_data = True

hh = 0
for h in alturas:
    data_h = df.query(f'altura == {h}')

    if sin_repetir_data:
        min_vs = data_h.groupby(['radio','densidad_nominal'])['vs'].idxmin()
        data_h = data_h.loc[min_vs.values]
    
    nn = 0
    for vs in vss:            
        data = data_h.query(f'vs == {vs}')   
        colorscale = [np.where(radios==r)[0][0] for r in data['radio']]        
        cmap = 'inferno'
        vmin = 0; vmax = 5.5
        eje_x = data['densidad']
        # eje_x = data['distancia'] - 2*data['radio']
        # ------- ---- delta
        # eje_y = data['delta_mic'] - data['delta_bulk']        
        eje_y = data['delta_mic']        
        ax = axs[hh]
        ax.scatter(eje_x, eje_y , marker=marks[nn],
                         c=colorscale, vmin=vmin, vmax=vmax, cmap=cmap,
                         edgecolor='k',
                         s=100, label=f"{vs:.3f}")       
        # c = plt.cm.inferno(colors) ##3 esto es si quiero color en el edge
        ax.scatter(eje_x, data['delta_bulk'] , marker=marks[nn],                    
                   # facecolor='none', edgecolors=c, lw=2 # para color en edge
                   c=colorscale, vmin=vmin, vmax=vmax, cmap=cmap,
                   s=100)        
        ax.set_xlim([-0.08, 1.08])
        ax.set_ylim([-5, 25])        
        # ----------- amp
        eje_y = data['amp_mic'] / data['amp_bulk']        
        ax = axs1[hh]
        ax.scatter(eje_x, eje_y , marker=marks[nn],
                         c=colorscale, vmin=vmin, vmax=vmax, cmap=cmap,
                         edgecolor='k',
                         s=100, label=f"vs = {vs} um")
        ax.set_yscale('log')
        ax.axhline(y=1, ls='--', color='k')
        ax.set_xlim([0, 1])
        ax.set_ylim([0.1, 30])
        nn += 1    
    hh+=1
    
# agrego ejes y leyendas:------------------------------------------------------
for ax in axs:
    ax.set_xlabel('Density')
    # ax.set_ylabel(r'$\delta_{mic}-\delta_{bulk}$ [ppm]')
    ax.set_ylabel(r'$\Delta\delta$ [ppm]')
for ax in axs1:
    ax.set_xlabel('Density')
    ax.set_ylabel(r'$A_{mic}/A_{bulk}$')
    
    

#### colorbar manual ----------------------------------------------------------
cMap = matplotlib.colormaps[cmap]
yi = 1.5
yi1 = 2
for rr in range(radios.size+1):    
    if rr<radios.size:
        radio = radios[rr]
        color = cMap(int(rr/vmax*256))
        # figura de deltas:
        ancho = 0.1 # unidades de densidad
        alto = 1.4
        xi = 0.06
        axs[1].text(xi+1.25*ancho, yi, f'{radio:.0f}', fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')    
        axs[1].add_patch(
            matplotlib.patches.Rectangle(xy=(xi, yi-alto/2.1), 
                                         width=ancho, height=alto, 
                                         facecolor=color))#, edgecolor='k'))
        
        # figura de amplitudes:
        # alto1 = 1            
        # xi1 = 0.06
        # axs1[0].text(xi1+1.25*ancho, yi, f'{radio:.0f}', fontsize=14,
        #         horizontalalignment='left',
        #         verticalalignment='center')    
        # axs1[0].add_patch(
        #     matplotlib.patches.Rectangle(xy=(xi1, yi1-alto/2.1), 
        #                                  width=ancho, height=alto, 
        #                                  facecolor=color))#, edgecolor='k'))
    else:
        axs[1].text(xi+1*ancho, yi*1.01, r'Radius ($\mu$m)', fontsize=15,
                horizontalalignment='center',
                verticalalignment='center')

    yi += alto
    # yi1 += alto1
##################### leyenda voxelsize:
ax = axs[0]
# access legend objects automatically created from data
handles, labels = ax.get_legend_handles_labels()
# where some data has already been plotted to ax
handles, labels = ax.get_legend_handles_labels()
# handles is a list, so append manual patch
# plot the legend
ax.legend(handles=handles, frameon=False, fontsize=14,
          loc="upper right", bbox_to_anchor=(1,0.9),          
          title=r"Voxel width ($\mu$m)", title_fontsize=15)

########## Leyenda altura:
pos_x = 1.0
pos_y = 23.5
fontsize = 15 
axs[0].text(pos_x, pos_y, rf'Height = ${alturas[0]:.0f}\,\mu$m', fontsize=fontsize,
        horizontalalignment='right',
        verticalalignment='center')
axs[1].text(pos_x, pos_y, rf'Height = ${alturas[1]:.0f}\,\mu$m', fontsize=fontsize,
        horizontalalignment='right',
        verticalalignment='center')

axs[1].label_outer()
fig.savefig(f"{path0}/Deltadelta_vs_density.png", format='png', bbox_inches='tight')
fig.savefig(f"{path0}/Deltadelta_vs_density.pdf", format='pdf',bbox_inches='tight')
fig.savefig(f"{path0}/Deltadelta_vs_density.eps", format='eps',bbox_inches='tight')