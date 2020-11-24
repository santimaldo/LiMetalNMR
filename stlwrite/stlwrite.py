from oct2py import Oct2Py
#%%
slz, sly, slx = muestra.slices
#tmpvol =  superposicion.muestra_sup[59:,sly[0]:sly[1],slx[0]:slx[1]]
tmpvol =  superposicion.muestra_sup[59:,:,:]
#%%
filename = 'model.stl'

with Oct2Py() as oc:
  fv = oc.isosurface(tmpvol, 0.5) # Make patch w. faces "out"
  oc.stlwrite(filename,fv)        # Save to binary .stl
