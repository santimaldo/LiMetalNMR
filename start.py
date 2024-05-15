# -*- coding: utf-8 -*-
"""
This script runs the basic programs to enable the data bases needed for the calculations
"""

import subprocess
 
# running other file using run()

path = "./DataBases/"
subprocess.run([path+"single_pulse.py",
                path+"smc.py",
                path+"hexagonal_parameter.py"])