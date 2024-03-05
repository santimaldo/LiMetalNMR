# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:54:43 2023

@author: santi
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure
from stl import mesh

def export_mesh_to_stl(verts, faces, filename):
    # Create the mesh object
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    # Populate the mesh with vertex data
    for i, vertex_indices in enumerate(faces):
        for j in range(3):
            mesh_data.vectors[i][j] = verts[vertex_indices[j]]
    # Save the mesh to an STL file
    mesh_data.save(filename)
  

# funcion para crear la figura 3D
def exportar_3D(matriz, archivo, give_full_name=False):
    
  print(" -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ")
  print("Creando figura 3D. Esto puede demorar varios minutos...")
  voxel_data = matriz
  # le doy margenes para que se vean los bordes
  voxel_data = np.pad(voxel_data, 2)
  # rotacion para que quede z en la direccion vertical
  voxel_data = np.moveaxis(voxel_data, 0 , -1)
  
  # Use marching cubes to obtain the surface mesh 
  verts, faces, _, _ = measure.marching_cubes(voxel_data, level=0)
  
  # save 
  if give_full_name:
    filename = archivo
  else:
    filename = './Outputs/{}.stl'.format(archivo)
  export_mesh_to_stl(verts, faces, filename)
  
  print("       Listo!") 
  print(f"guardado en:    '{filename}'")
  print(" -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ")