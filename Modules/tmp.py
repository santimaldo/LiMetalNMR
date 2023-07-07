from matplotlib import pyplot as plt, cm
cmap = cm.get_cmap("inferno_r").copy()
cmap.set_bad('w')
mat = superposicion.delta_muestra*superposicion.muestra_sup
mat = mat[67,:,:]
mues = superposicion.muestra_sup[67,:,:]
minn = np.min(mat*mues) 
mat= mat - minn*mues - mues + mues *0.01
print(np.max(mat), np.min(mat))
mat[mat==0] = np.nan
plt.figure(1)
#plt.pcolormesh(mat, cmap=cmap, vmax=5.8, vmin=-5.4)
plt.pcolormesh(mat, cmap=cmap, vmax=5.4)
plt.gca().set_aspect('equal', 'box')
#plt.xlim([50,130])
#plt.xlim([76,180])
plt.colorbar()
plt.show()


# 2.3 -0.3
# 5.8 0
