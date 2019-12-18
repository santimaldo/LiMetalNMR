# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 16:14:26 2019

@author: santi
"""


#------------------------------------------------------------------------------
def D(X):
    """
    downscales a 3D distribution by factor two, by collapsing each cube  
    of eight voxels into one single voxel (average value) 
    """
    DX =      X[ ::2, ::2, ::2]    
    DX = DX + X[1::2, ::2, ::2]    
    DX = DX + X[ ::2, ::2,1::2]    
    DX = DX + X[1::2, ::2,1::2]    
    DX = DX + X[ ::2,1::2, ::2]    
    DX = DX + X[1::2,1::2, ::2]
    DX = DX + X[ ::2,1::2,1::2]    
    DX = DX + X[1::2,1::2,1::2]
    DX = DX/8.
    
    return DX
#------------------------------------------------------------------------------
    

#------------------------------------------------------------------------------
    
def Zc(X):
    """
    This operator is complementary to zero-padding: the result is 
    a void space embedded in an environment of copies of X. 
    The resulting 3D distribution is 2 times as large 
    as the original in each dimension
    """
    dim = np.shape(X)
    # numpy follows te convention zyx
    # So.. x is the 3rd dimension: dim[2]
    #      y is the 2nd dimension: dim[1]
    #      z is the 1st dimension: dim[0]
    Nx = 2*dim[2]
    Ny = 2*dim[1]
    Nz = 2*dim[0]
    mid_x = range(int((Nx/4. + 1)), int((Nx*3./4.)+1))
    mid_y = range(int((Ny/4. + 1)), int((Ny*3./4)+1))
    mid_z = range(int((Nz/4. + 1)), int((Nz*3./4.)+1))
    
    print(mid_x, mid_y, mid_z)
    
    ####################################
    #############     no estoy seguro de si hice bien el ZcX
    ####################################
    # ZcX = repmat(circshift(X, [Ny/4, Nx/4, Nz/4]), [2 2 2]);  asi es en matlab
    ZcX = np.tile(np.roll(X, [int(Nz/4.), int(Ny/4.), int(Nx/4.)], axis=[0,1,2]), (2,2,2))
    ZcX[mid_z, mid_y, mid_x] = 0
    
    return ZcX

#------------------------------------------------------------------------------
    


ZcX = Zc( D(obj) )