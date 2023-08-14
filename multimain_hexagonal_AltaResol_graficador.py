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


# path0 = "./Outputs/2023-08-10_Cilindros_hexagonal_AltaResolucion/"
# print(path0)
# distancias, radios, alturas, vss, densidades_nominales, densidades = np.loadtxt(
#     path0+'Densidades.dat').T

path0 = "./Outputs/2023-08-10_Cilindros_hexagonal_AltaResolucion/"
print(path0)
parametros10 = np.loadtxt(path0+'Densidades10um.dat')
parametros50 = np.loadtxt(path0+'Densidades50um.dat')
parametros = np.concatenate((parametros10, parametros50))
distancias, radios, alturas, vss, densidades_nominales, densidades = parametros.T
for ii in range(radios.size):
    # path=path0+'SMC64-k1/iteracion{:d}/'.format(jj)
    h = alturas[ii]
    d = distancias[ii]
    r = radios[ii]
    p = densidades[ii]
    densidad_nominal = densidades_nominales[ii]
    vs = vss[ii]

    regiones = ['-microestructuras', '-bulk']
    col = ['k', 'r', 'b']

    n_r = -1
    for region in regiones:
        n_r += 1
        path = path0 + 'SP/'
        # archivo = 'h{:d}_r{:.2f}_d{:.2f}_vs{:.3f}um_SP{}.dat'.format(
        #     int(h), r, d, vs, region)
        archivo = 'h{:d}_r{:.2f}_dens{:.1f}_vs{:.3f}um_SP{}.dat'.format(
            int(h), r, densidad_nominal, vs, region)
        # archivo = 'h{:d}_r{:.2f}_dens{:.1f}_vs{:.3f}um_SMC{}.dat'.format(
        #      int(h), r, densidad_nominal, vs, region)

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
        spec_imag = datos[:,2]        
        spec = np.abs(spec+1j*spec_imag)

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
df = df.sort_values(by='radio', ascending=True)


amp_rel = amp_mic/amp_bulk
corrimientos = delta_mic-delta_bulk

# %%
plt.rcParams.update({'font.size': 16})
fig = plt.figure(num=1, figsize=(10,5))
gs = fig.add_gridspec(1,2,wspace=0.05)
axs = gs.subplots()
fig1 = plt.figure(num=2, figsize=(10,5))
gs1 = fig1.add_gridspec(1,2,wspace=0.05)
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

marks = ['^','o', 's', 'v', '*', 'p']

savedata = True # para guardar los dataframes
filename = False
# filename = "Deltadelta_vs_density"
plot_Deltadelta = False
# con esto utilizo solo el menor voxelsize para cada par (radio, densidad)
sin_repetir_data = True
letra = ['a', 'b']
hh = 0
for h in alturas:
    data_h = df[(df['altura']== h)]
    nn = 0
    for vs in vss:
        if sin_repetir_data:
            min_vs = data_h.groupby(['radio','densidad_nominal'])['vs'].idxmin()
            data = data_h.loc[min_vs.values]
        else:
            data = data_h[data_h['vs']==vs]

        # eje_x = data['distancia'] - 2*data['radio']
        eje_x = data['densidad']

        colorscale = [np.where(radios==r)[0][0] for r in data['radio']]
        cmap = 'inferno'
        vmin = 0; vmax = 5.5

        ax = axs[hh]

        if plot_Deltadelta:
            eje_y = data['delta_mic']-data['delta_bulk']
        else:
            eje_y = data['delta_mic']
        if sin_repetir_data:
            label= r"$\delta_{mic}$"
            marker = 'o'
        else:
            marker = marks[nn]
            label=rf"{vs:.3f}$\mu$m"

        ax.scatter(eje_x, eje_y, marker=marker,
                         c=colorscale, vmin=vmin, vmax=vmax, cmap=cmap,
                         edgecolor='k',
                         s=100, label=label)
        if not plot_Deltadelta:
            ax.scatter(eje_x, data['delta_bulk'] , marker='^',
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
        ax.scatter(eje_x, eje_y , marker = 'o',
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

    hh+=1

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



#### colorbar manual ----------------------------------------------------------
cMap = matplotlib.colormaps[cmap]
yi = 9
yi1 = 1.5
yf1 = 8
altos1 = np.logspace(np.log10(yi1), np.log10(yf1), radios.size+1)
for rr in range(radios.size+1):
    if rr<radios.size:
        radio = radios[rr]
        color = cMap(int(rr/vmax*256))
        # figura de deltas:
        ancho = 0.1 # unidades de densidad
        alto = 1.4
        xi = 0.82
        axs[0].text(xi+1.25*ancho, yi, f'{radio:.0f}', fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')
        axs[0].add_patch(
            matplotlib.patches.Rectangle(xy=(xi, yi-alto/2.1),
                                         width=ancho, height=alto,
                                         facecolor=color))#, edgecolor='k'))

        # figura de amplitudes:
        alto1 = np.diff(altos1)[rr]
        xi1 = 0.06
        axs1[0].text(xi1+1.25*ancho, altos1[rr]+alto1/2.5, f'{radio:.0f}', fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')
        axs1[0].add_patch(
            matplotlib.patches.Rectangle(xy=(xi1,  altos1[rr]),
                                          width=ancho, height=alto1,
                                          facecolor=color))#, edgecolor='k'))
    else:
        axs[0].text(xi+0.5*ancho, yi*1.02, r'Radius ($\mu$m)', fontsize=15,
                horizontalalignment='center',
                verticalalignment='center')
        axs1[0].text(xi1+1*ancho, altos1[rr]*1.2, r'Radius ($\mu$m)', fontsize=15,
                horizontalalignment='center',
                verticalalignment='center')

    yi += alto
    yi1 += alto1
##################### leyenda voxelsize:
ax = axs[0]
# access legend objects automatically created from data
handles, labels = ax.get_legend_handles_labels()
# where some data has already been plotted to ax
handles, labels = ax.get_legend_handles_labels()
# handles is a list, so append manual patch
# plot the legend
ax.legend(handles=handles, frameon=False, fontsize=14,
          loc="upper right")#, bbox_to_anchor=(0.8,1),
          #title=r"Voxel width ($\mu$m)", title_fontsize=15)

########## Leyenda altura:
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
    fig.savefig(f"{path0}/{filename}.eps", format='eps',bbox_inches='tight')

    fig1.savefig(f"{path0}/Amplitud_vs_density.png", format='png', bbox_inches='tight')
    fig1.savefig(f"{path0}/Amplitud_vs_density.eps", format='eps',bbox_inches='tight')


if savedata:
  df.to_csv(f'{path0}/datos.csv', index=False)    

#%%%
####### A PARTIR DE ACA VA LA INTERPOLACION 2D
interpolar2D = False
plot_3d = False


if interpolar2D:
    from scipy.interpolate import griddata

    x = df['densidad']
    y = df['radio']/df['altura']
    z = df['delta_mic']-df['delta_bulk']
    zmic = df['delta_mic']
    zbulk = df['delta_bulk']

    points = np.array([x,y]).T    

    grid_y, grid_x = np.meshgrid(np.linspace(min(y), max(y), 100),
                                 np.linspace(min(x), max(x), 100), indexing='ij')

    grid_z0 = griddata(points, z, (grid_x, grid_y), method='nearest')
    grid_z1 = griddata(points, z, (grid_x, grid_y), method='linear')
    grid_z2 = griddata(points, z, (grid_x, grid_y), method='cubic')

    fig, axs = plt.subplots(1,2, num=78621)    
    vmin = min(z)
    vmax = max(z)
    ax = axs[0]
    ax.pcolormesh(grid_x, grid_y, grid_z0, vmin=vmin, vmax=vmax)
    ax.scatter(points[:, 0], points[:, 1], c=z, s=200, edgecolor='k',
                vmin=vmin, vmax=vmax)   # data
    ax.set_title('interpolacion 2D: Nearest')
    ax.set_ylabel("r/h")
    ax.set_xlabel(r"$\rho$")
    ax = axs[1]
    ax.pcolormesh(grid_x, grid_y, grid_z1, vmin=vmin, vmax=vmax)
    ax.scatter(points[:, 0], points[:, 1], c=z, s=200, edgecolor='k',
                vmin=vmin, vmax=vmax)   # data
    ax.set_title('interpolacion 2D: Linear')
    ax.set_ylabel("r/h")
    ax.set_xlabel(r"$\rho$")
    
      
    metodo = 'nearest' # 'linear0, 'cubic'
    fig, axs = plt.subplots(1,3, num=78622)    
    ax = axs[0]    
    grid_z2 = griddata(points, z, (grid_x, grid_y), method=metodo)
    vmin = min(z)
    vmax = max(z)    
    ax.pcolormesh(grid_x, grid_y, grid_z2, vmin=vmin, vmax=vmax)
    ax.scatter(points[:, 0], points[:, 1], c=z, s=200, edgecolor='k',
                vmin=vmin, vmax=vmax)   # data    
    ax.set_title(r'interpolacion 2D: $\Delta\delta$')
    ax.set_ylabel("r/h")
    ax.set_xlabel(r"$\rho$")
    #--------------
    ax = axs[1]
    vmin = min(zmic)
    vmax = max(zmic)
    grid_z2_mic = griddata(points, zmic, (grid_x, grid_y), method=metodo)
    ax.pcolormesh(grid_x, grid_y, grid_z2_mic, vmin=vmin, vmax=vmax)
    ax.scatter(points[:, 0], points[:, 1], c=zmic, s=200, edgecolor='k',
                vmin=vmin, vmax=vmax)   # data
    ax.set_title(r'interpolacion 2D: $\delta_{mic}$')
    ax.set_ylabel("r/h")
    ax.set_xlabel(r"$\rho$")
    #--------------
    ax = axs[2]
    vmin = min(zbulk)
    vmax = max(zbulk)
    grid_z2_bulk = griddata(points, zbulk, (grid_x, grid_y), method=metodo)
    ax.pcolormesh(grid_x, grid_y, grid_z2_bulk, vmin=vmin, vmax=vmax)
    ax.scatter(points[:, 0], points[:, 1], c=zbulk, s=200, edgecolor='k',
                vmin=vmin, vmax=vmax)   # data
    ax.set_title(r'interpolacion 2D: $\delta_{bulk}$')
    ax.set_ylabel("r/h")
    ax.set_xlabel(r"$\rho$")

    if plot_3d:
        from mpl_toolkits import mplot3d

        # Creating dataset
        x = grid_x
        y = grid_y
        z = grid_z1

        # Creating figure
        fig = plt.figure(num=4566876, figsize =(14, 9))
        ax = plt.axes(projection ='3d')

        # Creating plot
        ax.plot_surface(x, y, z, cmap = 'viridis')
        ax.set_ylabel("r/h")
        ax.set_xlabel(r"$\rho$")
