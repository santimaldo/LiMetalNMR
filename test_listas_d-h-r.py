# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 15:06:45 2022

@author: santi
"""

import numpy as np
import matplotlib.pyplot as plt
from Modules.SimulationVolume import *
from Modules.Muestra import *
from Modules.Delta import *
from Modules.Superposicion import *
from Modules.Graficador import *
from Modules.Medicion import *


def get_param_a(d):
  if d>512:
    return 0
  else:    
    # distancias, parametros_a, errores relativos
    Ds, As, Es = np.loadtxt('./DataBases/Hexagonal_parametro_a.dat').T
    a = As[Ds==d][0]
    return a

    
    
# recordar que la convencion de python es {z,y,x}
# elijo el tamaño de voxels de forma tal que la lamina quepa justo en el
# volumen simulado.
vs = 0.1 # um
voxelSize = [vs*1e-3]*3# mm
vsz,vsy,vsx = voxelSize


# todo en micrometros
VSs = np.arange(1,11)*0.01
radios = [0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.5,0.8,1,2,5]
distancias= [0.2,0.3,0.5,0.8,1,2,3,4,5,10]
Nx = 512
Ny = 512

parametros_que_NO = []
parametros_que_SI = []
densidades = []
distanciasSI= []
radiosSI= []
Nceldasx =[]
Nceldasy =[]

for distancia in distancias:
  for radio in radios:
    ya_use_este_radio = False
    for vs in VSs:
      d = round(distancia/vs)
      r = int(radio/vs)
      if ya_use_este_radio:
        #  debe haber espacio vacio entre los cilindros 
        msj = 'radio ya usado con menorvs'
        parametros_que_NO.append([distancia, radio, vs, msj])        
        continue
      if radio<vs:
        #  debe haber espacio vacio entre los cilindros 
        msj = 'radio<vs'
        parametros_que_NO.append([distancia, radio, vs, msj])        
        continue
      if r>(d/2-1):
        #  debe haber espacio vacio entre los cilindros 
        msj = 'r>d/2-1'
        parametros_que_NO.append([distancia, radio, vs, msj])
        continue
      elif d>int(Nx/2) or d>int(Ny/2):
        #  No habra espacio para una celda unidad
        msj = 'd es muy grande, la celda unidad no entra'
        parametros_que_NO.append([distancia, radio, vs, msj])
        continue
      elif d<20:
        #  No habra espacio para una celda unidad
        msj = 'd es muy chico'
        parametros_que_NO.append([distancia, radio, vs, msj])
        continue
      elif d%2!=0:
        # d debe ser par
        msj = 'd es impar'
        parametros_que_NO.append([distancia, radio, vs, msj])
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
        msj = f'distancia efectiva: {d*vs} um, radio efectivo {r*vs}'
        parametros_que_SI.append([distancia, radio, vs, d*vs, r*vs, msj])
        ya_use_este_radio = True
        
        
        # h = round(5/vs)
        # vsz = vsx = vsy = vs*1e-3      
        # voxelSize = [vsz,vsy,vsz]
        # N = [256,Ny,Nx]        
        # volumen = SimulationVolume(voxelSize=voxelSize, N=N)
        # a = get_param_a(d)             
        
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

        


pNO = len(parametros_que_NO)
pSI = len(parametros_que_SI)

print(f'fueron rechazados {pNO} conjuntos de parametros, se aceptaron {pSI} conjuntos de parametros')