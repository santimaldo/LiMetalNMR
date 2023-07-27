# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:21:33 2023

@author: Santi
"""

#%%

# meto un calculo al medio:
# radio, distancia y vs estan en el archivo:
parametros2 = np.loadtxt('./DataBases/ParametrosASimular_2.dat')
df2 = pd.DataFrame(parametros2)
df2 = df2.sort_values(by=[1, 2, 0, 3, 4], ascending=True)
parametros2 = np.array(df2)

parametros = np.concatenate([parametros2, parametros_old])

#%%
