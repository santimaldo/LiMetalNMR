# -*- coding: utf-8 -*-
"""
This script runs the basic programs to enable the data bases needed for the calculations
"""
import os
pwd = os.getcwd()
os.chdir("./DataBases/")

from single_pulse import *
from smc import *
from hexagonal_parameter import *

os.chdir(pwd)


print("="*40,"\n"," "*10,"Ready to use!\n","="*40)