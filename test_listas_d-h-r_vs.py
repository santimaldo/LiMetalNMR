# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 15:06:45 2022

@author: santi
"""

import numpy as np
import matplotlib.pyplot as plt
from Modules.SimulationVolume import *


def get_param_a(d):
  if d>512:
    return 0
  else:    
    # distancias, parametros_a, errores relativos
    Ds, As, Es = np.loadtxt('./DataBases/Hexagonal_parametro_a.dat').T
    a = As[Ds==d][0]
    return a
    
skdp = 14 # um
# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
VSs = [0.125, 0.25, 0.5, 1] # um


# todo en micrometros
radios = [0.05,1,2,5,10,20,50]
rho_target = np.linspace(0.1,0.9,9) # densidades buscadas
alturas = [10, 50]


Nx = 1024
Ny = 1024

parametros_que_NO = []
parametros_que_SI = []
densidades = []
distanciasSI= []
radiosSI= []
Nceldasx =[]
Nceldasy =[]

for vs in VSs:
    voxelSize = [vs*1e-3]*3# mm
    vsz,vsy,vsx = voxelSize
    
    for radio in radios:
      print (f"========== radio {radio} um ")
      for rho in rho_target:    
        # distancias vs radio para una densidad deseada (cilindros arreglo hexag.):
        distancia = np.sqrt(2*np.pi*radio**2/rho/np.sqrt(3)) 
        print (f"------ radio: {radio} um, rho: {rho:.2f}")
        d = round(distancia/vs)
        r = int(radio/vs)  
        
        intentos = 0; d0=d;success=False
        fail = True
        while intentos<4 and fail:
            print(f" intento {intentos}, d = {d}")                   
            if r>(d/2-1):
              #  debe haber espacio vacio entre los cilindros 
              msj = 'r>d/2-1'
              parametros_que_NO.append([distancia, radio, vs, msj])          
              fail = True
            elif d>int(Nx/2) or d>int(Ny/2):
              #  No habra espacio para una celda unidad
              msj = 'd es muy grande, la celda unidad no entra en el FOVxy'
              parametros_que_NO.append([distancia, radio, vs, msj])          
              fail = True
            elif d<8:
              #  el error en el parametro a es muy grande para distancias menores a
              # 8 voxels
              msj = 'd es muy chico'
              parametros_que_NO.append([distancia, radio, vs, msj])          
              fail = True
            elif d%2!=0:
              # d debe ser par
              msj = 'd es impar'
              parametros_que_NO.append([distancia, radio, vs, msj])          
              fail = True
            else:             
                 print(f"radio={radio}, rho:{rho}, success! intentos:{intentos}")
                 fail = False
            # si fallo en alguno:
            if fail:
                intentos += 1
                d = d0 + (-1)**intentos * (intentos//2 + 1)
        # si luego de intentar 4 veces no lo logra, pasa al siguiente d.
        if fail:
            continue
        
        
        # Una vez pasados esos filtros, me fijo en otras cosas
        a = get_param_a(d)
        # calculo numero de celdas
        Ncx = (Nx/2)//d   # // es division entera en python3  (floor)
        Ncy = (Ny/2)//(2*a)
            
        if Ncx*Ncy<3:
          # exigo un minimo de 2 celdas unidad en cada direccion
          msj = 'Hay pocas celdas unidad, el vs es muy chico'
          parametros_que_NO.append([distancia, radio, vs, msj])
          continue
        else:              
          # ARMO UNA CELDA UNIDAD PARA CALCULAR LA DENSIDAD
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
          densidades.append(densidad)
          distanciasSI.append(distancia)
          radiosSI.append(radio)
          Nceldasx.append(Ncx)
          Nceldasy.append(Ncy)
          
          # print(f"&%$&#%$&#&# ---> {rho}, {densidad}")
          # una vez que llegamos aca, estamos en condiciones de evaluar altura:
          for altura in alturas:              
              h = int(altura/vs)
              Nz = 512
              if (Nz/2 < h) or (Nz/2*vs < 3*skdp):
                  Nz = Nz*2                
              msj = f'distancia efectiva: {d*vs} um, radio ef.: {r*vs}, densidad ef.: {densidad:.2f}'
              parametros_que_SI.append([vs, Nz, Nx,
                                        altura, radio, distancia,
                                        h*vs, r*vs, d*vs,
                                        densidad, msj])

# pNO = len(parametros_que_NO)
# pSI = len(parametros_que_SI)

# print(f'fueron rechazados {pNO} conjuntos de parametros, se aceptaron {pSI} conjuntos de parametros')

#%%
# duplicados ------------------------------------------------------------------
# chequeo distancias (par[6]),radios (par[7]) y alturas (par[8]) duplicados
mylist = [[par[0], par[1], par[6], par[7], par[8], par[9]]
          for par in parametros_que_SI]
newlist = []
duplist = []
for i in mylist:
    if i not in newlist:
        newlist.append(i)
    else:
        duplist.append(i)
parametros = newlist
#------------------------------------------------------------------------------

filename = "./DataBases/ParametrosASimular.dat"
with open(filename, 'w') as f:
    header = f"# voxelSize\t Nz\t altura(um)\t radio(um)\t distancia (um)\t densidad\n"
    f.write(header)
    for par in parametros:        
        vs, Nz, altura, radio, distancia, densidad = par
        line = f"{vs:.4f}\t{Nz}\t{altura:.4f}\t{radio:.4f}\t{distancia:.4f}\t{densidad:.4f}\n"
        f.write(line)
        
        
#%%      

vs, Nz, h, r, d, rho = np.loadtxt(filename).T

fig, ax = plt.subplots(num=11111212111)
cb = ax.scatter(rho, d, c=r, s=vs*100, cmap="jet")
# ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("densidad")
ax.set_ylabel("distancia (um)")
fig.colorbar(cb, label="Radios")
