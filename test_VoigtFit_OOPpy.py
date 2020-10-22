# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:37:40 2019

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
from VoigtFit import *



# directorio de datos
archivo = 'spec_N16_k1.0.dat'
#archivo = 'spec_single_pulse.dat'
carpeta= 'a10_p20'
path = "/home/santi/CuarenteDoctorado/LiMetal/simulaciones/2020-10-14_SMC_y_espectro/dendritas_porcentaje/espectros/{}/".format(carpeta)

datos = np.loadtxt(path+archivo)

ppmAxis0 = datos[:,0]
spec = datos[:,1]

# retoco:
ppmAxis = ppmAxis0
spec = spec - spec[0]
ventana = 200
ppmAxis = ppmAxis0[np.abs(246-ppmAxis0)<ventana]
spec = spec[np.abs(246-ppmAxis0)<ventana]



Npicos = 2
#vf = VoigtFit(ppmAxis,spec, Npicos=2, center=[246,252], fijar=['m2_center'])
vf = VoigtFit(ppmAxis,spec, Npicos=Npicos, center=[246,260])
#vf = VoigtFit(ppmAxis,spec, Npicos=Npicos, center=[246,260,250])
ajuste, componentes = vf.componentes(ppmAxis)


plt.figure(1231)
plt.plot(ppmAxis,spec)
plt.plot(ppmAxis, ajuste, 'k')
for comp in componentes:
    plt.plot(ppmAxis, comp, '--')


params = vf.params
vf = VoigtFit(ppmAxis,spec, Npicos=Npicos, params=params)
ajuste, componentes = vf.componentes(ppmAxis)

#%%
col =  ['b','r','g']
col =  ['r','b','g']
plt.figure(1232)
plt.plot(ppmAxis,spec,'k',  linewidth=3)
#plt.plot(ppmAxis, ajuste)
plt.yticks([])
n=0
for comp in componentes:    
#    plt.plot(ppmAxis, comp, col[n], linewidth=3)
    n+=1
plt.xlim([350,150])    
plt.xlabel(r"$^7$Li Chemical Shift [ppm]")

##%%
#plt.figure(1233)
#plt.plot(ppmAxis,spec)
#plt.plot(ppmAxis, componentes[2], '--')
#plt.plot(ppmAxis, componentes[0], '--')
#plt.plot(ppmAxis, componentes[2]+componentes[1], '--')

plt.show()