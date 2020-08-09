#!/usr/bin/env python3

from .vmec import *

# These next lines are to make _vmec_f90wrap accessible:
import sys
import os
print("Hello from ", __file__)
sys.path.append(os.path.dirname(__file__))

#all = ['Parameter']
