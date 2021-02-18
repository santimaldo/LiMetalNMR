from oct2py import Oct2Py
#%%
# en la matriz tmpvol, ponemos la matriz que queremos representar en 3D. superposicion.muestra_sup es la superposicion de las microestructuras con el bulk. Podemos aplicar un slice para no crear una figura 3D tan grande. Ademas, mientras mayor sea tmpvol, mas tiempo demora este script
tmpvol =  superposicion.muestra_sup[59:,:,:]
# si quiero agarrar solo la region de las microestructuras con un piso:
#slz, sly, slx = muestra.slices
#tmpvol =  superposicion.muestra_sup[59:,sly[0]:sly[1],slx[0]:slx[1]] # En z, el indice 59 coresponde a la superficie de LiMetal
#%%
filename = './model.stl'

with Oct2Py() as oc:
  print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
  print("Creando figura 3D. Esto puede demorar varios minutos...")
  fv = oc.isosurface(tmpvol, 0.5) # Make patch w. faces "out"
  oc.stlwrite(filename,fv)        # Save to binary .stl
print("       Listo!")  
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
