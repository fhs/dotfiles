"""
NetCDF4 file I/O
"""

import numpy as np

def loadnc(filename):
    import netCDF4
    return np.array(netCDF4.Dataset(filename).variables["data"])
