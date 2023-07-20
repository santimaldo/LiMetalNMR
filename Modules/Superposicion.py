#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 14:04:31 2020

@author: santi
"""


import numpy as np
import scipy.ndimage as ndimage
from scipy.interpolate import interp1d
from Modules.Funciones import timerClass
import warnings

@timerClass
class Superposicion(object):
  """
  Esta clase representa la superposicion de los deltas bulk y microestructuras

  INPUTS:
    muestra : objeto de la clase Muestra.
    delta   : objeto de la clase Duestra.

  ATRIBUTOS
  + muestra   : Muestra()   -  el objeto clase Muestra definido en el main
  + delta     : Delta()     -  el objeto clase Delta definido en el main
  + delta_in  : float       -  Al bulk lo aproximamos como una funcion esaclon.
                              delta_in es el valor de delta dentro de la lamina
                              de litio bulk
  + delta_out : float       -  Al bulk lo aproximamos como una funcion esaclon.
                              delta_out es el valor de delta fuera de la lamina
                              de litio bulk

  + z0        : int         - el indice en la direccion z en la cual comienzan
                              las dendritas. z0-1 es el ultimo indice donde hay
                              bulk. Por defecto es 60um,
  + slice     : list        - [[zi,zf], [yi,yf], [xi,xf]] Entre estos valores
                              recorto la matriz de volumen para definir el
                              volumen en cual hago la superposicion.

  + muestra_sup : array     - superposicion de la muestra (las dendritas), con
                              el bulk. Es decir, lleno de litio todo el volumen
                              hasta z0-1


  + delta_bulk : array      - Matriz con valores de delta generados por el bulk,
                              es decir, la funcion escalon en z:
                                delta_in  para 0  <  z  <=  z0-1
                                delta_out para z0 <= z
  + delta_muestra : array   - Matriz con los valores de delta generados por las
                              dendritas.

  + self.delta_sup : array  - Matriz con el delta superpuesto
                                  delta_sup = delta_bulk + delta_muestra

  + radio   :  float        - Para superponer con un perfil y no una funcion
                              escalon, debo decirle que perfil usar. Para ello,
                              le digo a que radio (o distancia al centro) se 
                              encuentra. Esto es porque los perfiles se
                              obtuvieron en un electrodo disco.
                              El radio esta expresado en MICROMETROS
                              Por defecto es None, con lo cual el delta_bulk es
                              una funcion escalon
  """

  def __init__(self, muestra, delta, delta_in=-12.79, delta_out=3.27,
               z0=None, skdp=14e-3, radio=None, superposicion_lateral=False,
               superposicion=True):
    
    self.muestra = muestra
    self.delta = delta
    self.delta_in = delta_in
    self.delta_out = delta_out
    # el nuevo valor de indice en z en el cual empiezan las dendritas:
    # [0:z0,:,:] --> bulk
    # [z0: ,:,:] --> dendritas
    
    if z0==None:
        # z0 = Nz - Nmz - Nvx_seguridad
        # las dendritas arrancan cerca de la mitad del FOV.
        z0 = int(7*skdp/self.muestra.voxelSize[0])
    
    if z0*self.muestra.voxelSize[0]/skdp < 3:
        
        msg = f"No hay suficiente FOVz para el bulk:\n"\
              f"\t bulk = {z0*self.muestra.voxelSize[0]*1000} um "\
              f"< 3 * skdp = {3*skdp*1000} um"
        # raise Exception(msg)
        warnings.warn(mensaje, DeprecationWarning, stacklevel=2)
        
    self.z0 = z0 # z0 en unidades de voexel
    self.slice = None
    self.definir_slice()

    self.muestra_sup = None
    self.delta_bulk = None
    self.delta_muestra = None
    
    self.checkpoint = False  # esta variable se prende solo se produce una superposicion
    
    if superposicion: # esto esta por si quiero el espectro de la muestra ya armada
      self.superponer_muestra()    
      self.crear_delta_bulk(radio)
      self.crear_delta_muestra()        
      if superposicion_lateral:
        self.superponer_laterales()
        self.superponer_laterales_muestra()
      
      self.delta_sup =  self.delta_bulk + self.delta_muestra
    
    else:
      self.muestra_sup = muestra.muestra/muestra.chi
      self.delta_sup = delta.delta
      
    
    
    
  #--- Metodos -------------------------------------------------------------------
  def definir_slice(self):
    """
    Este metodo es para definir donde cortar la matriz del volumen y de delta.
    """
    slz,sly,slx = self.muestra.slices
    vsz,vsy,vsx = self.muestra.voxelSize
    slz0 = slz[0] - self.z0
    if slz0 < 0:
      print('WARNING!!!!!  puede que haya poca profundidad de bulk ! ')
      print('     z0 pasa de {}um a -----> {} um'.format(self.z0*vsz*1e3, slz[0]*vsz*1e3))
      self.z0 = slz[0]
      slz0 = 0
    slz1 = slz[1]
    sly0 = 0
    sly1 = self.muestra.N[1]
    slx0 = 0
    slx1 = self.muestra.N[2]
    self.slice = [[slz0,slz1],[sly0,sly1],[slx0,slx1]]
    return 0

  #-------------------------------------------------------------------------------
  def superponer_muestra(self):
    """
    Toma la matriz de la muestra, crea el volumen entero
    y le agraga el bulk en la parte de abajo
    """
    slz,sly,slx = self.slice
    obj = self.muestra.construir_volumen()/self.muestra.chi
    # recorto el volumen
    obj = obj[slz[0]:slz[1], sly[0]:sly[1], slx[0]:slx[1]]
    # lleno al objeto de 1 en todos los lugaras HASTA z0 (exclusivo)
    obj[0:self.z0,:,:] = 1
    self.muestra_sup = obj
    self.checkpoint = True
    return 0

  #-------------------------------------------------------------------------------
  def crear_delta_bulk(self, radio):
    """
    Crea el delta bulk siguiendo el perfil de perturbacion del cambo simulado
    con menor resolucion. Para ello se toman dos perfiles, in y out, y se colocan
    en la matriz delta_bulk hasta z0 (in) y desde z0 hasta el final (out).
    En caso de que se requiera una funcion escalon, el parametro radio debe
    ser None
    """
    # defino el z donde arranca la muestra
    z0 = self.z0
    # lleno al objeto de delta_in en todos los lugaras HASTA z0 (exclusivo)
    # y de delta_out desde z0 en adelante
    delta_bulk = np.zeros_like(self.muestra_sup)
    
    if radio is None:
      delta_bulk[0:z0,:,:] = self.delta_in
      delta_bulk[z0: ,:,:] = self.delta_out
      self.delta_bulk = delta_bulk    
      print("--- delta_muestra es una FUNCION ESCALON")
    
    else:
      path = './DataBases/Bulk_perfiles/'
      archivo = path + 'perfil_radio{:04d}.{}'
      # leo el perfil:
      z_in, delta_in = np.loadtxt(archivo.format(radio,'in')).T
      z_out, delta_out = np.loadtxt(archivo.format(radio,'out')).T
      # chequeo que los z de los perfiles esten bien hechos
      readme = ' Ver ./DataBases/Bulk_perfiles/readme.md'
      if z_out[0]!=0 or z_in[0]!=0:
        msg = 'ERROR! Los perfiles deben comenzar desde z=0.{}'.format(readme)
        raise Exception(msg)
      elif any(z_in>0):
        msg = 'ERROR! El perfiles IN debe tener valores negativos de z.{}'.format(readme)                
        raise Exception(msg)
      # defino algunas variables utiles
      vsz,vsy,vsx = self.muestra.voxelSize #voxelSize de la muestra
      VS = z_out[1]
      Nin = z0
      Nout = delta_bulk.shape[0] - z0      
      zMAX = Nout * vsz
      zMIN = - Nin * vsz      
      # recorto los perfiles, para no hacer una interpolacion tan larga
      delta_in  =  delta_in[z_in  >= (zMIN-VS)]
      delta_out = delta_out[z_out <= (zMAX+VS)]
      z_in  =  z_in[z_in   >= (zMIN-VS)]
      z_out = z_out[z_out  <= (zMAX+VS)]      
      # print(VS)
      # print(z_in)
      # print(z_out)
      # INTERPOLACION            
      try: 
        # la cubica no funciona cuando hay solo dos puntos. Por lo tanto,
        # esto puede fallar cuando VS del perfil es muy grande
        din  = interp1d(z_in , delta_in, 'cubic')
      except:      
        din  = interp1d(z_in , delta_in)
      try:
        dout = interp1d(z_out, delta_out, 'cubic')
      except:  
        dout = interp1d(z_out, delta_out)         
      # CREO EL DELTA MUESTRA:
      # El reshape es para poder multiplicar el vector con la matriz
      # recordar que el delta se cuenta desde la superficie! por eso se da vuelta
      # con el slicing [::-1]
      zout= np.arange(0,Nout)*vsz
      zin = np.arange(0,Nin)* (-vsz)
      delta_bulk[0:z0,:,:] = din(zin)[::-1].reshape(Nin,1,1)
      delta_bulk[z0: ,:,:] = dout(zout).reshape(Nout,1,1)
      self.delta_bulk = delta_bulk
      print("--- delta_muestra es un PERFIL")
      
    return 0
  #-------------------------------------------------------------------------------
  def crear_delta_muestra(self):
    """
    Crea el delta muestra recortando el delta, usando muestra.slices,
    agregando los extras
    """
    slz,sly,slx = self.slice
    delta_muestra = self.delta.delta[slz[0]:slz[1], sly[0]:sly[1], slx[0]:slx[1]]
    self.delta_muestra = delta_muestra
    return 0
  #-------------------------------------------------------------------------------
  
  def superponer_laterales(self):
    # redimensiono para poder usar roll y se se "simetrice"  
    Nmy = self.muestra.N_muestra[1]
    Nmx = self.muestra.N_muestra[2]
    
    # y - - - - - - - - - - - - - - - - - - - - - 
    sly = int( (self.muestra.N[1] - 2*Nmy) / 2)
    ini_y=sly
    if sly!=0:
      fin_y = -sly
    else:
      fin_y = self.muestra.N[1]
    # x - - - - - - - - - - - - - - - - - - - - - 
    slx = int( (self.muestra.N[2] - 2*Nmx) / 2)
    ini_x=slx
    if slx!=0:
      fin_x = -slx
    else:
      fin_x = self.muestra.N[2]
    #   - - - - - - - - - - - - - - - - - - - - - 
    delta0 = self.delta_muestra
    # ahora voy sumando los corrimientos:
    # corro en y (tengo que redimensionar)
    delta1 = np.zeros_like(delta0)
    delta1[:,ini_y:fin_y,:] = np.roll(delta0[:,ini_y:fin_y,:], Nmy, axis=1)
    # corro en x
    delta2 = np.zeros_like(delta0)
    delta2[:,:,ini_x:fin_x]  = np.roll(delta0[:,:,ini_x:fin_x]+delta1[:,:,ini_x:fin_x] , Nmx, axis=2)
    
    ## para chequear si va bien
    # import matplotlib.pyplot as plt
    # vmax = 0.7*np.max(np.abs(delta0))
    # plt.figure(5000)
    # zz = 120
    # plt.subplot(2,2,1)
    # plt.pcolormesh(delta0[zz,:,:], cmap='seismic', vmin=-vmax, vmax=vmax)
    # plt.subplot(2,2,2)
    # plt.pcolormesh(delta1[zz,:,:], cmap='seismic', vmin=-vmax, vmax=vmax)
    # plt.subplot(2,2,3)
    # plt.pcolormesh(delta2[zz,:,:], cmap='seismic', vmin=-vmax, vmax=vmax)
    # plt.subplot(2,2,4)
    # plt.pcolormesh(delta0[zz,:,:]+delta1[64,:,:]+delta2[64,:,:], cmap='seismic', vmin=-vmax, vmax=vmax)
    
    
    self.delta_muestra = delta0 + delta1 + delta2 
    return 0
  #-------------------------------------------------------------------------------
  def superponer_laterales_muestra(self):
    # redimensiono para poder usar roll y se se "simetrice"  
    z0 = self.z0
    Nmy = self.muestra.N_muestra[1]
    Nmx = self.muestra.N_muestra[2]
    
    # y - - - - - - - - - - - - - - - - - - - - - 
    sly = int( (self.muestra.N[1] - 2*Nmy) / 2)
    ini_y=sly
    if sly!=0:
      fin_y = -sly
    else:
      fin_y = self.muestra.N[1]
    # x - - - - - - - - - - - - - - - - - - - - - 
    slx = int( (self.muestra.N[2] - 2*Nmx) / 2)
    ini_x=slx
    if slx!=0:
      fin_x = -slx
    else:
      fin_x = self.muestra.N[2]
    #   - - - - - - - - - - - - - - - - - - - - - 
    muestra0 = self.muestra_sup
    # debo quitar el bulk para hacer la superposicion lateral:
    muestra0[:z0,:,:] = 0
    # ahora voy sumando los corrimientos:
    # corro en y (tengo que redimensionar)
    muestra1 = np.zeros_like(muestra0)
    muestra1[:,ini_y:fin_y,:] = np.roll(muestra0[:,ini_y:fin_y,:], Nmy, axis=1)
    # corro en x
    muestra2 = np.zeros_like(muestra0)
    muestra2[:,:,ini_x:fin_x]  = np.roll(muestra0[:,:,ini_x:fin_x]+muestra1[:,:,ini_x:fin_x] , Nmx, axis=2)
    

    muestra_sup_lateral = muestra0 + muestra1 + muestra2    
    # agrego bulk:
    muestra_sup_lateral[:z0,:,:] = 1
    
    self.muestra_sup = muestra_sup_lateral
    return muestra_sup_lateral


  
  #-------------------------------------------------------------------------------
  def areas(self):
    """
    calculos las areas (2D) "solo bulk", y "con dendritas". Ojo, no es el area
    total de bulk, ya que existe bulk entre las dendritas. Es solo como para tener
    una idea orientativa. Tampoco es la superficie total, solo el area de litio
    cubierta
    """
    vs = self.muestra.voxelSize
    N = self.muestra.N
    Nm = self.muestra.N_muestra

    area_total =  N[1]*vs[1] * N[0]*vs[0]
    self.area_dendritas = Nm[1]*vs[1] * Nm[0]*vs[0]
    self.area_bulk = area_total - self.area_dendritas

    #print('area_bulk/area_dendritas = %.2f'%(self.area_bulk/self.area_dendritas))
    return self.area_bulk/self.area_dendritas
  
  #-------------------------------------------------------------------------------
  # getters:
  #-------------------------------------------------------------------------------
  def get_delta_dendritas(self):
    """
    metodo que devuelve una matriz con los valores de delta, solo en la region
    de la muestra, es decir, las dendritas
    """
    delta_muestra = self.delta_sens[self.z0:,:,:] # dendritas
    return delta_muestra
  #-------------------------------------------------------------------------------
  def get_delta_bulk(self):
    """
    metodo que devuelve una matriz con los valores de delta, solo en la region
    de la muestra
    """
    delta_bulk = self.delta_sens[0:self.z0,:,:] # bulk
    return delta_bulk
  #-------------------------------------------------------------------------------
