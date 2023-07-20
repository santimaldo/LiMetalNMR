# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:42:04 2023

@author: Santi M


Como me equivoque al armar los perfiles internos, cambio el signo de z en todos
los archivos
"""

# importing the library
import os
import numpy as np
 
# giving directory name
dirname = './'
 
# giving file extension
ext = ('.in')

# iterating over all files
for file in os.listdir(dirname):
    if file.endswith(ext):
        print(file)
        file_tmp = f"{file.split('.')[0]}_tmp{ext}"

        with open(file, 'r') as fr:
            with open(file_tmp, 'w') as fw:
                for line in fr.readlines():                
                    if line.startswith(("#", "0.000000000000000000e+00")):
                        fw.write(line)
                    else:
                        fw.write(f"-{line}")
        os.remove(file)
        os.rename(file_tmp, file)                           
    else:
        continue