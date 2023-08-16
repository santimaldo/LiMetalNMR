#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 13:54:04 2020

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import scipy.ndimage as ndimage
import os.path as path
import Modules.Export3D as Export3D
from Modules.Funciones import timer
from Modules.Funciones import timerClass
import time


@timerClass
class Medicion(object):
    """
    Esta clase representa a la medicion. Contiene el delta y la superposicion de la muestra, de las
    cuales obtiene la cantidad de senal de acuerdo a la secuencia utilizada

    INPUTS:
        . superposicion : Superposicion()
      Opcionales:
        . secuencia     : string       - opciones: 'SP', 'SMC'
        . k             : float
        . stl_file      : strig        - Nombre del archivo que en el que se desea
                                         guardar una figura 3D '.stl'. Si no se da
                                         este argumento, la figura 3D no se exporta.
                                         Estos archivos se guardan en el directorio
                                         'Outputs'.
                                         IMPORTANTE: no poner la extension '.stl'
                                         ya que se pone automaticamente.
                                           Ej: stl_file = 'cilindros/ancho16'
                                         El archivo guardado es:
                                           ~/Outputs/cilindros/ancho16.stl
                                         La carpeta 'cilindros' debe ser creada
                                         previamente.
        . borde_a_quitar : array-like(3) - Numero de voxels del borde que no deben
                                          aportar al volumen sensible.
                                          En el caso de z, solo se quitan del 
                                          borde superior.
                                          [borde_z, borde_y, borde_x]
      NO-IMPLEMENTADO: Argumentos con palabras clave que dependen de la secuencia (**seqkwargs)

      '

    ATRIBUTOS
    + superposicion  : Superposicion()  - el objeto clase Superposicion definido
                                          en el main. Contiene las microestructu
                                          ras superpuestas con el bulk.

    + secuencia      : string           - el nombre de la secuencia a utilizar.
                                          Opciones:
                                            'SP' (por defecto) single pulse
                                            'SMC' slice microscopy of conductors

    + k              : float            - pulso de k*pi. en 'SP' es el pulso.
                                          en 'SMC' es el tren del pulsos

    + volumen_medido : np.array()       - array logico de True en la region que
                                         deseo obtener senal y False donde no.
                                         Se utiliza como una mascara.

    + histograma     : list (3 elems)   - [X,Y,H2D] Histograma 2D conteniendo la
                                          cantidad de voxels que tienen un mismo
                                          valor de eta (corrimiento respecto al B0,
                                          antes llamado delta) y el mismo valor
                                          de beta (es B1/B10, es decir, solo la
                                          exponencial que decae). X,Y son una
                                          meshgrid:
                                              X valores de  ETA
                                              Y valores de BETA

    + ppmAxis        : np.array()       - Eje de los ppms
    + spec           : np.array()       - Espectro. Es un array COMPLEJO
    """

    def __init__(self, superposicion, secuencia='SP', k=0.5,
                 borde_a_quitar=[0, 0, 0], skindepth=14e-3, stl_file=False,
                 volumen_medido='completo', **seqkwargs):

        self.superposicion = superposicion
        self.secuencia = secuencia
        self.skindepth = skindepth
        self.skdp = int(skindepth/self.superposicion.muestra.voxelSize[0])
        self.borde_a_quitar = borde_a_quitar

        
        self.volumen_medido = self.crear_volumen_medido(volumen_medido)
        ### creo las matrices de utilidad:        
        self.eta = self.Crear_eta()
        self.beta = self.Crear_beta()
        

        # creacion de histograma 2D
        self.histograma = None
        # self.CrearHistograma2D() ## el histograma sera creado en el espectro

        self.ppmAxis = None
        self.spec = None
        # el espectro no se crea por defecto. Hay que hacerlo
        # self.CearEspectro(k)

        if stl_file:  # si stl_file es un string, se evalua como True
            matriz = self.get_volumen_medido()
            archivo = stl_file
            Export3D.exportar_3D(matriz, archivo)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @timer
    def crear_volumen_medido(self, volumen_medido):
        """
        Este metodo sirve para determinar que region de la superposicion utilizamos
        para calcular la senal. El resultado es un array logico, de manera que se
        puede utilizar como mascara, o como slicer.
        Opciones:
          'centro' : un cilindro que ocupa solo el centro de la muestra, con un
                     diametro de la mitad del area xy en la que se crearon las
                     microestructuras. De esta forma, 'evitamos' los efectos de
                     borde
          'centro-microestructuras'
          'centro-bulk'
          'completo'
          'completo-microestructuras'
          'completo-bulk'      
          'sin-borde'
          'sin-borde-microestructuras'
          'sin-borde-bulk'
        """
        if 'muestra' in volumen_medido.lower():
            condicion = (np.ones_like(self.superposicion.muestra_sup) == 1)
            mask = np.zeros_like(condicion)
            slz, sly, slx = self.superposicion.muestra.slices
            mask[:, sly[0]:sly[1], slx[0]:slx[1]] = 1
            condicion = condicion*mask
        # -----------------------------------------centro
        elif 'centro' in volumen_medido.lower():
            # primero creo un sistema de coordenadas
            N = self.superposicion.muestra_sup.shape
            z = np.arange(N[0])-N[0]/2
            y = np.arange(N[1])-N[1]/2
            x = np.arange(N[2])-N[2]/2
            Z, Y, X = np.meshgrid(z, y, x, indexing='ij')
            # vamos a seleccionar un circulo cuyo diametro va a ser la mitad del tamaño
            # de la muestra (es decir, la region con microestructuras)
            condicion = (X/(N[2]/4))**2+(Y/(N[1]/4))**2 < 1
            # if 'microestructuras' in volumen_medido.lower(): # la comparacion es case insenstive
            #   z0 = self.superposicion.z0
            #   condicion[0:z0,:,:]=False
            # elif 'bulk' in volumen_medido.lower():
            #   z0 = self.superposicion.z0
            #   condicion[z0:,:,:]=False
        # -----------------------------------------completo
        elif 'completo' in volumen_medido.lower():
            # return Ellipsis
            condicion = (np.ones_like(self.superposicion.muestra_sup) == 1)
            # if 'microestructuras' in volumen_medido.lower(): # la comparacion es case insenstive
            #   z0 = self.superposicion.z0
            #   condicion[0:z0,:,:]=False
            # elif 'bulk' in volumen_medido.lower():
            #   z0 = self.superposicion.z0
            #   condicion[z0:,:,:]=False
        # -----------------------------------------quitando borde
        elif 'sin-borde' in volumen_medido.lower():
            condicion = (np.ones_like(self.superposicion.muestra_sup) == 1)
            # quito el borde

            # if 'microestructuras' in volumen_medido.lower(): # la comparacion es case insenstive
            #   z0 = self.superposicion.z0
            #   condicion[0:z0,:,:]=False
            # elif 'bulk' in volumen_medido.lower():
            #   z0 = self.superposicion.z0
            #   condicion[z0:,:,:]=False


        # -----------------------------------------------------------REGION
        if 'microestructuras' in volumen_medido.lower():  # la comparacion es case insenstive
            z0 = self.superposicion.z0
            condicion[0:z0, :, :] = False
        elif 'bulk' in volumen_medido.lower():
            z0 = self.superposicion.z0
            condicion[z0:, :, :] = False            
        # -----------------------------------------------------------------

        # -----------------------------------------------------------REGION
        if 'esfera' in volumen_medido.lower():  # la comparacion es case insenstive

            N = self.superposicion.muestra_sup.shape
            z = np.arange(N[0])-N[0]/2
            y = np.arange(N[1])-N[1]/2
            x = np.arange(N[2])-N[2]/2
            Z, Y, X = np.meshgrid(z, y, x, indexing='ij')
            # vamos a seleccionar un circulo cuyo diametro va a ser la mitad del tamaño
            # de la muestra (es decir, la region con microestructuras)
            condicion = (X/(N[2]/2))**2+(Y/(N[1]/2))**2 + (Z/(N[2]/2))**2 < 1

        # -----------------------------------------------------------------

        # quito los bordes
        bordez = int(self.borde_a_quitar[0])
        bordey = int(self.borde_a_quitar[1])
        bordex = int(self.borde_a_quitar[2])
        if bordez > 0:
            condicion[-bordez:, :, :] = False
        if bordey > 0:
            condicion[:, 0:bordey, :] = False
            condicion[:, -bordey:, :] = False
        if bordex > 0:
            condicion[:, :, 0:bordex] = False
            condicion[:, :, -bordex:] = False


            
        self.volumen_medido = condicion
        return condicion
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @timer
    def Crear_beta(self, graficos=False):
        """
        Mediante erosiones de 1 voxel vamos creando una matriz de beta.
        beta es el factor exponencial con el que decae B1 en el interior.
          beta = exp(-r/skindepth),
        por lo tanto:
          B1(r)=B1*beta
        """
        # inicializo variables
        z0 = int(self.superposicion.z0)
        vs = self.superposicion.muestra.voxelSize
        skdp = self.skdp
        obj = self.superposicion.muestra_sup
        beta = np.zeros_like(obj)
        # chequeo que el voxelSize sea igual en todas las direcciones
        if np.all(vs == vs[0]):
            # como son todos iguales, llamo vs un lado del voxelSize
            vs = vs[0]
        else:
            # si en alguna direccion es diferente, el codigo tira error
            msj = 'ERROR!!! voxelSize debe ser igual en todas las direcciones!!!'
            raise Exception(msj)

        # esto es para las erosiones:
        mask = (obj == 1)
        struct = ndimage.generate_binary_structure(3, 1)
        # hago suficientes slices como para llegar a una profundidad de 5xSkinDepth
        # es decir, 98um
        n_slices = int(4*skdp)
        # print(n_slices)
        for n in range(n_slices):
            # erosiono:
            erode = ndimage.binary_erosion(mask, struct)
            # la erosion tambien se come los laterales del bulk, por eso los vuelvo a
            # rellenar con 1. La tajada va estar exactamente en z0-n-1, los 1 se llenan
            # hasta z0-n-2
            # solo añado el bulk si se hizo una superposicion con bulk.
            if self.superposicion.checkpoint:
                if z0-n-1<0:
                  # con esta condicion, corto si erosione hasta el fondo
                  break
                else:
                  erode[0:z0-n-1, :, :] = 1
            # obtengo la tajada
            tajada = mask ^ erode
            if np.sum(tajada) == 0:
                # si ya erosione todo, la tajada es nula, por lo tanto salgo del loop                
                break
            # voy llenando las capas con los valores de B1. la variable de profundidad
            # es (n+1)*vs/2, ya que en la primer tajada n=0 y la profundidad es de la
            # mitad del voxelsize (si tomo el centro del voxel)
            beta = beta + tajada*np.exp(-(n+1/2)/skdp) # RECORDAR QUE skdp ESTA EN UNIDADES DE VOXEL!!!
            # ahora el nuevo objeto a erosionar es el de la erosion anterior
            mask = (erode == 1)

            # GRAFICO PARA CHEQUEAR QUE ESTE TODO BIEN # comentar para no ver
            if graficos:                
                slz = int(obj.shape[0]-10)
                sly = int(obj.shape[1]/2)
                
                ncols = 6
                nrows = 6
                if n < ncols*nrows:
                    matriz = tajada
                    matriz = beta*self.volumen_medido
                    plt.figure(666)
                    plt.subplot(nrows, ncols, n+1)
                    plt.pcolormesh(matriz[slz, :, :])
                    plt.figure(667)
                    plt.subplot(nrows, ncols, n+1)
                    plt.pcolormesh(matriz[:, sly, :])

        beta = beta*self.volumen_medido  # solo selecciono la parte del volumen medido
        return beta
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @timer
    def Crear_eta(self):
        """
        Esto crea la matriz "eta", que corresponde al corrimiento en campo
        magnetico. i.e, es el resultado de calculateFieldShift, nuestro viejo delta.
        Ahora le llamo eta para no confundir con el corrimiento quimico.
        """
        eta = self.superposicion.delta_sup*self.volumen_medido
        return eta
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @timer
    def CrearHistograma2D(self, graficos=False):
        """
        Creacion del histograma 2D con los valores de beta y eta.

        Puedo definir si hago los graficos o no
        """
        # inicializo parametros utiles
        vs = self.superposicion.muestra.voxelSize[0]
        skdp = self.skdp
        # obtengo las matrices de eta y beta
        # eta = self.Crear_eta()
        # beta = self.Crear_beta()
        eta = self.eta
        beta = self.beta
        # los paso a array planos para armar el histograma. Para ello uso el slicing
        # del volumen medido, que los transforma a planos
        # eta_f  =  eta.flatten()
        # beta_f = beta.flatten()

        eta_f = eta[self.volumen_medido]
        beta_f = beta[self.volumen_medido]
        # quito las regiones en las que beta es cero, ya que no dan senal
        eta_f = eta_f[beta_f != 0]
        beta_f = beta_f[beta_f != 0]
        # ==========================histogramas 1D==================================
        # primero creo histogramas 1D para obtener los bins y pasarlos al 2D.
        # ---------eta----------
        eta_hist,  eta_bin_edges = np.histogram(eta_f, bins=64)
        eta_bin_centers = eta_bin_edges[:-1] + np.diff(eta_bin_edges)/2
        # --------beta----------
        # vamos a elegir los bins en beta de acuerdo al tamaño de voxel, para
        # asegurarnos de contar bien. para ello, definimos una variable n
        n = np.arange(int(5*skdp)+1)  # numero de voxel hacia el interior
        beta_bin_edges = np.exp(-n/skdp)
        # distancia a la superficie, representada por el centro del voxel
        r = (n[:-1]+0.5)*vs
        beta_bin_centers = np.exp(-r/(skdp*vs))
        # los doy vuelta para meter en el histograma (np.histogram exige que esten ordenados)
        beta_bin_edges = np.flip(beta_bin_edges)
        beta_bin_centers = np.flip(beta_bin_centers)
        # histograma:
        beta_hist, beta_bin_edges = np.histogram(beta_f, bins=beta_bin_edges)
        # ==========================histograma  2D==================================
        # en x pongo eta, en y pongo beta
        H2D, yedges, xedges = np.histogram2d(
            beta_f, eta_f, bins=(beta_bin_edges, eta_bin_edges))
        xcenters = xedges[:-1] + np.diff(xedges)/2
        ycenters = beta_bin_centers

        X, Y = np.meshgrid(xcenters, ycenters)
        if graficos:
            try:
                plt.figure(graficos)
            except:
                plt.figure(987643521)
            plt.title('Histograms')
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            plt.subplot(2, 3, 2)
            plt.title(r'$\beta$-histogram 1D')
            plt.plot(eta_bin_centers,  eta_hist, 'ro-')
            #plt.xlabel(r'$\eta$ [ppm]')
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            plt.subplot(2, 3, 3)
            plt.title(r'$\eta$-histogram 1D')
            plt.plot(beta_bin_centers, beta_hist, 'bo-')
            # plt.xlabel(r'$\beta$')
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            plt.subplot(2, 3, 4)
            plt.title(r'histogram 2D - $h(\eta,\beta)$')
            # plt.pcolormesh(X,Y,H2D)
            plt.pcolormesh(X, Y, 1+H2D,  norm=colors.LogNorm(vmin=1,
                           vmax=np.max(H2D)), cmap='inferno')
            plt.yscale('log')
            plt.ylim([0.01, 1])
            plt.xlim([np.max(X[0, :]), np.min(X[0, :])])
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            plt.subplot(2, 3, 5)
            plt.title(r'$\int h(\eta,\beta) \, d\beta$')
            plt.plot(X[0, :], np.sum(H2D, axis=0), 'ro-')
            plt.xlabel(r'$\eta$ [ppm]')
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            plt.subplot(2, 3, 6)
            plt.title(r'$\int h(\eta,\beta) \, d\eta$')
            plt.plot(Y[:, 0], np.sum(H2D, axis=1), 'bo-')
            plt.xlabel(r'$\beta$')

        self.histograma = [X, Y, H2D]
        return X, Y, H2D

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @timer
    def CrearEspectro(self, secuencia=None, k=0.5, N=16, figure=False, 
                      loadpath='./DataBases/', volumen_medido='completo', 
                      KS=None, return_angle=False, Norm=False, 
                      T2est=0.18*1e-3):
        """
        Mediante el histograma 2D y teniendo como dato la amplitud de senal para
        cierta secuencia (SP, SMC) de acuerdo a los parametros correspondientes
        (k, N), armamos el espectro resultante.

        En KS debo poner el knight shift, pero con KS=-self.superposicion.delta_in
        tengo el espectro RESPECTO AL BULK

        figure es el numero de figura para hacer los graficos. Por defecto es False,
        lo que implica que no se grafica
        """
        if secuencia is None:
            secuencia = self.secuencia
        # cada vez que corro este metodo, guardo la secuencia usada
        self.secuencia = secuencia
        if KS is None:
            KS = -self.superposicion.delta_in
        # de acuerdo a la secuencia, elegimos el archivo de signal intensity
        sp = ['sp', 'singlepulse', 'single_pulse', 'single']
        if secuencia.lower() in sp:
            file = 'SinglePulse/SinglePulse_k{:.2f}.dat'.format(k)
        elif secuencia.lower() == 'smc':
            file = 'SMC/SMC_N{:d}_k{:.2f}.dat'.format(N, k)

        if not path.exists(loadpath+file):
            loadpath = '../DataBases/'
            if not path.exists(loadpath+file):
                msg = 'No existe el archivo con la senal en funcion de k.'
                raise Exception(msg)

        print("Calculando espectro...")
        print(f"\t secuencia {secuencia}, pulso de {k}x180°")
        # creo el volumen
        self.crear_volumen_medido(volumen_medido)

        # SignalIntensity = np.loadtxt(loadpath+file, dtype=complex) ### NOTA: reemplazar archivos por dtype=float!!!!
        SignalIntensity = np.loadtxt(loadpath+file)

        Beta = SignalIntensity[:, 0]
        SignalIntensity = SignalIntensity[:, 1]

        # creo el histograma:
        X, Y, H2D = self.CrearHistograma2D()
        # X, Y, H2D = self.histograma

        # FID-----------------------------------------------------------------------
        ppm = 116.641899  # Hz
        T2est = T2est  # T2est=0.14ms estimado con ancho de espectro. 2020-11-13
        dw = 5e-6  # sacado de los experimentos. Esto da un SW=857ppm aprox
        NP = 4096  # experimentalmente usamos 2048, pero con 4096 sale mas lindo
        t = np.arange(NP)*dw
        fid = np.zeros_like(t).astype(complex)
        for j in range((Y[:, 0]).size):
            beta_j = Y[j, 0]
            ind = find_nearest(Beta, beta_j)
            signal = SignalIntensity[ind]
            for i in range((X[0, :]).size):
                # eta:
                eta_j = X[0, i]
                w = 2*np.pi*ppm*(eta_j+KS)
                # fid
                fid += H2D[j, i]*signal*np.exp(1j*w * t - t/T2est)
        # FOURIER-------------------------------------------------------------------
        freq = np.fft.fftshift(np.fft.fftfreq(NP, d=dw))
        ppmAxis = freq/ppm
        spec = np.fft.fftshift(np.fft.fft(fid))
        # corrijo la fase:
        spec, angle = autophase(ppmAxis, spec)

        self.ppmAxis = ppmAxis
        self.spec = spec

        if figure:
            plt.figure(figure)
            plt.subplot(1, 2, 1)
            plt.title('FID')
            if Norm:
                plt.plot(t*1e3, np.real(fid)/np.max(np.real(fid)), linewidth=2)
            else:
                plt.plot(t*1e3, np.real(fid), linewidth=2)
            plt.xlabel('time [ms]')
            plt.yticks([])
            plt.subplot(1, 2, 2)
            plt.title('Spectrum')
            if Norm:
                plt.plot(ppmAxis, np.real(spec) /
                         np.max(np.real(spec)), linewidth=2)
            else:
                plt.plot(ppmAxis, np.real(spec), linewidth=2)
            plt.xlabel('ppmAxis')
            if np.abs(KS) < 100:
                plt.xlim([100, -100])
                plt.vlines(0, 0, 1, 'k', linestyle='dashed')
            else:
                plt.xlim([350, 150])
            plt.yticks([])

        if return_angle == True:
            return ppmAxis, spec, angle
        else:
            return ppmAxis, spec

    def get_volumen_medido(self):
        return self.superposicion.muestra_sup*self.volumen_medido
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# --------------------FUNCIONES-------------------------------------------------
def find_nearest(array, value):
    """
    Encuentra el valor mas cercano a 'value' dentro de 'array'.
    Devuelve el indice del valor mas cercano
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    # return idx, array[idx]
    return idx


def autophase(ppmAxis, spec, precision = 1):
    """
    Corrijo automaticamente la fase, utilizando el método de minimizar el area
    de la parte imaginaria:   case{'MinIntImagSpec'}
    """    
    angle = np.arange(-180, 180, precision)
    spec.astype('complex')

    SPECS = []
    IntImagSpec = []
    for i in range(angle.size):
        Sp_try = spec*np.exp(-1j*angle[i]*np.pi/180)
        SPECS.append(Sp_try)
        IntImagSpec.append(np.abs(np.trapz(np.imag(Sp_try), x=ppmAxis)))
    IntImagSpec = np.array(IntImagSpec)
    # indice del minimo:
    idx = np.argmin(IntImagSpec)
    spec = SPECS[idx]
    ind_max = np.argmax(np.abs(np.real(spec)))
    if spec[ind_max] < 0:
        spec = -spec
    angle = angle[idx]
    return spec, angle
