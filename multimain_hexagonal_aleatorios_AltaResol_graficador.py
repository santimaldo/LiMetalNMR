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

Niteraciones=20

nn = 0
data_dir0 = "2023-07-20_Cilindros_hexagonal_AltaResolucion"
data_dir45 = "2023-08-07_Cilindros_45grados_hexagonal_AltaResolucion"
data_dir = "2023-08-02_Cilindros_aleatorios_hexagonal_AltaResolucion"

path0 = f"./Outputs/{data_dir0}/"
path45 = f"./Outputs/{data_dir45}/"
path = f"./Outputs/{data_dir}/"
distancias, radios, alturas, vss, densidades, densidades_volumetricas = np.loadtxt(path+'Densidades.dat').T

Ndens = 7 # cuantos valores de densidad apunte
for ii in range(Ndens):    
    # path=path0+'SMC64-k1/iteracion{:d}/'.format(jj)
    h = alturas[ii]
    d = distancias[ii]
    r = radios[ii]
    p = densidades[ii]    
    vs = vss[ii]

    regiones = ['-microestructuras', '-bulk']
    col = ['k', 'r', 'b']

    for nn_iter in range(Niteraciones+2):
        
        if nn_iter < Niteraciones:
            pv = densidades_volumetricas[nn_iter*Ndens+ii]        
            Niter = f'niter{nn_iter}_'
            directorio = path            
        elif nn_iter == Niteraciones:
            # CILINDROS RECTOS
            Niter = ''
            directorio = path0
        elif nn_iter == Niteraciones+1:
            # CILINDROS A 45 GRADOS
            Niter = ''
            directorio = path45
        n_r = -1
        for region in regiones:
            n_r += 1        
            archivo = 'h{:d}_r{:.2f}_d{:.2f}_vs{:.3f}um_{}SP{}.dat'.format(
                int(h), r, d, vs, Niter, region)
    
            # extraigo
            try:                
                datos = np.loadtxt(f"{directorio}SP/{archivo}")                
                if n_r == 0:
                    alturas_t.append(h)
                    distancias_t.append(d)
                    radios_t.append(r)
                    densidades_t.append(p)
                    densidades_vol_t.append(pv)
                    vss_t.append(vs)
                    Niter_t.append(nn_iter)                    
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
                           densidades_t, densidades_vol_t, distancias_t, vss_t,
                           delta_mic, delta_bulk, amp_mic, amp_bulk,
                           np.around(densidades_t, decimals=1), Niter_t)),
                  columns= ['altura', 'radio', 'densidad', 
                            'densidad_volumetrica', 'distancia', 'vs',
                            'delta_mic', 'delta_bulk', 'amp_mic', 'amp_bulk',
                            'densidad_nominal', 'Niter'])



amp_rel = amp_mic/amp_bulk
corrimientos = delta_mic-delta_bulk

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

savedata = True # para guardar los dataframes
# paa guardar figuras:
filename = False # si esto es falos, no se guarda la figura
# filename = "RandomOrientations"
plot_Deltadelta = True
# con esto utilizo solo el menor voxelsize para cada par (radio, densidad)
# eje_x = data['distancia'] - 2*data['radio']        



# cilindros rectos:
data = df[df['Niter']==Niteraciones]
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
#-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  

# cilindros A 45 GRADOS:
data = df[df['Niter']==Niteraciones+1]
data = data.sort_values(by='densidad', ascending=True)
eje_x = data['densidad']             
ax = axs
if plot_Deltadelta:
    eje_y = data['delta_mic']-data['delta_bulk']
else:
    eje_y = data['delta_mic']
    
label = r"$45^{\circ}$ cylinders"
ax.plot(eje_x, eje_y, 'o', color='gray', lw=2, ms=ms, label=label)

coef = np.polyfit(eje_x,eje_y,1)
linear_fit= np.poly1d(coef) 
ax.plot(eje_x, linear_fit(eje_x), '--', color='gray', lw=1)# marker=marker,

#-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
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
    ax.set_ylim([4, 22])            
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

  rectos = df[df['Niter']==Niteraciones].drop(columns="densidad_volumetrica")
  rectos.to_csv(f'{path0}/datos.csv', index=False)    
  
  inclinados = df[df['Niter']==Niteraciones+1].drop(columns="densidad_volumetrica")
  inclinados.to_csv(f'{path45}/datos.csv', index=False)

  random = df[df['Niter']<Niteraciones]
  random.to_csv(f'{path}/datos.csv', index=False)        

#%%%
####### A PARTIR DE ACA VA LA INTERPOLACION 2D
interpolar2D = True
plot_3d = True


if interpolar2D:
    from scipy.interpolate import griddata
    
    x = df['densidad']
    y = df['radio']/df['altura']
    z = df['delta_mic']-df['delta_bulk']
    
    points = np.array([x,y]).T
    values = df['delta_mic']-df['delta_bulk']
    
    grid_y, grid_x = np.meshgrid(np.linspace(min(y), max(y), 100),
                                 np.linspace(min(x), max(x), 100), indexing='ij')
    
    grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
    grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
    grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')
    
    
    
    fig, axs = plt.subplots(1,2, num=78621)
    plt.subplot(121)
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
