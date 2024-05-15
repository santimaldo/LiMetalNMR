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
densidades_vol_t = []
vss_t = []
Niter_t = []

Niteraciones=10

nn = 0
# data_dir0 = "2023-07-20_Cilindros_hexagonal_AltaResolucion"

# leo los cilindros aleatorios
data_dir = "2023-08-17_Cilindros_aleatorios_AltaResolucion"

# path0 = f"./Outputs/{data_dir0}/"
path = f"./Outputs/{data_dir}/"
# N_iter	radio (um)	altura (um)	vs (um)	densidad
parametros = np.loadtxt(path+'Densidades.dat')


for par in parametros:
    # path=path0+'SMC64-k1/iteracion{:d}/'.format(jj)

    Niter, radio, altura, vs, densidad, densidad_volumetrica = par

    Niter = int(Niter)
    dens_target = round(densidad, 1)

    regiones = ['-microestructuras', '-bulk', '']
    col = ['k', 'r', 'b']


    Niter_str = f'niter{Niter}_'
    directorio = path

    n_r = -1
    for region in regiones:
        n_r += 1


        archivo = 'h{:d}_r{:.2f}_dens{:.2f}_vs{:.3f}um_{}SP{}.dat'.format(
            int(altura), radio, dens_target, vs, Niter_str, region)

        # extraigo
        try:
            datos = np.loadtxt(f"{directorio}SP/{archivo}")
            print(f"success: {archivo}")
            if n_r == 0:
                alturas_t.append(altura)
                radios_t.append(radio)
                densidades_t.append(densidad)
                densidades_vol_t.append(densidad_volumetrica)
                vss_t.append(vs)
                Niter_t.append(Niter)
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
densidades_vol_t = np.array(densidades_vol_t)
vss_t = np.array(vss_t)

#%%
df = pd.DataFrame(list(zip(alturas_t, radios_t,
                           densidades_t, densidades_vol_t, vss_t,
                           delta_mic, delta_bulk, amp_mic, amp_bulk,
                           np.around(densidades_t, decimals=1), Niter_t)),
                  columns= ['altura', 'radio', 'densidad',
                            'densidad_volumetrica', 'vs',
                            'delta_mic', 'delta_bulk', 'amp_mic', 'amp_bulk',
                            'densidad_nominal', 'Niter'])



# amp_rel = amp_mic/amp_bulk
# corrimientos = delta_mic-delta_bulk

# %%
fontsize = 16
plt.rcParams.update({'font.size': fontsize})
fig = plt.figure(num=1, figsize=(7,5))
gs = fig.add_gridspec(1,1,wspace=0.05)
axs = gs.subplots()

alturas = df['altura'].unique()
radios = df['radio'].unique()
vss = df['vs'].sort_values().unique()

# markersize:
ms = 10


savedata = True # guada el dataframe
filename = False
# filename = "RandomOrientations"
plot_Deltadelta = True
# con esto utilizo solo el menor voxelsize para cada par (radio, densidad)
# eje_x = data['distancia'] - 2*data['radio']

data_dir0 = "2023-07-20_Cilindros_hexagonal_AltaResolucion"
df0 = pd.read_csv(f"./Outputs/{data_dir0}/datos.csv")



# cilindros rectos:
data = df0
data = data.sort_values(by='densidad', ascending=True)
eje_x = data['densidad']
ax = axs
if plot_Deltadelta:
    eje_y = data['delta_mic']-data['delta_bulk']
else:
    eje_y = data['delta_mic']

label = "Straight cylinders"
ax.plot(eje_x, eje_y, 'o', color='k', lw=2, ms=ms, label=label)

coef = np.polyfit(eje_x,eje_y,1)
linear_fit= np.poly1d(coef)
ax.plot(eje_x, linear_fit(eje_x), '--', color='k', lw=1)# marker=marker,




# cilindros aleatorios
data = df[df['Niter']<Niteraciones]
eje_x = data['densidad_volumetrica']
# eje_x = data['densidad']
ax = axs
if plot_Deltadelta:
    eje_y = data['delta_mic']-data['delta_bulk']
else:
    eje_y = data['delta_mic']

label = "Random orientation cylinders"
ax.scatter(eje_x, eje_y, s = 10*ms, facecolor='purple', #edgecolor='purple',
           marker='o', label=label, alpha=0.3)

ax.legend(fontsize=fontsize-2)

ax.set_xlim([0.05, 0.75])
if plot_Deltadelta:
    ax.set_ylim([0, 24])
else:
    ax.set_ylim([-5, 25])
    ax.axhline(y=0, color='gray', ls='--', lw=1)



# agrego ejes y leyendas:------------------------------------------------------
ax.set_xlabel('Density')
# ax.set_xlabel('Density')
if plot_Deltadelta:
# ax.set_ylabel(r'$\delta_{mic}-\delta_{bulk}$ [ppm]')
    ax.set_ylabel(r'$\Delta\delta$ [ppm]')
else:
    ax.set_ylabel(r'$\delta$ [ppm]')



#### colorbar manual ----------------------------------------------------------
# cMap = matplotlib.colormaps[cmap]
# yi = 9
# yi1 = 1.5
# yf1 = 8
# altos1 = np.logspace(np.log10(yi1), np.log10(yf1), radios.size+1)
# for rr in range(radios.size+1):
#     if rr<radios.size:
#         radio = radios[rr]
#         color = cMap(int(rr/vmax*256))
#         # figura de deltas:
#         ancho = 0.1 # unidades de densidad
#         alto = 1.4
#         xi = 0.82
#         axs[0].text(xi+1.25*ancho, yi, f'{radio:.0f}', fontsize=14,
#                 horizontalalignment='left',
#                 verticalalignment='center')
#         axs[0].add_patch(
#             matplotlib.patches.Rectangle(xy=(xi, yi-alto/2.1),
#                                          width=ancho, height=alto,
#                                          facecolor=color))#, edgecolor='k'))

#         # figura de amplitudes:
#         alto1 = np.diff(altos1)[rr]
#         xi1 = 0.06
#         axs1[0].text(xi1+1.25*ancho, altos1[rr]+alto1/2.5, f'{radio:.0f}', fontsize=14,
#                 horizontalalignment='left',
#                 verticalalignment='center')
#         axs1[0].add_patch(
#             matplotlib.patches.Rectangle(xy=(xi1,  altos1[rr]),
#                                           width=ancho, height=alto1,
#                                           facecolor=color))#, edgecolor='k'))
#     else:
#         axs[0].text(xi+0.5*ancho, yi*1.02, r'Radius ($\mu$m)', fontsize=15,
#                 horizontalalignment='center',
#                 verticalalignment='center')
#         axs1[0].text(xi1+1*ancho, altos1[rr]*1.2, r'Radius ($\mu$m)', fontsize=15,
#                 horizontalalignment='center',
#                 verticalalignment='center')

#     yi += alto
#     yi1 += alto1
##################### leyenda voxelsize:
# ax = axs[0]
# # access legend objects automatically created from data
# handles, labels = ax.get_legend_handles_labels()
# # where some data has already been plotted to ax
# handles, labels = ax.get_legend_handles_labels()
# # handles is a list, so append manual patch
# # plot the legend
# ax.legend(handles=handles, frameon=False, fontsize=14,
#           loc="upper right")#, bbox_to_anchor=(0.8,1),
#           #title=r"Voxel width ($\mu$m)", title_fontsize=15)

########## Leyenda altura:
# pos_x = -0.05
# pos_y = 23.5
# fontsize = 15
# for ax in [axs, axs1]:
#     ax[0].text(pos_x, pos_y, rf'a)    Height = ${alturas[0]:.0f}\,\mu$m',
#                 fontsize=fontsize,
#                 horizontalalignment='left', verticalalignment='center')
#     ax[1].text(pos_x, pos_y, rf'b)    Height = ${alturas[1]:.0f}\,\mu$m',
#                 fontsize=fontsize,
#                 horizontalalignment='left', verticalalignment='center')
#     ax[1].label_outer()


if filename:
    fig.savefig(f"{path}/{filename}.png", format='png', bbox_inches='tight')
    fig.savefig(f"{path}/{filename}.eps", format='eps',bbox_inches='tight')
    fig.savefig(f"{path}/{filename}.pdf", format='pdf',bbox_inches='tight')

if savedata:
  df.to_csv(f'{path}/datos.csv', index=False)
